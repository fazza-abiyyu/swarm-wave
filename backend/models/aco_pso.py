# models/aco_pso.py

import random
import copy
from .aco import ACO_MultiAgent_Scheduler
from .pso import PSO_MultiAgent_Scheduler

class AcoPsoScheduler:
    def __init__(self, tasks, agents, cost_function, task_id_col, agent_id_col,
                 num_default_agents, aco_params, pso_params, hybrid_iterations=10):
        
        self.tasks = tasks
        self.agents = agents
        self.cost_function = cost_function
        self.task_id_col = task_id_col
        self.agent_id_col = agent_id_col
        self.num_default_agents = num_default_agents
        
        self.aco_params = aco_params
        self.pso_params = pso_params
        self.hybrid_iterations = hybrid_iterations
        self.cost_history = []

    def run(self):
        # 1. Jalankan ACO untuk mendapatkan solusi awal yang baik
        print("Starting ACO phase...")
        aco_scheduler = ACO_MultiAgent_Scheduler(
            tasks=self.tasks,
            agents=self.agents,
            num_default_agents=self.num_default_agents,
            task_id_col=self.task_id_col,
            agent_id_col=self.agent_id_col,
            cost_function=self.cost_function,
            heuristic_function=lambda x: 1.0,
            **self.aco_params
        )
        best_aco_schedule, best_aco_cost = aco_scheduler.run()
        self.cost_history.extend(aco_scheduler.cost_history)

        # 2. Gunakan solusi ACO sebagai inisialisasi untuk PSO
        print("Starting PSO phase...")
        pso_scheduler = PSO_MultiAgent_Scheduler(
            tasks=self.tasks,
            agents=self.agents,
            cost_function=self.cost_function,
            task_id_col=self.task_id_col,
            agent_id_col=self.agent_id_col,
            **self.pso_params
        )

        # Inisialisasi posisi partikel dengan solusi ACO
        pso_scheduler.initialize_particles_from_schedule(best_aco_schedule)
        
        # Jalankan iterasi hybrid
        for _ in range(self.hybrid_iterations):
            pso_scheduler.update_particles()
            current_best_cost = pso_scheduler.gbest_cost
            self.cost_history.append(current_best_cost)
        
        final_best_schedule = pso_scheduler.gbest_position
        final_best_cost = pso_scheduler.gbest_cost
        
        return final_best_schedule, final_best_cost