classdef ACO_MultiAgent_Scheduler < handle
    % ACO Multi-Agent Task Scheduler for Cloud Computing
    % Ant Colony Optimization algorithm for task scheduling with dependencies
    
    properties
        tasks                   % Array of task structures
        agents                  % Array of agent structures
        cost_function          % Handle to cost function
        heuristic_function     % Handle to heuristic function
        task_id_col            % Task ID column name
        agent_id_col           % Agent ID column name
        enable_dependencies    % Boolean for dependency handling
        
        n_tasks               % Number of tasks
        n_agents              % Number of agents
        n_ants               % Number of ants
        n_iterations         % Number of iterations
        alpha                % Pheromone importance
        beta                 % Heuristic importance
        evaporation_rate     % Pheromone evaporation rate
        pheromone_deposit    % Amount of pheromone to deposit
        prioritize_balance   % Load balancing mode
        
        task_map             % Task ID to index mapping
        rev_task_map         % Index to task ID mapping
        dependencies         % Task dependencies map
        dependency_graph     % Dependency graph
        
        pheromones          % Pheromone matrix
        heuristics          % Heuristic matrix
        best_schedule       % Best schedule found
        best_cost           % Best cost found
        best_load_balance_index % Best load balance index
    end
    
    methods
        function obj = ACO_MultiAgent_Scheduler(tasks, cost_function, heuristic_function, varargin)
            % Constructor
            p = inputParser;
            addRequired(p, 'tasks');
            addRequired(p, 'cost_function');
            addRequired(p, 'heuristic_function');
            addParameter(p, 'agents', [], @(x) isstruct(x) || isempty(x));
            addParameter(p, 'num_default_agents', 3, @isnumeric);
            addParameter(p, 'task_id_col', 'id', @ischar);
            addParameter(p, 'agent_id_col', 'id', @ischar);
            addParameter(p, 'n_ants', 10, @isnumeric);
            addParameter(p, 'n_iterations', 100, @isnumeric);
            addParameter(p, 'alpha', 1.0, @isnumeric);
            addParameter(p, 'beta', 2.0, @isnumeric);
            addParameter(p, 'evaporation_rate', 0.5, @isnumeric);
            addParameter(p, 'pheromone_deposit', 100.0, @isnumeric);
            addParameter(p, 'enable_dependencies', false, @islogical);
            
            parse(p, tasks, cost_function, heuristic_function, varargin{:});
            
            obj.tasks = p.Results.tasks;
            obj.cost_function = p.Results.cost_function;
            obj.heuristic_function = p.Results.heuristic_function;
            obj.task_id_col = p.Results.task_id_col;
            obj.agent_id_col = p.Results.agent_id_col;
            obj.enable_dependencies = p.Results.enable_dependencies;
            
            if isempty(p.Results.agents)
                for i = 1:p.Results.num_default_agents
                    obj.agents(i).id = sprintf('DefaultAgent-%d', i);
                end
            else
                obj.agents = p.Results.agents;
            end
            
            obj.n_tasks = length(obj.tasks);
            obj.n_agents = length(obj.agents);
            obj.n_ants = p.Results.n_ants;
            obj.n_iterations = p.Results.n_iterations;
            obj.alpha = p.Results.alpha;
            obj.beta = p.Results.beta;
            obj.evaporation_rate = p.Results.evaporation_rate;
            obj.pheromone_deposit = p.Results.pheromone_deposit;
            obj.prioritize_balance = true;
            
            obj.build_task_mappings();
            
            if obj.enable_dependencies
                obj.parse_dependencies();
                obj.build_dependency_graph();
            end
            
            obj.pheromones = ones(obj.n_tasks, obj.n_tasks);
            obj.heuristics = obj.calculate_heuristics();
            obj.best_schedule = [];
            obj.best_cost = inf;
            obj.best_load_balance_index = inf;
        end
        
        function build_task_mappings(obj)
            % Build task ID mappings
            obj.task_map = containers.Map();
            obj.rev_task_map = containers.Map();
            
            for i = 1:obj.n_tasks
                task_id = obj.tasks(i).(obj.task_id_col);
                if isnumeric(task_id)
                    task_id = num2str(task_id);
                end
                obj.task_map(task_id) = i;
                obj.rev_task_map(num2str(i)) = task_id;
            end
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
        
        function ready_tasks = get_ready_tasks(obj, remaining_tasks, completed_tasks)
            % Get tasks whose dependencies are satisfied
            if ~obj.enable_dependencies
                ready_tasks = remaining_tasks;
                return;
            end
            
            ready_tasks = [];
            for i = 1:length(remaining_tasks)
                task_idx = remaining_tasks(i);
                task_id = obj.rev_task_map(num2str(task_idx));
                if obj.is_dependency_satisfied(task_id, completed_tasks)
                    ready_tasks = [ready_tasks, task_idx];
                end
            end
        end
        
        function heuristics = calculate_heuristics(obj)
            % Calculate heuristic matrix
            heuristics = zeros(obj.n_tasks, obj.n_tasks);
            
            for i = 1:obj.n_tasks
                for j = 1:obj.n_tasks
                    if i ~= j
                        heuristics(i, j) = obj.heuristic_function(obj.tasks(j));
                    end
                end
            end
        end
        
        function tour = construct_solution(obj)
            % Construct ant solution with dependency handling
            if ~obj.enable_dependencies
                % Original random construction for independent tasks
                tour = [];
                unvisited_tasks = 1:obj.n_tasks;
                current_task_idx = unvisited_tasks(randi(length(unvisited_tasks)));
                tour = [tour, current_task_idx];
                unvisited_tasks(unvisited_tasks == current_task_idx) = [];
                
                while ~isempty(unvisited_tasks)
                    probabilities = obj.calculate_probabilities(current_task_idx, unvisited_tasks);
                    next_task_idx = obj.roulette_wheel_selection(unvisited_tasks, probabilities);
                    tour = [tour, next_task_idx];
                    unvisited_tasks(unvisited_tasks == next_task_idx) = [];
                    current_task_idx = next_task_idx;
                end
            else
                % Dependency-aware construction
                tour = [];
                remaining_tasks = 1:obj.n_tasks;
                completed_tasks = {};
                current_task_idx = [];
                
                while ~isempty(remaining_tasks)
                    ready_tasks = obj.get_ready_tasks(remaining_tasks, completed_tasks);
                    
                    if isempty(ready_tasks)
                        % Fallback: pick task with fewest dependencies
                        min_deps = inf;
                        for i = 1:length(remaining_tasks)
                            task_idx = remaining_tasks(i);
                            task_id = obj.rev_task_map(num2str(task_idx));
                            if obj.dependencies.isKey(task_id)
                                n_deps = length(obj.dependencies(task_id));
                            else
                                n_deps = 0;
                            end
                            if n_deps < min_deps
                                min_deps = n_deps;
                                ready_tasks = task_idx;
                            end
                        end
                    end
                    
                    if isempty(current_task_idx) || ~any(ready_tasks == current_task_idx)
                        next_task_idx = ready_tasks(randi(length(ready_tasks)));
                    else
                        probabilities = obj.calculate_probabilities(current_task_idx, ready_tasks);
                        next_task_idx = obj.roulette_wheel_selection(ready_tasks, probabilities);
                    end
                    
                    tour = [tour, next_task_idx];
                    remaining_tasks(remaining_tasks == next_task_idx) = [];
                    completed_tasks{end+1} = obj.rev_task_map(num2str(next_task_idx));
                    current_task_idx = next_task_idx;
                end
            end
        end
        
        function probabilities = calculate_probabilities(obj, current_task_idx, unvisited_tasks)
            % Calculate selection probabilities
            pheromone_values = obj.pheromones(current_task_idx, unvisited_tasks) .^ obj.alpha;
            heuristic_values = obj.heuristics(current_task_idx, unvisited_tasks) .^ obj.beta;
            desirability = pheromone_values .* heuristic_values;
            total_desirability = sum(desirability);
            
            if total_desirability == 0
                probabilities = ones(1, length(unvisited_tasks)) / length(unvisited_tasks);
            else
                probabilities = desirability / total_desirability;
            end
        end
        
        function selected = roulette_wheel_selection(obj, candidates, probabilities)
            % Roulette wheel selection
            cumulative = cumsum(probabilities);
            r = rand();
            
            for i = 1:length(cumulative)
                if r <= cumulative(i)
                    selected = candidates(i);
                    return;
                end
            end
            
            selected = candidates(end);
        end
        
        function [schedule, makespan, load_balance_index] = assign_to_agents(obj, task_sequence_indices)
            % Enhanced agent assignment with dependency and load balancing
            agent_finish_times = containers.Map();
            for i = 1:obj.n_agents
                agent_id = obj.agents(i).(obj.agent_id_col);
                agent_finish_times(agent_id) = 0;
            end
            
            schedule = struct('task_id', {}, 'agent_id', {}, 'start_time', {}, 'finish_time', {});
            completed_tasks = {};
            
            for i = 1:length(task_sequence_indices)
                task_idx = task_sequence_indices(i);
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
        end
        
        function best_agent = find_best_agent(obj, agent_finish_times, task_duration)
            % Find agent with balance between makespan and load balancing
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
                
                if obj.prioritize_balance
                    % Pure load balancing approach
                    balance_score = obj.calculate_load_balance_index(temp_finish_times);
                    makespan_penalty = max(cell2mat(values(temp_finish_times))) / 1000;
                    combined_score = balance_score * 1000 + makespan_penalty;
                else
                    % Balanced approach
                    makespan_penalty = max(cell2mat(values(temp_finish_times)));
                    balance_penalty = obj.calculate_load_balance_index(temp_finish_times) * current_max_time * 2;
                    combined_score = makespan_penalty + balance_penalty;
                end
                
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
        
        function update_pheromones(obj, all_tours, all_costs)
            % Update pheromone trails
            obj.pheromones = obj.pheromones * (1 - obj.evaporation_rate);
            
            for i = 1:length(all_tours)
                tour = all_tours{i};
                cost = all_costs(i);
                
                if cost == 0
                    continue;
                end
                
                pheromone_to_add = obj.pheromone_deposit / cost;
                
                for j = 1:length(tour)-1
                    obj.pheromones(tour(j), tour(j+1)) = ...
                        obj.pheromones(tour(j), tour(j+1)) + pheromone_to_add;
                end
                
                % Close the loop
                obj.pheromones(tour(end), tour(1)) = ...
                    obj.pheromones(tour(end), tour(1)) + pheromone_to_add;
            end
        end
        
        function result = run(obj)
            % Main optimization loop
            tic;
            fprintf('Starting ACO optimization...\n');
            
            result.log_messages = {};
            result.iterations = [];
            
            for i = 1:obj.n_iterations
                all_tours = {};
                all_costs = [];
                new_best_found_in_iter = false;
                
                for ant = 1:obj.n_ants
                    task_sequence = obj.construct_solution();
                    [schedule, makespan, load_balance_index] = obj.assign_to_agents(task_sequence);
                    cost = obj.cost_function(schedule, makespan);
                    
                    all_tours{end+1} = task_sequence;
                    all_costs(end+1) = cost;
                    
                    if cost < obj.best_cost || (cost == obj.best_cost && load_balance_index < obj.best_load_balance_index)
                        obj.best_cost = cost;
                        obj.best_schedule = schedule;
                        obj.best_load_balance_index = load_balance_index;
                        
                        log_msg = sprintf('Iteration %d: New best solution! Makespan: %.2f, Load Balance: %.4f', ...
                                        i, obj.best_cost, load_balance_index);
                        result.log_messages{end+1} = log_msg;
                        fprintf('%s\n', log_msg);
                        new_best_found_in_iter = true;
                    end
                end
                
                obj.update_pheromones(all_tours, all_costs);
                
                % Store iteration data
                progress_log = sprintf('Progress: Iteration %d/%d -> Current Best: %.2f', ...
                                     i, obj.n_iterations, obj.best_cost);
                result.iterations(i).iteration = i;
                result.iterations(i).makespan = obj.best_cost;
                result.iterations(i).log_message = progress_log;
                
                if mod(i, 10) == 0 || new_best_found_in_iter
                    fprintf('%s\n', progress_log);
                end
            end
            
            computation_time = toc * 1000; % Convert to milliseconds
            
            % Final results
            result.schedule = obj.best_schedule;
            result.makespan = obj.best_cost;
            result.computation_time = computation_time;
            result.log_messages{end+1} = 'ACO Optimization Finished!';
            
            fprintf('ACO Optimization Finished! Total time: %.2f ms\n', computation_time);
            fprintf('Best makespan: %.2f\n', obj.best_cost);
            fprintf('Best load balance index: %.4f\n', obj.best_load_balance_index);
        end
    end
end