# Backend-Frontend Integration Guide

## Overview
The backend `run_scheduling` endpoint has been updated to fully align with the frontend fetch structure used in the Vue.js application.

## Request Format

### Frontend Request Structure
```json
{
  "algorithm": "aco",
  "tasks": [
    {
      "TaskID": 1,
      "Duration": 25,
      "Weight": 10,
      "Cost": 100
    }
  ],
  "parameters": {
    "num_default_agents": 3,
    "n_iterations": 100,
    "n_ants": 10,
    "alpha": 1,
    "beta": 2,
    "evaporation_rate": 0.5,
    "pheromone_deposit": 100,
    "n_particles": 10,
    "w": 0.5,
    "c1": 1.5,
    "c2": 1.5,
    "task_id_col": "TaskID",
    "agent_id_col": "id"
  }
}
```

## Response Format

### Frontend-Compatible Response Structure
```json
{
  "success": true,
  "algorithm": "ACO",
  "bestMakespan": 4.0,
  "makespan": 4.0,
  "computing_time": 0.189,
  "executionTime": 0.189,
  "loadBalanceIndex": 0.3,
  "loadbalancing": 0.3,
  "computationTime": 0.189,
  "total_execution_time": 0.189,
  "results": [
    {
      "task_id": "1",
      "agent_id": "Agent-1",
      "start_time": 0,
      "finish_time": 25
    }
  ],
  "iterations": [
    {
      "index": 1,
      "makespan": 4.0,
      "loadbalancing": 0.3,
      "computing_time": 0.00189
    }
  ],
  "finalAssignment": [
    {
      "task_id": "1",
      "agent_id": "Agent-1",
      "start_time": 0,
      "finish_time": 25
    }
  ]
}
```

## Supported Algorithms

### ACO (Ant Colony Optimization)
- **Algorithm**: "aco"
- **Required Parameters**: `n_ants`, `n_iterations`, `alpha`, `beta`, `evaporation_rate`, `pheromone_deposit`

### PSO (Particle Swarm Optimization)
- **Algorithm**: "pso"
- **Required Parameters**: `n_particles`, `n_iterations`, `w`, `c1`, `c2`

### ACOPSO (Hybrid)
- **Algorithm**: "acopso"
- **Uses**: Combined ACO and PSO parameters

## Key Features

### 1. Flexible Task Data Parsing
The backend automatically detects and maps various task field names:
- **Task ID**: `TaskID`, `task_id`, `id`, or auto-generated
- **Duration**: `Duration`, `duration`, `length`, `Length`, `Weight`, `weight`
- **Priority**: `priority`, `Priority`, `weight`, `Weight`
- **Cost**: `Cost`, `cost`, `price`, `Price`

### 2. Error Handling
- Returns structured error responses compatible with frontend error handling
- Includes detailed error messages and stack traces in development

### 3. CORS Support
- Full CORS headers for cross-origin requests
- Handles preflight OPTIONS requests

## Usage Examples

### Frontend Integration
```javascript
// Frontend fetch call
const runScheduling = async (algorithm) => {
  const requestBody = {
    algorithm: algorithm.toLowerCase(),
    tasks: filteredTasks.value,
    parameters: {
      num_default_agents: parameters.num_default_agents,
      n_iterations: parameters.n_iterations,
      // ... other algorithm-specific parameters
    }
  };
  
  const response = await fetch('http://localhost:5001/run_scheduling', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(requestBody)
  });
  
  const result = await response.json();
  return result;
};
```

### Testing Endpoints
The backend provides two test scripts:
- `test_frontend_format.py`: Basic functionality test
- `test_complex_data.py`: Real-world data test with CSV integration

## API Endpoints

### Main Scheduling Endpoint
- **URL**: `POST /run_scheduling`
- **Content-Type**: `application/json`
- **Response**: JSON with frontend-compatible structure

### Health Check
- **URL**: `GET /health`
- **Response**: `{"status": "healthy", "timestamp": 1234567890}`

### Available Algorithms
- **URL**: `GET /algorithms`
- **Response**: List of supported algorithms with descriptions

## Running the Server
```bash
# Install dependencies
pip3 install -r requirements.txt

# Start the server
python3 app.py

# Server will run on http://localhost:5001
```