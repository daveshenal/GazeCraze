import unittest
import numpy as np
import sys
import os
from unittest.mock import Mock, patch

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.camera_manager import CameraManager

class TestCameraManager(unittest.TestCase):
    """Test cases for CameraManager class."""
    
    @patch('cv2.VideoCapture')
    def test_initialization_success(self, mock_video_capture):
        """Test successful camera initialization."""
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = [640, 480]  # width, height
        mock_video_capture.return_value = mock_cap
        
        camera = CameraManager()
        
        self.assertEqual(camera.frame_width, 640)
        self.assertEqual(camera.frame_height, 480)
        mock_cap.set.assert_called()
    
    @patch('cv2.VideoCapture')
    def test_initialization_failure(self, mock_video_capture):
        """Test camera initialization failure."""
        mock_cap = Mock()
        mock_cap.isOpened.return_value = False
        mock_video_capture.return_value = mock_cap
        
        with self.assertRaises(RuntimeError):
            CameraManager()
    
    @patch('cv2.VideoCapture')
    def test_read_frame(self, mock_video_capture):
        """Test frame reading."""
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = [640, 480]
        mock_cap.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))
        mock_video_capture.return_value = mock_cap
        
        camera = CameraManager()
        ret, frame = camera.read_frame()
        
        self.assertTrue(ret)
        self.assertIsNotNone(frame)
        mock_cap.read.assert_called_once()
    
    @patch('cv2.VideoCapture')
    def test_get_dimensions(self, mock_video_capture):
        """Test getting camera dimensions."""
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = [640, 480]
        mock_video_capture.return_value = mock_cap
        
        camera = CameraManager()
        width, height = camera.get_dimensions()
        
        self.assertEqual(width, 640)
        self.assertEqual(height, 480)
    
    @patch('cv2.VideoCapture')
    def test_release(self, mock_video_capture):
        """Test camera release."""
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = [640, 480]
        mock_video_capture.return_value = mock_cap
        
        camera = CameraManager()
        camera.release()
        
        mock_cap.release.assert_called_once()
