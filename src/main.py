# concentration_detector.py
import cv2
import logging

from src.concentration_detector import ConcentrationDetector
from src.modules.camera_manager import CameraManager
from src.modules.display_manager import DisplayManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main function to run the concentration detection system."""
    try:
        # Initialize components
        detector = ConcentrationDetector()
        camera = CameraManager()
        display = DisplayManager()
        
        frame_width, frame_height = camera.get_dimensions()
        
        while True:
            ret, frame = camera.read_frame()
            if not ret:
                logger.warning("Failed to read frame")
                break
            
            # Process frame
            processed_frame, concentration_status, status_color, confidence = detector.process_frame(frame)
            
            # Draw status and info
            display.draw_status(processed_frame, concentration_status, status_color, confidence)
            display.draw_info(processed_frame, frame_height)
            
            cv2.imshow("Concentration Detection", processed_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                detector.reset_history()
        
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        # Cleanup
        if 'camera' in locals():
            camera.release()
        cv2.destroyAllWindows()
        if 'detector' in locals():
            detector.cleanup()
        
        # Print performance stats
        if 'detector' in locals():
            stats = detector.get_performance_stats()
            logger.info(f"Performance: {stats['fps']:.1f} FPS, "
                       f"{stats['total_frames']} frames, "
                       f"{stats['runtime']:.1f}s runtime")


if __name__ == "__main__":
    main()