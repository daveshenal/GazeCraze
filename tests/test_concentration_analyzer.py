import unittest
import sys
import os

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.concentration_analyzer import ConcentrationAnalyzer

class TestConcentrationAnalyzer(unittest.TestCase):
    """Test cases for ConcentrationAnalyzer class."""
    
    def setUp(self):
        self.analyzer = ConcentrationAnalyzer()
    
    def test_initialization(self):
        """Test ConcentrationAnalyzer initialization."""
        self.assertEqual(self.analyzer.gaze_ratio_threshold, 0.55)
        self.assertEqual(self.analyzer.iris_alignment_threshold, 0.14)
    
    def test_analyze_gaze_center_aligned(self):
        """Test gaze analysis with center head and aligned eyes."""
        is_concentrated, status, confidence = self.analyzer.analyze_gaze_direction(
            0.5, 0.5, "center"  # Both eyes looking center
        )
        
        self.assertTrue(is_concentrated)
        self.assertEqual(status, "Eyes on screen")
        self.assertGreater(confidence, 0.8)
    
    def test_analyze_gaze_center_misaligned(self):
        """Test gaze analysis with center head but misaligned eyes."""
        is_concentrated, status, confidence = self.analyzer.analyze_gaze_direction(
            0.3, 0.7, "center"  # Eyes looking in different directions
        )
        
        self.assertFalse(is_concentrated)
        self.assertIn("Eyes on", status)
    
    def test_analyze_gaze_left_turn_concentrated(self):
        """Test gaze analysis with left head turn but concentrated."""
        is_concentrated, status, confidence = self.analyzer.analyze_gaze_direction(
            0.4, 0.5, "left"  # Left gaze ratio below threshold
        )
        
        self.assertTrue(is_concentrated)
        self.assertEqual(status, "Head: Left Turn")
    
    def test_analyze_gaze_left_turn_distracted(self):
        """Test gaze analysis with left head turn and distracted."""
        is_concentrated, status, confidence = self.analyzer.analyze_gaze_direction(
            0.8, 0.5, "left"  # Left gaze ratio above threshold
        )
        
        self.assertFalse(is_concentrated)
        self.assertEqual(status, "Looking Left")
    
    def test_analyze_gaze_right_turn_concentrated(self):
        """Test gaze analysis with right head turn but concentrated."""
        is_concentrated, status, confidence = self.analyzer.analyze_gaze_direction(
            0.5, 0.4, "right"  # Right gaze ratio below threshold
        )
        
        self.assertTrue(is_concentrated)
        self.assertEqual(status, "Head: Right Turn")
    
    def test_analyze_gaze_right_turn_distracted(self):
        """Test gaze analysis with right head turn and distracted."""
        is_concentrated, status, confidence = self.analyzer.analyze_gaze_direction(
            0.5, 0.8, "right"  # Right gaze ratio above threshold
        )
        
        self.assertFalse(is_concentrated)
        self.assertEqual(status, "Looking Right")

