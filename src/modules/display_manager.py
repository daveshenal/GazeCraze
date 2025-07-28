import time
import cv2

class DisplayManager:
    """Manages display and UI elements."""
    
    def __init__(self):
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.current_fps = 0.0
    
    def draw_status(self, frame, concentration_status: str, status_color: tuple, confidence: float):
        """Draw concentration status on frame."""
        cv2.putText(frame, concentration_status, (30, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
        
        # Draw confidence
        if confidence > 0:
            cv2.putText(frame, f"Confidence: {confidence:.2f}", (30, 80), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    def update_fps(self, frame_height: int):
        """Update and return current FPS."""
        self.fps_counter += 1
        
        if self.fps_counter >= 30:  # Update every 30 frames
            elapsed = time.time() - self.fps_start_time
            self.current_fps = self.fps_counter / elapsed
            self.fps_counter = 0
            self.fps_start_time = time.time()
        
        return self.current_fps
    
    def draw_info(self, frame, frame_height: int):
        """Draw FPS and instructions on frame."""
        fps = self.update_fps(frame_height)
        cv2.putText(frame, f"FPS: {fps:.1f}", (30, frame_height - 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # Instructions
        cv2.putText(frame, "Press 'q' to quit, 'r' to reset", (30, frame_height - 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)