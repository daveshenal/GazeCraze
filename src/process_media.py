"""Annotate an image or video with concentration labels and save the result."""

import argparse
import logging
import sys
from pathlib import Path

import cv2

from src.concentration_detector import ConcentrationDetector
from src.modules.display_manager import DisplayManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}
VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".wmv", ".webm", ".m4v"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run concentration detection on an image or video and save labeled output."
    )
    parser.add_argument("input", type=Path, help="Path to an input image or video file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output path (default: <input_stem>_labeled<ext> in the same folder)",
    )
    parser.add_argument(
        "--mirror",
        action="store_true",
        help="Mirror output like the live webcam app (default: keep original orientation)",
    )
    return parser.parse_args()


def resolve_output_path(input_path: Path, output_path: Path | None) -> Path:
    if output_path is not None:
        return output_path

    suffix = input_path.suffix or ".jpg"
    return input_path.with_name(f"{input_path.stem}_labeled{suffix}")


def prepare_frame(frame, mirror_output: bool):
    """Undo ConcentrationDetector's internal horizontal flip unless mirror is requested."""
    if mirror_output:
        return frame
    return cv2.flip(frame, 1)


def annotate_frame(detector: ConcentrationDetector, display: DisplayManager, frame, mirror_output: bool):
    frame = prepare_frame(frame, mirror_output)
    processed_frame, status, color, confidence = detector.process_frame(frame)
    display.draw_status(processed_frame, status, color, confidence)
    return processed_frame


def process_image(
    input_path: Path,
    output_path: Path,
    detector: ConcentrationDetector,
    display: DisplayManager,
    mirror_output: bool,
) -> None:
    frame = cv2.imread(str(input_path))
    if frame is None:
        raise RuntimeError(f"Could not read image: {input_path}")

    detector.reset_history()
    annotated = annotate_frame(detector, display, frame, mirror_output)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(output_path), annotated):
        raise RuntimeError(f"Could not write image: {output_path}")

    logger.info("Saved labeled image to %s", output_path)


def process_video(
    input_path: Path,
    output_path: Path,
    detector: ConcentrationDetector,
    display: DisplayManager,
    mirror_output: bool,
) -> None:
    capture = cv2.VideoCapture(str(input_path))
    if not capture.isOpened():
        raise RuntimeError(f"Could not open video: {input_path}")

    frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = capture.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(
        str(output_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (frame_width, frame_height),
    )
    if not writer.isOpened():
        capture.release()
        raise RuntimeError(f"Could not create output video: {output_path}")

    detector.reset_history()
    frame_index = 0

    try:
        while True:
            ret, frame = capture.read()
            if not ret:
                break

            annotated = annotate_frame(detector, display, frame, mirror_output)
            writer.write(annotated)
            frame_index += 1

            if frame_index % 30 == 0:
                if total_frames > 0:
                    logger.info("Processed %s/%s frames", frame_index, total_frames)
                else:
                    logger.info("Processed %s frames", frame_index)
    finally:
        capture.release()
        writer.release()

    logger.info("Saved labeled video to %s (%s frames)", output_path, frame_index)


def main() -> int:
    args = parse_args()
    input_path = args.input.resolve()

    if not input_path.exists():
        logger.error("Input file not found: %s", input_path)
        return 1

    suffix = input_path.suffix.lower()
    output_path = resolve_output_path(input_path, args.output)

    detector = ConcentrationDetector()
    display = DisplayManager()

    try:
        if suffix in IMAGE_EXTENSIONS:
            process_image(input_path, output_path, detector, display, args.mirror)
        elif suffix in VIDEO_EXTENSIONS:
            process_video(input_path, output_path, detector, display, args.mirror)
        else:
            logger.error(
                "Unsupported file type '%s'. Supported images: %s. Supported videos: %s.",
                suffix,
                ", ".join(sorted(IMAGE_EXTENSIONS)),
                ", ".join(sorted(VIDEO_EXTENSIONS)),
            )
            return 1
    except Exception as exc:
        logger.error("%s", exc)
        return 1
    finally:
        detector.cleanup()

    stats = detector.get_performance_stats()
    logger.info(
        "Performance: %.1f FPS, %s frames, %.1fs runtime",
        stats["fps"],
        stats["total_frames"],
        stats["runtime"],
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
