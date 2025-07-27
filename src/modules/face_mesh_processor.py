import logging
import mediapipe as mp

logger = logging.getLogger(__name__)

class FaceMeshProcessor:
    """Handles MediaPipe Face Mesh initialization and processing."""
    
    def __init__(self, detection_confidence: float = 0.7, tracking_confidence: float = 0.7):
        self.face_mesh = self._initialize_face_mesh(detection_confidence, tracking_confidence)
        logger.info("FaceMeshProcessor initialized successfully")
    
    def _initialize_face_mesh(self, detection_confidence: float, tracking_confidence: float):
        """Initialize MediaPipe Face Mesh with error handling."""
        try:
            mp_face_mesh = mp.solutions.face_mesh
            face_mesh = mp_face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                static_image_mode=False,
                min_detection_confidence=detection_confidence,
                min_tracking_confidence=tracking_confidence
            )
            return face_mesh
        except Exception as e:
            logger.error(f"Failed to initialize Face Mesh: {e}")
            raise
    
    def process_frame(self, frame_rgb):
        """Process frame and return face landmarks."""
        return self.face_mesh.process(frame_rgb)
    
    def cleanup(self):
        """Clean up MediaPipe resources."""
        if hasattr(self, 'face_mesh') and self.face_mesh:
            self.face_mesh.close()