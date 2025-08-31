# 🐜 Swarm Lab Backend - Cloud Task Scheduling API

A **Flask-based REST API** implementing **Swarm Intelligence algorithms** for cloud task scheduling optimization. Supports **Ant Colony Optimization (ACO)** and **Particle Swarm Optimization (PSO)** with real-time streaming results.

## 🚀 Overview

The backend provides a robust API for:
- **Algorithm Execution**: Run ACO and PSO algorithms with customizable parameters
- **Real-time Streaming**: Server-Sent Events for live algorithm progress
- **Flexible Data Formats**: Support for various task data structures
- **Performance Metrics**: Comprehensive scheduling performance analysis
- **CORS Support**: Cross-origin requests for frontend integration

## 🎯 Key Features

### 🧠 **Swarm Intelligence Algorithms**
- **Ant Colony Optimization (ACO)**: Bio-inspired optimization using pheromone trails
- **Particle Swarm Optimization (PSO)**: Population-based optimization mimicking bird flocking
- **Multi-agent Systems**: Configurable number of processing agents
- **Parameter Tuning**: Fine-grained control over algorithm behavior

### 📊 **Real-time Processing**
- **Server-Sent Events**: Live streaming of algorithm progress
- **Iteration Tracking**: Real-time performance metrics updates
- **Progress Monitoring**: Convergence tracking and best solution updates
- **Error Handling**: Graceful error reporting with detailed information

### 🔧 **Flexible Configuration**
- **Dynamic Task Format**: Automatic detection of task properties
- **Agent Management**: Auto-generation or custom agent definitions  
- **Parameter Validation**: Input validation with sensible defaults
- **Multiple Data Sources**: CSV file processing and JSON data handling

## 🛠️ Technology Stack

### **Core Framework**
- **Flask**: Lightweight WSGI web application framework
- **Flask-CORS**: Cross-Origin Resource Sharing support
- **Python 3.9+**: Modern Python features and performance

### **Algorithm Libraries**
- **NumPy**: Numerical computing and array operations
- **Pandas**: Data manipulation and analysis
- **Custom Implementations**: Optimized ACO and PSO algorithms

### **Visualization & Monitoring**
- **Matplotlib**: Algorithm performance plotting
- **Plotly**: Interactive visualization support
- **tqdm**: Progress bars for long-running operations

### **Deployment**
- **Gunicorn**: WSGI HTTP server for production
- **Docker**: Containerization support
- **Heroku**: Cloud deployment configuration (Procfile)

## 📁 Project Structure

```
backend/
├── models/                     # Algorithm Implementations
│   ├── __init__.py            # Package Initialization
│   ├── aco.py                 # Ant Colony Optimization
│   └── pso.py                 # Particle Swarm Optimization
├── templates/                 # Flask Templates
│   └── index.html             # Basic HTML Template
├── app.py                     # Main Flask Application
├── requirements.txt           # Python Dependencies
├── test_health.py             # Health Endpoint Testing Script
├── Dockerfile                 # Docker Configuration
├── Procfile                   # Heroku Deployment
├── .dockerignore              # Docker Ignore Rules
└── data                       # Dataset files
    └──cloud_task_scheduling_dataset.csv  # Sample Dataset
```

## ⚙️ Installation & Setup

### **Prerequisites**
- **Python 3.9+**
- **pip** package manager
- **Virtual environment** (recommended)

### **Quick Start**

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
```

The API will be available at: `http://localhost:5001`

### **Docker Setup**

```bash
# Build Docker image
docker build -t swarm-lab-backend .

# Run container
docker run -p 5001:5000 swarm-lab-backend

# Or use docker-compose
docker compose up backend
```

## 🔗 API Endpoints

### **Health & Information**

#### `GET /`
Basic health check endpoint.

**Response:**
```json
{
  "message": "Cloud Task Scheduling API is running"
}
```

#### `GET /health`
Comprehensive health status with system information, algorithm availability, and performance metrics.

