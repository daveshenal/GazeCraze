import unittest
import numpy as np
import sys
import os
from unittest.mock import patch

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from concentration_detector import ConcentrationDetector
from tests.test_config import MockFaceLandmarks, MockFaceMeshProcessor

class TestConcentrationDetectorIntegration(unittest.TestCase):
    """Integration tests for the complete ConcentrationDetector."""
    
    def setUp(self):
        """Set up integration test with patched modules."""
        patcher = patch("concentration_detector.FaceMeshProcessor", new=MockFaceMeshProcessor)
        self.mock_processor = patcher.start()
        self.addCleanup(patcher.stop)

        self.detector = ConcentrationDetector()
    
    def test_initialization(self):
        """Test complete detector initialization."""
        self.assertIsNotNone(self.detector.eye_analyzer)
        self.assertIsNotNone(self.detector.head_analyzer)
        self.assertIsNotNone(self.detector.concentration_analyzer)
        self.assertIsNotNone(self.detector.smoother)
        self.assertIsNotNone(self.detector.performance_tracker)
    
    def test_is_concentrated_with_blinking(self):
        """Test concentration detection with blinking."""
        # Create landmarks for closed eyes
        landmarks = MockFaceLandmarks({
            # Closed eyes
            159: (0.3, 0.425, 0.0), 145: (0.3, 0.425, 0.0),
            133: (0.25, 0.425, 0.0), 33: (0.35, 0.425, 0.0),
            386: (0.7, 0.425, 0.0), 374: (0.7, 0.425, 0.0),
            362: (0.65, 0.425, 0.0), 263: (0.75, 0.425, 0.0)
        })
        
        is_concentrated, status, confidence = self.detector.is_concentrated(
            landmarks, 640, 480
        )
        
        self.assertFalse(is_concentrated)
        self.assertEqual(status, "Eyes Closed")
        self.assertEqual(confidence, 0.0)
    
    def test_is_concentrated_normal_gaze(self):
        """Test concentration detection with normal gaze."""
        landmarks = MockFaceLandmarks({
            # Open eyes
            159: (0.3, 0.4, 0.0), 145: (0.3, 0.45, 0.0),
            133: (0.25, 0.425, 0.0), 33: (0.35, 0.425, 0.0),
            386: (0.7, 0.4, 0.0), 374: (0.7, 0.45, 0.0),
            362: (0.65, 0.425, 0.0), 263: (0.75, 0.425, 0.0),
            # Center gaze
            468: (0.3, 0.425, 0.0), 473: (0.7, 0.425, 0.0)
        })
        
        is_concentrated, status, confidence = self.detector.is_concentrated(
            landmarks, 640, 480
        )
        
        self.assertTrue(is_concentrated)
        self.assertEqual(status, "Eyes on screen")
        self.assertGreater(confidence, 0.8)
    
    @patch('cv2.flip')
    @patch('cv2.cvtColor')
    def test_process_frame_no_face(self, mock_cvt_color, mock_flip):
        """Test frame processing with no face detected."""
        # Mock frame processing
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        mock_flip.return_value = frame
        mock_cvt_color.return_value = frame
        
        # The MockFaceMeshProcessor already returns no face landmarks
        processed_frame, status, color, confidence = self.detector.process_frame(frame)
        
        self.assertEqual(status, "No Face Detected")
        self.assertEqual(color, (0, 0, 255))  # Red
        self.assertEqual(confidence, 0.0)
    
    def test_reset_history(self):
        """Test resetting detection history."""
        # Add some history
        self.detector.smoother.smooth_result(True)
        self.detector.smoother.smooth_result(False)
        
        self.assertGreater(len(self.detector.smoother.concentration_history), 0)
        
        self.detector.reset_history()
        
        self.assertEqual(len(self.detector.smoother.concentration_history), 0)
    
    def test_get_performance_stats(self):
        """Test getting performance statistics."""
        # Simulate some frame processing
        self.detector.performance_tracker.increment_frame()
        self.detector.performance_tracker.increment_frame()
        
        stats = self.detector.get_performance_stats()
        
        self.assertIn('fps', stats)
        self.assertIn('total_frames', stats)
        self.assertIn('runtime', stats)
        self.assertEqual(stats['total_frames'], 2)