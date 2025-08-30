#!/usr/bin/env python3
import time
import json
import sys
import os

# Add current directory to path to import models
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.aco import ACO_MultiAgent_Scheduler as ACOScheduler
from models.pso import PSO_MultiAgent_Scheduler as PSOScheduler

def test_direct_metrics():
    """Test algorithms directly to verify metrics calculation"""
    
    # Test data
    tasks = [
        {'id': '1', 'length': 25},
        {'id': '2', 'length': 30}, 
        {'id': '3', 'length': 20}
    ]
    
    agents = [
        {'id': 'Agent-1'},
        {'id': 'Agent-2'},
        {'id': 'Agent-3'}
    ]
    
    def cost_function(schedule, makespan):
        return makespan
        
    def heuristic_function(task):
        return 1.0 / max(task.get('length', 1), 0.1)
    
    print("🧪 Testing ACO Algorithm Direct Execution...")
    
    # Test ACO
    start_time = time.time()
    
    scheduler = ACOScheduler(
        tasks=tasks,
        agents=agents,
        cost_function=cost_function,
        heuristic_function=heuristic_function,
        n_ants=5,
        n_iterations=10,
        task_id_col='id',
        agent_id_col='id'
    )
    
    final_result = None
    algorithm_computation_time = 0
    
    # Run algorithm and capture results
    for data_chunk in scheduler.run():
        chunk_obj = json.loads(data_chunk)
        if chunk_obj.get("type") == "done":
            final_result = chunk_obj
            algorithm_computation_time = chunk_obj.get('computation_time', 0)
            break
    
    total_execution_time = time.time() - start_time
    
    print(f"\n📊 ACO RESULTS:")
    print(f"   Total Execution Time: {total_execution_time:.4f} seconds")
    print(f"   Algorithm Computation Time: {algorithm_computation_time:.4f} seconds")
    print(f"   Overhead Time: {total_execution_time - algorithm_computation_time:.4f} seconds")
    print(f"   Best Makespan: {final_result.get('makespan', 'N/A')}")
    
    if total_execution_time != algorithm_computation_time:
        print("✅ SUCCESS: ACO metrics are now different!")
    else:
        print("❌ ISSUE: ACO metrics are still the same")
    
    print("\n" + "="*60)
    print("🧪 Testing PSO Algorithm Direct Execution...")
    
    # Test PSO
    start_time = time.time()
    
    pso_scheduler = PSOScheduler(
        tasks=tasks,
        agents=agents,
        cost_function=cost_function,
        n_particles=10,
        n_iterations=10,
        task_id_col='id',
        agent_id_col='id'
    )
    
    pso_final_result = None
    pso_algorithm_computation_time = 0
    
    # Run PSO algorithm and capture results
    for data_chunk in pso_scheduler.run():
        chunk_obj = json.loads(data_chunk)
        if chunk_obj.get("type") == "done":
            pso_final_result = chunk_obj
            pso_algorithm_computation_time = chunk_obj.get('computation_time', 0)
            break
    
    pso_total_execution_time = time.time() - start_time
    
    print(f"\n📊 PSO RESULTS:")
    print(f"   Total Execution Time: {pso_total_execution_time:.4f} seconds")
    print(f"   Algorithm Computation Time: {pso_algorithm_computation_time:.4f} seconds")
    print(f"   Overhead Time: {pso_total_execution_time - pso_algorithm_computation_time:.4f} seconds")
    print(f"   Best Makespan: {pso_final_result.get('makespan', 'N/A')}")
    
    if pso_total_execution_time != pso_algorithm_computation_time:
        print("✅ SUCCESS: PSO metrics are now different!")
    else:
        print("❌ ISSUE: PSO metrics are still the same")
    
    print("\n" + "="*60)
    print("📋 SUMMARY:")
    print(f"ACO - Total: {total_execution_time:.4f}s, Computation: {algorithm_computation_time:.4f}s")  
    print(f"PSO - Total: {pso_total_execution_time:.4f}s, Computation: {pso_algorithm_computation_time:.4f}s")
    
    if (total_execution_time != algorithm_computation_time and 
        pso_total_execution_time != pso_algorithm_computation_time):
        print("🎉 ALL GOOD: Both algorithms now have different execution time and computation time!")
    else:
        print("⚠️  STILL ISSUES: Some metrics are the same")

if __name__ == "__main__":
    test_direct_metrics()