**Response:**
```json
{
  "status": "healthy",
  "health_score": 100,
  "timestamp": 1693497600.123,
  "datetime": "2025-08-31T15:20:24.512372",
  "uptime_seconds": 45.2,
  "application": {
    "name": "Swarm Lab Backend API",
    "version": "1.0.0",
    "environment": "development",
    "debug_mode": false
  },
  "system": {
    "platform": "Darwin",
    "python_version": "3.12.11",
    "architecture": "arm64",
    "hostname": "MacBook-Air"
  },
  "algorithms": {
    "ACO": {"available": true, "status": "operational"},
    "PSO": {"available": true, "status": "operational"}
  },
  "resources": {
    "process_id": 12345,
    "current_working_directory": "/app"
  },
  "endpoints": {
    "health": "/health",
    "health_simple": "/health/simple",
    "algorithms": "/algorithms",
    "stream_scheduling": "/stream_scheduling"
  }
}
```

#### `GET /health/simple`
Lightweight health check for Docker health checks and load balancers.

**Response:**
```json
{
  "status": "ok",
  "timestamp": 1693497600.123
}
```

#### `GET /algorithms`
List available algorithms and descriptions.

**Response:**
```json
{
  "algorithms": ["ACO", "PSO"],
  "descriptions": {
    "ACO": "Ant Colony Optimization for task scheduling",
    "PSO": "Particle Swarm Optimization for task scheduling"
  }
}
```

### **Algorithm Execution**

#### `POST /stream_scheduling`
Execute scheduling algorithm with real-time streaming results.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "algorithm": "ACO",
  "tasks": [
    {
      "id": "task1",
      "length": 25,
      "cost": 100
    },
    {
      "id": "task2", 
      "length": 30,
      "cost": 150
    }
  ],
  "parameters": {
    "num_default_agents": 3,
    "n_iterations": 100,
    "n_ants": 10,
    "alpha": 1.0,
    "beta": 2.0,
    "evaporation_rate": 0.1,
    "pheromone_deposit": 1.0
  }
}
```

**Response:** Server-Sent Events stream
```
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive

data: {"type": "progress", "iteration": 1, "best_fitness": 45.2, "current_makespan": 47.8}

data: {"type": "progress", "iteration": 2, "best_fitness": 43.1, "current_makespan": 43.1}

