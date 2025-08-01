from unittest.mock import Mock

class MockLandmark:
    """Mock class for MediaPipe landmarks."""
    def __init__(self, x=0.5, y=0.5, z=0.0):
        self.x = x
        self.y = y
        self.z = z


class MockFaceLandmarks:
    """Mock class for MediaPipe face landmarks."""
    def __init__(self, landmarks_dict=None):
        self.landmark = {}
        if landmarks_dict:
            for idx, (x, y, z) in landmarks_dict.items():
                self.landmark[idx] = MockLandmark(x, y, z)
        else:
            # Default landmarks for basic testing
            for i in range(500):  # MediaPipe has 468+ landmarks
                self.landmark[i] = MockLandmark()

# Mock the import for integration tests
class MockFaceMeshProcessor:
    def __init__(self, *args, **kwargs):
        pass
    
    def process_frame(self, frame):
        mock_results = Mock()
        mock_results.multi_face_landmarks = None
        return mock_results
    
    def cleanup(self):
        pass