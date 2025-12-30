import unittest
import sys
import os

# Tambahkan direktori induk ke path untuk mengimpor modul tes
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_app import TestFlaskApp
from tests.test_aco import TestACOAlgorithm
from tests.test_pso import TestPSOAlgorithm

def create_test_suite():
    """Membuat test suite komprehensif untuk semua komponen backend"""
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    # Tambahkan tes Flask app
    test_suite.addTest(loader.loadTestsFromTestCase(TestFlaskApp))
    
    # Tambahkan tes algoritma ACO
    test_suite.addTest(loader.loadTestsFromTestCase(TestACOAlgorithm))
    
    # Tambahkan tes algoritma PSO
    test_suite.addTest(loader.loadTestsFromTestCase(TestPSOAlgorithm))
    
    return test_suite

if __name__ == '__main__':
    # Buat dan jalankan test suite
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Cetak ringkasan
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
            
    # Keluar dengan kode yang sesuai
    sys.exit(0 if result.wasSuccessful() else 1)
