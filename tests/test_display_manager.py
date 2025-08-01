import unittest
import numpy as np
import sys
import os
from unittest.mock import patch
import time

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.display_manager import DisplayManager

class TestDisplayManager(unittest.TestCase):
    """Test cases for DisplayManager class."""
    
    def setUp(self):
        self.display = DisplayManager()
    
    def test_initialization(self):
        """Test DisplayManager initialization."""
        self.assertEqual(self.display.fps_counter, 0)
        self.assertEqual(self.display.current_fps, 0.0)
    
    @patch('cv2.putText')
    def test_draw_status(self, mock_put_text):
        """Test drawing status on frame."""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        self.display.draw_status(frame, "Test Status", (0, 255, 0), 0.85)
        
        # Should be called at least twice (status and confidence)
        self.assertGreaterEqual(mock_put_text.call_count, 2)
    
    def test_update_fps_fixed(self):
        """Test FPS updating with proper timing."""
        # Set a proper start time to avoid division by zero
        self.display.fps_start_time = time.time() - 1.0  # 1 second ago
        
        # Simulate 30 frame updates
        for _ in range(30):
            fps = self.display.update_fps(480)
        
        # After 30 frames, FPS should be calculated and > 0
        self.assertGreater(fps, 0)
    
    @patch('cv2.putText')
    def test_draw_info(self, mock_put_text):
        """Test drawing info on frame."""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # Set proper timing to avoid division by zero
        self.display.fps_start_time = time.time() - 1.0
        self.display.draw_info(frame, 480)
        
        # Should be called twice (FPS and instructions)
        self.assertEqual(mock_put_text.call_count, 2)
