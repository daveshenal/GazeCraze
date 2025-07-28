class ResultSmoother:
    """Handles temporal smoothing of detection results."""
    
    def __init__(self, history_size: int = 30):
        self.concentration_history = []
        self.history_size = history_size
    
    @property
    def history(self):
        """Property to match test expectations."""
        return self.concentration_history
    
    def smooth_result(self, current_result: bool) -> bool:
        """Apply temporal smoothing to reduce jitter."""
        self.concentration_history.append(current_result)
        
        # Keep only recent history
        if len(self.concentration_history) > self.history_size:
            self.concentration_history.pop(0)
        
        # Calculate smoothed result
        if len(self.concentration_history) >= 5:
            recent_concentrated = sum(self.concentration_history[-5:])
            return recent_concentrated >= 3  # Majority vote
        
        return current_result
    
    def clear_history(self):
        """Clear the smoothing history."""
        self.concentration_history.clear()