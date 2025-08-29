#!/usr/bin/env python3
"""
Test script to verify backend endpoint matches frontend expectations
"""

import requests
import json

def test_frontend_format():
    """Test the run_scheduling endpoint with frontend-compatible format"""
    
    # Test data matching frontend structure
    test_data = {
        "algorithm": "aco",
        "tasks": [
            {
                "TaskID": 1,
                "Duration": 25,
                "Weight": 10,
                "Cost": 100
            },
            {
                "TaskID": 2,
                "Duration": 30,
                "Weight": 15,
                "Cost": 150
            },
            {
                "TaskID": 3,
                "Duration": 20,
                "Weight": 8,
                "Cost": 80
            }
        ],
        "parameters": {
            "num_default_agents": 3,
            "n_iterations": 50,
            "n_ants": 10,
            "alpha": 1,
            "beta": 2,
            "evaporation_rate": 0.5,
            "pheromone_deposit": 100,
            "task_id_col": "TaskID",
            "agent_id_col": "id"
        }
    }
    
    url = "http://localhost:5001/run_scheduling"
    headers = {"Content-Type": "application/json"}
    
    try:
        print("🧪 Testing ACO algorithm...")
        response = requests.post(url, headers=headers, json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Response received successfully!")
            
            # Check required frontend fields
            required_fields = [
                'success', 'algorithm', 'bestMakespan', 'makespan',
                'computing_time', 'executionTime', 'loadBalanceIndex',
                'loadbalancing', 'computationTime', 'total_execution_time',
                'results', 'iterations', 'finalAssignment'
            ]
            
            print("\n📋 Checking required fields:")
            for field in required_fields:
                status = "✅" if field in result else "❌"
                print(f"{status} {field}: {type(result.get(field)) if field in result else 'MISSING'}")
            
            print(f"\n📊 Summary:")
            print(f"   Algorithm: {result.get('algorithm')}")
            print(f"   Best Makespan: {result.get('bestMakespan')}")
            print(f"   Execution Time: {result.get('executionTime')} seconds")
            print(f"   Load Balance Index: {result.get('loadBalanceIndex')}")
            print(f"   Results Count: {len(result.get('results', []))}")
            print(f"   Iterations Count: {len(result.get('iterations', []))}")
            
            # Test PSO
            print("\n" + "="*50)
            test_data["algorithm"] = "pso"
            test_data["parameters"]["n_particles"] = 10
            test_data["parameters"]["w"] = 0.5
            test_data["parameters"]["c1"] = 1.5
            test_data["parameters"]["c2"] = 1.5
            
            print("🧪 Testing PSO algorithm...")
            response = requests.post(url, headers=headers, json=test_data)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ PSO Response received!")
                print(f"   Algorithm: {result.get('algorithm')}")
                print(f"   Best Makespan: {result.get('bestMakespan')}")
                print(f"   Execution Time: {result.get('executionTime')} seconds")
            else:
                print(f"❌ PSO Error: {response.status_code} - {response.text}")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception occurred: {e}")

if __name__ == "__main__":
    test_frontend_format()