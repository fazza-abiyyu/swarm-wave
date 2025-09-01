import unittest
import numpy as np
import sys
import os
from unittest.mock import patch, MagicMock

# Add parent directory to path to import the models
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.pso import PSO_MultiAgent_Scheduler

class TestPSOAlgorithm(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
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
        """Test PSO scheduler initialization"""
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
        
        self.assertEqual(pso.n_tasks, 3)
        self.assertEqual(pso.n_agents, 2)
        self.assertEqual(pso.n_particles, 10)
        self.assertEqual(pso.n_iterations, 20)
        self.assertEqual(pso.w, 0.5)
        self.assertEqual(pso.c1, 1.5)
        self.assertEqual(pso.c2, 1.5)
        self.assertFalse(pso.enable_dependencies)
        
        # Check swarm initialization
        self.assertEqual(pso.positions.shape, (10, 3))
        self.assertEqual(pso.velocities.shape, (10, 3))
        self.assertEqual(len(pso.pbest_costs), 10)
        
    def test_pso_with_dependencies(self):
        """Test PSO scheduler with dependencies enabled"""
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
        self.assertIn('Task_1', pso.dependencies)
        self.assertIn('Task_2', pso.dependencies)
        self.assertIn('Task_3', pso.dependencies)
        
        # Check dependency parsing
        self.assertEqual(pso.dependencies['Task_1'], [])
        self.assertEqual(pso.dependencies['Task_2'], ['Task_1'])
        self.assertEqual(pso.dependencies['Task_3'], ['Task_1', 'Task_2'])

    def test_position_to_sequence_without_dependencies(self):
        """Test position to sequence conversion without dependencies"""
        pso = PSO_MultiAgent_Scheduler(
            tasks=self.tasks,
            agents=self.agents,
            cost_function=self.cost_function
        )
        
        # Test position vector
        position = np.array([0.8, 0.2, 0.6])
        sequence = pso._position_to_sequence(position)
        
        # Should return sorted indices by position values (ascending for argsort)
        expected = np.array([1, 2, 0])  # argsort gives [0.2, 0.6, 0.8] indices
        np.testing.assert_array_equal(sequence, expected)

    def test_position_to_sequence_with_dependencies(self):
        """Test position to sequence conversion with dependencies"""
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
        
        # Test position vector that would prefer Task_3 first, but dependencies prevent it
        position = np.array([0.5, 0.3, 0.9])
        sequence = pso._position_to_sequence(position)
        
        # Task_1 should come first (no dependencies)
        # Task_2 should come after Task_1
        # Task_3 should come after Task_2
        self.assertEqual(sequence[0], 0)  # Task_1 first
        
        # Check that dependencies are respected
        task1_pos = np.where(sequence == 0)[0][0]
        task2_pos = np.where(sequence == 1)[0][0]
        task3_pos = np.where(sequence == 2)[0][0]
        
        self.assertLess(task1_pos, task2_pos)  # Task_1 before Task_2
        self.assertLess(task2_pos, task3_pos)  # Task_2 before Task_3

    def test_dependency_satisfaction(self):
        """Test dependency satisfaction checking"""
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
        
        # Task_1 has no dependencies, should always be satisfied
        self.assertTrue(pso._is_dependency_satisfied('Task_1', set()))
        
        # Task_2 depends on Task_1
        self.assertFalse(pso._is_dependency_satisfied('Task_2', set()))
        self.assertTrue(pso._is_dependency_satisfied('Task_2', {'Task_1'}))
        
        # Task_3 depends on both Task_1 and Task_2
        self.assertFalse(pso._is_dependency_satisfied('Task_3', {'Task_1'}))
        self.assertTrue(pso._is_dependency_satisfied('Task_3', {'Task_1', 'Task_2'}))

    def test_load_balance_calculation(self):
        """Test load balance index calculation"""
        pso = PSO_MultiAgent_Scheduler(
            tasks=self.tasks,
            agents=self.agents,
            cost_function=self.cost_function
        )
        
        # Test balanced scenario
        agent_times_balanced = {'Agent_1': 10, 'Agent_2': 10}
        balance_index = pso._calculate_load_balance_index(agent_times_balanced)
        self.assertEqual(balance_index, 0.0)
        
        # Test unbalanced scenario  
        agent_times_unbalanced = {'Agent_1': 5, 'Agent_2': 15}
        balance_index = pso._calculate_load_balance_index(agent_times_unbalanced)
        self.assertGreater(balance_index, 0.0)

    def test_evaluate_sequence_basic(self):
        """Test basic sequence evaluation"""
        pso = PSO_MultiAgent_Scheduler(
            tasks=self.tasks,
            agents=self.agents,
            cost_function=self.cost_function
        )
        
        sequence = np.array([0, 1, 2])  # Task_1, Task_2, Task_3
        cost, schedule, balance = pso._evaluate_sequence(sequence)
        
        # Should return valid cost, schedule and balance
        self.assertIsInstance(cost, (int, float))
        self.assertIsInstance(schedule, list)
        self.assertIsInstance(balance, (int, float))
        self.assertEqual(len(schedule), 3)
        
        # Check schedule structure
        for task_schedule in schedule:
            self.assertIn('task_id', task_schedule)
            self.assertIn('agent_id', task_schedule)
            self.assertIn('start_time', task_schedule)
            self.assertIn('finish_time', task_schedule)

if __name__ == '__main__':
    unittest.main()
