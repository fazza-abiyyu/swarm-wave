import numpy as np
import random
# from tqdm import tqdm <-- tidak perlu jika tidak digunakan

class ACO_MultiAgent_Scheduler:
    def __init__(self, tasks, cost_function, heuristic_function,
                 agents=None, num_default_agents=3,
                 task_id_col='id', agent_id_col='id',
                 n_ants=10, n_iterations=100, alpha=1.0, beta=2.0,
                 evaporation_rate=0.5, pheromone_deposit=100.0):
        
        self.tasks = tasks
        self.cost_function = cost_function
        self.heuristic_function = heuristic_function
        self.task_id_col = task_id_col
        self.agent_id_col = agent_id_col

        if not agents:
            print(f"⚠️ Data agent tidak ditemukan. Membuat {num_default_agents} agent default secara otomatis.")
            self.agents = [{self.agent_id_col: f'DefaultAgent-{i+1}'} for i in range(num_default_agents)]
        else:
            self.agents = agents

        self.n_tasks = len(self.tasks)
        self.n_agents = len(self.agents)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.pheromone_deposit = pheromone_deposit

        self.task_map = {task[self.task_id_col]: i for i, task in enumerate(self.tasks)}
        self.rev_task_map = {i: task[self.task_id_col] for i, task in enumerate(self.tasks)}

        self.pheromones = np.ones((self.n_tasks, self.n_tasks))
        self.heuristics = self._calculate_heuristics()
        self.best_schedule = None
        self.best_cost = float('inf')
        
        # BARIS BARU: Untuk menyimpan riwayat cost terbaik
        self.cost_history = []

    # ... (metode-metode lain seperti _calculate_heuristics, _construct_solution, dll. tidak diubah) ...
    def _calculate_heuristics(self):
        heuristics = np.zeros((self.n_tasks, self.n_tasks))
        for i in range(self.n_tasks):
            for j in range(self.n_tasks):
                if i != j:
                    heuristics[i, j] = self.heuristic_function(self.tasks[j])
        return heuristics

    def _construct_solution(self):
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
        agent_finish_times = {agent[self.agent_id_col]: 0 for agent in self.agents}
        schedule = []
        for task_idx in task_sequence_indices:
            task = self.tasks[task_idx]
            best_agent_id = min(agent_finish_times, key=agent_finish_times.get)
            start_time = agent_finish_times[best_agent_id]
            # Cari field execution time dengan berbagai kemungkinan nama
            duration = task.get('Execution_Time (s)', task.get('execution_time', task.get('duration', 1)))
            finish_time = start_time + duration
            agent_finish_times[best_agent_id] = finish_time
            
            schedule.append({
                'task_id': task[self.task_id_col],
                'agent_id': best_agent_id,
                'start_time': start_time,
                'finish_time': finish_time
            })
            
        makespan = max(agent_finish_times.values()) if agent_finish_times else 0
        return schedule, makespan

    def _update_pheromones(self, all_tours, all_costs):
        self.pheromones *= (1 - self.evaporation_rate)
        for tour, cost in zip(all_tours, all_costs):
            if cost == 0: continue
            pheromone_to_add = self.pheromone_deposit / cost
            for i in range(self.n_tasks - 1):
                self.pheromones[tour[i], tour[i+1]] += pheromone_to_add
            self.pheromones[tour[-1], tour[0]] += pheromone_to_add
    
    def run(self):
        # Hapus cetakan "Memulai optimasi..." agar lebih ringkas
        # print("Memulai optimasi penjadwalan dengan ACO...")
        
        for i in range(self.n_iterations):
            all_tours, all_costs = [], []
            for _ in range(self.n_ants):
                task_sequence = self._construct_solution()
                schedule, makespan = self._assign_to_agents(task_sequence)
                cost = self.cost_function(schedule, makespan)
                all_tours.append(task_sequence)
                all_costs.append(cost)
                if cost < self.best_cost:
                    self.best_cost = cost
                    self.best_schedule = schedule
                
            # --- Perubahan PENTING: Hapus SEMUA cetakan di dalam loop ---
            # Hapus atau komentari baris ini:
            # if self.best_cost < old_best_cost:
            #     print(f"\nIterasi {i + 1}: Ditemukan solusi baru yang lebih baik! Makespan: {self.best_cost:.2f}")
            # print(f"\rIterasi {i + 1}/{self.n_iterations} -> Terbaik Iterasi Ini: {best_in_iteration:.2f} | Terbaik Sejauh Ini: {self.best_cost:.2f}", end="")

            self._update_pheromones(all_tours, all_costs)
            self.cost_history.append(self.best_cost)
        
        # Hapus cetakan "Optimasi Selesai!"
        # print("\nOptimasi Selesai!")
        
        return self.best_schedule, self.best_cost