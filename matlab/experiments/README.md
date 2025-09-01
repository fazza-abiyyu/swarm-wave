# MATLAB Experiments - Swarm Intelligence Lab

## Overview
Organized experiment suite for comparing ACO and PSO algorithms in cloud task scheduling. All experiments are self-contained with built-in algorithms and no external dependencies.

## 🚀 Quick Start

**Run the Interactive Launcher:**
```matlab
run_experiments
```

This launches an interactive menu with all available experiment types.

## 📁 Project Structure

```
experiments/
├── run_experiments.m          # 🎯 Interactive launcher (START HERE)
├── quick_experiment.m         # 🚀 Fast analysis (20 tasks, 3 runs)
├── comprehensive_experiment.m # 🔬 Complete analysis (30 tasks, 5 runs)
├── parameter_tuning.m         # ⚙️  Parameter optimization
├── README.md                  # 📖 This file
├── EXPERIMENT_SYSTEM_SUMMARY.md # 📋 Detailed system documentation
├── data/                      # 📊 Dataset folder
├── plots/                     # 📈 Generated visualizations
├── results/                   # 📄 Analysis reports
└── archive/                   # 🗂️  Previous versions
```

## 🧪 Available Experiments

### 1. Quick Experiment (`quick_experiment.m`)
- **Purpose:** Fast comparison for initial testing
- **Configuration:** 20 tasks, 3 agents, 3 runs
- **Duration:** ~2 minutes
- **Output:** Basic comparison plots and summary

### 2. Comprehensive Analysis (`comprehensive_experiment.m`)
- **Purpose:** Complete research-grade analysis
- **Configuration:** 30 tasks, 4 agents, 5 runs
- **Duration:** 5-8 minutes  
- **Output:** 4 detailed visualizations in organized subfolders
- **Features:** Statistical analysis, performance trends, distribution comparison

### 3. Parameter Tuning (`parameter_tuning.m`)
- **Purpose:** Find optimal algorithm parameters
- **Configuration:** Grid search across multiple parameter combinations
- **Duration:** 10-15 minutes
- **Output:** Heatmaps, sensitivity analysis, optimal configurations

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
