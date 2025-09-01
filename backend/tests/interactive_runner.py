#!/usr/bin/env python3
"""
Individual test runner for backend components
Run specific test modules with detailed output
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_individual_tests():
    """Interactive menu for running individual test modules"""
    
    test_modules = {
        '1': ('tests.test_app', 'Flask Application Tests'),
        '2': ('tests.test_aco', 'ACO Algorithm Tests'),  
        '3': ('tests.test_pso', 'PSO Algorithm Tests'),
        '4': ('tests.test_utilities', 'Utility Function Tests'),
        '5': ('all', 'All Tests (Comprehensive Suite)')
    }
    
    print("\n" + "="*50)
    print("BACKEND UNIT TEST RUNNER")  
    print("="*50)
    print("Select tests to run:")
    
    for key, (module, description) in test_modules.items():
        print(f"{key}. {description}")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice not in test_modules:
        print(f"Invalid choice: {choice}")
        return
        
    module, description = test_modules[choice]
    
    print(f"\nRunning: {description}")
    print("-" * 50)
    
    if choice == '5':  # All tests
        from tests.run_tests import create_test_suite
        suite = create_test_suite()
    else:
        # Load specific module
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromName(module)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # Print detailed summary
    print(f"\n" + "="*50)
    print(f"DETAILED TEST RESULTS: {description}")
    print("="*50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(getattr(result, 'skipped', []))}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFAILURES ({len(result.failures)}):")
        for i, (test, traceback) in enumerate(result.failures, 1):
            print(f"{i}. {test}")
            print(f"   {traceback.strip().split()[-1]}")
    
    if result.errors:
        print(f"\nERRORS ({len(result.errors)}):")
        for i, (test, traceback) in enumerate(result.errors, 1):
            print(f"{i}. {test}")
            print(f"   {traceback.strip().split()[-1]}")
    
    if result.wasSuccessful():
        print(f"\n✅ ALL TESTS PASSED!")
    else:
        print(f"\n❌ Some tests failed. Check output above.")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_individual_tests()
    sys.exit(0 if success else 1)
