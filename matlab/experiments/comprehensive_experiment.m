%% =================================================================
%% COMPREHENSIVE SWARM INTELLIGENCE EXPERIMENT
%% =================================================================
% Real-time ACO vs PSO comparison with structured dependencies
% Features: Live plotting, dependency handling, manual inspection
% Version: 4.0 - Clean & Optimized

clear all; close all; clc;

%% =================================================================
%% CONFIGURATION
%% =================================================================

% Experiment Settings
EXPERIMENT_NAME = 'ComprehensiveManual';
RUN_DATE = datestr(now, 'yyyy-mm-dd_HHMMSS');
OUTPUT_DIR = './results/';
PLOTS_DIR = './plots/';

% Dataset Configuration
USE_REAL_DATA = true;
NUM_TASKS = 1000;
NUM_AGENTS = 10;
NUM_RUNS = 1;
NUM_ITER = 100;

% Visualization Settings
ENABLE_REALTIME_PLOTS = true;
ENABLE_TASK_DISTRIBUTION = true;
PLOT_UPDATE_INTERVAL = 2;
KEEP_PLOTS_OPEN = true;

% ACO Parameters
ACO_CONFIG = struct(...
    'n_ants', 6, ...
    'n_iterations', NUM_ITER, ...
    'alpha', 1.0, ...
    'beta', 2.0, ...
    'evaporation_rate', 0.3, ...
    'pheromone_deposit', 100.0 ...
);

% PSO Parameters
PSO_CONFIG = struct(...
    'n_particles', 8, ...
    'n_iterations', NUM_ITER, ...
    'w', 0.5, ...
    'c1', 1.5, ...
    'c2', 1.5 ...
);

% Output Settings
SAVE_PLOTS = true;
PLOT_FORMAT = 'png';
FIGURE_SIZE = [1200, 800];

%% =================================================================
%% INITIALIZATION
%% =================================================================

fprintf('🧪 Comprehensive Swarm Intelligence Experiment\n');
fprintf('═══════════════════════════════════════════════\n');
fprintf('Experiment: %s\n', EXPERIMENT_NAME);
fprintf('Date/Time: %s\n', RUN_DATE);
fprintf('Configuration: %d tasks, %d agents, %d runs\n', NUM_TASKS, NUM_AGENTS, NUM_RUNS);
if KEEP_PLOTS_OPEN
    fprintf('Real-time plots: ENABLED | Keep open: YES\n');
else
    fprintf('Real-time plots: ENABLED | Keep open: NO\n');
end
fprintf('───────────────────────────────────────────────\n');

% Create directory structure
PLOT_SUBFOLDER = sprintf('%s_%s', EXPERIMENT_NAME, RUN_DATE);
FULL_PLOTS_DIR = fullfile(PLOTS_DIR, PLOT_SUBFOLDER);

RUN_DIRS = cell(NUM_RUNS, 1);
for run_idx = 1:NUM_RUNS
    RUN_DIRS{run_idx} = fullfile(FULL_PLOTS_DIR, sprintf('Run_%d', run_idx));
end

if ~exist(OUTPUT_DIR, 'dir'), mkdir(OUTPUT_DIR); end
if ~exist(PLOTS_DIR, 'dir'), mkdir(PLOTS_DIR); end  
if ~exist(FULL_PLOTS_DIR, 'dir'), mkdir(FULL_PLOTS_DIR); end

for run_idx = 1:NUM_RUNS
    if ~exist(RUN_DIRS{run_idx}, 'dir'), mkdir(RUN_DIRS{run_idx}); end
end

fprintf('📁 Output directories created\n');
fprintf('   Main: %s\n', FULL_PLOTS_DIR);

