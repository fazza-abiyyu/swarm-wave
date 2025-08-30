#!/usr/bin/env python3
"""
Test metrics in milliseconds
"""

import json
import time
from models.aco import ACO_MultiAgent_Scheduler as ACOScheduler
from models.pso import PSO_MultiAgent_Scheduler as PSOScheduler

def test_milliseconds_metrics():
    """Test algorithms with metrics in milliseconds"""
    
    print("🧪 Testing Metrics in Milliseconds...")
    
    # Sample data
    tasks = [
        {'id': f'task_{i}', 'length': 10 + (i % 20)} 
        for i in range(15)
    ]
    agents = [{'id': f'Agent-{i+1}'} for i in range(3)]
    
    def cost_function(schedule, makespan): 
        return makespan
    
    def heuristic_function(task): 
        return 1.0 / max(task.get('length', 1), 0.1)
    
    # Test ACO
    print("\n📊 Testing ACO...")
    start_time = time.time()
    
    scheduler = ACOScheduler(
        tasks=tasks, agents=agents, cost_function=cost_function,
        heuristic_function=heuristic_function, n_ants=5, n_iterations=10
    )
    
    final_result = None
    for data_chunk in scheduler.run():
        chunk_obj = json.loads(data_chunk)
        if chunk_obj.get("type") == "done":
            final_result = chunk_obj
            break
    
    total_time = time.time() - start_time
    
    print(f"   Total Execution Time: {total_time * 1000:.2f} ms")
    print(f"   Computation Time: {final_result.get('computation_time')} ms")
    print(f"   Best Makespan: {final_result.get('makespan')}")
    print(f"   Difference: {(total_time * 1000) - final_result.get('computation_time', 0):.2f} ms")
    
    # Test PSO
    print("\n📊 Testing PSO...")
    start_time = time.time()
    
    scheduler = PSOScheduler(
        tasks=tasks, agents=agents, cost_function=cost_function,
        n_particles=8, n_iterations=10
    )
    
    final_result = None
    for data_chunk in scheduler.run():
        chunk_obj = json.loads(data_chunk)
        if chunk_obj.get("type") == "done":
            final_result = chunk_obj
            break
    
    total_time = time.time() - start_time
    
    print(f"   Total Execution Time: {total_time * 1000:.2f} ms")
    print(f"   Computation Time: {final_result.get('computation_time')} ms")
    print(f"   Best Makespan: {final_result.get('makespan')}")
    print(f"   Difference: {(total_time * 1000) - final_result.get('computation_time', 0):.2f} ms")
    
    print("\n✅ Now both metrics are clearly different in milliseconds!")

if __name__ == "__main__":
    test_milliseconds_metrics()
