function tasks = load_csv_data_octave(filename)
% LOAD_CSV_DATA_OCTAVE Load task data from CSV file (Octave compatible)
% 
% Usage:
%   tasks = load_csv_data_octave('data.csv')
%
% Input:
%   filename - Path to CSV file containing task data
%
% Output:
%   tasks - Structure array with task information

    % Check if file exists
    if ~exist(filename, 'file')
        error('File %s not found', filename);
    end
    
    % Read CSV file using built-in functions
    try
        % Try to read with dlmread first (for numeric data)
        fid = fopen(filename, 'r');
        if fid == -1
            error('Cannot open file %s', filename);
        end
        
        % Read header line
        header_line = fgetl(fid);
        col_names = strsplit(header_line, ',');
        
        % Clean up column names (remove quotes and spaces)
        for i = 1:length(col_names)
            col_names{i} = strtrim(strrep(col_names{i}, '"', ''));
        end
        
        fprintf('Available columns: %s\n', strjoin(col_names, ', '));
        
        % Read data lines
        data_lines = {};
        line_count = 0;
        while ~feof(fid)
            line = fgetl(fid);
            if ischar(line) && ~isempty(line)
                line_count = line_count + 1;
                data_lines{line_count} = line;
            end
        end
        fclose(fid);
        
        fprintf('Read %d data lines\n', line_count);
        
        % Initialize tasks structure
        tasks = struct();
        
        % Determine column indices
        id_col_idx = find(strcmp(col_names, 'Task_ID') | strcmp(col_names, 'id'));
        duration_col_idx = find(strcmp(col_names, 'Duration') | ...
                               strcmp(col_names, 'Execution_Time (s)') | ...
                               strcmp(col_names, 'length'));
        deps_col_idx = find(strcmp(col_names, 'Dependencies') | ...
                           strcmp(col_names, 'dependencies'));
        priority_col_idx = find(strcmp(col_names, 'Priority'));
        
        if isempty(id_col_idx)
            error('No task ID column found. Expected "Task_ID" or "id"');
        end
        
        % Process each data line
        for i = 1:line_count
            line = data_lines{i};
            % Split by comma, but handle quoted strings
            values = parse_csv_line(line);
            
            if length(values) >= length(col_names)
                % Task ID
                tasks(i).id = str2num(values{id_col_idx(1)});
                if isempty(tasks(i).id)
                    tasks(i).id = i; % fallback
                end
                
                % Duration/length
                if ~isempty(duration_col_idx)
                    tasks(i).length = str2num(values{duration_col_idx(1)});
                    if isempty(tasks(i).length)
                        tasks(i).length = 1; % default
                    end
                else
                    tasks(i).length = 1; % default
                end
                
                % Dependencies
                if ~isempty(deps_col_idx)
                    dep_str = values{deps_col_idx(1)};
                    dep_str = strtrim(strrep(dep_str, '"', ''));
                    if ~isempty(dep_str) && ~strcmpi(dep_str, 'nan')
                        tasks(i).dependencies = dep_str;
                    else
                        tasks(i).dependencies = '';
                    end
                else
                    tasks(i).dependencies = '';
                end
                
                % Priority (optional)
                if ~isempty(priority_col_idx) && length(values) >= priority_col_idx(1)
                    tasks(i).priority = str2num(values{priority_col_idx(1)});
                end
            end
        end
        
    catch ME
        error('Error reading CSV file: %s', ME.message);
    end
    
    fprintf('Loaded %d tasks from %s\n', length(tasks), filename);
    
    % Show sample task
    if length(tasks) > 0
        fprintf('Sample task: ID=%d, Length=%.2f, Dependencies="%s"\n', ...
                tasks(1).id, tasks(1).length, tasks(1).dependencies);
    end
end

function values = parse_csv_line(line)
    % Simple CSV parser that handles quotes
    values = {};
    current_value = '';
    in_quotes = false;
    
    for i = 1:length(line)
        char = line(i);
        
        if char == '"'
            in_quotes = ~in_quotes;
        elseif char == ',' && ~in_quotes
            values{end+1} = strtrim(current_value);
            current_value = '';
        else
            current_value = [current_value, char];
        end
    end
    
    % Add last value
    if ~isempty(current_value) || ~isempty(values)
        values{end+1} = strtrim(current_value);
    end
end