% Initialize real-time visualization
if ENABLE_REALTIME_PLOTS
    fig_realtime = figure('Position', [100, 100, FIGURE_SIZE]);
    set(fig_realtime, 'Name', '🎯 Real-time Monitoring - Will Stay Open');
    
    subplot(2, 2, 1); 
    title('ACO Convergence'); xlabel('Iteration'); ylabel('Best Makespan');
    grid on;
    
    subplot(2, 2, 2); 
    title('PSO Convergence'); xlabel('Iteration'); ylabel('Best Makespan');
    grid on;
    
    subplot(2, 2, 3); 
    title('Progress Comparison'); xlabel('Run'); ylabel('Best Result');
    grid on;
    
    subplot(2, 2, 4); 
    title('Task Distribution'); xlabel('Agent'); ylabel('Load');
    grid on;
    
    drawnow;
    fprintf('📺 Real-time monitoring initialized\n\n');
end

%% =================================================================
%% DATA LOADING & PREPARATION
%% =================================================================

fprintf('📊 Loading dataset...\n');

if USE_REAL_DATA
    data_path = fullfile(pwd, 'data', 'cloud_task_scheduling_with_dependencies.csv');
    
    if exist(data_path, 'file')
        fprintf('   Loading from: %s\n', data_path);
        fid = fopen(data_path, 'r');
        
        if fid ~= -1
            fgetl(fid); % Skip header
            
            tasks = struct();
            dependencies = struct(); % Structured dependencies like backend
            count = 0;
            
            while count < 1000 && ~feof(fid)
                line = fgetl(fid);
                if ischar(line)
                    parts = strsplit(line, ',');
                    if length(parts) >= 7
                        count = count + 1;
                        task_id = str2double(parts{1});
                        
                        % Task properties
                        tasks(count).id = task_id;
                        tasks(count).length = str2double(parts{2});
                        tasks(count).cpu_usage = str2double(parts{3});
                        tasks(count).ram_usage = str2double(parts{4});
                        tasks(count).priority = str2double(parts{5});
                        tasks(count).cost = str2double(parts{6});
                        
                        % Structured dependency handling
                        if length(parts) >= 7 && ~isempty(strtrim(parts{7}))
                            dep_str = strtrim(parts{7});
                            if ~isempty(dep_str)
                                dep_ids = str2double(strsplit(dep_str, ';'));
                                dependencies(count).task_id = task_id;
                                dependencies(count).depends_on = dep_ids;
                                dependencies(count).num_dependencies = length(dep_ids);
                            else
                                dependencies(count).task_id = task_id;
                                dependencies(count).depends_on = [];
                                dependencies(count).num_dependencies = 0;
                            end
                        else
                            dependencies(count).task_id = task_id;
                            dependencies(count).depends_on = [];
                            dependencies(count).num_dependencies = 0;
                        end
                    end
                end
            end
            fclose(fid);
            
            if count > NUM_TASKS
                indices = randperm(count, NUM_TASKS);
                tasks = tasks(indices);
                dependencies = dependencies(indices);
            end
            
            fprintf('   ✅ Loaded %d tasks from dataset\n', length(tasks));
        else
            error('Could not open dataset file');
        end
    else
        error('Dataset file not found: %s', data_path);
    end
else
    % Generate synthetic data with structured dependencies
    tasks = struct();
    dependencies = struct();
    
    for i = 1:NUM_TASKS
        tasks(i).id = i;
        tasks(i).length = 5 + rand() * 40;
        tasks(i).cpu_usage = 30 + rand() * 60;
        tasks(i).ram_usage = 1000 + rand() * 15000;
        tasks(i).priority = randi(3);
        tasks(i).cost = tasks(i).length * 10;
        
        % Create structured dependency relationships
        dependencies(i).task_id = i;
        if i > 1 && rand() < 0.3
            num_deps = randi(min(2, i-1));
            dep_candidates = 1:(i-1);
            selected_deps = dep_candidates(randperm(length(dep_candidates), num_deps));
            dependencies(i).depends_on = selected_deps;
            dependencies(i).num_dependencies = num_deps;
        else
            dependencies(i).depends_on = [];
            dependencies(i).num_dependencies = 0;
        end
    end
    
    fprintf('   ✅ Generated %d synthetic tasks with structured dependencies\n', NUM_TASKS);
end

