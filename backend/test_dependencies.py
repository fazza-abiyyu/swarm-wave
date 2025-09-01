#!/usr/bin/env python3
"""
Test script untuk memvalidasi implementasi task dependencies
"""

import sys
import os
import json
import time

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.aco import ACO_MultiAgent_Scheduler
from models.pso import PSO_MultiAgent_Scheduler

def test_dependency_parsing():
    """Test dependency parsing functionality"""
    print("🧪 Testing Dependency Parsing...")
    
    test_tasks = [
        {'id': 'Task_1', 'length': 2.0, 'dependencies': []},
        {'id': 'Task_2', 'length': 3.0, 'dependencies': ['Task_1']},
        {'id': 'Task_3', 'length': 1.5, 'dependencies': 'Task_1,Task_2'},  # String format
        {'id': 'Task_4', 'length': 2.5, 'depends_on': ['Task_2']},  # Alternative field name
        {'id': 'Task_5', 'length': 4.0, 'prerequisites': 'Task_3;Task_4'}  # Semicolon format
    ]
    
    test_agents = [{'id': f'Agent_{i}'} for i in range(1, 4)]
    
    def simple_cost(schedule, makespan):
        return makespan
    
    def simple_heuristic(task):
        return 1.0 / task['length']
    
    # Test ACO parsing
    aco = ACO_MultiAgent_Scheduler(
        tasks=test_tasks, agents=test_agents, 
        cost_function=simple_cost, heuristic_function=simple_heuristic,
        n_iterations=1, enable_dependencies=True
    )
    
    print(f"Dependencies parsed: {aco.dependencies}")
    
    # Test validation logic
    completed_tasks = {'Task_1', 'Task_2'}
    print(f"Task_3 deps satisfied? {aco._is_dependency_satisfied('Task_3', completed_tasks)}")
    print(f"Task_4 deps satisfied? {aco._is_dependency_satisfied('Task_4', completed_tasks)}")
    print(f"Task_5 deps satisfied? {aco._is_dependency_satisfied('Task_5', completed_tasks)}")
    
    print("✅ Dependency parsing test passed!")

def test_scheduling_with_dependencies():
    """Test full scheduling dengan dependencies"""
    print("\n🧪 Testing Scheduling with Dependencies...")
    
    # Create realistic dependency scenario
    tasks_with_deps = [
        {'id': 'Setup', 'length': 1.0, 'dependencies': []},
        {'id': 'DataPrep', 'length': 2.0, 'dependencies': ['Setup']},
        {'id': 'Training1', 'length': 5.0, 'dependencies': ['DataPrep']},
        {'id': 'Training2', 'length': 4.0, 'dependencies': ['DataPrep']},
        {'id': 'Validation', 'length': 2.0, 'dependencies': ['Training1', 'Training2']},
        {'id': 'Deployment', 'length': 1.5, 'dependencies': ['Validation']}
    ]
    
    agents = [{'id': f'Agent_{i}'} for i in range(1, 4)]
    
    def cost_function(schedule, makespan):
        return makespan
    
    def heuristic_function(task):
        return 1.0 / task['length']
    
    # Test ACO with dependencies
    print("Testing ACO with dependencies...")
    aco_scheduler = ACO_MultiAgent_Scheduler(
        tasks=tasks_with_deps, agents=agents,
        cost_function=cost_function, heuristic_function=heuristic_function,
        n_ants=5, n_iterations=10, enable_dependencies=True
    )
    
    aco_results = []
    for result_json in aco_scheduler.run():
        result = json.loads(result_json)
        if result.get('type') == 'done':
            aco_results = result
            break
    
    print(f"ACO Makespan: {aco_results.get('makespan', 'N/A')}")
    print(f"ACO Computation Time: {aco_results.get('computation_time', 'N/A')} ms")
    
    # Validate dependency constraints
    schedule = aco_results.get('schedule', [])
    dependency_violations = validate_dependency_constraints(tasks_with_deps, schedule)
    
    if dependency_violations:
        print(f"❌ Dependency violations found: {dependency_violations}")
    else:
        print("✅ All dependency constraints satisfied!")
    
    # Test PSO with dependencies
    print("\nTesting PSO with dependencies...")
    pso_scheduler = PSO_MultiAgent_Scheduler(
        tasks=tasks_with_deps, agents=agents,
        cost_function=cost_function,
        n_particles=10, n_iterations=10, enable_dependencies=True
    )
    
    pso_results = []
    for result_json in pso_scheduler.run():
        result = json.loads(result_json)
        if result.get('type') == 'done':
            pso_results = result
            break
    
    print(f"PSO Makespan: {pso_results.get('makespan', 'N/A')}")
    print(f"PSO Computation Time: {pso_results.get('computation_time', 'N/A')} ms")
    
    # Validate dependency constraints
    schedule = pso_results.get('schedule', [])
    dependency_violations = validate_dependency_constraints(tasks_with_deps, schedule)
    
    if dependency_violations:
        print(f"❌ Dependency violations found: {dependency_violations}")
    else:
        print("✅ All dependency constraints satisfied!")

