import unittest
import sys
import os

from tests.test_camera_manager import TestCameraManager
from tests.test_concentration_analyzer import TestConcentrationAnalyzer
from tests.test_concentration_detector import TestConcentrationDetectorIntegration
from tests.test_display_manager import TestDisplayManager
from tests.test_eye_analyzer import TestEyeAnalyzer
from tests.test_head_pose_analyzer import TestHeadPoseAnalyzer
from tests.test_performance_tracker import TestPerformanceTracker
from tests.test_result_smoother import TestResultSmoother

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def run_tests():
    """Run all tests with better error handling."""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestEyeAnalyzer,
        TestHeadPoseAnalyzer,
        TestConcentrationAnalyzer,
        TestResultSmoother,
        TestPerformanceTracker,
        TestCameraManager,
        TestDisplayManager,
        TestConcentrationDetectorIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Create custom test runner with better formatting
    class CustomTestResult(unittest.TextTestResult):
        def addError(self, test, err):
            super().addError(test, err)
            print(f"\nERROR in {test}: {err[1]}")
        
        def addFailure(self, test, err):
            super().addFailure(test, err)
            print(f"\nFAILURE in {test}: {err[1]}")
    
    class CustomTestRunner(unittest.TextTestRunner):
        resultclass = CustomTestResult
    
    # Run tests
    runner = CustomTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100)
        print(f"Success rate: {success_rate:.1f}%")
    else:
        print("No tests were run!")
    print(f"{'='*60}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)