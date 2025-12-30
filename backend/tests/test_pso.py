import unittest
import numpy as np
import sys
import os
from unittest.mock import patch, MagicMock

# Tambahkan direktori induk ke path untuk mengimpor model
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.pso import PSO_MultiAgent_Scheduler

class TestPSOAlgorithm(unittest.TestCase):
    def setUp(self):
        """Menyiapkan perlengkapan tes sebelum setiap metode tes."""
        self.tasks = [
            {'id': 'Task_1', 'length': 5, 'cost': 10},
            {'id': 'Task_2', 'length': 3, 'cost': 8},
            {'id': 'Task_3', 'length': 7, 'cost': 12}
        ]
        
        self.agents = [
            {'id': 'Agent_1'},
            {'id': 'Agent_2'}
        ]
        
        def cost_function(schedule, makespan):
            return makespan
            
        self.cost_function = cost_function
        
    def test_pso_initialization(self):
        """Menguji inisialisasi penjadwal PSO"""
        pso = PSO_MultiAgent_Scheduler(
            tasks=self.tasks,
            agents=self.agents,
            cost_function=self.cost_function,
            n_particles=10,
            n_iterations=20,
            w=0.5,
            c1=1.5,
            c2=1.5
        )
        
        self.assertEqual(pso.jumlah_tugas, 3)
        self.assertEqual(pso.jumlah_agen, 2)
        self.assertEqual(pso.jumlah_partikel, 10)
        self.assertEqual(pso.jumlah_iterasi, 20)
        self.assertEqual(pso.w, 0.5)
        self.assertEqual(pso.c1, 1.5)
        self.assertEqual(pso.c2, 1.5)
        self.assertFalse(pso.enable_dependencies)
        
        # Periksa inisialisasi swarm
        self.assertEqual(pso.posisi.shape, (10, 3))
        self.assertEqual(pso.kecepatan.shape, (10, 3))
        self.assertEqual(len(pso.biaya_pbest), 10)
        
    def test_pso_with_dependencies(self):
        """Menguji penjadwal PSO dengan dependensi diaktifkan"""
        tasks_with_deps = [
            {'id': 'Task_1', 'length': 5, 'dependencies': []},
            {'id': 'Task_2', 'length': 3, 'dependencies': ['Task_1']},
            {'id': 'Task_3', 'length': 7, 'dependencies': ['Task_1', 'Task_2']}
        ]
        
        pso = PSO_MultiAgent_Scheduler(
            tasks=tasks_with_deps,
            agents=self.agents,
            cost_function=self.cost_function,
            enable_dependencies=True
        )
        
        self.assertTrue(pso.enable_dependencies)
        self.assertIn('Task_1', pso.dependensi)
        self.assertIn('Task_2', pso.dependensi)
        self.assertIn('Task_3', pso.dependensi)
        
        # Periksa parsing dependensi
        self.assertEqual(pso.dependensi['Task_1'], [])
        self.assertEqual(pso.dependensi['Task_2'], ['Task_1'])
        self.assertEqual(pso.dependensi['Task_3'], ['Task_1', 'Task_2'])

    def test_position_to_sequence_without_dependencies(self):
        """Menguji konversi posisi ke urutan tanpa dependensi"""
        pso = PSO_MultiAgent_Scheduler(
            tasks=self.tasks,
            agents=self.agents,
            cost_function=self.cost_function
        )
        
        # Uji vektor posisi
        position = np.array([0.8, 0.2, 0.6])
        sequence = pso.position_to_sequence(position)
        
        # Harus mengembalikan indeks yang diurutkan berdasarkan nilai posisi (ascending untuk argsort)
        expected = np.array([1, 2, 0])  # argsort gives [0.2, 0.6, 0.8] indices
        np.testing.assert_array_equal(sequence, expected)

    def test_position_to_sequence_with_dependencies(self):
        """Menguji konversi posisi ke urutan dengan dependensi"""
        tasks_with_deps = [
            {'id': 'Task_1', 'length': 5, 'dependencies': []},
            {'id': 'Task_2', 'length': 3, 'dependencies': ['Task_1']},
            {'id': 'Task_3', 'length': 7, 'dependencies': ['Task_2']}
        ]
        
        pso = PSO_MultiAgent_Scheduler(
            tasks=tasks_with_deps,
            agents=self.agents,
            cost_function=self.cost_function,
            enable_dependencies=True
        )
        
        # Uji vektor posisi yang akan memilih Task_3 terlebih dahulu, tetapi dependensi mencegahnya
        position = np.array([0.5, 0.3, 0.9])
        sequence = pso.position_to_sequence(position)
        
        # Task_1 harus didahulukan (tanpa dependensi)
        # Task_2 harus setelah Task_1
        # Task_3 harus setelah Task_2
        self.assertEqual(sequence[0], 0)  # Task_1 pertama
        
        # Periksa bahwa dependensi dipatuhi
        task1_pos = np.where(sequence == 0)[0][0]
        task2_pos = np.where(sequence == 1)[0][0]
        task3_pos = np.where(sequence == 2)[0][0]
        
        self.assertLess(task1_pos, task2_pos)  # Task_1 before Task_2
        self.assertLess(task2_pos, task3_pos)  # Task_2 before Task_3

    def test_dependency_satisfaction(self):
        """Menguji pengecekan pemenuhan dependensi"""
        tasks_with_deps = [
            {'id': 'Task_1', 'length': 5, 'dependencies': []},
            {'id': 'Task_2', 'length': 3, 'dependencies': ['Task_1']},
            {'id': 'Task_3', 'length': 7, 'dependencies': ['Task_1', 'Task_2']}
        ]
        
        pso = PSO_MultiAgent_Scheduler(
            tasks=tasks_with_deps,
            agents=self.agents,
            cost_function=self.cost_function,
            enable_dependencies=True
        )
        
        # Task_1 tidak memiliki dependensi, harus selalu terpenuhi
        self.assertTrue(pso.is_dependency_satisfied('Task_1', set()))
        
        # Task_2 bergantung pada Task_1
        self.assertFalse(pso.is_dependency_satisfied('Task_2', set()))
        self.assertTrue(pso.is_dependency_satisfied('Task_2', {'Task_1'}))
        
        # Task_3 bergantung pada Task_1 dan Task_2
        self.assertFalse(pso.is_dependency_satisfied('Task_3', {'Task_1'}))
        self.assertTrue(pso.is_dependency_satisfied('Task_3', {'Task_1', 'Task_2'}))

    def test_load_balance_calculation(self):
        """Menguji perhitungan indeks load balance"""
        pso = PSO_MultiAgent_Scheduler(
            tasks=self.tasks,
            agents=self.agents,
            cost_function=self.cost_function
        )
        
        # Menguji skenario seimbang
        agent_times_balanced = {'Agent_1': 10, 'Agent_2': 10}
        balance_index = pso.calculate_load_balance_index(agent_times_balanced)
        self.assertEqual(balance_index, 0.0)
        
        # Menguji skenario tidak seimbang  
        agent_times_unbalanced = {'Agent_1': 5, 'Agent_2': 15}
        balance_index = pso.calculate_load_balance_index(agent_times_unbalanced)
        self.assertGreater(balance_index, 0.0)

    def test_evaluate_sequence_basic(self):
        """Menguji evaluasi urutan dasar"""
        pso = PSO_MultiAgent_Scheduler(
            tasks=self.tasks,
            agents=self.agents,
            cost_function=self.cost_function
        )
        
        sequence = np.array([0, 1, 2])  # Task_1, Task_2, Task_3
        # Manually perform evaluation matching optimize logic
        jadwal, waktu_agen = pso.position_to_schedule(sequence)
        durasi_total = max(waktu_agen.values(), default=0)
        balance = pso.calculate_load_balance_index(waktu_agen)
        cost = pso.fungsi_biaya(jadwal, durasi_total)
        
        # Harus mengembalikan biaya, jadwal, dan keseimbangan yang valid
        self.assertIsInstance(cost, (int, float))
        self.assertIsInstance(jadwal, list)
        self.assertIsInstance(balance, (int, float))
        self.assertEqual(len(jadwal), 3)
        
        # Periksa struktur jadwal
        for task_schedule in jadwal:
            self.assertIn('task_id', task_schedule)
            self.assertIn('agent_id', task_schedule)
            self.assertIn('start_time', task_schedule)
            self.assertIn('finish_time', task_schedule)

if __name__ == '__main__':
    unittest.main()
