# MATLAB Experiments - Swarm Intelligence

## 🎯 Overview
Production-ready experiment suite for ACO vs PSO comparison in multi-agent task scheduling with structured dependencies and real-time visualization.

## 🚀 Quick Start

**Run Main Experiment:**
```bash
cd matlab/experiments
octave comprehensive_experiment.m
```

## 📁 Clean Project Structure

```
experiments/
├── comprehensive_experiment.m  # ⭐ Primary experiment (START HERE)
├── data/                      # � Datasets
│   ├── cloud_task_scheduling_dataset.csv
│   └── cloud_task_scheduling_with_dependencies.csv
├── plots/                     # 📈 Generated visualizations (git ignored)
├── results/                   # 📄 Experiment outputs (git ignored)
└── README.md                  # � This file
```

## 🧪 Main Experiment Features

### comprehensive_experiment.m
- **Purpose**: Complete research-grade ACO vs PSO analysis
- **Configuration**: 100 tasks, 5 agents, 3 runs  
- **Duration**: ~3-5 minutes
- **Key Features**:
  - 📊 Real-time streaming visualization
  - 🔗 Structured dependency handling (like backend)
  - 🎯 Manual plot control (stays open for inspection)
  - 📈 4-subplot monitoring (ACO/PSO convergence, progress, distribution)
## ⚙️ Configuration Options

```matlab
% Main settings in comprehensive_experiment.m
USE_REAL_DATA = true;             % Use dataset vs synthetic
NUM_TASKS = 100;                  % Task count
NUM_AGENTS = 5;                   # Agent count  
NUM_RUNS = 3;                     % Experiment runs

% Visualization controls
ENABLE_REALTIME_PLOTS = true;     % Live plotting
ENABLE_TASK_DISTRIBUTION = true;  % Agent workload plots
PLOT_UPDATE_INTERVAL = 2;         % Update every N iterations
KEEP_PLOTS_OPEN = true;           % Manual plot control
```

## 📊 Expected Output

### Console Output
```
🧪 Comprehensive Swarm Intelligence Experiment
═══════════════════════════════════════════════
📋 Dependencies: 35 tasks have dependencies (51 total links)
🚀 Starting experiments...
Progress: [1/3] [2/3] [3/3]
✅ Experiments completed!

📊 Statistical Analysis
ACO Results: 117.85 ± 1.13
PSO Results: 118.79 ± 1.67  
🏆 ACO outperforms PSO by 0.8%
```

### Visualization
- **Real-time convergence plots** for ACO & PSO
- **Multi-run progress comparison**
- **Agent task distribution analysis**  
- **Manual plot control** - stays open for inspection

## 🎯 Latest Performance

**Benchmark Results (100 tasks, 5 agents):**
- **ACO**: 117.85 ± 1.13ms 🏆
- **PSO**: 118.79 ± 1.67ms  
- **Dependencies**: 35 tasks with 51 links processed
- **Execution**: ~3 minutes total
- **Memory**: ~200MB peak

Publication-ready results with comprehensive analysis! 🎉

## 🔧 Features

### Self-Contained Design
- ✅ No external dependencies
- ✅ Built-in ACO and PSO algorithms
- ✅ Integrated data generation
- ✅ All functions included in experiment files

### Organized Output Structure
- 📊 **Plots:** Timestamped subfolders for each experiment run
- 📄 **Results:** Detailed text reports with raw data
- 📈 **Visualizations:** Multiple chart types (comparison, trends, distributions)

### Clean Code Structure
- 🧹 Modular configuration sections
- 📝 Clear documentation and comments
- 🏗️ Organized helper functions
- 🎨 Consistent formatting and style

## 📊 Output Examples

### Quick Experiment
```
plots/QuickComparison_2025-09-01_143022.png
results/QuickResults_2025-09-01_143022.txt
```

### Comprehensive Analysis
```
plots/ComprehensiveAnalysis_2025-09-01_143022/
├── Performance_Comparison.png
├── Performance_Trends.png
├── Statistical_Summary.png
└── Distribution_Comparison.png
results/ComprehensiveResults_2025-09-01_143022.txt
```

### Parameter Tuning
```
plots/ParameterHeatmaps_2025-09-01_143022.png
plots/ParameterAnalysis_2025-09-01_143022.png
plots/SensitivityAnalysis_2025-09-01_143022.png
results/ParameterTuningResults_2025-09-01_143022.txt
```

## ⚡ Performance Specifications

| Experiment | Tasks | Agents | Runs | Duration | Plots | Analysis Depth |
|------------|-------|---------|------|----------|-------|----------------|
| Quick | 20 | 3 | 3 | ~2 min | 1 | Basic |
| Comprehensive | 30 | 4 | 5 | 5-8 min | 4 | Advanced |
| Parameter Tuning | 25 | 4 | 3/config | 10-15 min | 3 | Expert |

## 🎯 Usage Instructions

### Option 1: Interactive Launcher (Recommended)
```matlab
run_experiments  % Choose from menu
```

### Option 2: Direct Execution
```matlab
quick_experiment          % For quick results
comprehensive_experiment  % For detailed analysis  
parameter_tuning         % For parameter optimization
```

## 📈 Algorithm Configurations

### ACO (Ant Colony Optimization)
- **Ants:** 8
- **Iterations:** 15-20
- **Alpha (α):** Pheromone importance
- **Beta (β):** Heuristic importance
- **Rho (ρ):** Evaporation rate

### PSO (Particle Swarm Optimization)
- **Particles:** 10
- **Iterations:** 15-20
- **w:** Inertia weight
- **c1:** Cognitive coefficient
- **c2:** Social coefficient

## 🛠️ Customization

### Modifying Parameters
Edit the configuration section at the top of each experiment file:

```matlab
%% EXPERIMENT CONFIGURATION
NUM_TASKS = 30;      % Adjust dataset size
NUM_AGENTS = 4;      # Modify cloud nodes
NUM_RUNS = 5;        # Change statistical runs
```

### Algorithm Parameters
Modify algorithm configurations in the respective structs:

```matlab
ACO_CONFIG = struct(...
    'n_ants', 8, ...
    'alpha', 1.0, ...   % Tune these values
    'beta', 2.0, ...
    % ... other parameters
);
```

## 📋 System Requirements

- **MATLAB/Octave:** Any recent version
- **Memory:** ~100MB for comprehensive experiments
- **Storage:** ~50MB for full experiment outputs
- **Dependencies:** None (completely self-contained)

## 🔍 Troubleshooting

### Common Issues
1. **"Function not found" errors:** Ensure you're running from the experiments/ directory
2. **Plot display issues:** Check if graphics are enabled in your MATLAB/Octave environment
3. **Memory issues:** Reduce NUM_TASKS or NUM_RUNS for large experiments

### Performance Optimization
- Use `quick_experiment` for testing and development
- Run `comprehensive_experiment` for publication-ready results
- Use `parameter_tuning` for algorithm optimization research

## 📚 Additional Documentation

- **EXPERIMENT_SYSTEM_SUMMARY.md:** Detailed technical documentation
- **Archive folder:** Contains previous versions for reference
- **Generated results:** Check plots/ and results/ folders for experiment outputs

## 🎯 Research Applications

Perfect for:
- Cloud computing research
- Swarm intelligence studies
- Algorithm comparison analysis
- Parameter optimization studies
- Academic paper generation

---

**Version:** 2.0 (Cleaned & Organized)  
**Last Updated:** September 2025  
**Compatibility:** MATLAB R2016b+ / GNU Octave 4.0+