% Create agents
agents = struct();
for i = 1:NUM_AGENTS
    agents(i).id = i;
    agents(i).capacity = 0.8 + rand() * 0.4;
end

fprintf('✅ Dataset ready: %d tasks, %d agents\n\n', length(tasks), length(agents));

% Print dependency statistics
dep_count = 0;
total_dep_links = 0;
for i = 1:length(dependencies)
    if dependencies(i).num_dependencies > 0
        dep_count = dep_count + 1;
        total_dep_links = total_dep_links + dependencies(i).num_dependencies;
    end
end
fprintf('📋 Dependencies: %d tasks have dependencies (%d total dependency links)\n', dep_count, total_dep_links);

% Show sample dependencies
if dep_count > 0
    fprintf('   Sample dependencies:\n');
    sample_count = 0;
    for i = 1:length(dependencies)
        if dependencies(i).num_dependencies > 0 && sample_count < 3
            fprintf('   Task %d depends on: [%s]\n', dependencies(i).task_id, ...
                    num2str(dependencies(i).depends_on));
            sample_count = sample_count + 1;
        end
    end
end
fprintf('\n');

%% =================================================================
%% HELPER FUNCTIONS
%% =================================================================

% Check if task dependencies are satisfied
function satisfied = are_dependencies_satisfied(task_idx, tasks, dependencies, schedule, agent_loads)
    satisfied = true;
    
    if task_idx < 1 || task_idx > length(dependencies)
        satisfied = false;
        return;
    end
    
    deps = dependencies(task_idx).depends_on;
    if isempty(deps) || dependencies(task_idx).num_dependencies == 0
        return;
    end
    
    for dep_id = deps
        dep_idx = find([tasks.id] == dep_id);
        if isempty(dep_idx)
            continue;
        end
        
        if schedule(dep_idx) == 0
            satisfied = false;
            return;
        end
        
        % Simple timing check - could be enhanced
        dep_agent = schedule(dep_idx);
        dep_finish_time = agent_loads(dep_agent);
    end
end

% Get tasks eligible for scheduling
function eligible = get_eligible_tasks(tasks, dependencies, schedule)
    eligible = [];
    for i = 1:length(tasks)
        if schedule(i) == 0
            if dependencies(i).num_dependencies == 0
                eligible = [eligible, i];
            else
                all_deps_scheduled = true;
                for dep_id = dependencies(i).depends_on
                    dep_idx = find([tasks.id] == dep_id);
                    if ~isempty(dep_idx) && schedule(dep_idx) == 0
                        all_deps_scheduled = false;
                        break;
                    end
                end
                if all_deps_scheduled
                    eligible = [eligible, i];
                end
            end
        end
    end
end

%% =================================================================
%% MAIN EXPERIMENT LOOP
%% =================================================================

fprintf('🚀 Starting experiments...\n');
fprintf('Progress: ');

% Initialize result storage
aco_results = zeros(1, NUM_RUNS);
pso_results = zeros(1, NUM_RUNS);
aco_times = zeros(1, NUM_RUNS);
pso_times = zeros(1, NUM_RUNS);

% Real-time tracking variables
if ENABLE_REALTIME_PLOTS
    aco_progress = cell(NUM_RUNS, 1);
    pso_progress = cell(NUM_RUNS, 1);
    run_best_aco = zeros(NUM_RUNS, 1);
    run_best_pso = zeros(NUM_RUNS, 1);
end

