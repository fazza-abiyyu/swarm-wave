import unittest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestUtilities(unittest.TestCase):
    def setUp(self):
        """Menyiapkan perlengkapan tes sebelum setiap metode tes."""
        pass
        
    def test_safe_convert_functions(self):
        """Menguji fungsi utilitas untuk konversi aman"""
        # Impor fungsi utilitas dari app
        from app import safe_convert_to_float, safe_convert_to_int
        
        # Menguji safe_convert_to_float
        self.assertEqual(safe_convert_to_float("3.14"), 3.14)
        self.assertEqual(safe_convert_to_float("invalid", 0.0), 0.0)
        self.assertEqual(safe_convert_to_float(None, 1.0), 1.0)
        self.assertEqual(safe_convert_to_float("", 2.0), 2.0)
        self.assertEqual(safe_convert_to_float("NaN", 3.0), 3.0)
        
        # Menguji safe_convert_to_int
        self.assertEqual(safe_convert_to_int("42"), 42)
        self.assertEqual(safe_convert_to_int("3.7"), 3)
        self.assertEqual(safe_convert_to_int("invalid", 0), 0)
        self.assertEqual(safe_convert_to_int(None, 1), 1)

    def test_data_formatting(self):
        """Menguji fungsi pemformatan data"""
        from app import safe_number
        
        # Menguji fungsi safe_number
        self.assertEqual(safe_number("5.5"), 5.5)
        self.assertEqual(safe_number("invalid"), 0.0)
        self.assertEqual(safe_number(None), 0.0)
        self.assertEqual(safe_number(""), 0.0)
        
    def test_generate_default_agents(self):
        """Menguji pembuatan agen default"""
        from app import generate_default_agents
        
        agents = generate_default_agents(3)
        self.assertEqual(len(agents), 3)
        
        for i, agent in enumerate(agents):
            self.assertIn('id', agent)
            self.assertEqual(agent['id'], f'Agent_{i+1}')
            self.assertIn('capacity', agent)
            self.assertIn('cost_per_hour', agent)
            
    def test_cost_function(self):
        """Menguji implementasi fungsi biaya"""
        from app import cost_function
        
        # Menguji jadwal dasar
        schedule = [
            {'task_id': 'Task_1', 'agent_id': 'Agent_1', 'start_time': 0, 'finish_time': 5},
            {'task_id': 'Task_2', 'agent_id': 'Agent_2', 'start_time': 0, 'finish_time': 3}
        ]
        
        makespan = 5
        cost = cost_function(schedule, makespan)
        
        # Biaya harus sama dengan makespan untuk kasus sederhana ini
        self.assertEqual(cost, makespan)

if __name__ == '__main__':
    unittest.main()
