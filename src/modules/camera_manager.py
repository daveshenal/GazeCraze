import cv2
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

class CameraManager:
    """Manages camera initialization and properties."""
    
    def __init__(self, camera_index: int = 0, width: int = 640, height: int = 480, fps: int = 30):
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            logger.error("Cannot access webcam")
            raise RuntimeError("Cannot access webcam")
        
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        logger.info(f"Camera initialized: {self.frame_width}x{self.frame_height}")
    
    def read_frame(self):
        """Read a frame from the camera."""
        return self.cap.read()
    
    def get_dimensions(self) -> Tuple[int, int]:
        """Get camera frame dimensions."""
        return self.frame_width, self.frame_height
    
    def release(self):
        """Release camera resources."""
        self.cap.release()