% Main experiment loop
for run = 1:NUM_RUNS
    fprintf('[%d/%d] ', run, NUM_RUNS);
    
    %% ACO Algorithm
    tic;
    num_tasks = length(tasks);
    num_agents = length(agents);
    
    pheromones = ones(num_tasks, num_agents);
    best_makespan = inf;
    best_schedule = [];
    
    if ENABLE_REALTIME_PLOTS
        aco_convergence = zeros(1, ACO_CONFIG.n_iterations);
    end
    
    for iter = 1:ACO_CONFIG.n_iterations
        for ant = 1:ACO_CONFIG.n_ants
            schedule = zeros(1, num_tasks);
            agent_loads = zeros(1, num_agents);
            
            % Schedule tasks with dependency constraints
            scheduled_count = 0;
            while scheduled_count < num_tasks
                eligible_tasks = get_eligible_tasks(tasks, dependencies, schedule);
                
                if isempty(eligible_tasks)
                    % Force scheduling if no eligible tasks
                    remaining = find(schedule == 0);
                    if ~isempty(remaining)
                        eligible_tasks = remaining;
                    else
                        break;
                    end
                end
                
                % Select task from eligible candidates
                task_idx = eligible_tasks(randi(length(eligible_tasks)));
                task = task_idx;
                
                % Calculate agent probabilities
                probs = zeros(1, num_agents);
                for agent = 1:num_agents
                    completion_time = agent_loads(agent) + tasks(task).length / agents(agent).capacity;
                    heuristic = 1.0 / max(completion_time, 0.1);
                    
                    % Priority bonus
                    priority_bonus = 1.0;
                    if isfield(tasks, 'priority') && ~isempty(tasks(task).priority)
                        priority_bonus = 1.0 + (tasks(task).priority - 1) * 0.1;
                    end
                    
                    probs(agent) = (pheromones(task, agent)^ACO_CONFIG.alpha) * (heuristic^ACO_CONFIG.beta) * priority_bonus;
                end
                
                probs = probs / sum(probs);
                cumprobs = cumsum(probs);
                agent = find(cumprobs >= rand(), 1);
                
                schedule(task) = agent;
                agent_loads(agent) = agent_loads(agent) + tasks(task).length / agents(agent).capacity;
                scheduled_count = scheduled_count + 1;
            end
            
            makespan = max(agent_loads);
            
            if makespan < best_makespan
                best_makespan = makespan;
                best_schedule = schedule;
            end
        end
        
        if ENABLE_REALTIME_PLOTS
            aco_convergence(iter) = best_makespan;
        end
        
        % Update pheromones
        pheromones = pheromones * (1 - ACO_CONFIG.evaporation_rate);
        for task = 1:num_tasks
            for agent = 1:num_agents
                improvement = 1.0 / max(best_makespan, 0.1);
                pheromones(task, agent) = pheromones(task, agent) + ACO_CONFIG.pheromone_deposit * improvement;
            end
        end
        
        % Real-time visualization update
        if ENABLE_REALTIME_PLOTS && (mod(iter, PLOT_UPDATE_INTERVAL) == 0 || iter == 1 || iter == ACO_CONFIG.n_iterations)
            set(0, 'CurrentFigure', fig_realtime);
            subplot(2, 2, 1);
            plot(1:iter, aco_convergence(1:iter), 'r-', 'LineWidth', 2);
            title(sprintf('ACO Run %d - Iter %d (Best: %.2f)', run, iter, best_makespan));
            xlabel('Iteration'); ylabel('Makespan'); grid on;
            drawnow; pause(0.01);
        end
    end
    
    aco_results(run) = best_makespan;
    aco_times(run) = toc * 1000;
    
    if ENABLE_REALTIME_PLOTS
        aco_progress{run} = aco_convergence;
        run_best_aco(run) = best_makespan;
        
        set(0, 'CurrentFigure', fig_realtime);
        subplot(2, 2, 3);
        plot(1:run, run_best_aco(1:run), 'ro-', 'LineWidth', 2, 'MarkerSize', 6);
        hold on;
        title('Progress Comparison'); xlabel('Run'); ylabel('Best Result'); 
        grid on; drawnow;
    end
    
% Calculate fitness with dependency penalty
function fitness = calculate_fitness_with_dependencies(position, tasks, agents, dependencies)
    agent_loads = zeros(1, length(agents));
    dependency_penalty = 0;
    
    for task = 1:length(tasks)
        agent = position(task);
        agent_loads(agent) = agent_loads(agent) + tasks(task).length / agents(agent).capacity;
        
        % Apply penalty for dependency violations
        if dependencies(task).num_dependencies > 0
            for dep_id = dependencies(task).depends_on
                dep_idx = find([tasks.id] == dep_id);
                if ~isempty(dep_idx)
                    dep_agent = position(dep_idx);
                    if dep_agent == agent
                        % Simplified penalty for same-agent dependencies
                        dependency_penalty = dependency_penalty + 0.1;
                    end
                end
            end
        end
    end
    
    fitness = max(agent_loads) + dependency_penalty;
