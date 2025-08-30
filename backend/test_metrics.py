#!/usr/bin/env python3
import requests
import json
import time

def test_metrics():
    url = "http://localhost:5001/stream_scheduling"
    data = {
        "algorithm": "ACO",
        "tasks": [
            {"TaskID": 1, "Duration": 25},
            {"TaskID": 2, "Duration": 30},
            {"TaskID": 3, "Duration": 20}
        ],
        "parameters": {
            "num_default_agents": 3,
            "n_iterations": 10,
            "n_ants": 5
        }
    }
    
    try:
        print("Testing ACO algorithm...")
        response = requests.post(url, json=data, stream=True)
        
        if response.status_code == 200:
            print("✅ Request successful, processing stream...")
            
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data:'):
                        try:
                            data_str = line_str[5:].strip()
                            if data_str:
                                parsed_data = json.loads(data_str)
                                
                                if parsed_data.get('type') == 'final_metrics':
                                    print("\n🎯 FINAL METRICS:")
                                    print(f"   Total Execution Time: {parsed_data.get('total_execution_time', 'N/A')} seconds")
                                    print(f"   Computation Time: {parsed_data.get('computation_time', 'N/A')} seconds")
                                    print(f"   Load Balance Index: {parsed_data.get('load_balance_index', 'N/A')}")
                                    
                                    # Verify they're different
                                    total_time = parsed_data.get('total_execution_time', 0)
                                    comp_time = parsed_data.get('computation_time', 0)
                                    
                                    if total_time != comp_time:
                                        print("✅ SUCCESS: Metrics are now different!")
                                        print(f"   Difference: {total_time - comp_time:.4f} seconds")
                                    else:
                                        print("❌ ISSUE: Metrics are still the same")
                                    break
                                    
                        except json.JSONDecodeError:
                            continue
        else:
            print(f"❌ Request failed with status: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_metrics()
