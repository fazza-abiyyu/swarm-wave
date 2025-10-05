import numpy as np
import random
import json

class PSO_MultiAgent_Scheduler:
    def __init__(self, tasks, agents, cost_function, task_id_col='id', agent_id_col='id',
                 n_particles=30, n_iterations=100, w=0.5, c1=1.5, c2=1.5, enable_dependencies=False, random_seed=None):
        
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
        
        # Set random seed for reproducibility
        if random_seed is not None:
            np.random.seed(random_seed)
            random.seed(random_seed)
        
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
        """Convert position to sequence with penalty-based approach for more freedom"""
        if not self.enable_dependencies:
            # Original sorting for independent tasks
            return np.argsort(position)
        
        # Penalty-based approach: allows more exploration like MATLAB
        # Instead of strict dependency ordering, use position values with penalty corrections
        
        # Create initial sequence based on position values
        initial_sequence = np.argsort(position)
        
        # Apply penalty-based corrections for dependencies
        corrected_sequence = self._apply_dependency_penalties(initial_sequence, position)
        
        return corrected_sequence
    
    def _apply_dependency_penalties(self, sequence, position):
        """Apply penalty-based dependency corrections (MATLAB-inspired approach)"""
        n_tasks = len(sequence)
        corrected_sequence = []
        available_tasks = set(sequence)
        completed_tasks = set()
        
        # Build a penalty-adjusted priority list
        task_penalties = {}
        for i, task_idx in enumerate(sequence):
            task_id = str(self.tasks[task_idx][self.task_id_col])
            
            # Base priority from position
            base_priority = position[task_idx]
            
            # Calculate dependency penalty
            dependency_penalty = 0
            if task_id in self.dependencies:
                unsatisfied_deps = 0
                for dep_id in self.dependencies[task_id]:
                    if dep_id not in completed_tasks:
                        unsatisfied_deps += 1
                
                # Penalty increases with unsatisfied dependencies
                dependency_penalty = unsatisfied_deps * 0.5
            
            # Adjusted priority (higher is better, penalty reduces priority)
            adjusted_priority = base_priority - dependency_penalty
            task_penalties[task_idx] = adjusted_priority
        
        # Build sequence using penalty-adjusted priorities
        max_iterations = n_tasks * 2  # Safety limit
        iteration = 0
        
        while available_tasks and iteration < max_iterations:
            iteration += 1
            
            # Find tasks with satisfied dependencies
            ready_tasks = []
            for task_idx in available_tasks:
                task_id = str(self.tasks[task_idx][self.task_id_col])
                if self._is_dependency_satisfied(task_id, completed_tasks):
                    ready_tasks.append(task_idx)
            
            if ready_tasks:
                # Choose task with highest penalty-adjusted priority among ready tasks
                best_task = max(ready_tasks, key=lambda t: task_penalties[t])
                corrected_sequence.append(best_task)
                available_tasks.remove(best_task)
                task_id = str(self.tasks[best_task][self.task_id_col])
                completed_tasks.add(task_id)
            else:
                # Fallback: if no ready tasks, pick one with minimum penalty
                if available_tasks:
                    fallback_task = min(available_tasks, key=lambda t: len(self.dependencies.get(str(self.tasks[t][self.task_id_col]), [])))
                    corrected_sequence.append(fallback_task)
                    available_tasks.remove(fallback_task)
                    task_id = str(self.tasks[fallback_task][self.task_id_col])
                    completed_tasks.add(task_id)
        
        # Add any remaining tasks (safety measure)
        if available_tasks:
            corrected_sequence.extend(sorted(available_tasks))
        
        return np.array(corrected_sequence)

    def _evaluate_sequence(self, task_sequence):
        """Enhanced evaluation with penalty-based approach (like MATLAB implementation)"""
        agent_finish_times = {agent[self.agent_id_col]: 0 for agent in self.agents}
        task_finish_times = {}  # For dependency tracking
        schedule = []
        
        for task_idx in task_sequence:
            task = self.tasks[task_idx]
            task_id = str(task[self.task_id_col])
            duration = task.get('length', 1)
            
            # Find best agent using penalty-based approach
            best_agent_id = self._find_best_agent_with_penalty(agent_finish_times, duration, task_id, task_finish_times)
            
            # Calculate start time based on dependencies
            dependency_finish_time = 0
            if self.enable_dependencies and task_id in self.dependencies:
                deps = self.dependencies[task_id]
                for dep_id in deps:
                    if dep_id in task_finish_times:
                        dependency_finish_time = max(dependency_finish_time, task_finish_times[dep_id])
            
            start_time = max(agent_finish_times[best_agent_id], dependency_finish_time)
            finish_time = start_time + duration
            
            # Update tracking
            agent_finish_times[best_agent_id] = finish_time
            task_finish_times[task_id] = finish_time
            schedule.append({
                'task_id': task_id,
                'agent_id': best_agent_id,
                'start_time': start_time,
                'finish_time': finish_time
            })
        
        times = list(agent_finish_times.values())
        makespan = max(times) if times else 0
        load_balance_index = self._calculate_load_balance_index(agent_finish_times)
        
        # Use penalty-based cost calculation (inspired by MATLAB)
        cost = self._calculate_penalty_based_cost(makespan, load_balance_index, agent_finish_times)
        
        return cost, schedule, load_balance_index
    
    def _find_best_agent_with_penalty(self, agent_finish_times, task_duration, task_id, task_finish_times):
        """Find best agent using penalty-based approach (MATLAB-inspired)"""
        best_agent_id = None
        best_score = float('inf')
        current_max_time = max(agent_finish_times.values()) if agent_finish_times.values() else 0
        
        for agent in self.agents:
            agent_id = agent[self.agent_id_col]
            
            # Simulate assignment to this agent
            temp_finish_times = agent_finish_times.copy()
            
            # Calculate dependency start time
            dependency_finish_time = 0
            if self.enable_dependencies and task_id in self.dependencies:
                deps = self.dependencies[task_id]
                for dep_id in deps:
                    if dep_id in task_finish_times:
                        dependency_finish_time = max(dependency_finish_time, task_finish_times[dep_id])
            
            start_time = max(temp_finish_times[agent_id], dependency_finish_time)
            temp_finish_times[agent_id] = start_time + task_duration
            
            # Calculate penalties (MATLAB approach)
            new_makespan = max(temp_finish_times.values())
            makespan_penalty = new_makespan
            
            # Aggressive load balancing penalty
            balance_penalty = self._calculate_load_balance_index(temp_finish_times) * current_max_time * 2
            
            # Combined score with emphasis on balance
            combined_score = makespan_penalty + balance_penalty
            
            if combined_score < best_score:
                best_score = combined_score
                best_agent_id = agent_id
        
        # Fallback: choose agent with minimum finish time
        if best_agent_id is None:
            min_time = float('inf')
            for agent_id, time in agent_finish_times.items():
                if time < min_time:
                    min_time = time
                    best_agent_id = agent_id
        
        return best_agent_id
    
    def _calculate_penalty_based_cost(self, makespan, load_balance_index, agent_finish_times):
        """Calculate cost using penalty-based approach"""
        # Base cost is makespan
        base_cost = makespan
        
        # Add load balance penalty (weighted by makespan)
        balance_penalty = load_balance_index * makespan * 0.5
        
        # Total penalty-based cost
        total_cost = base_cost + balance_penalty
        
        return total_cost

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