end
    %% PSO Algorithm
    tic;
    
    particles = struct();
    for p = 1:PSO_CONFIG.n_particles
        particles(p).position = randi(num_agents, 1, num_tasks);
        particles(p).velocity = zeros(1, num_tasks);
        particles(p).best_position = particles(p).position;
        particles(p).best_fitness = inf;
    end
    
    global_best_position = particles(1).position;
    global_best_fitness = inf;
    
    if ENABLE_REALTIME_PLOTS
        pso_convergence = zeros(1, PSO_CONFIG.n_iterations);
    end
    
    for iter = 1:PSO_CONFIG.n_iterations
        for p = 1:PSO_CONFIG.n_particles
            % Calculate fitness with dependencies
            fitness = calculate_fitness_with_dependencies(particles(p).position, tasks, agents, dependencies);
            
            if fitness < particles(p).best_fitness
                particles(p).best_fitness = fitness;
                particles(p).best_position = particles(p).position;
            end
            
            if fitness < global_best_fitness
                global_best_fitness = fitness;
                global_best_position = particles(p).position;
            end
        end
        
        if ENABLE_REALTIME_PLOTS
            pso_convergence(iter) = global_best_fitness;
        end
        
        for p = 1:PSO_CONFIG.n_particles
            for d = 1:num_tasks
                r1 = rand(); r2 = rand();
                cognitive = PSO_CONFIG.c1 * r1 * (particles(p).best_position(d) - particles(p).position(d));
                social = PSO_CONFIG.c2 * r2 * (global_best_position(d) - particles(p).position(d));
                
                particles(p).velocity(d) = PSO_CONFIG.w * particles(p).velocity(d) + cognitive + social;
                particles(p).position(d) = particles(p).position(d) + particles(p).velocity(d);
                particles(p).position(d) = max(1, min(num_agents, round(particles(p).position(d))));
            end
        end
        
        if ENABLE_REALTIME_PLOTS && (mod(iter, PLOT_UPDATE_INTERVAL) == 0 || iter == 1 || iter == PSO_CONFIG.n_iterations)
            set(0, 'CurrentFigure', fig_realtime);
            subplot(2, 2, 2);
            plot(1:iter, pso_convergence(1:iter), 'b-', 'LineWidth', 2);
            title(sprintf('PSO Run %d - Iter %d (Best: %.2f)', run, iter, global_best_fitness));
            xlabel('Iteration'); ylabel('Makespan'); grid on;
            drawnow; pause(0.01);
        end
    end
    
    pso_results(run) = global_best_fitness;
    pso_times(run) = toc * 1000;
    
    if ENABLE_REALTIME_PLOTS
        pso_progress{run} = pso_convergence;
        run_best_pso(run) = global_best_fitness;
        
        set(0, 'CurrentFigure', fig_realtime);
        subplot(2, 2, 3);
        plot(1:run, run_best_pso(1:run), 'bo-', 'LineWidth', 2, 'MarkerSize', 6);
        if run == NUM_RUNS
            legend('ACO', 'PSO', 'Location', 'northeast');
        end
        title('Progress Comparison'); xlabel('Run'); ylabel('Best Result');
        grid on; hold off; drawnow;
    end
    
    % Task distribution plot  
    if ENABLE_TASK_DISTRIBUTION
        aco_loads = zeros(1, num_agents);
        pso_loads = zeros(1, num_agents);
        
        for task = 1:num_tasks
            if ~isempty(best_schedule) && best_schedule(task) > 0
                agent = best_schedule(task);
                aco_loads(agent) = aco_loads(agent) + tasks(task).length / agents(agent).capacity;
            end
        end
        
        for task = 1:num_tasks
            agent = global_best_position(task);
            pso_loads(agent) = pso_loads(agent) + tasks(task).length / agents(agent).capacity;
        end
        
        set(0, 'CurrentFigure', fig_realtime);
        subplot(2, 2, 4);
        bar_width = 0.35;
        agents_x = 1:num_agents;
        
        bar(agents_x - bar_width/2, aco_loads, bar_width, 'r');
        hold on;
        bar(agents_x + bar_width/2, pso_loads, bar_width, 'b');
        
        title(sprintf('Task Distribution - Run %d', run));
        xlabel('Agent ID'); ylabel('Load');
        legend('ACO', 'PSO', 'Location', 'northeast'); 
        grid on; hold off; drawnow;
    end
