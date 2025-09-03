#!/usr/bin/env python3
"""
Script to generate test data with task dependencies
To support dependency task testing scenarios
"""

import json
import random
import csv
import os

def generate_tasks_with_dependencies(num_tasks=50, dependency_probability=0.3, max_dependencies=3):
    """
    Generate tasks with dependencies
    
    Args:
        num_tasks: Number of tasks
        dependency_probability: Probability task has dependency (0.0 - 1.0) 
        max_dependencies: Maximum dependencies per task
    """
    tasks = []
    
    # Generate basic tasks first
    for i in range(1, num_tasks + 1):
        task = {
            'id': f'Task_{i}',
            'name': f'Task {i}',
            'length': round(random.uniform(1.0, 10.0), 2),  # Duration 1-10 units
            'cost': round(random.uniform(5.0, 50.0), 2),    # Cost 5-50 units
            'priority': random.randint(1, 5),               # Priority 1-5
            'dependencies': []
        }
        tasks.append(task)
    
    # Add dependencies (only to previously existing tasks)
    for i in range(1, num_tasks):  # Skip first task (no dependencies)
        task = tasks[i]
        
        if random.random() < dependency_probability:
            # Determine number of dependencies
            num_deps = random.randint(1, min(max_dependencies, i))
            
            # Pick dependencies from previous tasks
            possible_deps = [tasks[j]['id'] for j in range(i)]
            dependencies = random.sample(possible_deps, num_deps)
            
            task['dependencies'] = dependencies
    
    return tasks

def generate_scenario_data():
    """Generate berbagai skenario test data"""
    scenarios = {}
    
    # Scenario 1: Agent Number Variations (Fixed 100 tasks, no dependencies)
    print("Generating Scenario 1: Agent Variations...")
    scenarios['agent_variations'] = {
        'tasks_100_agents_5': {
            'tasks': generate_tasks_with_dependencies(100, dependency_probability=0.0),
            'agents': [{'id': f'Agent_{i}'} for i in range(1, 6)],
            'parameters': {'num_default_agents': 5, 'n_iterations': 50}
        },
        'tasks_100_agents_10': {
            'tasks': generate_tasks_with_dependencies(100, dependency_probability=0.0),
            'agents': [{'id': f'Agent_{i}'} for i in range(1, 11)],
            'parameters': {'num_default_agents': 10, 'n_iterations': 50}
        },
        'tasks_100_agents_20': {
            'tasks': generate_tasks_with_dependencies(100, dependency_probability=0.0),
            'agents': [{'id': f'Agent_{i}'} for i in range(1, 21)],
            'parameters': {'num_default_agents': 20, 'n_iterations': 50}
        }
    }
    
    # Scenario 2: Task Number Variations (Fixed 10 agents, no dependencies)
    print("Generating Scenario 2: Task Variations...")
    scenarios['task_variations'] = {
        'tasks_50_agents_10': {
            'tasks': generate_tasks_with_dependencies(50, dependency_probability=0.0),
            'agents': [{'id': f'Agent_{i}'} for i in range(1, 11)],
            'parameters': {'num_default_agents': 10, 'n_iterations': 50}
        },
        'tasks_100_agents_10': {
            'tasks': generate_tasks_with_dependencies(100, dependency_probability=0.0),
            'agents': [{'id': f'Agent_{i}'} for i in range(1, 11)],
            'parameters': {'num_default_agents': 10, 'n_iterations': 50}
        },
        'tasks_150_agents_10': {
            'tasks': generate_tasks_with_dependencies(150, dependency_probability=0.0),
            'agents': [{'id': f'Agent_{i}'} for i in range(1, 11)],
            'parameters': {'num_default_agents': 10, 'n_iterations': 50}
        }
    }
    
    # Scenario 3: Task Dependency Levels (Fixed 100 tasks, 10 agents)
    print("Generating Scenario 3: Dependency Variations...")
    scenarios['dependency_variations'] = {
        'no_dependencies': {
            'tasks': generate_tasks_with_dependencies(100, dependency_probability=0.0),
            'agents': [{'id': f'Agent_{i}'} for i in range(1, 11)],
            'parameters': {'num_default_agents': 10, 'n_iterations': 50, 'enable_dependencies': False}
        },
        'low_dependencies': {
            'tasks': generate_tasks_with_dependencies(100, dependency_probability=0.2, max_dependencies=1),
            'agents': [{'id': f'Agent_{i}'} for i in range(1, 11)],
            'parameters': {'num_default_agents': 10, 'n_iterations': 50, 'enable_dependencies': True}
        },
        'medium_dependencies': {
            'tasks': generate_tasks_with_dependencies(100, dependency_probability=0.4, max_dependencies=2),
            'agents': [{'id': f'Agent_{i}'} for i in range(1, 11)],
            'parameters': {'num_default_agents': 10, 'n_iterations': 50, 'enable_dependencies': True}
        },
        'high_dependencies': {
            'tasks': generate_tasks_with_dependencies(100, dependency_probability=0.6, max_dependencies=3),
            'agents': [{'id': f'Agent_{i}'} for i in range(1, 11)],
            'parameters': {'num_default_agents': 10, 'n_iterations': 50, 'enable_dependencies': True}
        }
    }
    
    return scenarios

