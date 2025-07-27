from typing import Tuple

class ConcentrationAnalyzer:
    """Main analyzer that combines all components to determine concentration."""
    
    def __init__(self, gaze_ratio_threshold: float = 0.55, iris_alignment_threshold: float = 0.14):
        self.gaze_ratio_threshold = gaze_ratio_threshold
        self.iris_alignment_threshold = iris_alignment_threshold
    
    def analyze_gaze_direction(self, left_gaze_ratio: float, right_gaze_ratio: float, 
                             head_direction: str) -> Tuple[bool, str, float]:
        """Analyze gaze direction based on ratios and head pose."""
        if head_direction == "left":
            if left_gaze_ratio > self.gaze_ratio_threshold:
                return False, "Looking Left", max(0, 1 - (left_gaze_ratio - 0.5) * 2)
            else:
                return True, "Head: Left Turn", min(1, (self.gaze_ratio_threshold - left_gaze_ratio) * 2)
        elif head_direction == "right":
            if right_gaze_ratio > self.gaze_ratio_threshold:
                return False, "Looking Right", max(0, 1 - (right_gaze_ratio - 0.5) * 2)
            else:
                return True, "Head: Right Turn", min(1, (self.gaze_ratio_threshold - right_gaze_ratio) * 2)
        
        # Center head position - check iris alignment
        iris_diff = abs(left_gaze_ratio - right_gaze_ratio)
        if iris_diff < self.iris_alignment_threshold:
            confidence = max(0, 1 - (iris_diff / self.iris_alignment_threshold))
            return True, "Eyes on screen", confidence
        elif left_gaze_ratio > right_gaze_ratio:
            return False, "Eyes on left", max(0, 1 - (iris_diff / self.iris_alignment_threshold))
        else:
            return False, "Eyes on right", max(0, 1 - (iris_diff / self.iris_alignment_threshold))