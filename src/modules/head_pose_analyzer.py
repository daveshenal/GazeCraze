from typing import Tuple

class HeadPoseAnalyzer:
    """Handles head pose and face tilt analysis."""
    
    def __init__(self, face_tilt_threshold: float = 15, head_pose_threshold: float = 0.028):
        self.face_tilt_threshold = face_tilt_threshold
        self.head_pose_threshold = head_pose_threshold
        
        # Landmarks for face tilt detection
        self.left_eye_outer = 33
        self.right_eye_outer = 263
        
        # Iris indices for head pose
        self.left_iris_index = 468
        self.right_iris_index = 473
    
    def check_face_tilt(self, face_landmarks, frame_width: int, frame_height: int) -> Tuple[bool, float]:
        """Check if face is tilted beyond threshold."""
        left_eye_y = face_landmarks.landmark[self.left_eye_outer].y * frame_height
        right_eye_y = face_landmarks.landmark[self.right_eye_outer].y * frame_height
        eye_y_difference = abs(left_eye_y - right_eye_y)
        
        is_tilted = eye_y_difference > self.face_tilt_threshold
        confidence = max(0, 1 - (eye_y_difference / self.face_tilt_threshold)) if is_tilted else 1.0
        
        return is_tilted, confidence
    
    def analyze_head_pose(self, face_landmarks) -> Tuple[bool, str, float]:
        """Analyze head pose based on iris Z positions."""
        left_iris_z = face_landmarks.landmark[self.left_iris_index].z
        right_iris_z = face_landmarks.landmark[self.right_iris_index].z
        z_diff = abs(left_iris_z - right_iris_z)
        
        if z_diff > self.head_pose_threshold:
            if left_iris_z > right_iris_z:
                return True, "left", z_diff
            else:
                return True, "right", z_diff
        
        return False, "center", z_diff