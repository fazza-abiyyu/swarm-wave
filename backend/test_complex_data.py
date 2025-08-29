#!/usr/bin/env python3
"""
Test script with more complex data to verify backend robustness
"""

import requests
import json
import pandas as pd

def test_with_csv_data():
    """Test with actual CSV data structure"""
    
    # Load some sample data from the CSV file
    try:
        df = pd.read_csv('cloud_task_scheduling_dataset.csv')
        # Take first 10 tasks
        sample_tasks = df.head(10).to_dict('records')
        
        # Format tasks to match frontend structure
        formatted_tasks = []
        for task in sample_tasks:
            formatted_task = {
                "TaskID": int(task.get('Task_ID', 0)),
                "Duration": float(task.get('Execution_Time (s)', 1.0)),
                "Weight": int(task.get('Priority', 1)),
                "Cost": float(task.get('CPU_Usage (%)', 50))
            }
            formatted_tasks.append(formatted_task)
        
    except Exception as e:
        print(f"Could not load CSV data, using synthetic data: {e}")
        # Fallback to synthetic data
        formatted_tasks = [
            {"TaskID": i+1, "Duration": 20 + i*5, "Weight": (i % 3) + 1, "Cost": 100 + i*10}
            for i in range(5)
        ]
    
    url = "http://localhost:5001/run_scheduling"
    headers = {"Content-Type": "application/json"}
    
    # Test ACO with complex data
    test_data = {
        "algorithm": "aco",
        "tasks": formatted_tasks,
        "parameters": {
            "num_default_agents": 3,
            "n_iterations": 100,
            "n_ants": 20,
            "alpha": 1,
            "beta": 2,
            "evaporation_rate": 0.5,
            "pheromone_deposit": 100,
            "task_id_col": "TaskID",
            "agent_id_col": "id"
        }
    }
    
    try:
        print(f"🧪 Testing ACO with {len(formatted_tasks)} tasks...")
        response = requests.post(url, headers=headers, json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Complex data test successful!")
            print(f"   Tasks processed: {len(formatted_tasks)}")
            print(f"   Best Makespan: {result.get('bestMakespan')}")
            print(f"   Execution Time: {result.get('executionTime')} seconds")
            print(f"   Load Balance Index: {result.get('loadBalanceIndex')}")
            
            # Verify structure
            print(f"   Results structure: {len(result.get('results', []))} assignments")
            print(f"   Iterations structure: {len(result.get('iterations', []))} data points")
            
            # Check if iterations have correct format
            iterations = result.get('iterations', [])
            if iterations:
                sample_iter = iterations[0]
                print(f"   Sample iteration: {sample_iter}")
                
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_with_csv_data()