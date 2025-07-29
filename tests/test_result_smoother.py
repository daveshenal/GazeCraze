import unittest
import sys
import os

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.result_smoother import ResultSmoother

class TestResultSmoother(unittest.TestCase):
    """Test cases for ResultSmoother class."""
    
    def setUp(self):
        self.smoother = ResultSmoother(history_size=10)
    
    def test_initialization(self):
        """Test ResultSmoother initialization."""
        self.assertEqual(len(self.smoother.concentration_history), 0)
        self.assertEqual(self.smoother.history_size, 10)
    
    def test_smooth_result_insufficient_history(self):
        """Test smoothing with insufficient history."""
        result = self.smoother.smooth_result(True)
        self.assertTrue(result)  # Should return current result
        
        # Add a few more
        self.smoother.smooth_result(False)
        self.smoother.smooth_result(True)
        result = self.smoother.smooth_result(False)
        self.assertFalse(result)  # Should return current result
    
    def test_smooth_result_sufficient_history(self):
        """Test smoothing with sufficient history."""
        # Add enough history for majority vote
        for _ in range(3):
            self.smoother.smooth_result(True)
        for _ in range(2):
            self.smoother.smooth_result(False)
        
        # Should return True (3 out of 5)
        result = self.smoother.smooth_result(True)
        self.assertTrue(result)
    
    def test_smooth_result_majority_false(self):
        """Test smoothing with majority false."""
        # Add enough history for majority vote
        for _ in range(2):
            self.smoother.smooth_result(True)
        for _ in range(3):
            self.smoother.smooth_result(False)
        
        # Should return False (3 out of 5)
        result = self.smoother.smooth_result(False)
        self.assertFalse(result)
    
    def test_history_size_limit(self):
        """Test that history is limited to specified size."""
        # Add more entries than history size
        for i in range(15):
            self.smoother.smooth_result(i % 2 == 0)
        
        self.assertEqual(len(self.smoother.concentration_history), 10)
    
    def test_clear_history(self):
        """Test clearing history."""
        self.smoother.smooth_result(True)
        self.smoother.smooth_result(False)
        self.assertEqual(len(self.smoother.concentration_history), 2)
        
        self.smoother.clear_history()
        self.assertEqual(len(self.smoother.concentration_history), 0)
