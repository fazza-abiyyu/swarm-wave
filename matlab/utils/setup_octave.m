% GNU Octave Setup Script for Swarm Algorithms
% Run this script to set up the Octave environment

fprintf('=== GNU Octave Swarm Algorithms Setup ===\n');

%% Check Octave version
try
    octave_version = version();
    fprintf('GNU Octave Version: %s\n', octave_version);
catch
    fprintf('GNU Octave Version: Unknown\n');
end

%% Add current directory to path
current_dir = pwd;
fprintf('Adding directory to Octave path: %s\n', current_dir);
addpath(current_dir);

%% Check required packages
fprintf('\nChecking Octave packages...\n');

% Check if we have basic functionality
try
    % Test random number generation
    rand('seed', 42);
    test_matrix = rand(10, 10);
    fprintf('  ✓ Random number generation: Working\n');
    
    % Test struct arrays
    test_struct = struct('id', {1, 2}, 'value', {'a', 'b'});
    if length(test_struct) == 2
        fprintf('  ✓ Structure arrays: Working\n');
    end
    
    % Test basic plotting (if display available)
    try
        figure('visible', 'off');
        plot(1:10, rand(1, 10));
        close;
        fprintf('  ✓ Basic plotting: Working\n');
    catch
        fprintf('  ⚠ Plotting: Limited (no display)\n');
    end
    
catch ME
    fprintf('  ✗ Error in basic functionality test: %s\n', ME.message);
end

%% Create directories for results
if ~exist('results', 'dir')
    mkdir('results');
    fprintf('\nCreated results directory\n');
end

if ~exist('plots', 'dir')
    mkdir('plots');
    fprintf('Created plots directory\n');
end

%% Run quick validation
fprintf('\nRunning quick validation test...\n');

try
    % Create minimal test case
    tasks = struct();
    tasks(1) = struct('id', 1, 'length', 5, 'dependencies', '');
    tasks(2) = struct('id', 2, 'length', 3, 'dependencies', '');
    
    agents = struct();
    agents(1) = struct('id', 'TestAgent');
    
    cost_function = @(schedule, makespan) makespan;
    heuristic_function = @(task) 1.0 / task.length;
    
    % Test ACO creation
    fprintf('  Testing ACO scheduler creation...\n');
    aco = ACO_MultiAgent_Scheduler(tasks, cost_function, heuristic_function, ...
        'agents', agents, 'n_ants', 2, 'n_iterations', 2);
    fprintf('  ✓ ACO scheduler creation: Working\n');
    
    % Test PSO creation
    fprintf('  Testing PSO scheduler creation...\n');
    pso = PSO_MultiAgent_Scheduler(tasks, agents, cost_function, ...
        'n_particles', 2, 'n_iterations', 2);
    fprintf('  ✓ PSO scheduler creation: Working\n');
    
    % Quick run test
    fprintf('  Running quick algorithm test...\n');
    result = aco.run();
    if ~isempty(result.schedule)
        fprintf('  ✓ Algorithm execution: Working\n');
        fprintf('    Test makespan: %.2f\n', result.makespan);
    end
    
catch ME
    fprintf('  ✗ Validation test failed: %s\n', ME.message);
    fprintf('    Error occurred at line: %s\n', ME.stack(1).name);
    
    % Try to give more specific guidance
    if strfind(ME.message, 'containers.Map')
        fprintf('    Note: containers.Map might not be available in Octave\n');
        fprintf('    Consider using cell arrays or structs instead\n');
    elseif strfind(ME.message, 'handle')
        fprintf('    Note: Handle classes might work differently in Octave\n');
        fprintf('    Consider using regular classes or function-based approach\n');
    end
end

%% Check dataset availability
fprintf('\nChecking dataset availability...\n');

datasets = {
    '../backend/data/cloud_task_scheduling_dataset.csv', 'Basic cloud scheduling dataset';
    '../backend/data/cloud_task_scheduling_with_dependencies.csv', 'Cloud scheduling with dependencies'
};

for i = 1:size(datasets, 1)
    if exist(datasets{i, 1}, 'file')
        fprintf('  ✓ %s: Available\n', datasets{i, 2});
    else
        fprintf('  ⚠ %s: Not found\n', datasets{i, 2});
    end
end

%% Display next steps
fprintf('\n=== Setup Status ===\n');
fprintf('Your GNU Octave environment setup is complete!\n\n');

fprintf('Important Notes for Octave:\n');
fprintf('• GNU Octave is mostly compatible with MATLAB syntax\n');
fprintf('• Some advanced features (like containers.Map) may need alternatives\n');
fprintf('• Handle classes work differently - may need function-based approach\n');
fprintf('• Most mathematical operations should work identically\n\n');

fprintf('Next steps:\n');
fprintf('1. Try running the test script:\n');
fprintf('   octave --eval "run(''test_implementation_octave'')" \n\n');

fprintf('2. Test with simple example:\n');
fprintf('   octave --eval "run(''example_usage_octave'')" \n\n');

fprintf('3. For interactive use:\n');
fprintf('   octave\n');
fprintf('   >> addpath(''%s'')\n', current_dir);
fprintf('   >> help ACO_MultiAgent_Scheduler\n\n');

fprintf('Available files:\n');
files = dir('*.m');
for i = 1:length(files)
    fprintf('  • %s\n', files(i).name);
end

fprintf('\nFor help with any function in Octave, use:\n');
fprintf('   >> help function_name\n');
fprintf('   >> doc function_name\n\n');

fprintf('Happy optimizing with GNU Octave! 🐜🐝\n');

%% Save path if possible
try
    savepath;
    fprintf('\nPath configuration saved.\n');
catch
    fprintf('\nNote: Could not save path permanently.\n');
    fprintf('You may need to run addpath(''%s'') in future sessions.\n', current_dir);
end
