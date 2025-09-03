import numpy as np
import random
import json

class PSO_MultiAgent_Scheduler:
    def __init__(self, tasks, agents, cost_function, task_id_col='id', agent_id_col='id',
                 n_particles=30, n_iterations=100, w=0.5, c1=1.5, c2=1.5, enable_dependencies=False):
        
        # Core configuration
        self.tasks = tasks
        self.agents = agents
        self.cost_function = cost_function
        self.task_id_col = task_id_col
        self.agent_id_col = agent_id_col
        self.enable_dependencies = enable_dependencies
        
        # Algorithm parameters
        self.n_tasks = len(tasks)
        self.n_agents = len(agents)
        self.n_particles = n_particles
        self.n_iterations = n_iterations
        self.w = w
        self.c1 = c1
        self.c2 = c2
        
        # Dependency handling
        self.dependencies = self._parse_dependencies() if self.enable_dependencies else {}
        self.dependency_graph = self._build_dependency_graph() if self.enable_dependencies else None
        
        # Check for circular dependencies
        if self.enable_dependencies and self._detect_circular_dependencies():
            print("Warning: Circular dependencies detected. Algorithm will use fallback mechanisms.")
        
        # Swarm initialization
        self.positions = np.random.rand(self.n_particles, self.n_tasks)
        self.velocities = np.random.rand(self.n_particles, self.n_tasks) * 0.1
        self.pbest_positions = self.positions.copy()
        self.pbest_costs = np.array([float('inf')] * self.n_particles)
        self.gbest_position = None
        self.gbest_cost = float('inf')
        self.gbest_schedule = None
        self.gbest_load_balance_index = float('inf')

    def _calculate_load_balance_index(self, agent_finish_times):
        """Calculate load balance index (lower = better balance)"""
        times = list(agent_finish_times.values())
        if len(times) <= 1:
            return 0.0
        
        mean_time = sum(times) / len(times)
        if mean_time == 0:
            return 0.0
            
        # Standard deviation normalized by mean
        variance = sum((t - mean_time) ** 2 for t in times) / len(times)
        std_dev = variance ** 0.5
        load_balance_index = std_dev / mean_time
        return load_balance_index
    
    def _detect_circular_dependencies(self):
        """Detect circular dependencies using DFS"""
        if not self.enable_dependencies:
            return False
            
        # Use DFS to detect cycles
        visited = set()
        rec_stack = set()
        
        def has_cycle(task_id):
            if task_id in rec_stack:
                return True
            if task_id in visited:
                return False
                
            visited.add(task_id)
            rec_stack.add(task_id)
            
            for dep_id in self.dependencies.get(task_id, []):
                if has_cycle(dep_id):
                    return True
                    
            rec_stack.remove(task_id)
            return False
        
        for task_id in self.dependencies:
            if task_id not in visited:
                if has_cycle(task_id):
                    return True
        return False

    def _parse_dependencies(self):
        """Parse task dependencies from tasks data with robust handling"""
        dependencies = {}
        for task in self.tasks:
            task_id = str(task[self.task_id_col])
            # Find dependency field from various possible names
            deps = None
            for field in ['dependencies', 'depends_on', 'prerequisites', 'requires', 'Dependencies']:
                if field in task and task[field] is not None:
                    deps = task[field]
                    break
            
            if deps:
                if isinstance(deps, str):
                    if deps.strip() == '' or deps.lower() in ['null', 'nan', 'none']:
                        deps = []
                    else:
                        # Split by comma or semicolon, handle null/empty values
                        deps = [str(d).strip() for d in deps.replace(';', ',').split(',') 
                               if d.strip() and str(d).lower() not in ['null', 'nan', 'none', '']]
                elif isinstance(deps, (list, tuple)):
                    deps = [str(d).strip() for d in deps 
                           if d is not None and str(d).strip() and str(d).lower() not in ['null', 'nan', 'none']]
                elif deps is not None:
                    dep_str = str(deps).strip()
                    deps = [dep_str] if dep_str and dep_str.lower() not in ['null', 'nan', 'none'] else []
                else:
                    deps = []
            else:
                deps = []
            
            dependencies[task_id] = deps
        return dependencies
    
    def _build_dependency_graph(self):
        """Build dependency graph for validation and topological sort"""
        graph = {}
        for task_id in self.dependencies:
            graph[task_id] = self.dependencies[task_id]
        return graph
    
    def _is_dependency_satisfied(self, task_id, completed_tasks):
        """Check if all dependencies are completed"""
        if not self.enable_dependencies or task_id not in self.dependencies:
            return True
        
        for dep_id in self.dependencies[task_id]:
            if dep_id not in completed_tasks:
                return False
        return True

    def _position_to_sequence(self, position):
        """Enhanced position to sequence with dependency consideration"""
        if not self.enable_dependencies:
            # Original sorting for independent tasks
            return np.argsort(position)
        
        # Dependency-aware sequence generation
        task_priorities = sorted(enumerate(position), key=lambda x: x[1], reverse=True)
        
        sequence = []
        scheduled_task_indices = set()
        completed_task_ids = set()
        
        # Safety net to prevent infinite loops in case of bad dependencies
        max_attempts = self.n_tasks * self.n_tasks 
        attempts = 0

        while len(scheduled_task_indices) < self.n_tasks and attempts < max_attempts:
            made_progress = False
            for task_idx, _ in task_priorities:
                if task_idx not in scheduled_task_indices:
                    task_id = str(self.tasks[task_idx][self.task_id_col])
                    
                    if self._is_dependency_satisfied(task_id, completed_task_ids):
                        sequence.append(task_idx)
                        scheduled_task_indices.add(task_idx)
                        completed_task_ids.add(task_id)
                        made_progress = True
            
            attempts += 1
            # If a full pass makes no progress, there might be a circular dependency or issue
            if not made_progress and len(scheduled_task_indices) < self.n_tasks:
                # Fallback: add any remaining unscheduled task to avoid infinite loop
                remaining = set(range(self.n_tasks)) - scheduled_task_indices
                if remaining:
                    # Add one task that has the fewest remaining dependencies to break the cycle
                    min_deps_task = -1
                    min_deps_count = float('inf')
                    for rem_idx in remaining:
                        rem_id = str(self.tasks[rem_idx][self.task_id_col])
                        deps = self.dependencies.get(rem_id, [])
                        unsatisfied_count = len([d for d in deps if d not in completed_task_ids])
                        if unsatisfied_count < min_deps_count:
                            min_deps_count = unsatisfied_count
                            min_deps_task = rem_idx
                    
                    if min_deps_task != -1:
                        sequence.append(min_deps_task)
                        scheduled_task_indices.add(min_deps_task)
                        completed_task_ids.add(str(self.tasks[min_deps_task][self.task_id_col]))

        # Ensure all tasks are in the sequence, even if dependencies were problematic
        if len(sequence) < self.n_tasks:
            remaining_tasks = set(range(self.n_tasks)) - scheduled_task_indices
            sequence.extend(sorted(list(remaining_tasks)))
            
        return np.array(sequence)

    def _evaluate_sequence(self, task_sequence):
        """Enhanced evaluation with dependency and load balancing consideration"""
        agent_finish_times = {agent[self.agent_id_col]: 0 for agent in self.agents}
        task_finish_times = {}  # Optimization: O(1) lookup for dependency finish times
        schedule = []
        
        for task_idx in task_sequence:
            task = self.tasks[task_idx]
            task_id = str(task[self.task_id_col])
            duration = task.get('length', 1)
            
            # Find best agent with load balancing
            best_agent_id = self._find_best_agent(agent_finish_times, duration)
            
            # Calculate start time based on dependencies
            dependency_finish_time = 0
            if self.enable_dependencies and task_id in self.dependencies:
                for dep_id in self.dependencies[task_id]:
                    # Optimization: Use dict for faster lookup
                    dependency_finish_time = max(dependency_finish_time, task_finish_times.get(dep_id, 0))
            
            # Start time is max of agent availability and dependency completion
            start_time = max(agent_finish_times[best_agent_id], dependency_finish_time)
            finish_time = start_time + duration
            agent_finish_times[best_agent_id] = finish_time
            task_finish_times[task_id] = finish_time # Optimization: Store finish time
            
            schedule.append({
                'task_id': task_id, 
                'agent_id': best_agent_id,
                'start_time': start_time, 
                'finish_time': finish_time
            })
        
        makespan = max(agent_finish_times.values()) if agent_finish_times else 0
        load_balance_index = self._calculate_load_balance_index(agent_finish_times)
        
        return self.cost_function(schedule, makespan), schedule, load_balance_index
    
    def _find_best_agent(self, agent_finish_times, task_duration):
        """Find agent with balance between makespan and load balancing - AGGRESSIVE VERSION"""
        best_score = float('inf')
        best_agent = None
        current_max_time = max(agent_finish_times.values()) if agent_finish_times else 0
        
        for agent_id in agent_finish_times:
            # Simulate assignment to this agent
            temp_finish_times = agent_finish_times.copy()
            temp_finish_times[agent_id] += task_duration
            
            # Calculate penalties
            new_makespan = max(temp_finish_times.values())
            makespan_penalty = new_makespan
            
            # AGGRESSIVE load balancing penalty
            balance_penalty = self._calculate_load_balance_index(temp_finish_times) * current_max_time * 2
            
            # Combined score with emphasis on balance
            combined_score = makespan_penalty + balance_penalty
            
            if combined_score < best_score:
                best_score = combined_score
                best_agent = agent_id
        
        return best_agent

    def run(self):
        import time
        computation_start_time = time.time()
        
        log_message = "Starting PSO optimization..."
        yield json.dumps({"type": "log", "message": log_message})
        
        for i in range(self.n_iterations):
            new_best_found_in_iter = False
            for p in range(self.n_particles):
                sequence = self._position_to_sequence(self.positions[p])
                cost, schedule, load_balance_index = self._evaluate_sequence(sequence)

                if cost < self.pbest_costs[p]:
                    self.pbest_costs[p] = cost
                    self.pbest_positions[p] = self.positions[p].copy()

                if cost < self.gbest_cost or (cost == self.gbest_cost and load_balance_index < self.gbest_load_balance_index):
                    self.gbest_cost = cost
                    self.gbest_position = self.positions[p].copy()
                    self.gbest_schedule = schedule
                    self.gbest_load_balance_index = load_balance_index
                    new_best_found_in_iter = True

            if new_best_found_in_iter:
                log_message = f"Iteration {i + 1}: New best solution! Makespan: {self.gbest_cost:.2f}, Load Balance: {self.gbest_load_balance_index:.4f}"
                yield json.dumps({"type": "log", "message": log_message})

            for p in range(self.n_particles):
                r1, r2 = np.random.rand(self.n_tasks), np.random.rand(self.n_tasks)
                cognitive_velocity = self.c1 * r1 * (self.pbest_positions[p] - self.positions[p])
                social_velocity = self.c2 * r2 * (self.gbest_position - self.positions[p])
                self.velocities[p] = (self.w * self.velocities[p]) + cognitive_velocity + social_velocity
                self.positions[p] += self.velocities[p]
            
            progress_log = f"Progress: Iteration {i + 1}/{self.n_iterations} -> Current Best: {self.gbest_cost:.2f}"
            yield json.dumps({
                "type": "iteration",
                "iteration": i + 1,
                "makespan": self.gbest_cost,
                "log_message": progress_log
            })

        computation_time = time.time() - computation_start_time

        # Send final result
        yield json.dumps({
            "type": "done",
            "schedule": self.gbest_schedule,
            "makespan": self.gbest_cost,
            "load_balance_index": self.gbest_load_balance_index,
            "computation_time": round(computation_time * 1000, 2),  # Convert to milliseconds
            "log_message": "PSO Optimization Finished!"
        })