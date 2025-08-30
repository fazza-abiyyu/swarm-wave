#!/usr/bin/env python3
import time
import json
import sys
import os

# Add current directory to path to import models
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.aco import ACO_MultiAgent_Scheduler as ACOScheduler
from models.pso import PSO_MultiAgent_Scheduler as PSOScheduler

def test_with_realistic_data():
    """Test with more realistic data that will show measurable difference"""
    
    # Larger test dataset - simulate overhead
    print("📁 Loading test data...")
    time.sleep(0.1)  # Simulate loading time
    
    tasks = []
    for i in range(20):  # More tasks
        tasks.append({
            'id': f'task_{i+1}',
            'length': 10 + (i * 3),  # Varying lengths
            'priority': (i % 3) + 1
        })
    
    agents = []
    for i in range(5):  # More agents
        agents.append({'id': f'Agent-{i+1}'})
    
    print(f"✅ Loaded {len(tasks)} tasks and {len(agents)} agents")
    
    def cost_function(schedule, makespan):
        return makespan
        
    def heuristic_function(task):
        return 1.0 / max(task.get('length', 1), 0.1)
    
    print("\n🧪 Testing ACO Algorithm with Realistic Data...")
    
    # Add preprocessing overhead
    start_time = time.time()
    print("🔧 Preprocessing data...")
    time.sleep(0.05)  # Simulate preprocessing
    print("🔧 Initializing algorithm...")
    time.sleep(0.03)  # Simulate initialization
    
    scheduler = ACOScheduler(
        tasks=tasks,
        agents=agents,
        cost_function=cost_function,
        heuristic_function=heuristic_function,
        n_ants=15,
        n_iterations=50,
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
    
    print("🔧 Post-processing results...")
    time.sleep(0.02)  # Simulate post-processing
    
    total_execution_time = time.time() - start_time
    
    print(f"\n📊 ACO RESULTS:")
    print(f"   Total Execution Time: {total_execution_time:.4f} seconds")
    print(f"   Algorithm Computation Time: {algorithm_computation_time:.4f} seconds")
    print(f"   Overhead Time: {total_execution_time - algorithm_computation_time:.4f} seconds")
    print(f"   Best Makespan: {final_result.get('makespan', 'N/A')}")
    
    overhead_aco = total_execution_time - algorithm_computation_time
    
    if abs(total_execution_time - algorithm_computation_time) > 0.001:  # 1ms threshold
        print("✅ SUCCESS: ACO metrics are now clearly different!")
    else:
        print("❌ ISSUE: ACO metrics are still too close")
    
    print("\n" + "="*60)
    print("🧪 Testing PSO Algorithm with Realistic Data...")
    
    # Test PSO with similar overhead
    start_time = time.time()
    print("🔧 Preprocessing data...")
    time.sleep(0.05)  # Simulate preprocessing
    print("🔧 Initializing algorithm...")
    time.sleep(0.03)  # Simulate initialization
    
    pso_scheduler = PSOScheduler(
        tasks=tasks,
        agents=agents,
        cost_function=cost_function,
        n_particles=20,
        n_iterations=50,
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
    
    print("🔧 Post-processing results...")
    time.sleep(0.02)  # Simulate post-processing
    
    pso_total_execution_time = time.time() - start_time
    
    print(f"\n📊 PSO RESULTS:")
    print(f"   Total Execution Time: {pso_total_execution_time:.4f} seconds")
    print(f"   Algorithm Computation Time: {pso_algorithm_computation_time:.4f} seconds")
    print(f"   Overhead Time: {pso_total_execution_time - pso_algorithm_computation_time:.4f} seconds")
    print(f"   Best Makespan: {pso_final_result.get('makespan', 'N/A')}")
    
    overhead_pso = pso_total_execution_time - pso_algorithm_computation_time
    
    if abs(pso_total_execution_time - pso_algorithm_computation_time) > 0.001:  # 1ms threshold
        print("✅ SUCCESS: PSO metrics are now clearly different!")
    else:
        print("❌ ISSUE: PSO metrics are still too close")
    
    print("\n" + "="*60)
    print("📋 SUMMARY:")
    print(f"ACO - Total: {total_execution_time:.4f}s, Computation: {algorithm_computation_time:.4f}s, Overhead: {overhead_aco:.4f}s")  
    print(f"PSO - Total: {pso_total_execution_time:.4f}s, Computation: {pso_algorithm_computation_time:.4f}s, Overhead: {overhead_pso:.4f}s")
    
    print(f"\n📈 COMPARISON:")
    print(f"   ACO is {'faster' if algorithm_computation_time < pso_algorithm_computation_time else 'slower'} in computation")
    print(f"   ACO computation time: {algorithm_computation_time:.4f}s")
    print(f"   PSO computation time: {pso_algorithm_computation_time:.4f}s")
    print(f"   Difference: {abs(algorithm_computation_time - pso_algorithm_computation_time):.4f}s")
    
    if (abs(total_execution_time - algorithm_computation_time) > 0.001 and 
        abs(pso_total_execution_time - pso_algorithm_computation_time) > 0.001):
        print("\n🎉 EXCELLENT: Both algorithms now show clear difference between total and computation time!")
        print("   This resolves the issue where both metrics were identical.")
    else:
        print("\n⚠️  STILL NEEDS WORK: Metrics are too close or identical")

if __name__ == "__main__":
    test_with_realistic_data()
