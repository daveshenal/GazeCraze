import unittest
import sys
import os

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.eye_analyzer import EyeAnalyzer
from tests.test_config import MockFaceLandmarks

class TestEyeAnalyzer(unittest.TestCase):
    """Test cases for EyeAnalyzer class."""
    
    def setUp(self):
        self.eye_analyzer = EyeAnalyzer()
        self.frame_width = 640
        self.frame_height = 480
    
    def test_initialization(self):
        """Test EyeAnalyzer initialization."""
        self.assertEqual(self.eye_analyzer.ear_threshold, 0.25)
        self.assertEqual(self.eye_analyzer.left_eye_top, 159)
        self.assertEqual(self.eye_analyzer.right_eye_top, 386)
    
    def test_calculate_ear_normal(self):
        """Test EAR calculation with normal eye opening."""
        landmarks = MockFaceLandmarks({
            159: (0.3, 0.4, 0.0),  # left_eye_top
            145: (0.3, 0.45, 0.0),  # left_eye_bottom
            133: (0.25, 0.425, 0.0),  # left_eye_inner
            33: (0.35, 0.425, 0.0)   # left_eye_outer
        })
        
        ear = self.eye_analyzer.calculate_ear(
            159, 145, 133, 33, landmarks, self.frame_width, self.frame_height
        )
        
        self.assertGreater(ear, 0)
        self.assertLess(ear, 1)
    
    def test_calculate_ear_closed_eye(self):
        """Test EAR calculation with closed eye."""
        landmarks = MockFaceLandmarks({
            159: (0.3, 0.425, 0.0),  # left_eye_top
            145: (0.3, 0.425, 0.0),  # left_eye_bottom (same as top = closed)
            133: (0.25, 0.425, 0.0),  # left_eye_inner
            33: (0.35, 0.425, 0.0)   # left_eye_outer
        })
        
        ear = self.eye_analyzer.calculate_ear(
            159, 145, 133, 33, landmarks, self.frame_width, self.frame_height
        )
        
        self.assertEqual(ear, 0)  # Closed eye should have EAR of 0
    
    def test_detect_blinks_open_eyes(self):
        """Test blink detection with open eyes."""
        landmarks = MockFaceLandmarks({
            # Left eye (open)
            159: (0.3, 0.4, 0.0), 145: (0.3, 0.45, 0.0),
            133: (0.25, 0.425, 0.0), 33: (0.35, 0.425, 0.0),
            # Right eye (open)
            386: (0.7, 0.4, 0.0), 374: (0.7, 0.45, 0.0),
            362: (0.65, 0.425, 0.0), 263: (0.75, 0.425, 0.0)
        })
        
        is_blinking = self.eye_analyzer.detect_blinks(landmarks, self.frame_width, self.frame_height)
        self.assertFalse(is_blinking)
    
    def test_detect_blinks_closed_eyes(self):
        """Test blink detection with closed eyes."""
        landmarks = MockFaceLandmarks({
            # Left eye (closed)
            159: (0.3, 0.425, 0.0), 145: (0.3, 0.425, 0.0),
            133: (0.25, 0.425, 0.0), 33: (0.35, 0.425, 0.0),
            # Right eye (closed)
            386: (0.7, 0.425, 0.0), 374: (0.7, 0.425, 0.0),
            362: (0.65, 0.425, 0.0), 263: (0.75, 0.425, 0.0)
        })
        
        is_blinking = self.eye_analyzer.detect_blinks(landmarks, self.frame_width, self.frame_height)
        self.assertTrue(is_blinking)
    
    def test_calculate_gaze_ratios_center(self):
        """Test gaze ratio calculation for center gaze."""
        landmarks = MockFaceLandmarks({
            468: (0.3, 0.425, 0.0),   # left iris (center of eye)
            473: (0.7, 0.425, 0.0),   # right iris (center of eye)
            133: (0.25, 0.425, 0.0),  # left_eye_inner
            33: (0.35, 0.425, 0.0),   # left_eye_outer
            362: (0.65, 0.425, 0.0),  # right_eye_inner
            263: (0.75, 0.425, 0.0)   # right_eye_outer
        })
        
        left_ratio, right_ratio = self.eye_analyzer.calculate_gaze_ratios(
            landmarks, self.frame_width, self.frame_height
        )
        
        # Center gaze should have ratios around 0.5
        self.assertAlmostEqual(left_ratio, 0.5, places=1)
        self.assertAlmostEqual(right_ratio, 0.5, places=1)
    
    def test_calculate_gaze_ratios_division_by_zero(self):
        """Test gaze ratio calculation with zero eye width."""
        landmarks = MockFaceLandmarks({
            468: (0.3, 0.425, 0.0),   # left iris
            473: (0.7, 0.425, 0.0),   # right iris
            133: (0.3, 0.425, 0.0),   # left_eye_inner (same as outer)
            33: (0.3, 0.425, 0.0),    # left_eye_outer
            362: (0.65, 0.425, 0.0),  # right_eye_inner
            263: (0.75, 0.425, 0.0)   # right_eye_outer
        })
        
        with self.assertRaises(ValueError):
            self.eye_analyzer.calculate_gaze_ratios(landmarks, self.frame_width, self.frame_height)