data: {"type": "final", "best_solution": [...], "makespan": 42.5, "execution_time": 2.34}
```

## 📊 Algorithm Parameters

### **ACO Parameters**

| Parameter | Description | Type | Default | Range |
|-----------|-------------|------|---------|--------|
| `n_ants` | Number of ants in colony | int | 10 | 5-50 |
| `alpha` | Pheromone influence factor | float | 1.0 | 0.1-5.0 |
| `beta` | Heuristic influence factor | float | 2.0 | 0.1-5.0 |
| `evaporation_rate` | Pheromone evaporation rate | float | 0.1 | 0.01-0.9 |
| `pheromone_deposit` | Pheromone deposit amount | float | 1.0 | 0.1-10.0 |
| `n_iterations` | Maximum iterations | int | 100 | 10-1000 |

### **PSO Parameters**

| Parameter | Description | Type | Default | Range |
|-----------|-------------|------|---------|--------|
| `n_particles` | Number of particles in swarm | int | 10 | 5-50 |
| `w` | Inertia weight | float | 0.7 | 0.1-1.0 |
| `c1` | Cognitive acceleration coefficient | float | 1.4 | 0.1-4.0 |
| `c2` | Social acceleration coefficient | float | 1.4 | 0.1-4.0 |
| `n_iterations` | Maximum iterations | int | 100 | 10-1000 |

### **General Parameters**

| Parameter | Description | Type | Default |
|-----------|-------------|------|---------|
| `num_default_agents` | Number of processing agents | int | 3 |
| `task_id_col` | Task ID column name | string | "id" |
| `agent_id_col` | Agent ID column name | string | "id" |

## 📋 Data Format Specifications

### **Task Data Structure**

The API supports flexible task data formats with automatic field detection:

**Minimal Format:**
```json
{
  "id": "task1",
  "length": 25
}
```

**Extended Format:**
```json
{
  "TaskID": "T001",
  "Duration": 25,
  "Cost": 100,
  "Weight": 15,
  "Priority": 1,
  "deadline": "2025-01-01T12:00:00Z"
}
```

**Supported Field Names (Auto-detected):**

| Property | Possible Field Names |
|----------|---------------------|
| **Task ID** | `TaskID`, `task_id`, `id`, `name`, `Name` |
| **Duration** | `Duration`, `duration`, `length`, `Length`, `Weight`, `weight`, `execution_time`, `Execution_Time (s)` |
| **Cost** | `Cost`, `cost`, `price`, `Price` |

### **Agent Data Structure**

**Auto-generated (Default):**
```json
[
  {"id": "Agent-1"},
  {"id": "Agent-2"}, 
  {"id": "Agent-3"}
]
```

**Custom Agents:**
```json
{
  "parameters": {
    "agents": [
      {"id": "Server-A", "capacity": 100},
      {"id": "Server-B", "capacity": 80}
    ]
  }
}
```
## 📊 Response Format

### **Stream Response Data**

During algorithm execution, the API sends real-time updates via Server-Sent Events:

**Progress Update:**
```json
{
  "type": "progress",
  "iteration": 25,
  "best_fitness": 42.3,
  "current_makespan": 45.7,
  "timestamp": 1693497625.456
}
```

**Final Results:**
```json
{
  "type": "final",
  "algorithm": "ACO",
  "best_solution": [
    {
      "task_id": "task1",
      "agent_id": "Agent-1", 
      "start_time": 0,
      "finish_time": 25
    },
    {
      "task_id": "task2",
      "agent_id": "Agent-2",
      "start_time": 0,
      "finish_time": 30
    }
  ],
  "metrics": {
    "makespan": 42.5,
    "execution_time": 2.34,
    "load_balance_index": 0.15,
    "total_cost": 250,
    "resource_utilization": 0.85
  },
  "iterations": [
    {
      "iteration": 1,
      "makespan": 47.8,
      "best_fitness": 47.8
    },
    {
      "iteration": 2, 
      "makespan": 45.2,
      "best_fitness": 45.2
    }
  ]
}
```

**Error Response:**
```json
{
  "type": "error",
  "message": "Invalid algorithm parameter",
  "traceback": "...",
  "timestamp": 1693497630.123
}
```

## 🧪 Testing & Validation

### **Health Endpoint Testing**

Use the included health testing script:

```bash
# Navigate to backend directory
cd backend

# Test health endpoints with current server
python3 test_health.py

# Test with specific URL
python3 test_health.py http://localhost:5001

# Test Docker deployment
python3 test_health.py http://localhost:5001
```

**Expected Output:**
```
Testing health endpoints at http://localhost:5001
==================================================

🔍 Testing Simple Health Check...
Status Code: 200
✅ Simple Health Check: OK
⏰ Timestamp: 1756628424.539446

🔍 Testing Detailed Health Check...
Status Code: 200
✅ Overall Status: HEALTHY
🏆 Health Score: 100/100
⏱️ Uptime: 45.2 seconds
🐍 Python Version: 3.12.11
💻 Platform: Darwin

🤖 Algorithms Status:
  ✅ ACO: operational
  ✅ PSO: operational

🔗 Available Endpoints:
  • health: /health
  • health_simple: /health/simple
  • algorithms: /algorithms
  • stream_scheduling: /stream_scheduling
```

### **API Testing with cURL**

**Test ACO Algorithm:**
```bash
curl -X POST http://localhost:5001/stream_scheduling \
  -H "Content-Type: application/json" \
  -d '{
    "algorithm": "ACO",
    "tasks": [
      {"id": "T1", "length": 25, "cost": 100},
      {"id": "T2", "length": 30, "cost": 150},
      {"id": "T3", "length": 20, "cost": 80}
    ],
    "parameters": {
      "num_default_agents": 2,
      "n_iterations": 50,
      "n_ants": 8,
      "alpha": 1.2,
      "beta": 2.5,
      "evaporation_rate": 0.1
    }
  }'
