import logging
from typing import Tuple

logger = logging.getLogger(__name__)

class EyeAnalyzer:
    """Handles eye-related calculations including blink detection and gaze analysis."""
    
    def __init__(self, ear_threshold: float = 0.25):
        # Eye state tracking for blink detection
        self.left_eye_top = 159
        self.left_eye_bottom = 145
        self.right_eye_top = 386
        self.right_eye_bottom = 374
        self.ear_threshold = ear_threshold
        
        # Eye corner landmarks
        self.left_eye_inner = 133
        self.left_eye_outer = 33
        self.right_eye_inner = 362
        self.right_eye_outer = 263
    
    def calculate_ear(self, eye_top: int, eye_bottom: int, eye_left: int, eye_right: int, 
                     face_landmarks, frame_width: int, frame_height: int) -> float:
        """Calculate Eye Aspect Ratio for blink detection."""
        try:
            # Calculate vertical distance
            top_y = face_landmarks.landmark[eye_top].y * frame_height
            bottom_y = face_landmarks.landmark[eye_bottom].y * frame_height
            vertical_distance = abs(top_y - bottom_y)
            
            # Calculate horizontal distance
            left_x = face_landmarks.landmark[eye_left].x * frame_width
            right_x = face_landmarks.landmark[eye_right].x * frame_width
            horizontal_distance = abs(right_x - left_x)
            
            # Avoid division by zero
            if horizontal_distance == 0:
                return 0
            
            return vertical_distance / horizontal_distance
        except (IndexError, ZeroDivisionError) as e:
            logger.warning(f"Error calculating EAR: {e}")
            return 0.3  # Default value
    
    def detect_blinks(self, face_landmarks, frame_width: int, frame_height: int) -> bool:
        """Detect if eyes are closed (blinking)."""
        left_ear = self.calculate_ear(self.left_eye_top, self.left_eye_bottom, 
                                    self.left_eye_inner, self.left_eye_outer, 
                                    face_landmarks, frame_width, frame_height)
        right_ear = self.calculate_ear(self.right_eye_top, self.right_eye_bottom, 
                                     self.right_eye_inner, self.right_eye_outer, 
                                     face_landmarks, frame_width, frame_height)
        
        return left_ear < self.ear_threshold and right_ear < self.ear_threshold
    
    def calculate_gaze_ratios(self, face_landmarks, frame_width: int, frame_height: int) -> Tuple[float, float]:
        """Calculate gaze ratios for both eyes."""
        # Get iris positions
        left_iris_x = face_landmarks.landmark[468].x * frame_width  # left_iris_index
        right_iris_x = face_landmarks.landmark[473].x * frame_width  # right_iris_index
        
        left_eye_inner_x = face_landmarks.landmark[self.left_eye_inner].x * frame_width
        left_eye_outer_x = face_landmarks.landmark[self.left_eye_outer].x * frame_width
        right_eye_inner_x = face_landmarks.landmark[self.right_eye_inner].x * frame_width
        right_eye_outer_x = face_landmarks.landmark[self.right_eye_outer].x * frame_width
        
        # Avoid division by zero
        left_eye_width = left_eye_outer_x - left_eye_inner_x
        right_eye_width = right_eye_outer_x - right_eye_inner_x
        
        if left_eye_width == 0 or right_eye_width == 0:
            raise ValueError("Invalid Eye Measurements")
        
        left_gaze_ratio = (left_iris_x - left_eye_inner_x) / left_eye_width
        right_gaze_ratio = (right_iris_x - right_eye_inner_x) / right_eye_width
        
        return left_gaze_ratio, right_gaze_ratio