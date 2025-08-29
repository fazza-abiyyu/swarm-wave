import numpy as np
import random
import json

class PSO_MultiAgent_Scheduler:
    def __init__(self, tasks, agents, cost_function, task_id_col='id', agent_id_col='id',
                 n_particles=30, n_iterations=100, w=0.5, c1=1.5, c2=1.5):
        self.tasks = tasks
        self.agents = agents
        self.cost_function = cost_function
        self.task_id_col = task_id_col
        self.agent_id_col = agent_id_col
        self.n_tasks = len(tasks)
        self.n_agents = len(agents)
        self.n_particles = n_particles
        self.n_iterations = n_iterations
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.positions = np.random.rand(self.n_particles, self.n_tasks)
        self.velocities = np.random.rand(self.n_particles, self.n_tasks) * 0.1
        self.pbest_positions = self.positions.copy()
        self.pbest_costs = np.array([float('inf')] * self.n_particles)
        self.gbest_position = None
        self.gbest_cost = float('inf')
        self.gbest_schedule = None

    def _position_to_sequence(self, position):
        return np.argsort(position)

    def _evaluate_sequence(self, task_sequence):
        agent_finish_times = {agent[self.agent_id_col]: 0 for agent in self.agents}
        schedule = []
        for task_idx in task_sequence:
            task = self.tasks[task_idx]
            best_agent_id = min(agent_finish_times, key=agent_finish_times.get)
            start_time = agent_finish_times[best_agent_id]
            duration = task.get('length', 1) 
            finish_time = start_time + duration
            agent_finish_times[best_agent_id] = finish_time
            schedule.append({
                'task_id': task[self.task_id_col], 'agent_id': best_agent_id,
                'start_time': start_time, 'finish_time': finish_time
            })
        makespan = max(agent_finish_times.values()) if agent_finish_times else 0
        return self.cost_function(schedule, makespan), schedule

    def run(self):
        log_message = "Starting PSO optimization..."
        yield json.dumps({"type": "log", "message": log_message})
        
        for i in range(self.n_iterations):
            new_best_found_in_iter = False
            for p in range(self.n_particles):
                sequence = self._position_to_sequence(self.positions[p])
                cost, schedule = self._evaluate_sequence(sequence)

                if cost < self.pbest_costs[p]:
                    self.pbest_costs[p] = cost
                    self.pbest_positions[p] = self.positions[p].copy()

                if cost < self.gbest_cost:
                    self.gbest_cost = cost
                    self.gbest_position = self.positions[p].copy()
                    self.gbest_schedule = schedule
                    new_best_found_in_iter = True

            if new_best_found_in_iter:
                log_message = f"Iteration {i + 1}: New best solution found! Makespan: {self.gbest_cost:.2f}"
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

        # Kirim hasil final
        yield json.dumps({
            "type": "done",
            "schedule": self.gbest_schedule,
            "makespan": self.gbest_cost,
            "log_message": "PSO Optimization Finished!"
        })