```

**Test PSO Algorithm:**
```bash
curl -X POST http://localhost:5001/stream_scheduling \
  -H "Content-Type: application/json" \
  -d '{
    "algorithm": "PSO", 
    "tasks": [
      {"TaskID": "Task1", "Duration": 15},
      {"TaskID": "Task2", "Duration": 25},
      {"TaskID": "Task3", "Duration": 35}
    ],
    "parameters": {
      "num_default_agents": 3,
      "n_iterations": 100,
      "n_particles": 15,
      "w": 0.8,
      "c1": 1.5,
      "c2": 1.5
    }
  }'
```

**Health Check:**
```bash
# Basic health check
curl http://localhost:5001/

# Simple health check (for monitoring)
curl http://localhost:5001/health/simple

# Detailed health status
curl http://localhost:5001/health

# Available algorithms
curl http://localhost:5001/algorithms
```

## 🔧 Configuration

### **Environment Variables**

Create a `.env` file in the backend directory:

```bash
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=1
FLASK_APP=app.py

# Server Configuration
HOST=0.0.0.0
PORT=5001

# CORS Origins
CORS_ORIGINS=http://localhost:3000,https://swarm-lab.vercel.app

# Algorithm Defaults
DEFAULT_ITERATIONS=100
DEFAULT_AGENTS=3
```

### **Production Configuration**

For production deployment, update the CORS settings:

```python
# app.py
CORS(app, origins=[
    'https://your-frontend-domain.com',
    'https://swarm-lab.vercel.app'
], supports_credentials=True)
```

## 🚀 Deployment

### **Docker Deployment**

```bash
# Build and run with Docker
docker build -t swarm-lab-backend .
docker run -p 5001:5000 -e FLASK_ENV=production swarm-lab-backend

# Using docker-compose
docker compose up -d backend
```

### **Heroku Deployment**

The backend includes a `Procfile` for Heroku deployment:

```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-swarm-lab-backend

# Set environment variables
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main

# Open application
heroku open
```

### **Manual Production Deployment**

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn --bind 0.0.0.0:5001 --workers 4 --timeout 120 app:app

# Or use systemd service
sudo systemctl start swarm-lab-backend
```

## 📈 Performance Optimization

### **Algorithm Performance**
- **Iteration Limits**: Set reasonable iteration counts (50-200)
- **Population Size**: Balance between exploration and computation time
- **Early Termination**: Implement convergence criteria
- **Parallel Processing**: Consider multi-threading for large datasets

### **API Performance**
- **Request Validation**: Input validation to prevent invalid requests
- **Memory Management**: Efficient data structures for large task sets
- **Caching**: Cache common algorithm configurations
- **Connection Pooling**: Database connection optimization (if used)

### **Monitoring**
- **Logging**: Comprehensive request/response logging
- **Metrics Collection**: Track algorithm performance metrics
- **Error Tracking**: Detailed error reporting and debugging
- **Health Checks**: Automated health monitoring

## 🔍 Algorithm Details

### **Ant Colony Optimization (ACO)**

**Implementation Features:**
- Multi-agent pheromone trail management
- Dynamic pheromone evaporation
- Heuristic information integration
- Elitist ant selection
- Local and global pheromone updates

**Best Use Cases:**
- Large-scale task scheduling
- Resource allocation optimization
- Path finding in distributed systems
- Complex constraint satisfaction

### **Particle Swarm Optimization (PSO)**

**Implementation Features:**
- Particle position and velocity updates
- Personal and global best tracking
- Inertia weight adjustment
- Boundary constraint handling
- Swarm diversity maintenance

**Best Use Cases:**
- Continuous optimization problems
- Real-time scheduling adjustments
- Multi-objective optimization
- Parameter tuning scenarios

## 🛠️ Development

### **Development Setup**

