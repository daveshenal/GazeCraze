from typing import Tuple

# Camera/mirror view uses image coordinates; labels should match the subject's left/right.
SUBJECT_POV_LABELS = {
    "Looking Left": "Looking Right",
    "Looking Right": "Looking Left",
    "Head: Left Turn": "Head: Right Turn",
    "Head: Right Turn": "Head: Left Turn",
    "Eyes on left": "Eyes on right",
    "Eyes on right": "Eyes on left",
}


class ConcentrationAnalyzer:
    """Main analyzer that combines all components to determine concentration."""
    
    def __init__(self, gaze_ratio_threshold: float = 0.55, iris_alignment_threshold: float = 0.14):
        self.gaze_ratio_threshold = gaze_ratio_threshold
        self.iris_alignment_threshold = iris_alignment_threshold

    def _to_subject_pov(self, label: str) -> str:
        """Map camera-relative direction labels to the subject's perspective."""
        return SUBJECT_POV_LABELS.get(label, label)
    
    def analyze_gaze_direction(self, left_gaze_ratio: float, right_gaze_ratio: float, 
                             head_direction: str) -> Tuple[bool, str, float]:
        """Analyze gaze direction based on ratios and head pose."""
        if head_direction == "left":
            if left_gaze_ratio > self.gaze_ratio_threshold:
                return False, self._to_subject_pov("Looking Left"), max(0, 1 - (left_gaze_ratio - 0.5) * 2)
            else:
                return True, self._to_subject_pov("Head: Left Turn"), min(1, (self.gaze_ratio_threshold - left_gaze_ratio) * 2)
        elif head_direction == "right":
            if right_gaze_ratio > self.gaze_ratio_threshold:
                return False, self._to_subject_pov("Looking Right"), max(0, 1 - (right_gaze_ratio - 0.5) * 2)
            else:
                return True, self._to_subject_pov("Head: Right Turn"), min(1, (self.gaze_ratio_threshold - right_gaze_ratio) * 2)
        
        # Center head position - check iris alignment
        iris_diff = abs(left_gaze_ratio - right_gaze_ratio)
        if iris_diff < self.iris_alignment_threshold:
            confidence = max(0, 1 - (iris_diff / self.iris_alignment_threshold))
            return True, "Eyes on screen", confidence
        elif left_gaze_ratio > right_gaze_ratio:
            return False, self._to_subject_pov("Eyes on left"), max(0, 1 - (iris_diff / self.iris_alignment_threshold))
        else:
            return False, self._to_subject_pov("Eyes on right"), max(0, 1 - (iris_diff / self.iris_alignment_threshold))