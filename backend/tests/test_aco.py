import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Tambahkan direktori induk ke path untuk mengimpor model
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.aco import ACO_MultiAgent_Scheduler

class TestACOAlgorithm(unittest.TestCase):
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
            
        def heuristic_function(task):
            return 1.0 / task.get('length', 1)  # Inverse of task length
            
        self.cost_function = cost_function
        self.heuristic_function = heuristic_function
        
    def test_aco_initialization(self):
        """Menguji inisialisasi penjadwal ACO"""
        aco = ACO_MultiAgent_Scheduler(
            tasks=self.tasks,
            agents=self.agents,
            cost_function=self.cost_function,
            heuristic_function=self.heuristic_function,
            n_ants=5,
            n_iterations=10
        )
        
        self.assertEqual(aco.jumlah_tugas, 3)
        self.assertEqual(aco.jumlah_agen, 2)
        self.assertEqual(aco.jumlah_semut, 5)
        self.assertEqual(aco.jumlah_iterasi, 10)
        self.assertFalse(aco.enable_dependencies)
        
    def test_aco_with_dependencies(self):
        """Menguji penjadwal ACO dengan dependensi diaktifkan"""
        tasks_with_deps = [
            {'id': 'Task_1', 'length': 5, 'dependencies': []},
            {'id': 'Task_2', 'length': 3, 'dependencies': ['Task_1']},
            {'id': 'Task_3', 'length': 7, 'dependencies': ['Task_1', 'Task_2']}
        ]
        
        aco = ACO_MultiAgent_Scheduler(
            tasks=tasks_with_deps,
            agents=self.agents,
            cost_function=self.cost_function,
            heuristic_function=self.heuristic_function,
            enable_dependencies=True
        )
        
        self.assertTrue(aco.enable_dependencies)
        self.assertIn('Task_1', aco.dependensi)
        self.assertIn('Task_2', aco.dependensi)
        self.assertIn('Task_3', aco.dependensi)
        
        # Periksa parsing dependensi
        self.assertEqual(aco.dependensi['Task_1'], [])
        self.assertEqual(aco.dependensi['Task_2'], ['Task_1'])
        self.assertEqual(aco.dependensi['Task_3'], ['Task_1', 'Task_2'])

    def test_dependency_satisfaction(self):
        """Menguji pengecekan pemenuhan dependensi"""
        tasks_with_deps = [
            {'id': 'Task_1', 'length': 5, 'dependencies': []},
            {'id': 'Task_2', 'length': 3, 'dependencies': ['Task_1']},
            {'id': 'Task_3', 'length': 7, 'dependencies': ['Task_1', 'Task_2']}
        ]
        
        aco = ACO_MultiAgent_Scheduler(
            tasks=tasks_with_deps,
            agents=self.agents,
            cost_function=self.cost_function,
            heuristic_function=self.heuristic_function,
            enable_dependencies=True
        )
        
        # Task_1 tidak memiliki dependensi, harus selalu terpenuhi
        self.assertTrue(aco.is_dependency_satisfied('Task_1', set()))
        
        # Task_2 bergantung pada Task_1
        self.assertFalse(aco.is_dependency_satisfied('Task_2', set()))
        self.assertTrue(aco.is_dependency_satisfied('Task_2', {'Task_1'}))
        
        # Task_3 bergantung pada Task_1 dan Task_2
        self.assertFalse(aco.is_dependency_satisfied('Task_3', {'Task_1'}))
        self.assertTrue(aco.is_dependency_satisfied('Task_3', {'Task_1', 'Task_2'}))

    def test_sequence_generation(self):
        """Menguji pembuatan urutan tanpa dependensi"""
        aco = ACO_MultiAgent_Scheduler(
            tasks=self.tasks,
            agents=self.agents,
            cost_function=self.cost_function,
            heuristic_function=self.heuristic_function
        )
        
        # Mock matriks feromon untuk pengujian deterministik
        aco.pheromone_matrix = [[1.0, 0.5], [0.5, 1.0], [0.8, 0.3]]
        
        # Generate urutan
        sequence = aco.construct_solution()
        
        # Harus mengembalikan urutan yang valid
        self.assertEqual(len(sequence), 3)
        self.assertEqual(set(sequence), {0, 1, 2})

    def test_load_balance_calculation(self):
        """Menguji perhitungan indeks load balance"""
        aco = ACO_MultiAgent_Scheduler(
            tasks=self.tasks,
            agents=self.agents,
            cost_function=self.cost_function,
            heuristic_function=self.heuristic_function
        )
        
        # Menguji skenario seimbang
        agent_times_balanced = {'Agent_1': 10, 'Agent_2': 10}
        balance_index = aco.calculate_load_balance_index(agent_times_balanced)
        self.assertEqual(balance_index, 0.0)
        
        # Menguji skenario tidak seimbang  
        agent_times_unbalanced = {'Agent_1': 5, 'Agent_2': 15}
        balance_index = aco.calculate_load_balance_index(agent_times_unbalanced)
        self.assertGreater(balance_index, 0.0)

if __name__ == '__main__':
    unittest.main()
