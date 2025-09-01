# 🐜 Swarm Lab - Intelligent Cloud Task Scheduling System

[![Tests](https://img.shields.io/badge/tests-17%2F17%20passing-brightgreen?style=for-the-badge&logo=checkmarx)](./backend/tests)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen?style=for-the-badge&logo=codecov)](./backend/tests)
[![Backend](https://img.shields.io/badge/backend-Flask%20API-blue?style=for-the-badge&logo=flask)](./backend)
[![Frontend](https://img.shields.io/badge/frontend-Nuxt%204-green?style=for-the-badge&logo=nuxt.js)](./frontend)
[![Algorithms](https://img.shields.io/badge/algorithms-ACO%20%7C%20PSO-orange?style=for-the-badge&logo=algorithm)](./matlab/experiments)

A comprehensive web application for **Cloud Task Scheduling** using **Swarm Intelligence algorithms** - specifically **Ant Colony Optimization (ACO)** and **Particle Swarm Optimization (PSO)**. Built with Nuxt 4 (frontend) and Flask (backend).

## 🚀 Project Overview

Swarm Lab is an intelligent task scheduling platform that leverages bio-inspired optimization algorithms to efficiently allocate computational tasks across cloud resources. The system provides an intuitive web interface for:

- 📊 **Interactive simulation** of ACO and PSO algorithms
- 📈 **Real-time visualization** of optimization progress 
- 🔧 **Parameter tuning** for algorithm customization
- 📋 **Task management** with CSV data import
- 📉 **Performance metrics** and comparative analysis

## 🎯 Key Features

- **🐜 Ant Colony Optimization (ACO)**: Bio-inspired algorithm mimicking ant foraging behavior
- **🐦 Particle Swarm Optimization (PSO)**: Population-based optimization inspired by bird flocking
- **📊 Interactive Dashboard**: Real-time monitoring and visualization
- **🔄 Streaming Results**: Live updates during algorithm execution
- **📱 Responsive Design**: Works seamlessly across all devices
- **🐳 Docker Support**: Easy deployment with containerization
- **🧪 Comprehensive Testing**: 100% test coverage with 17 unit tests
- **📈 Performance Analysis**: Benchmarking and algorithm comparison

## 🏗️ Architecture

This project follows a modern microservices architecture with clear separation between frontend and backend:

```
swarm-lab/
├── backend/                    # Flask API Server
│   ├── models/                 # Algorithm Implementations
│   │   ├── aco.py             # Ant Colony Optimization
│   │   └── pso.py             # Particle Swarm Optimization
│   ├── tests/                 # Comprehensive Unit Tests
│   │   ├── test_app.py        # Flask API Tests (5 tests)
│   │   ├── test_aco.py        # ACO Algorithm Tests (5 tests)
│   │   ├── test_pso.py        # PSO Algorithm Tests (7 tests)
│   │   ├── run_tests.py       # Test Runner (100% success rate)
│   │   └── README.md          # Testing Documentation
│   ├── templates/             # Flask Templates
│   ├── app.py                 # Main Flask Application
│   ├── requirements.txt       # Python Dependencies
│   ├── Makefile              # Test Commands
│   └── cloud_task_scheduling_dataset.csv
├── frontend/                   # Nuxt 4 Web Application
│   ├── app/
│   │   ├── components/
│   │   │   ├── SimulationPage.vue  # Main Simulation Interface
│   │   │   └── DynamicTable.vue    # Data Visualization
│   │   ├── pages/
│   │   │   ├── index.vue           # Landing Page
│   │   │   ├── about.vue           # About Page
│   │   │   └── dashboard/          # Dashboard Views
│   │   └── composables/
│   │       └── useAiChatStream.ts  # Streaming API Client
│   ├── server/
│   │   └── api/               # Server API Routes
│   │       ├── chat-stream.post.ts
│   │       └── test.get.ts
│   ├── assets/css/            # Global Styles
│   ├── public/                # Static Assets
│   ├── nuxt.config.ts         # Nuxt Configuration
│   └── package.json           # Node.js Dependencies
├── matlab/                     # MATLAB/Octave Experiments
│   ├── experiments/
│   │   ├── comprehensive_experiment.m  # Main Experiment (v4.0)
│   │   ├── data/              # Clean Dataset Files
│   │   ├── plots/             # Auto-generated Visualizations
│   │   ├── results/           # Experiment Results & Logs
│   │   └── .gitkeep          # Directory Preservation
│   └── utils/                 # Experiment Utilities
├── docker-compose.yml         # Docker Orchestration
└── example.env               # Environment Variables Template
```

## 🛠️ Technology Stack

### Frontend (Nuxt 4)
- **Framework**: Nuxt 4 with Vue 3 and TypeScript
- **Styling**: Tailwind CSS with custom components
- **Visualization**: Chart.js for real-time plotting
- **HTTP Client**: Native Fetch API with streaming support
- **Icons**: Custom SVG icons
- **State Management**: Vue 3 Composition API

### Backend (Flask)
- **Framework**: Flask with CORS support
- **Algorithms**: Custom ACO/PSO implementations
- **Data Processing**: Pandas and NumPy
- **Visualization**: Matplotlib and Plotly
- **Performance**: Progress tracking with tqdm
- **Deployment**: Gunicorn WSGI server

### Algorithms Implemented

#### 🐜 Ant Colony Optimization (ACO)
- **Multi-agent pheromone-based optimization**
- **Parameters**: Ants count, Alpha (pheromone influence), Beta (heuristic influence), Evaporation rate
- **Application**: Efficient task-to-resource mapping

#### 🐦 Particle Swarm Optimization (PSO) 
- **Swarm intelligence optimization**
- **Parameters**: Particles count, Inertia weight (w), Acceleration coefficients (c1, c2)
- **Application**: Global optimization of resource allocation

## 📊 Algorithm Parameters

### ACO Parameters
| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `n_ants` | Number of ants in colony | 10 | 5-50 |
| `alpha` | Pheromone influence | 1.0 | 0.1-5.0 |
| `beta` | Heuristic influence | 2.0 | 0.1-5.0 |
| `evaporation_rate` | Pheromone decay | 0.1 | 0.01-0.9 |
| `pheromone_deposit` | Pheromone strength | 1.0 | 0.1-10.0 |

### PSO Parameters
| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `n_particles` | Number of particles | 10 | 5-50 |
| `w` | Inertia weight | 0.7 | 0.1-1.0 |
| `c1` | Cognitive coefficient | 1.4 | 0.1-4.0 |
| `c2` | Social coefficient | 1.4 | 0.1-4.0 |

## 🧪 Testing & Quality Assurance

### Backend Unit Tests
Comprehensive unit test suite with **100% success rate** for backend components:

```bash
# Navigate to backend directory
cd backend

# Run all tests
make test

# Run specific test modules
make test-app          # Flask API tests
make test-aco          # ACO algorithm tests  
make test-pso          # PSO algorithm tests
make test-utils        # Utility function tests

# Advanced testing options
make test-verbose      # Detailed output
make test-interactive  # Interactive menu
make test-coverage     # Coverage analysis
```

#### Test Coverage
- **17 comprehensive tests** covering all major components
- **Flask API endpoints**: Health checks, error handling, parameter validation
- **ACO Algorithm**: Initialization, dependency handling, solution construction
- **PSO Algorithm**: Swarm initialization, position conversion, sequence generation
- **Utility Functions**: Data formatting, type conversion, agent generation

#### Test Structure
```
backend/tests/
├── test_app.py          # Flask application tests (5 tests)
├── test_aco.py          # ACO algorithm tests (5 tests)
├── test_pso.py          # PSO algorithm tests (7 tests)
├── test_utilities.py    # Utility function tests
├── run_tests.py         # Comprehensive test runner
├── interactive_runner.py # Interactive test menu
└── README.md           # Testing documentation
```

### MATLAB/Octave Experiments
Clean, well-documented experimental framework for algorithm validation:

```bash
# Navigate to MATLAB experiments
cd matlab/experiments

# Run comprehensive analysis
octave comprehensive_experiment.m
```

#### Experiment Features
- **Real-time visualization** with streaming updates
- **Dependency-aware scheduling** with task relationships  
- **Non-intrusive plotting** (windows don't auto-focus)
- **Professional result logging** with timestamp organization
- **Load balancing metrics** and performance analysis

## 🚦 Getting Started

### Prerequisites

- **Node.js** 18+ and npm/yarn
- **Python** 3.9+
- **Docker** (optional, for containerized deployment)

### 🐳 Quick Start with Docker (Recommended)

The fastest way to get started:

```bash
# Clone the repository
git clone https://github.com/fazza-abiyyu/swarm-lab.git
cd swarm-lab

# Copy example environment file
cp example.env .env

# Edit .env file and add your GEMINI_API_KEY
# GEMINI_API_KEY=your_actual_api_key_here

# Build and run with Docker Compose
docker compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:5001
```

### 🧪 Quick Test Verification

Verify everything is working correctly:

```bash
# Test backend functionality
cd backend
make test                    # Should show: 17/17 tests passing (100%)

# Test MATLAB experiments  
cd ../matlab/experiments
octave comprehensive_experiment.m  # Should generate plots and results
```

Expected output:
- ✅ **Backend**: `Tests run: 17, Failures: 0, Errors: 0, Success rate: 100.0%`
- ✅ **MATLAB**: Performance comparison showing ACO vs PSO results with visualization

### 🔧 Manual Setup

#### Environment Setup (Required)

1. **Set up environment variables:**
   ```bash
   # Copy environment template
   cp example.env .env
   
   # Edit .env and add your GEMINI_API_KEY
   nano .env  # or use your preferred editor
   ```

#### Frontend Setup

2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

3. Install dependencies:
   ```bash
   # Using npm
   npm install
   
   # Or using yarn
   yarn install
   ```

4. Development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```
   
   Frontend will be available at: http://localhost:3000

5. Build for production:
   ```bash
   npm run build
   # or
   yarn build
   ```

#### Backend Setup

6. Navigate to the backend directory:
   ```bash
   cd backend
   ```

7. Create and activate virtual environment:
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

8. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

9. Run the development server:
   ```bash
   python app.py
   ```
   
   Backend API will be available at: http://localhost:5001

## 🎮 Usage Guide

### 1. **Data Input**
- Upload CSV files with task and resource data
- Or use the sample dataset provided
- Required columns: task_id, resource_requirements, execution_time

### 2. **Algorithm Selection**
- Choose between ACO or PSO algorithms
- Adjust algorithm parameters using the interactive controls
- Set number of iterations and convergence criteria

### 3. **Run Simulation**
- Click "Start Simulation" to begin optimization
- Watch real-time progress with streaming updates
- Monitor convergence through interactive charts

### 4. **Analyze Results**
- View detailed metrics: makespan, resource utilization, load balancing
- Compare algorithm performance
- Export results for further analysis

## 📊 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/health` | Detailed health status |
| `POST` | `/stream_scheduling` | Run optimization with streaming results |

### Example API Usage

```bash
# Run ACO algorithm
curl -X POST http://localhost:5001/stream_scheduling \
  -H "Content-Type: application/json" \
  -d '{
    "algorithm": "ACO",
    "tasks": [
      {"id": "task1", "length": 25},
      {"id": "task2", "length": 30},
      {"id": "task3", "length": 20}
    ],
    "parameters": {
      "n_ants": 15,
      "alpha": 1.2,
      "beta": 2.5,
      "n_iterations": 100
    }
  }'

# Run PSO algorithm
curl -X POST http://localhost:5001/stream_scheduling \
  -H "Content-Type: application/json" \
  -d '{
    "algorithm": "PSO", 
    "tasks": [
      {"id": "task1", "length": 25},
      {"id": "task2", "length": 30}
    ],
    "parameters": {
      "n_particles": 20,
      "w": 0.8,
      "c1": 1.5,
      "c2": 1.5,
      "n_iterations": 50
    }
  }'
```

## 🔧 Configuration

### Environment Variables

#### Root Project (.env)
The project includes an `example.env` file that you should copy to `.env`:

```bash
# Copy the example file
cp example.env .env
```

**Root .env file structure:**
```bash
# Environment variables for Docker Compose
GEMINI_API_KEY=your_gemini_api_key_here

# Docker-specific settings
COMPOSE_PROJECT_NAME=swarm-lab

# API URL for backend service (host access via port 5001)  
API_URL=http://localhost:5001
BACKEND_URL=http://localhost:5001
```

#### Frontend (.env)
```bash
# API Configuration
NUXT_PUBLIC_API_BASE=http://localhost:5001

# Development
NUXT_HOST=0.0.0.0
NUXT_PORT=3000
```

#### Backend (.env)
```bash
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=1
FLASK_APP=app.py

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,https://swarm-lab.vercel.app
```

### Algorithm Configuration

You can modify default algorithm parameters in the backend:

```python
# backend/app.py
DEFAULT_PARAMS = {
    'ACO': {
        'n_ants': 10,
        'alpha': 1.0,
        'beta': 2.0,
        'evaporation_rate': 0.1,
        'pheromone_deposit': 1.0
    },
    'PSO': {
        'n_particles': 10,
        'w': 0.7,
        'c1': 1.4,
        'c2': 1.4
    }
}
```

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run performance tests
python test_direct_metrics.py

# Run with Python's unittest module
python -m unittest test_direct_metrics.py

# Check algorithm performance
python test_direct_metrics.py -v
```

### Frontend Tests

```bash
cd frontend

# Run unit tests
npm run test

# Run E2E tests
npm run test:e2e

# Type checking
npm run type-check
```

## 🚀 Deployment

### Docker Deployment (Production)

```bash
# Production build and run
docker compose up -d --build

# View logs
docker compose logs -f

# Stop services
docker compose down
```

### Manual Deployment

#### Frontend (Static Hosting)

```bash
cd frontend
npm run build

# Deploy .output/public/ to your static hosting provider
# (Vercel, Netlify, GitHub Pages, etc.)
```

#### Backend (Cloud Platforms)

For **Heroku**:
```bash
# Already configured with Procfile
git push heroku main
```

For **Railway**, **Render**, or **DigitalOcean**:
- Use the provided `Dockerfile`
- Set environment variables in your platform
- Deploy from GitHub repository

### Environment-Specific Configurations

#### Development
```bash
# Use main compose file (optimized for development)
docker compose up
```

#### Production
```bash
# Use production-optimized settings
docker compose up -d
```

## 📈 Performance Metrics

The system tracks comprehensive performance metrics:

### Optimization Metrics
- **Makespan**: Total time to complete all tasks
- **Resource Utilization**: Efficiency of resource usage
- **Load Balancing**: Distribution evenness across resources
- **Convergence Rate**: Speed of algorithm convergence
- **Solution Quality**: Fitness function improvements over time

### System Metrics
- **Response Time**: API endpoint performance
- **Memory Usage**: Algorithm memory consumption
- **Throughput**: Tasks processed per second
- **Scalability**: Performance with increasing problem size

## 🤝 Contributing

We welcome contributions! Please follow these steps:

### Development Setup

1. **Fork the repository**
   ```bash
   git fork https://github.com/fazza-abiyyu/swarm-lab.git
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/swarm-lab.git
   cd swarm-lab
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

4. **Set up development environment**
   ```bash
   # Use Docker for quick setup
   docker compose up
   ```

### Contribution Guidelines

- **Code Style**: Follow existing code patterns
- **Testing**: Add tests for new features and run full test suite
- **Documentation**: Update relevant documentation
- **Commit Messages**: Use conventional commit format

#### Testing Requirements
All contributions must pass the existing test suite:

```bash
# Backend tests (required for backend changes)
cd backend
make test                    # Run all tests
make test-coverage          # Generate coverage report

# MATLAB/Octave validation (required for algorithm changes)
cd matlab/experiments
octave comprehensive_experiment.m
```

**Expected Results:**
- ✅ **17/17 backend unit tests** must pass (100% success rate)
- ✅ **Algorithm validation** must show consistent performance metrics
- ✅ **Code coverage** should maintain or improve existing levels

```bash
# Example commit messages
feat: add enhanced PSO algorithm
fix: resolve memory leak in PSO implementation
docs: update API documentation
test: add performance tests for optimization metrics
```

### Pull Request Process

1. **Update documentation** if needed
2. **Add/update tests** for your changes  
3. **Ensure all tests pass** - run `make test` in backend directory
4. **Verify test coverage** - maintain or improve coverage metrics
5. **Create pull request** with detailed description
6. **Address review feedback**

#### Pre-submission Checklist
- [ ] All unit tests pass (`make test`)
- [ ] Code coverage maintained/improved
- [ ] Documentation updated
- [ ] MATLAB experiments validate correctly
- [ ] No breaking changes to existing API

## � Research & References

This implementation is based on the following research:

### Key Papers
- **ACO**: Dorigo, M., & Stützle, T. (2004). "Ant Colony Optimization"
- **PSO**: Kennedy, J., & Eberhart, R. (1995). "Particle Swarm Optimization"
- **Cloud Scheduling**: Chen, H., et al. (2018). "Task Scheduling in Cloud Computing"

### Algorithm Implementations
- Multi-agent systems with communication protocols
- Adaptive parameter tuning mechanisms
- Advanced optimization strategies

## 🆘 Support & Documentation

### Getting Help
- 📖 **Documentation**: Check `/docs` directory
- 🐛 **Issues**: [GitHub Issues](https://github.com/fazza-abiyyu/swarm-lab/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/fazza-abiyyu/swarm-lab/discussions)

### Troubleshooting

#### Common Issues

**Frontend won't start:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Backend API errors:**
```bash
# Check Python environment
python --version
pip list

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Docker issues:**
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker compose build --no-cache
```

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### Citation

If you use this work in your research, please cite:

```bibtex
@software{swarm_lab_2025,
  title={Swarm Lab: Intelligent Cloud Task Scheduling System},
  author={Fazza Abiyyu},
  year={2025},
  url={https://github.com/fazza-abiyyu/swarm-lab}
}
```

## 🔄 Project Status

This project is actively maintained and developed. Check the [GitHub repository](https://github.com/fazza-abiyyu/swarm-lab) for the latest updates and releases.

## 🌟 Acknowledgments

- **Bio-inspired Computing Research Community**
- **Open Source Contributors**
- **Flask and Nuxt.js Communities**

---

**Built with ❤️ using Swarm Intelligence, Nuxt 4, and Flask**

[![GitHub stars](https://img.shields.io/github/stars/fazza-abiyyu/swarm-lab?style=social)](https://github.com/fazza-abiyyu/swarm-lab/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/fazza-abiyyu/swarm-lab?style=social)](https://github.com/fazza-abiyyu/swarm-lab/network/members)
[![GitHub issues](https://img.shields.io/github/issues/fazza-abiyyu/swarm-lab)](https://github.com/fazza-abiyyu/swarm-lab/issues)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
