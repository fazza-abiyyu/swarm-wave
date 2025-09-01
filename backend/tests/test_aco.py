import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add parent directory to path to import the models
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.aco import ACO_MultiAgent_Scheduler

class TestACOAlgorithm(unittest.TestCase):
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
            
        def heuristic_function(task):
            return 1.0 / task.get('length', 1)  # Inverse of task length
            
        self.cost_function = cost_function
        self.heuristic_function = heuristic_function
        
    def test_aco_initialization(self):
        """Test ACO scheduler initialization"""
        aco = ACO_MultiAgent_Scheduler(
            tasks=self.tasks,
            agents=self.agents,
            cost_function=self.cost_function,
            heuristic_function=self.heuristic_function,
            n_ants=5,
            n_iterations=10
        )
        
        self.assertEqual(aco.n_tasks, 3)
        self.assertEqual(aco.n_agents, 2)
        self.assertEqual(aco.n_ants, 5)
        self.assertEqual(aco.n_iterations, 10)
        self.assertFalse(aco.enable_dependencies)
        
    def test_aco_with_dependencies(self):
        """Test ACO scheduler with dependencies enabled"""
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
        self.assertIn('Task_1', aco.dependencies)
        self.assertIn('Task_2', aco.dependencies)
        self.assertIn('Task_3', aco.dependencies)
        
        # Check dependency parsing
        self.assertEqual(aco.dependencies['Task_1'], [])
        self.assertEqual(aco.dependencies['Task_2'], ['Task_1'])
        self.assertEqual(aco.dependencies['Task_3'], ['Task_1', 'Task_2'])

    def test_dependency_satisfaction(self):
        """Test dependency satisfaction checking"""
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
        
        # Task_1 has no dependencies, should always be satisfied
        self.assertTrue(aco._is_dependency_satisfied('Task_1', set()))
        
        # Task_2 depends on Task_1
        self.assertFalse(aco._is_dependency_satisfied('Task_2', set()))
        self.assertTrue(aco._is_dependency_satisfied('Task_2', {'Task_1'}))
        
        # Task_3 depends on both Task_1 and Task_2
        self.assertFalse(aco._is_dependency_satisfied('Task_3', {'Task_1'}))
        self.assertTrue(aco._is_dependency_satisfied('Task_3', {'Task_1', 'Task_2'}))

    def test_sequence_generation(self):
        """Test sequence generation without dependencies"""
        aco = ACO_MultiAgent_Scheduler(
            tasks=self.tasks,
            agents=self.agents,
            cost_function=self.cost_function,
            heuristic_function=self.heuristic_function
        )
        
        # Mock pheromone matrix for deterministic testing
        aco.pheromone_matrix = [[1.0, 0.5], [0.5, 1.0], [0.8, 0.3]]
        
        # Generate sequence
        sequence = aco._construct_solution()
        
        # Should return a valid sequence
        self.assertEqual(len(sequence), 3)
        self.assertEqual(set(sequence), {0, 1, 2})

    def test_load_balance_calculation(self):
        """Test load balance index calculation"""
        aco = ACO_MultiAgent_Scheduler(
            tasks=self.tasks,
            agents=self.agents,
            cost_function=self.cost_function,
            heuristic_function=self.heuristic_function
        )
        
        # Test balanced scenario
        agent_times_balanced = {'Agent_1': 10, 'Agent_2': 10}
        balance_index = aco._calculate_load_balance_index(agent_times_balanced)
        self.assertEqual(balance_index, 0.0)
        
        # Test unbalanced scenario  
        agent_times_unbalanced = {'Agent_1': 5, 'Agent_2': 15}
        balance_index = aco._calculate_load_balance_index(agent_times_unbalanced)
        self.assertGreater(balance_index, 0.0)

if __name__ == '__main__':
    unittest.main()
