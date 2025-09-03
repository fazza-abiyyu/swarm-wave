# MATLAB/Octave Implementation

Implementasi swarm intelligence algorithms (ACO & PSO) untuk multi-agent task scheduling dengan structured dependencies.

## ✨ Features

- 🐜 **ACO Algorithm** - Ant Colony Optimization dengan dependency handling
- 🦅 **PSO Algorithm** - Particle Swarm Optimization dengan structured dependencies  
- 📊 **Real-time Visualization** - Live plotting dengan streaming updates
- 🔗 **Dependency Support** - Structured task dependencies seperti backend
- 🎯 **Manual Plot Control** - Plots tetap terbuka untuk inspeksi detail
- 📈 **Comparative Analysis** - ACO vs PSO performance comparison

## 🚀 Quick Start

### 1. Install GNU Octave (Free)
```bash
# macOS
brew install octave

# Ubuntu/Debian
sudo apt install octave

# Windows - Download from https://octave.org/download
```

### 2. Run Main Experiment
```bash
cd matlab/experiments
octave comprehensive_experiment.m
```

## 📁 Project Structure

```
matlab/
├── algorithms/                    # 🔬 Core Algorithms
│   ├── ACO_MultiAgent_Scheduler.m  # ACO implementation
│   └── PSO_MultiAgent_Scheduler.m  # PSO implementation
├── experiments/                   # Main Experiments
│   ├── comprehensive_experiment.m  # Primary experiment
│   ├── data/                      # Dataset storage
│   │   ├── cloud_task_scheduling_dataset.csv
│   │   └── cloud_task_scheduling_with_dependencies.csv
│   ├── plots/                     # Generated visualizations
│   └── results/                   # Experiment outputs
├── utils/                         # 🛠️ Utilities
│   ├── load_csv_data_octave.m     # CSV data loader
│   └── setup_octave.m             # Environment setup
└── docs/                          # 📚 Documentation
```
## 🔬 Algorithms

### 🐜 ACO (Ant Colony Optimization)
- **Multi-agent scheduling** dengan pheromone trails
- **Dependency-aware** task scheduling 
- **Load balancing** dengan priority support
- **Real-time convergence** visualization

### � PSO (Particle Swarm Optimization)
- **Particle swarm** untuk scheduling optimization
- **Structured dependencies** handling
- **Global & personal best** tracking dengan penalty system
- **Velocity & position** updates dengan constraints

## 🎯 Usage Examples

### Basic Experiment Run
```matlab
cd matlab/experiments
octave comprehensive_experiment.m
```

### Configuration Options
```matlab
% Edit comprehensive_experiment.m
USE_REAL_DATA = true;        % Use dataset or synthetic data
NUM_TASKS = 100;             % Number of tasks
NUM_AGENTS = 5;              # Number of agents
NUM_RUNS = 3;                % Experiment repetitions
ENABLE_REALTIME_PLOTS = true; % Live visualization
KEEP_PLOTS_OPEN = true;      % Manual plot control
```

## 📊 Output Features

- **Real-time Charts** - ACO & PSO convergence plots
- **Progress Tracking** - Multi-run comparison
- **Task Distribution** - Agent workload visualization  
- **Statistical Analysis** - Mean, std, performance comparison
- **Manual Inspection** - Plots stay open for detailed analysis

## 🔧 Requirements

- **GNU Octave 4.0+** atau **MATLAB R2016b+**
- **Dataset**: `experiments/data/cloud_task_scheduling_with_dependencies.csv`
- **Memory**: ~500MB for 100 tasks experiment

## 📈 Performance Benchmarks

**Latest Results (100 tasks, 5 agents, 3 runs):**
- **ACO**: 117.85 ± 1.13ms 🏆 
- **PSO**: 118.79 ± 1.67ms
- **ACO Advantage**: 0.8% better performance
- **Dependencies**: 35+ tasks with 50+ dependency links processed

**System Performance:**
- **Execution Time**: ~2-3 minutes for full experiment
- **Memory Usage**: ~200MB peak for 100 tasks
- **Real-time Updates**: Every 2 iterations
- **Scalability**: Tested up to 1000+ tasks

## 🔧 Troubleshooting

### Common Issues
```matlab
% Error: Dataset not found
% Solution: Check data file path
ls experiments/data/

% Error: Figure issues  
% Solution: Ensure display is available
export DISPLAY=:0  # Linux

% Error: Memory issues
% Solution: Reduce task count
NUM_TASKS = 50;  % Instead of 100
```

## 🎯 Version Info

- **Current Version**: 4.0 - Clean & Optimized
- **Compatibility**: GNU Octave 4.0+ / MATLAB R2016b+
- **Last Updated**: September 2025
- **Status**: Production Ready

This implementation is fully compatible with MATLAB syntax and runs optimally on GNU Octave (free).
