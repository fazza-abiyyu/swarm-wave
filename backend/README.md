# Swarm Wave Backend

A Flask-based REST API implementing Swarm Intelligence algorithms (ACO and PSO) for multi-agent task scheduling optimization with real-time streaming results.

## Overview

The backend provides a robust API for algorithm execution, real-time progress streaming via Server-Sent Events (SSE), flexible task data handling, and comprehensive performance metrics.

## Key Features

- **Algorithms**: Ant Colony Optimization (ACO) and Particle Swarm Optimization (PSO).
- **Real-time Processing**: Live streaming of algorithm progress and metrics.
- **Flexible Configuration**: Dynamic task format detection and configurable agent management.
- **Performance Metrics**: Detailed tracking of makespan, load balance, and convergence.

## Technology Stack

- **Core**: Flask, Flask-CORS, Python 3.9+
- **Algorithms**: NumPy, Pandas
- **Deployment**: Gunicorn, Docker support

## Project Structure

```
backend/
├── models/         # Algorithm Implementations (ACO, PSO)
├── app.py          # Main Flask Application
├── requirements.txt # Dependencies
├── Dockerfile      # Docker Configuration
└── data/           # Dataset files
```

## Installation & Setup

### Prerequisites
- Python 3.9+
- pip

### Quick Start

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The API will be available at `http://localhost:5001`.

### Docker Setup

```bash
docker build -t swarm-wave-backend .
docker run -p 5001:5000 swarm-wave-backend
# Or: docker compose up backend
```

## API Endpoints

### Health Check

- `GET /health`: Comprehensive system status.
- `GET /health/simple`: Lightweight status check.

### Algorithm Execution

**POST /stream_scheduling**

Execute scheduling with real-time results.

**Request Body Example:**

```json
{
  "algorithm": "ACO",
  "tasks": [
    {"id": "t1", "length": 25, "cost": 100},
    {"id": "t2", "length": 30, "cost": 150}
  ],
  "parameters": {
    "num_default_agents": 3,
    "n_iterations": 100
  }
}
```

**Response:** Server-Sent Events (SSE) stream containing progress updates and final results.

## Testing

Run the included test suite:

```bash
# Run all tests
python3 backend/tests/run_tests.py

# Run specific tests interactively
python3 backend/tests/interactive_runner.py
```

## Configuration

Environment variables can be set in a `.env` file:

```bash
FLASK_ENV=development
PORT=5001
CORS_ORIGINS=http://localhost:3000
```
