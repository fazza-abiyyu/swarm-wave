import requests
import json

# Test the endpoint
url = "http://localhost:5001/run_scheduling"
headers = {"Content-Type": "application/json"}
data = {
    "algorithm": "aco",
    "parameters": {
        "n_iterations": 2,
        "n_ants": 2
    }
}

try:
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        print("Computing time:", result.get("computing_time"))
        print("Makespan:", result.get("makespan"))
        
        # Check iterations data
        iterations = result.get("iterations_data", [])
        for iter_data in iterations:
            print(f"Iteration {iter_data['index']}: computing_time={iter_data['computing_time']}ms")
        
        # Print total iterations
        print(f"Total iterations: {len(iterations)}")
        
        # Debug: Check result structure
        print(f"Result keys: {list(result.keys())}")
        print(f"Has iterations_data: {'iterations_data' in result}")
    else:
        print("Error:", response.status_code, response.text)
except Exception as e:
    print("Exception:", e)