```bash
# Install development dependencies
pip install -r requirements.txt

# Test health endpoints
python3 test_health.py

# Run Flask development server
python3 app.py

# Test API endpoints
curl http://localhost:5001/health
```

### **Adding New Algorithms**

1. **Create algorithm file** in `models/` directory
2. **Implement required methods**: `run()`, `get_best_solution()`
3. **Add algorithm to app.py** routing
4. **Update API documentation**
5. **Add comprehensive tests**

Example algorithm structure:
```python
class NewAlgorithmScheduler:
    def __init__(self, tasks, agents, cost_function, **kwargs):
        self.tasks = tasks
        self.agents = agents
        self.cost_function = cost_function
        
    def run(self):
        # Implementation here
        pass
        
    def get_best_solution(self):
        # Return best scheduling solution
        pass
```

## 🆘 Troubleshooting

### **Common Issues**

**Port Already in Use:**
```bash
# Check what's using port 5001
lsof -i :5001

# Kill process using port
kill -9 <PID>

# Or change port in app.py
app.run(port=5002)
```

**Import Errors:**
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Ensure models directory is accessible
export PYTHONPATH="${PYTHONPATH}:/path/to/backend"
```

**Memory Issues:**
```bash
# Monitor memory usage
python -c "
import tracemalloc
tracemalloc.start()
# Your code here
current, peak = tracemalloc.get_traced_memory()
print(f'Current: {current / 1024 / 1024:.1f} MB')
print(f'Peak: {peak / 1024 / 1024:.1f} MB')
"
```

### **Logging & Debugging**

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Debug algorithm execution:
```python
# Add debug prints in algorithm files
print(f"Iteration {i}: Best fitness = {best_fitness}")
```

### **CORS Configuration**

Update CORS settings for development:
```python
# app.py - Development only
CORS(app, origins=['*'], supports_credentials=True)

# Production - Specific origins
CORS(app, origins=[
    'https://your-frontend-domain.com',
    'https://swarm-lab.vercel.app'
], supports_credentials=True)
```

### **Docker Health Checks**

The Docker configuration includes automated health monitoring:

```yaml
# docker-compose.yml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/health/simple"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

**Monitor container health:**
```bash
# Check container health status
docker compose ps

# View detailed health status
docker inspect swarm-lab-backend --format='{{.State.Health.Status}}'

# View health check logs
docker inspect swarm-lab-backend --format='{{range .State.Health.Log}}{{.Output}}{{end}}'

# Test health endpoint manually
docker compose exec backend curl http://localhost:5000/health/simple
```

### **Dependencies**

The project includes these key dependencies in `requirements.txt`:

```text
Flask                 # Web framework
flask-cors           # Cross-Origin Resource Sharing
pandas               # Data manipulation  
numpy                # Numerical computing
matplotlib           # Plotting and visualization
plotly               # Interactive visualizations
tqdm                 # Progress bars
gunicorn            # WSGI HTTP server
requests            # HTTP client library (for testing)
```

**Install all dependencies:**
```bash
pip install -r requirements.txt
```

## 🤝 Contributing

### **Development Guidelines**

1. **Follow PEP 8** style guidelines
2. **Add comprehensive tests** for new features
3. **Document API changes** in README
4. **Use type hints** where appropriate
5. **Maintain backward compatibility**

### **Pull Request Process**

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-algorithm`
3. Make changes and add tests
4. Update documentation
5. Submit pull request with detailed description

## 📄 License

This project is licensed under the **MIT License** - see the root [LICENSE](../LICENSE) file for details.

---

## 📚 Research References

- **Dorigo, M., & Stützle, T.** (2004). Ant Colony Optimization. MIT Press.
- **Kennedy, J., & Eberhart, R.** (1995). Particle Swarm Optimization. IEEE.
- **Chen, H., et al.** (2018). Task Scheduling in Cloud Computing: A Survey. Future Generation Computer Systems.

---

**Built with ❤️ for swarm intelligence research and cloud computing optimization**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?logo=flask)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://www.docker.com/)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
