import unittest
import sys
import os

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.head_pose_analyzer import HeadPoseAnalyzer
from tests.test_config import MockFaceLandmarks

class TestHeadPoseAnalyzer(unittest.TestCase):
    """Test cases for HeadPoseAnalyzer class."""
    
    def setUp(self):
        self.head_analyzer = HeadPoseAnalyzer()
        self.frame_width = 640
        self.frame_height = 480
    
    def test_initialization(self):
        """Test HeadPoseAnalyzer initialization."""
        self.assertEqual(self.head_analyzer.face_tilt_threshold, 15)
        self.assertEqual(self.head_analyzer.head_pose_threshold, 0.028)
    
    def test_check_face_tilt_normal(self):
        """Test face tilt detection with normal pose."""
        landmarks = MockFaceLandmarks({
            33: (0.35, 0.4, 0.0),   # left_eye_outer
            263: (0.65, 0.4, 0.0)   # right_eye_outer (same Y = no tilt)
        })
        
        is_tilted, confidence = self.head_analyzer.check_face_tilt(
            landmarks, self.frame_width, self.frame_height
        )
        
        self.assertFalse(is_tilted)
        self.assertEqual(confidence, 1.0)
    
    def test_check_face_tilt_tilted(self):
        """Test face tilt detection with tilted face."""
        landmarks = MockFaceLandmarks({
            33: (0.35, 0.35, 0.0),   # left_eye_outer
            263: (0.65, 0.45, 0.0)   # right_eye_outer (significant Y difference)
        })
        
        is_tilted, confidence = self.head_analyzer.check_face_tilt(
            landmarks, self.frame_width, self.frame_height
        )
        
        self.assertTrue(is_tilted)
        self.assertLess(confidence, 1.0)
    
    def test_analyze_head_pose_center(self):
        """Test head pose analysis for center position."""
        landmarks = MockFaceLandmarks({
            468: (0.3, 0.425, 0.0),   # left iris
            473: (0.7, 0.425, 0.0)    # right iris (same Z = center)
        })
        
        has_turn, direction, z_diff = self.head_analyzer.analyze_head_pose(landmarks)
        
        self.assertFalse(has_turn)
        self.assertEqual(direction, "center")
        self.assertLessEqual(z_diff, self.head_analyzer.head_pose_threshold)
    
    def test_analyze_head_pose_left_turn(self):
        """Test head pose analysis for left turn."""
        landmarks = MockFaceLandmarks({
            468: (0.3, 0.425, 0.05),  # left iris (higher Z)
            473: (0.7, 0.425, 0.0)    # right iris
        })
        
        has_turn, direction, z_diff = self.head_analyzer.analyze_head_pose(landmarks)
        
        self.assertTrue(has_turn)
        self.assertEqual(direction, "left")
        self.assertGreater(z_diff, self.head_analyzer.head_pose_threshold)
    
    def test_analyze_head_pose_right_turn(self):
        """Test head pose analysis for right turn."""
        landmarks = MockFaceLandmarks({
            468: (0.3, 0.425, 0.0),   # left iris
            473: (0.7, 0.425, 0.05)   # right iris (higher Z)
        })
        
        has_turn, direction, z_diff = self.head_analyzer.analyze_head_pose(landmarks)
        
        self.assertTrue(has_turn)
        self.assertEqual(direction, "right")
        self.assertGreater(z_diff, self.head_analyzer.head_pose_threshold)