end

fprintf('\n✅ Experiments completed!\n\n');

%% =================================================================
%% RESULTS ANALYSIS
%% =================================================================

fprintf('📊 Statistical Analysis\n');
fprintf('─────────────────────\n');

aco_stats = struct();
aco_stats.mean = mean(aco_results);
aco_stats.std = std(aco_results);
aco_stats.min = min(aco_results);
aco_stats.max = max(aco_results);

pso_stats = struct();
pso_stats.mean = mean(pso_results);
pso_stats.std = std(pso_results);
pso_stats.min = min(pso_results);
pso_stats.max = max(pso_results);

fprintf('ACO Results: %.2f ± %.2f\n', aco_stats.mean, aco_stats.std);
fprintf('PSO Results: %.2f ± %.2f\n', pso_stats.mean, pso_stats.std);

if aco_stats.mean < pso_stats.mean
    improvement = ((pso_stats.mean - aco_stats.mean) / pso_stats.mean) * 100;
    fprintf('🏆 ACO outperforms PSO by %.1f%%\n', improvement);
else
    improvement = ((aco_stats.mean - pso_stats.mean) / aco_stats.mean) * 100;
    fprintf('🏆 PSO outperforms ACO by %.1f%%\n', improvement);
end

fprintf('\n🎉 EXPERIMENT COMPLETED!\n');
fprintf('═════════════════════════\n');

if KEEP_PLOTS_OPEN && ENABLE_REALTIME_PLOTS
    fprintf('\n📊 PLOTS KEPT OPEN FOR MANUAL INSPECTION\n');
    fprintf('────────────────────────────────────────────\n');
    fprintf('🖼️  Real-time monitoring window: OPEN\n');
    
    fprintf('\n💡 Manual Inspection Guide:\n');
    fprintf('   🔍 Zoom in/out on charts for detailed analysis\n');
    fprintf('   📈 Check convergence patterns and stability\n');
    fprintf('   ⚖️  Compare ACO vs PSO performance trends\n');
    fprintf('   📊 Analyze task distribution balance per run\n');
    fprintf('   � All plots are interactive and resizable\n');
    
    fprintf('\n🎯 Plot Windows Summary:\n');
    fprintf('   • Main real-time monitoring: 4 subplots\n');
    
    % Set final plot title (without bringing to front)
    if exist('fig_realtime', 'var')
        set(fig_realtime, 'Name', '🎯 Main Real-time Monitoring - Close When Done');
    end
    
    fprintf('\n⏳ PLOTS WILL STAY OPEN UNTIL YOU CLOSE THEM MANUALLY\n');
    fprintf('   ❌ Close individual windows when finished inspecting\n');
    fprintf('   🔄 Or press Ctrl+C to exit script and close all\n');
    
    fprintf('\n🔍 Ready for detailed manual inspection...\n');
    fprintf('══════════════════════════════════════════════════════════════\n\n');
    
    % Force plots to stay open by waiting for user input
    fprintf('📌 PLOTS ARE NOW OPEN FOR INSPECTION\n');
    fprintf('   Press Enter to close plots and exit, or close windows manually: ');
    
    % Keep script running until user decides to exit
    input('');
    
    fprintf('\n👋 Closing experiment...\n');
else
    fprintf('\n🎉 EXPERIMENT COMPLETED!\n');
    fprintf('═════════════════════════\n\n');
end