def save_scenarios_to_files(scenarios, output_dir='test_scenarios'):
    """Save scenarios to JSON files"""
    os.makedirs(output_dir, exist_ok=True)
    
    for scenario_type, scenario_data in scenarios.items():
        scenario_dir = os.path.join(output_dir, scenario_type)
        os.makedirs(scenario_dir, exist_ok=True)
        
        for scenario_name, data in scenario_data.items():
            file_path = os.path.join(scenario_dir, f'{scenario_name}.json')
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Saved: {file_path}")

def generate_csv_format(tasks, filename):
    """Generate CSV format untuk compatibility dengan existing data loader"""
    fieldnames = ['Task_ID', 'Duration', 'Cost', 'Priority', 'Dependencies']
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for task in tasks:
            deps_str = ';'.join(task['dependencies']) if task['dependencies'] else ''
            writer.writerow({
                'Task_ID': task['id'],
                'Duration': task['length'],
                'Cost': task['cost'],
                'Priority': task['priority'],
                'Dependencies': deps_str
            })

if __name__ == '__main__':
    print("🚀 Generating Test Scenarios for Swarm Wave...")
    
    # Generate all scenarios
    scenarios = generate_scenario_data()
    
    # Save to files
    save_scenarios_to_files(scenarios)
    
    # Generate sample CSV files
    print("\nGenerating sample CSV files...")
    sample_tasks_no_deps = generate_tasks_with_dependencies(50, dependency_probability=0.0)
    sample_tasks_with_deps = generate_tasks_with_dependencies(50, dependency_probability=0.5, max_dependencies=2)
    
    generate_csv_format(sample_tasks_no_deps, 'test_scenarios/sample_tasks_no_dependencies.csv')
    generate_csv_format(sample_tasks_with_deps, 'test_scenarios/sample_tasks_with_dependencies.csv')
    
    print("\n✅ Test scenarios generated successfully!")
    print("\nStructure:")
    print("📁 test_scenarios/")
    print("  📁 agent_variations/")
    print("    📄 tasks_100_agents_5.json")
    print("    📄 tasks_100_agents_10.json")
    print("    📄 tasks_100_agents_20.json")
    print("  📁 task_variations/")
    print("    📄 tasks_50_agents_10.json")
    print("    📄 tasks_100_agents_10.json")
    print("    📄 tasks_150_agents_10.json")
    print("  📁 dependency_variations/")
    print("    📄 no_dependencies.json")
    print("    📄 low_dependencies.json")
    print("    📄 medium_dependencies.json")
    print("    📄 high_dependencies.json")
    print("  📄 sample_tasks_no_dependencies.csv")
    print("  📄 sample_tasks_with_dependencies.csv")
