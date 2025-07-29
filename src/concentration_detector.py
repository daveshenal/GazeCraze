# concentration_detector.py
import cv2
import logging
from typing import Tuple, Dict

from src.modules.face_mesh_processor import FaceMeshProcessor
from src.modules.eye_analyzer import EyeAnalyzer
from src.modules.head_pose_analyzer import HeadPoseAnalyzer
from src.modules.concentration_analyzer import ConcentrationAnalyzer
from src.modules.result_smoother import ResultSmoother
from src.modules.performance_tracker import PerformanceTracker

logger = logging.getLogger(__name__)

class ConcentrationDetector:
    """Main concentration detector that orchestrates all components."""
    
    def __init__(self, 
                 detection_confidence: float = 0.7, 
                 tracking_confidence: float = 0.7,
                 face_tilt_threshold: float = 15,
                 head_pose_threshold: float = 0.028,
                 gaze_ratio_threshold: float = 0.55,
                 iris_alignment_threshold: float = 0.14,
                 ear_threshold: float = 0.25,
                 history_size: int = 30):
        """Initialize all components with configurable parameters."""
        
        # Initialize components
        self.face_processor = FaceMeshProcessor(detection_confidence, tracking_confidence)
        self.eye_analyzer = EyeAnalyzer(ear_threshold)
        self.head_analyzer = HeadPoseAnalyzer(face_tilt_threshold, head_pose_threshold)
        self.concentration_analyzer = ConcentrationAnalyzer(gaze_ratio_threshold, iris_alignment_threshold)
        self.smoother = ResultSmoother(history_size)
        self.performance_tracker = PerformanceTracker()
        
        logger.info("ConcentrationDetector initialized successfully")
    
    def is_concentrated(self, face_landmarks, frame_width: int, frame_height: int) -> Tuple[bool, str, float]:
        """
        Determine if the user is concentrated based on gaze and head pose.
        
        Returns:
            tuple: (is_concentrated: bool, status_message: str, confidence: float)
        """
        try:
            # Check for blinks first
            if self.eye_analyzer.detect_blinks(face_landmarks, frame_width, frame_height):
                return False, "Eyes Closed", 0.0
            
            # Check face tilt
            is_tilted, tilt_confidence = self.head_analyzer.check_face_tilt(face_landmarks, frame_width, frame_height)
            if is_tilted:
                return False, "Face Tilted", tilt_confidence
            
            # Calculate gaze ratios
            try:
                left_gaze_ratio, right_gaze_ratio = self.eye_analyzer.calculate_gaze_ratios(
                    face_landmarks, frame_width, frame_height)
            except ValueError as e:
                return False, str(e), 0.0
            
            # Analyze head pose
            has_head_turn, head_direction, _ = self.head_analyzer.analyze_head_pose(face_landmarks)
            
            # Analyze concentration based on gaze and head pose
            if has_head_turn:
                return self.concentration_analyzer.analyze_gaze_direction(
                    left_gaze_ratio, right_gaze_ratio, head_direction)
            else:
                return self.concentration_analyzer.analyze_gaze_direction(
                    left_gaze_ratio, right_gaze_ratio, "center")
            
        except Exception as e:
            logger.error(f"Error in concentration detection: {e}")
            return False, "Detection Error", 0.0
    
    def process_frame(self, frame):
        """Process a single frame and return concentration status."""
        self.performance_tracker.increment_frame()
        
        # Mirror the frame for better user experience
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_height, frame_width = frame.shape[:2]
        
        # Process frame
        results = self.face_processor.process_frame(frame_rgb)
        
        concentration_status = "No Face Detected"
        status_color = (0, 0, 255)  # Red
        confidence = 0.0
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                is_concentrated, status_msg, conf = self.is_concentrated(
                    face_landmarks, frame_width, frame_height
                )
                
                # Apply smoothing
                smoothed_concentrated = self.smoother.smooth_result(is_concentrated)
                
                if smoothed_concentrated:
                    concentration_status = f"Concentrated ({status_msg})"
                    status_color = (0, 255, 0)  # Green
                else:
                    concentration_status = f"Not Concentrated ({status_msg})"
                    status_color = (0, 0, 255)  # Red
                
                confidence = conf
        
        return frame, concentration_status, status_color, confidence
    
    def get_performance_stats(self) -> Dict[str, float]:
        """Get performance statistics."""
        return self.performance_tracker.get_stats()
    
    def reset_history(self):
        """Reset the smoothing history."""
        self.smoother.clear_history()
        logger.info("Detection history reset")
    
    def cleanup(self):
        """Clean up all resources."""
        self.face_processor.cleanup()
        logger.info("ConcentrationDetector cleaned up")