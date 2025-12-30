#!/usr/bin/env python3
"""
Individual test runner for backend components
Run specific test modules with detailed output
"""

import unittest
import sys
import os

# Tambahkan direktori induk ke path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_individual_tests():
    """Menu interaktif untuk menjalankan modul tes individu"""
    
    test_modules = {
        '1': ('tests.test_app', 'Tes Aplikasi Flask'),
        '2': ('tests.test_aco', 'Tes Algoritma ACO'),  
        '3': ('tests.test_pso', 'Tes Algoritma PSO'),
        '4': ('tests.test_utilities', 'Tes Fungsi Utilitas'),
        '5': ('all', 'Semua Tes (Suite Komprehensif)')
    }
    
    print("\n" + "="*50)
    print("BACKEND UNIT TEST RUNNER")  
    print("="*50)
    print("Pilih tes yang akan dijalankan:")
    
    for key, (module, description) in test_modules.items():
        print(f"{key}. {description}")
    
    choice = input("\nMasukkan pilihan Anda (1-5): ").strip()
    
    if choice not in test_modules:
        print(f"Pilihan tidak valid: {choice}")
        return
        
    module, description = test_modules[choice]
    
    print(f"\nMenjalankan: {description}")
    print("-" * 50)
    
    if choice == '5':  # Semua tes
        from tests.run_tests import create_test_suite
        suite = create_test_suite()
    else:
        # Muat modul spesifik
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromName(module)
    
    # Jalankan tes dengan output verbose
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # Cetak ringkasan detail
    print(f"\n" + "="*50)
    print(f"HASIL TES DETAIL: {description}")
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
        print(f"\n✅ SEMUA TES BERHASIL!")
    else:
        print(f"\n❌ Beberapa tes gagal. Periksa output di atas.")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_individual_tests()
    sys.exit(0 if success else 1)
