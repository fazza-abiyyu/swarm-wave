import unittest
import json
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertIn('timestamp', data)
        self.assertIn('application', data)
        self.assertIn('version', data['application'])
        self.assertIn('algorithms', data)
        
    def test_health_check_structure(self):
        """Test health check response structure"""
        response = self.client.get('/health')
        data = json.loads(response.data)
        
        # Check algorithms availability
        self.assertIn('algorithms', data)
        self.assertIn('ACO', data['algorithms'])
        self.assertIn('PSO', data['algorithms'])
        
        # Check algorithm structure
        aco_status = data['algorithms']['ACO']
        pso_status = data['algorithms']['PSO']
        
        self.assertIn('available', aco_status)
        self.assertIn('status', aco_status)
        self.assertIn('available', pso_status)
        self.assertIn('status', pso_status)

    def test_stream_scheduling_missing_algorithm(self):
        """Test stream scheduling with missing algorithm parameter"""
        data = {
            "tasks_data": [
                {"id": "Task_1", "length": 5, "cost": 10},
                {"id": "Task_2", "length": 3, "cost": 8}
            ],
            "parameters": {
                "n_iterations": 10
            }
        }
        
        response = self.client.post('/stream_scheduling',
                                  data=json.dumps(data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Algorithm not specified')

    def test_stream_scheduling_invalid_algorithm(self):
        """Test stream scheduling with invalid algorithm"""
        data = {
            "algorithm": "INVALID_ALGO",
            "tasks_data": [
                {"id": "Task_1", "length": 5, "cost": 10}
            ],
            "parameters": {
                "n_iterations": 10
            }
        }
        
        response = self.client.post('/stream_scheduling',
                                  data=json.dumps(data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_stream_scheduling_missing_tasks(self):
        """Test stream scheduling with missing tasks data"""
        data = {
            "algorithm": "ACO",
            "parameters": {
                "n_iterations": 10
            }
        }
        
        response = self.client.post('/stream_scheduling',
                                  data=json.dumps(data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
