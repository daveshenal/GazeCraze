import time
from typing import Dict

class PerformanceTracker:
    """Tracks performance metrics."""
    
    def __init__(self):
        self.frame_count = 0
        self.start_time = time.time()
    
    @property
    def total_frames(self):
        """Property to match test expectations."""
        return self.frame_count
    
    def increment_frame(self):
        """Increment frame counter."""
        self.frame_count += 1
    
    def get_stats(self) -> Dict[str, float]:
        """Get performance statistics."""
        elapsed_time = time.time() - self.start_time
        fps = self.frame_count / elapsed_time if elapsed_time > 0 else 0
        return {
            'fps': fps,
            'total_frames': self.frame_count,
            'runtime': elapsed_time
        }