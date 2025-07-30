import unittest
import sys
import os
import time

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.performance_tracker import PerformanceTracker

class TestPerformanceTracker(unittest.TestCase):
    """Test cases for PerformanceTracker class."""
    
    def setUp(self):
        self.tracker = PerformanceTracker()
    
    def test_initialization(self):
        """Test PerformanceTracker initialization."""
        self.assertEqual(self.tracker.frame_count, 0)
        self.assertIsInstance(self.tracker.start_time, float)
    
    def test_increment_frame(self):
        """Test frame counting."""
        initial_count = self.tracker.frame_count
        self.tracker.increment_frame()
        self.assertEqual(self.tracker.frame_count, initial_count + 1)
    
    def test_get_stats(self):
        """Test performance statistics."""
        self.tracker.increment_frame()
        time.sleep(0.1)  # Small delay
        self.tracker.increment_frame()
        
        stats = self.tracker.get_stats()
        
        self.assertIn('fps', stats)
        self.assertIn('total_frames', stats)
        self.assertIn('runtime', stats)
        self.assertEqual(stats['total_frames'], 2)
        self.assertGreater(stats['runtime'], 0)
        self.assertGreater(stats['fps'], 0)

