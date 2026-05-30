import time
import cv2

REF_WIDTH = 640
REF_HEIGHT = 480

class DisplayManager:
    """Manages display and UI elements."""
    
    def __init__(self):
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.current_fps = 0.0

    def _layout(self, frame):
        """Scale text positions and sizes relative to the reference 640x480 layout."""
        height, width = frame.shape[:2]
        scale_x = width / REF_WIDTH
        scale_y = height / REF_HEIGHT
        scale = min(scale_x, scale_y)

        return {
            "margin_x": int(round(30 * scale_x)),
            "status_y": int(round(50 * scale_y)),
            "confidence_y": int(round(80 * scale_y)),
            "status_font": 0.8 * scale,
            "confidence_font": 0.6 * scale,
            "info_font": 0.6 * scale,
            "instructions_font": 0.5 * scale,
            "status_thickness": max(1, int(round(2 * scale))),
            "confidence_thickness": max(1, int(round(1 * scale))),
            "info_thickness": max(1, int(round(1 * scale))),
            "bottom_margin": int(round(30 * scale_y)),
            "instructions_offset": int(round(60 * scale_y)),
        }
    
    def draw_status(self, frame, concentration_status: str, status_color: tuple, confidence: float):
        """Draw concentration status on frame."""
        layout = self._layout(frame)

        cv2.putText(
            frame,
            concentration_status,
            (layout["margin_x"], layout["status_y"]),
            cv2.FONT_HERSHEY_SIMPLEX,
            layout["status_font"],
            status_color,
            layout["status_thickness"],
        )
        
        if confidence > 0:
            cv2.putText(
                frame,
                f"Confidence: {confidence:.2f}",
                (layout["margin_x"], layout["confidence_y"]),
                cv2.FONT_HERSHEY_SIMPLEX,
                layout["confidence_font"],
                (255, 255, 255),
                layout["confidence_thickness"],
            )
    
    def update_fps(self, frame_height: int):
        """Update and return current FPS."""
        self.fps_counter += 1
        
        if self.fps_counter >= 30:  # Update every 30 frames
            elapsed = time.time() - self.fps_start_time
            self.current_fps = self.fps_counter / elapsed
            self.fps_counter = 0
            self.fps_start_time = time.time()
        
        return self.current_fps
    
    def draw_info(self, frame, frame_height: int):
        """Draw FPS and instructions on frame."""
        layout = self._layout(frame)
        fps = self.update_fps(frame_height)

        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (layout["margin_x"], frame_height - layout["bottom_margin"]),
            cv2.FONT_HERSHEY_SIMPLEX,
            layout["info_font"],
            (255, 255, 255),
            layout["info_thickness"],
        )

        cv2.putText(
            frame,
            "Press 'q' to quit, 'r' to reset",
            (layout["margin_x"], frame_height - layout["instructions_offset"]),
            cv2.FONT_HERSHEY_SIMPLEX,
            layout["instructions_font"],
            (255, 255, 255),
            layout["info_thickness"],
        )