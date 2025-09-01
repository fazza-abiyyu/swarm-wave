import numpy as np
import random
import json

class ACO_MultiAgent_Scheduler:
    def __init__(self, tasks, cost_function, heuristic_function,
                 agents=None, num_default_agents=3,
                 task_id_col='id', agent_id_col='id',
                 n_ants=10, n_iterations=100, alpha=1.0, beta=2.0,
                 evaporation_rate=0.5, pheromone_deposit=100.0,
                 enable_dependencies=False):
        
        # Core configuration
        self.tasks = tasks
        self.cost_function = cost_function
        self.heuristic_function = heuristic_function
        self.task_id_col = task_id_col
        self.agent_id_col = agent_id_col
        self.enable_dependencies = enable_dependencies

        # Agents setup
        if not agents:
            self.agents = [{self.agent_id_col: f'DefaultAgent-{i+1}'} for i in range(num_default_agents)]
        else:
            self.agents = agents

        # Algorithm parameters
        self.n_tasks = len(self.tasks)
        self.n_agents = len(self.agents)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.pheromone_deposit = pheromone_deposit
        self.prioritize_balance = True

        # Task mapping for efficient lookup
        self.task_map = {str(task[self.task_id_col]): i for i, task in enumerate(self.tasks)}
        self.rev_task_map = {i: str(task[self.task_id_col]) for i, task in enumerate(self.tasks)}

        # Dependency handling
        self.dependencies = self._parse_dependencies() if self.enable_dependencies else {}
        self.dependency_graph = self._build_dependency_graph() if self.enable_dependencies else None

        # Algorithm state
        self.pheromones = np.ones((self.n_tasks, self.n_tasks))
        self.heuristics = self._calculate_heuristics()
        self.best_schedule = None
        self.best_cost = float('inf')
        self.best_load_balance_index = float('inf')
        
    def _calculate_load_balance_index(self, agent_finish_times):
        """Hitung load balance index (lower = better balance)"""
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
        
    def _parse_dependencies(self):
        """Parse task dependencies with robust field handling"""
        dependencies = {}
        for task in self.tasks:
            task_id = str(task[self.task_id_col])
            
            # Find dependency field with flexible naming
            deps = None
            for field in ['dependencies', 'depends_on', 'prerequisites', 'requires', 'Dependencies']:
                if field in task and task[field] is not None:
                    deps = task[field]
                    break
            
            # Parse dependency data
            if deps:
                if isinstance(deps, str):
                    if deps.strip() == '' or deps.lower() in ['null', 'nan', 'none']:
                        deps = []
                    else:
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
        """Build dependency graph for validation"""
        graph = {}
        for task_id in self.dependencies:
            graph[task_id] = self.dependencies[task_id]
        return graph
    
    def _is_dependency_satisfied(self, task_id, completed_tasks):
        """Check apakah semua dependencies sudah completed"""
        if not self.enable_dependencies or task_id not in self.dependencies:
            return True
        
        for dep_id in self.dependencies[task_id]:
            if dep_id not in completed_tasks:
                return False
        return True
    
    def _get_ready_tasks(self, remaining_tasks, completed_tasks):
        """Get tasks yang dependencies-nya sudah satisfied"""
        if not self.enable_dependencies:
            return remaining_tasks
            
        ready_tasks = []
        for task_idx in remaining_tasks:
            task_id = str(self.rev_task_map[task_idx])
            if self._is_dependency_satisfied(task_id, completed_tasks):
                ready_tasks.append(task_idx)
        return ready_tasks
        
    def _calculate_heuristics(self):
        heuristics = np.zeros((self.n_tasks, self.n_tasks))
        for i in range(self.n_tasks):
            for j in range(self.n_tasks):
                if i != j:
                    heuristics[i, j] = self.heuristic_function(self.tasks[j])
        return heuristics

    def _construct_solution(self):
        """Enhanced solution construction with dependency handling"""
        if not self.enable_dependencies:
            # Original random construction for independent tasks
            tour = []
            unvisited_tasks = list(range(self.n_tasks))
            current_task_idx = random.choice(unvisited_tasks)
            tour.append(current_task_idx)
            unvisited_tasks.remove(current_task_idx)
            
            while unvisited_tasks:
                probabilities = self._calculate_probabilities(current_task_idx, unvisited_tasks)
                next_task_idx = np.random.choice(unvisited_tasks, p=probabilities)
                tour.append(next_task_idx)
                unvisited_tasks.remove(next_task_idx)
                current_task_idx = next_task_idx
            return tour
        else:
            # Dependency-aware construction
            tour = []
            remaining_tasks = list(range(self.n_tasks))
            completed_tasks = set()
            current_task_idx = None
            
            while remaining_tasks:
                # Get tasks yang dependencies-nya sudah satisfied
                ready_tasks = self._get_ready_tasks(remaining_tasks, completed_tasks)
                
                if not ready_tasks:
                    # Fallback: pilih task dengan dependencies paling sedikit
                    ready_tasks = [min(remaining_tasks, key=lambda t: len(self.dependencies.get(str(self.rev_task_map[t]), [])))]
                
                if current_task_idx is None or current_task_idx not in ready_tasks:
                    # Pilih task pertama atau random dari ready tasks
                    next_task_idx = random.choice(ready_tasks)
                else:
                    # Gunakan pheromone-based selection dari ready tasks
                    probabilities = self._calculate_probabilities(current_task_idx, ready_tasks)
                    next_task_idx = np.random.choice(ready_tasks, p=probabilities)
                
                tour.append(next_task_idx)
                remaining_tasks.remove(next_task_idx)
                completed_tasks.add(str(self.rev_task_map[next_task_idx]))
                current_task_idx = next_task_idx
                
            return tour

    def _calculate_probabilities(self, current_task_idx, unvisited_tasks):
        pheromone_values = self.pheromones[current_task_idx, unvisited_tasks] ** self.alpha
        heuristic_values = self.heuristics[current_task_idx, unvisited_tasks] ** self.beta
        desirability = pheromone_values * heuristic_values
        total_desirability = np.sum(desirability)
        if total_desirability == 0:
            return np.ones(len(unvisited_tasks)) / len(unvisited_tasks)
        probabilities = desirability / total_desirability
        return probabilities
        
    def _assign_to_agents(self, task_sequence_indices):
        """Enhanced agent assignment dengan dependency dan load balancing consideration"""
        agent_finish_times = {agent[self.agent_id_col]: 0 for agent in self.agents}
        schedule = []
        completed_tasks = set()
        
        for task_idx in task_sequence_indices:
            task = self.tasks[task_idx]
            task_id = str(task[self.task_id_col])
            duration = task.get('length', 1)
            
            # Cari agent terbaik dengan combined score
            best_agent_id = self._find_best_agent(agent_finish_times, duration)
            
            # Calculate start time berdasarkan dependencies
            dependency_finish_time = 0
            if self.enable_dependencies and task_id in self.dependencies:
                for dep_id in self.dependencies[task_id]:
                    # Cari kapan dependency selesai
                    for completed_task in schedule:
                        if completed_task['task_id'] == dep_id:
                            dependency_finish_time = max(dependency_finish_time, completed_task['finish_time'])
                            break
            
            # Start time adalah max dari agent availability dan dependency completion
            start_time = max(agent_finish_times[best_agent_id], dependency_finish_time)
            finish_time = start_time + duration
            agent_finish_times[best_agent_id] = finish_time
            
            schedule.append({
                'task_id': task_id,
                'agent_id': best_agent_id,
                'start_time': start_time,
                'finish_time': finish_time
            })
            
            completed_tasks.add(task_id)
            
        makespan = max(agent_finish_times.values()) if agent_finish_times else 0
        load_balance_index = self._calculate_load_balance_index(agent_finish_times)
        
        return schedule, makespan, load_balance_index
    
    def _find_best_agent(self, agent_finish_times, task_duration):
        """Find agent dengan balance antara makespan dan load balancing - AGGRESSIVE VERSION"""
        best_score = float('inf')
        best_agent = None
        current_max_time = max(agent_finish_times.values()) if agent_finish_times else 0
        
        for agent_id in agent_finish_times:
            # Simulasi assignment ke agent ini
            temp_finish_times = agent_finish_times.copy()
            temp_finish_times[agent_id] += task_duration
            
            if self.prioritize_balance:
                # PURE load balancing approach
                balance_score = self._calculate_load_balance_index(temp_finish_times)
                makespan_penalty = max(temp_finish_times.values()) / 1000  # Minimal weight
                combined_score = balance_score * 1000 + makespan_penalty
            else:
                # Balanced approach
                makespan_penalty = max(temp_finish_times.values())
                balance_penalty = self._calculate_load_balance_index(temp_finish_times) * current_max_time * 2
                combined_score = makespan_penalty + balance_penalty
            
            if combined_score < best_score:
                best_score = combined_score
                best_agent = agent_id
        
        return best_agent or min(agent_finish_times, key=agent_finish_times.get)

    def _update_pheromones(self, all_tours, all_costs):
        self.pheromones *= (1 - self.evaporation_rate)
        for tour, cost in zip(all_tours, all_costs):
            if cost == 0: continue
            pheromone_to_add = self.pheromone_deposit / cost
            for i in range(self.n_tasks - 1):
                self.pheromones[tour[i], tour[i+1]] += pheromone_to_add
            self.pheromones[tour[-1], tour[0]] += pheromone_to_add
    
    def run(self):
        import time
        computation_start_time = time.time()
        
        log_message = "Starting ACO optimization..."
        yield json.dumps({"type": "log", "message": log_message})
        
        for i in range(self.n_iterations):
            all_tours, all_costs = [], []
            new_best_found_in_iter = False
            for _ in range(self.n_ants):
                task_sequence = self._construct_solution()
                schedule, makespan, load_balance_index = self._assign_to_agents(task_sequence)
                cost = self.cost_function(schedule, makespan)
                all_tours.append(task_sequence)
                all_costs.append(cost)
                if cost < self.best_cost or (cost == self.best_cost and load_balance_index < self.best_load_balance_index):
                    self.best_cost = cost
                    self.best_schedule = schedule
                    self.best_load_balance_index = load_balance_index
                    log_message = f"Iteration {i + 1}: New best solution! Makespan: {self.best_cost:.2f}, Load Balance: {load_balance_index:.4f}"
                    yield json.dumps({"type": "log", "message": log_message})
                    new_best_found_in_iter = True
                
            self._update_pheromones(all_tours, all_costs)
            
            # Kirim data update untuk grafik dan log progress
            progress_log = f"Progress: Iteration {i + 1}/{self.n_iterations} -> Current Best: {self.best_cost:.2f}"
            yield json.dumps({
                "type": "iteration",
                "iteration": i + 1,
                "makespan": self.best_cost,
                "log_message": progress_log
            })

        computation_time = time.time() - computation_start_time

        # Kirim hasil final
        yield json.dumps({
            "type": "done",
            "schedule": self.best_schedule,
            "makespan": self.best_cost,
            "computation_time": round(computation_time * 1000, 2),  # Convert to milliseconds
            "log_message": "ACO Optimization Finished!"
        })