classdef PSO_MultiAgent_Scheduler < handle
    % PSO Multi-Agent Task Scheduler for Cloud Computing
    % Particle Swarm Optimization algorithm for task scheduling with dependencies
    
    properties
        tasks                   % Array of task structures
        agents                  % Array of agent structures
        cost_function          % Handle to cost function
        task_id_col            % Task ID column name
        agent_id_col           % Agent ID column name
        enable_dependencies    % Boolean for dependency handling
        
        n_tasks               % Number of tasks
        n_agents              % Number of agents
        n_particles          % Number of particles
        n_iterations         % Number of iterations
        w                    % Inertia weight
        c1                   % Cognitive parameter
        c2                   % Social parameter
        
        dependencies         % Task dependencies map
        dependency_graph     % Dependency graph
        
        positions           % Particle positions
        velocities          % Particle velocities
        pbest_positions     % Personal best positions
        pbest_costs         % Personal best costs
        gbest_position      % Global best position
        gbest_cost          % Global best cost
        gbest_schedule      % Global best schedule
        gbest_load_balance_index % Global best load balance index
    end
    
    methods
        function obj = PSO_MultiAgent_Scheduler(tasks, agents, cost_function, varargin)
            % Constructor
            p = inputParser;
            addRequired(p, 'tasks');
            addRequired(p, 'agents');
            addRequired(p, 'cost_function');
            addParameter(p, 'task_id_col', 'id', @ischar);
            addParameter(p, 'agent_id_col', 'id', @ischar);
            addParameter(p, 'n_particles', 30, @isnumeric);
            addParameter(p, 'n_iterations', 100, @isnumeric);
            addParameter(p, 'w', 0.5, @isnumeric);
            addParameter(p, 'c1', 1.5, @isnumeric);
            addParameter(p, 'c2', 1.5, @isnumeric);
            addParameter(p, 'enable_dependencies', false, @islogical);
            
            parse(p, tasks, agents, cost_function, varargin{:});
            
            obj.tasks = p.Results.tasks;
            obj.agents = p.Results.agents;
            obj.cost_function = p.Results.cost_function;
            obj.task_id_col = p.Results.task_id_col;
            obj.agent_id_col = p.Results.agent_id_col;
            obj.enable_dependencies = p.Results.enable_dependencies;
            
            obj.n_tasks = length(obj.tasks);
            obj.n_agents = length(obj.agents);
            obj.n_particles = p.Results.n_particles;
            obj.n_iterations = p.Results.n_iterations;
            obj.w = p.Results.w;
            obj.c1 = p.Results.c1;
            obj.c2 = p.Results.c2;
            
            if obj.enable_dependencies
                obj.parse_dependencies();
                obj.build_dependency_graph();
            end
            
            % Initialize particles
            obj.positions = rand(obj.n_particles, obj.n_tasks);
            obj.velocities = rand(obj.n_particles, obj.n_tasks) * 0.1;
            obj.pbest_positions = obj.positions;
            obj.pbest_costs = inf(obj.n_particles, 1);
            obj.gbest_position = [];
            obj.gbest_cost = inf;
            obj.gbest_schedule = [];
            obj.gbest_load_balance_index = inf;
        end
        
        function parse_dependencies(obj)
            % Parse task dependencies
            obj.dependencies = containers.Map();
            
            for i = 1:obj.n_tasks
                task = obj.tasks(i);
                task_id = task.(obj.task_id_col);
                if isnumeric(task_id)
                    task_id = num2str(task_id);
                end
                
                deps = {};
                if isfield(task, 'dependencies') && ~isempty(task.dependencies)
                    if ischar(task.dependencies) || isstring(task.dependencies)
                        dep_str = char(task.dependencies);
                        if ~isempty(strtrim(dep_str)) && ~strcmpi(strtrim(dep_str), 'null')
                            deps = strsplit(strrep(dep_str, ';', ','), ',');
                            deps = strtrim(deps);
                            deps = deps(~cellfun(@isempty, deps));
                        end
                    elseif iscell(task.dependencies)
                        deps = task.dependencies;
                    end
                end
                
                obj.dependencies(task_id) = deps;
            end
        end
        
        function build_dependency_graph(obj)
            % Build dependency graph
            obj.dependency_graph = obj.dependencies;
        end
        
        function index = calculate_load_balance_index(obj, agent_finish_times)
            % Calculate load balance index (lower = better balance)
            times = cell2mat(values(agent_finish_times));
            
            if length(times) <= 1
                index = 0.0;
                return;
            end
            
            mean_time = mean(times);
            if mean_time == 0
                index = 0.0;
                return;
            end
            
            % Standard deviation normalized by mean
            std_time = std(times);
            index = std_time / mean_time;
        end
        
        function satisfied = is_dependency_satisfied(obj, task_id, completed_tasks)
            % Check if all dependencies are satisfied
            if ~obj.enable_dependencies || ~obj.dependencies.isKey(task_id)
                satisfied = true;
                return;
            end
            
            deps = obj.dependencies(task_id);
            satisfied = true;
            
            for i = 1:length(deps)
                if ~any(strcmp(deps{i}, completed_tasks))
                    satisfied = false;
                    return;
                end
            end
        end
        
        function sequence = position_to_sequence(obj, position)
            % Enhanced position to sequence with dependency consideration
            if ~obj.enable_dependencies
                % Original sorting for independent tasks
                [~, sequence] = sort(position, 'descend');
            else
                % Dependency-aware sequence generation
                task_priorities = [(1:obj.n_tasks)', position(:)];
                sequence = [];
                remaining_tasks = 1:obj.n_tasks;
                completed_tasks = {};
                
                % Sort by priority but respect dependencies
                [~, sorted_idx] = sort(task_priorities(:,2), 'descend');
                
                while ~isempty(remaining_tasks)
                    % Find task with highest priority whose dependencies are satisfied
                    selected_task = [];
                    
                    for i = 1:length(sorted_idx)
                        task_idx = sorted_idx(i);
                        if any(remaining_tasks == task_idx)
                            task_id = obj.tasks(task_idx).(obj.task_id_col);
                            if isnumeric(task_id)
                                task_id = num2str(task_id);
                            end
                            
                            if obj.is_dependency_satisfied(task_id, completed_tasks)
                                selected_task = task_idx;
                                break;
                            end
                        end
                    end
                    
                    if isempty(selected_task)
                        % Fallback: pick task with fewest dependencies
                        min_deps = inf;
                        for i = 1:length(remaining_tasks)
                            task_idx = remaining_tasks(i);
                            task_id = obj.tasks(task_idx).(obj.task_id_col);
                            if isnumeric(task_id)
                                task_id = num2str(task_id);
                            end
                            
                            if obj.dependencies.isKey(task_id)
                                n_deps = length(obj.dependencies(task_id));
                            else
                                n_deps = 0;
                            end
                            
                            if n_deps < min_deps
                                min_deps = n_deps;
                                selected_task = task_idx;
                            end
                        end
                    end
                    
                    sequence = [sequence, selected_task];
                    remaining_tasks(remaining_tasks == selected_task) = [];
                    
                    task_id = obj.tasks(selected_task).(obj.task_id_col);
                    if isnumeric(task_id)
                        task_id = num2str(task_id);
                    end
                    completed_tasks{end+1} = task_id;
                end
            end
        end
        
        function [cost, schedule, load_balance_index] = evaluate_sequence(obj, task_sequence)
            % Enhanced evaluation with dependency and load balancing consideration
            agent_finish_times = containers.Map();
            for i = 1:obj.n_agents
                agent_id = obj.agents(i).(obj.agent_id_col);
                agent_finish_times(agent_id) = 0;
            end
            
            schedule = struct('task_id', {}, 'agent_id', {}, 'start_time', {}, 'finish_time', {});
            completed_tasks = {};
            
            for i = 1:length(task_sequence)
                task_idx = task_sequence(i);
                task = obj.tasks(task_idx);
                task_id = task.(obj.task_id_col);
                if isnumeric(task_id)
                    task_id = num2str(task_id);
                end
                
                if isfield(task, 'length')
                    duration = task.length;
                else
                    duration = 1;
                end
                
                best_agent_id = obj.find_best_agent(agent_finish_times, duration);
                
                % Calculate start time based on dependencies
                dependency_finish_time = 0;
                if obj.enable_dependencies && obj.dependencies.isKey(task_id)
                    deps = obj.dependencies(task_id);
                    for j = 1:length(deps)
                        dep_id = deps{j};
                        for k = 1:length(schedule)
                            if strcmp(schedule(k).task_id, dep_id)
                                dependency_finish_time = max(dependency_finish_time, schedule(k).finish_time);
                                break;
                            end
                        end
                    end
                end
                
                start_time = max(agent_finish_times(best_agent_id), dependency_finish_time);
                finish_time = start_time + duration;
                agent_finish_times(best_agent_id) = finish_time;
                
                schedule(end+1) = struct('task_id', task_id, 'agent_id', best_agent_id, ...
                                       'start_time', start_time, 'finish_time', finish_time);
                completed_tasks{end+1} = task_id;
            end
            
            times = cell2mat(values(agent_finish_times));
            makespan = max(times);
            load_balance_index = obj.calculate_load_balance_index(agent_finish_times);
            cost = obj.cost_function(schedule, makespan);
        end
        
        function best_agent = find_best_agent(obj, agent_finish_times, task_duration)
            % Find agent with balance between makespan and load balancing - AGGRESSIVE VERSION
            best_score = inf;
            best_agent = '';
            agent_ids = keys(agent_finish_times);
            current_times = cell2mat(values(agent_finish_times));
            current_max_time = max(current_times);
            
            for i = 1:length(agent_ids)
                agent_id = agent_ids{i};
                
                % Simulate assignment to this agent
                temp_finish_times = agent_finish_times;
                temp_finish_times(agent_id) = temp_finish_times(agent_id) + task_duration;
                
                % Calculate penalties
                new_makespan = max(cell2mat(values(temp_finish_times)));
                makespan_penalty = new_makespan;
                
                % AGGRESSIVE load balancing penalty
                balance_penalty = obj.calculate_load_balance_index(temp_finish_times) * current_max_time * 2;
                
                % Combined score with emphasis on balance
                combined_score = makespan_penalty + balance_penalty;
                
                if combined_score < best_score
                    best_score = combined_score;
                    best_agent = agent_id;
                end
            end
            
            if isempty(best_agent)
                times = cell2mat(values(agent_finish_times));
                [~, idx] = min(times);
                agent_ids = keys(agent_finish_times);
                best_agent = agent_ids{idx};
            end
        end
        
        function result = run(obj)
            % Main optimization loop
            tic;
            fprintf('Starting PSO optimization...\n');
            
            result.log_messages = {};
            result.iterations = [];
            
            for i = 1:obj.n_iterations
                new_best_found_in_iter = false;
                
                % Evaluate all particles
                for p = 1:obj.n_particles
                    sequence = obj.position_to_sequence(obj.positions(p, :));
                    [cost, schedule, load_balance_index] = obj.evaluate_sequence(sequence);
                    
                    % Update personal best
                    if cost < obj.pbest_costs(p)
                        obj.pbest_costs(p) = cost;
                        obj.pbest_positions(p, :) = obj.positions(p, :);
                    end
                    
                    % Update global best
                    if cost < obj.gbest_cost || (cost == obj.gbest_cost && load_balance_index < obj.gbest_load_balance_index)
                        obj.gbest_cost = cost;
                        obj.gbest_position = obj.positions(p, :);
                        obj.gbest_schedule = schedule;
                        obj.gbest_load_balance_index = load_balance_index;
                        new_best_found_in_iter = true;
                    end
                end
                
                if new_best_found_in_iter
                    log_msg = sprintf('Iteration %d: New best solution! Makespan: %.2f, Load Balance: %.4f', ...
                                    i, obj.gbest_cost, obj.gbest_load_balance_index);
                    result.log_messages{end+1} = log_msg;
                    fprintf('%s\n', log_msg);
                end
                
                % Update particle velocities and positions
                for p = 1:obj.n_particles
                    r1 = rand(1, obj.n_tasks);
                    r2 = rand(1, obj.n_tasks);
                    
                    cognitive_velocity = obj.c1 * r1 .* (obj.pbest_positions(p, :) - obj.positions(p, :));
                    social_velocity = obj.c2 * r2 .* (obj.gbest_position - obj.positions(p, :));
                    
                    obj.velocities(p, :) = obj.w * obj.velocities(p, :) + cognitive_velocity + social_velocity;
                    obj.positions(p, :) = obj.positions(p, :) + obj.velocities(p, :);
                end
                
                % Store iteration data
                progress_log = sprintf('Progress: Iteration %d/%d -> Current Best: %.2f', ...
                                     i, obj.n_iterations, obj.gbest_cost);
                result.iterations(i).iteration = i;
                result.iterations(i).makespan = obj.gbest_cost;
                result.iterations(i).log_message = progress_log;
                
                if mod(i, 10) == 0 || new_best_found_in_iter
                    fprintf('%s\n', progress_log);
                end
            end
            
            computation_time = toc * 1000; % Convert to milliseconds
            
            % Final results
            result.schedule = obj.gbest_schedule;
            result.makespan = obj.gbest_cost;
            result.computation_time = computation_time;
            result.log_messages{end+1} = 'PSO Optimization Finished!';
            
            fprintf('PSO Optimization Finished! Total time: %.2f ms\n', computation_time);
            fprintf('Best makespan: %.2f\n', obj.gbest_cost);
            fprintf('Best load balance index: %.4f\n', obj.gbest_load_balance_index);
        end
    end
end