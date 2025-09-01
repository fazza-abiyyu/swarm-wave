import unittest
import sys
import os

# Add parent directory to path to import test modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_app import TestFlaskApp
from tests.test_aco import TestACOAlgorithm
from tests.test_pso import TestPSOAlgorithm

def create_test_suite():
    """Create a comprehensive test suite for all backend components"""
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    # Add Flask app tests
    test_suite.addTest(loader.loadTestsFromTestCase(TestFlaskApp))
    
    # Add ACO algorithm tests
    test_suite.addTest(loader.loadTestsFromTestCase(TestACOAlgorithm))
    
    # Add PSO algorithm tests
    test_suite.addTest(loader.loadTestsFromTestCase(TestPSOAlgorithm))
    
    return test_suite

if __name__ == '__main__':
    # Create and run the test suite
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"TEST SUMMARY")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print(f"\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
            
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