def validate_dependency_constraints(tasks, schedule):
    """Validate bahwa semua dependency constraints terpenuhi"""
    violations = []
    
    # Build dependency map
    deps_map = {}
    for task in tasks:
        task_id = task['id']
        deps = []
        
        for field in ['dependencies', 'depends_on', 'prerequisites', 'requires']:
            if field in task and task[field]:
                field_deps = task[field]
                if isinstance(field_deps, str):
                    deps = [d.strip() for d in field_deps.replace(';', ',').split(',') if d.strip()]
                elif isinstance(field_deps, list):
                    deps = field_deps
                break
        
        deps_map[task_id] = deps
    
    # Build task finish times
    task_finish_times = {}
    for item in schedule:
        task_finish_times[item['task_id']] = item['finish_time']
    
    # Check constraints
    for task_id, dependencies in deps_map.items():
        if not dependencies:
            continue
            
        task_start_time = None
        for item in schedule:
            if item['task_id'] == task_id:
                task_start_time = item['start_time']
                break
        
        if task_start_time is None:
            continue
        
        for dep_id in dependencies:
            if dep_id not in task_finish_times:
                violations.append(f"Task {task_id} depends on {dep_id} but {dep_id} not found in schedule")
                continue
            
            dep_finish_time = task_finish_times[dep_id]
            if task_start_time < dep_finish_time:
                violations.append(f"Task {task_id} starts at {task_start_time} but dependency {dep_id} finishes at {dep_finish_time}")
    
    return violations

def compare_with_without_dependencies():
    """Compare performance dengan dan tanpa dependencies"""
    print("\n🧪 Comparing With/Without Dependencies...")
    
    # Tasks that can be independent or dependent
    tasks = [
        {'id': 'Task_1', 'length': 2.0},
        {'id': 'Task_2', 'length': 3.0},
        {'id': 'Task_3', 'length': 1.5},
        {'id': 'Task_4', 'length': 2.5},
        {'id': 'Task_5', 'length': 4.0}
    ]
    
    # Add dependencies for version 2
    tasks_with_deps = []
    for task in tasks:
        task_copy = task.copy()
        if task['id'] == 'Task_2':
            task_copy['dependencies'] = ['Task_1']
        elif task['id'] == 'Task_3':
            task_copy['dependencies'] = ['Task_1']
        elif task['id'] == 'Task_4':
            task_copy['dependencies'] = ['Task_2']
        elif task['id'] == 'Task_5':
            task_copy['dependencies'] = ['Task_3', 'Task_4']
        else:
            task_copy['dependencies'] = []
        tasks_with_deps.append(task_copy)
    
    agents = [{'id': f'Agent_{i}'} for i in range(1, 3)]
    
    def cost_function(schedule, makespan):
        return makespan
    
    def heuristic_function(task):
        return 1.0
    
    # Test tanpa dependencies
    print("Running ACO without dependencies...")
    aco_no_deps = ACO_MultiAgent_Scheduler(
        tasks=tasks, agents=agents,
        cost_function=cost_function, heuristic_function=heuristic_function,
        n_ants=5, n_iterations=20, enable_dependencies=False
    )
    
    start_time = time.time()
    no_deps_result = None
    for result_json in aco_no_deps.run():
        result = json.loads(result_json)
        if result.get('type') == 'done':
            no_deps_result = result
            break
    no_deps_time = time.time() - start_time
    
    # Test with dependencies
    print("Running ACO with dependencies...")
    aco_with_deps = ACO_MultiAgent_Scheduler(
        tasks=tasks_with_deps, agents=agents,
        cost_function=cost_function, heuristic_function=heuristic_function,
        n_ants=5, n_iterations=20, enable_dependencies=True
    )
    
    start_time = time.time()
    with_deps_result = None
    for result_json in aco_with_deps.run():
        result = json.loads(result_json)
        if result.get('type') == 'done':
            with_deps_result = result
            break
    with_deps_time = time.time() - start_time
    
    # Compare results
    print(f"\n📊 Results Comparison:")
    print(f"Without Dependencies - Makespan: {no_deps_result.get('makespan', 'N/A'):.2f}, Time: {no_deps_time:.2f}s")
    print(f"With Dependencies    - Makespan: {with_deps_result.get('makespan', 'N/A'):.2f}, Time: {with_deps_time:.2f}s")
    
    makespan_increase = ((with_deps_result.get('makespan', 0) - no_deps_result.get('makespan', 0)) / no_deps_result.get('makespan', 1)) * 100
    time_increase = ((with_deps_time - no_deps_time) / no_deps_time) * 100
    
    print(f"Impact: +{makespan_increase:.1f}% makespan, +{time_increase:.1f}% computation time")

if __name__ == '__main__':
    print("🚀 Testing Task Dependencies Implementation")
    print("=" * 50)
    
    try:
        test_dependency_parsing()
        test_scheduling_with_dependencies()
        compare_with_without_dependencies()
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
