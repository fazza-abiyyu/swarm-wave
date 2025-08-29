# Cloud Task Scheduling API

Flask-based API untuk task scheduling menggunakan algoritma ACO, PSO, dan ACOPSO.

## Instalasi

```bash
pip3 install -r requirements.txt
```

## Menjalankan Server

```bash
python3 app.py
```

Server akan berjalan di `http://localhost:5001`

## Endpoint

### 1. Health Check
```http
GET /health
```

### 2. Daftar Algoritma
```http
GET /algorithms
```

### 3. Task Scheduling
```http
POST /run_scheduling
```

**Body Request:**
```json
{
  "algorithm": "aco",
  "tasks_data": [
    {
      "TaskID": 1,
      "Weight": 10,
      "Duration": 25,
      "Cost": 100
    },
    {
      "TaskID": 2,
      "Weight": 15,
      "Duration": 30,
      "Cost": 150
    }
  ],
  "parameters": {
    "num_default_agents": 3,
    "task_id_col": "TaskID",
    "agent_id_col": "",
    "n_iterations": 100,
    "n_ants": 10,
    "alpha": 1,
    "beta": 2,
    "evaporation_rate": 0.5,
    "pheromone_deposit": 100
  }
}
```

**Alternative format:**
```json
{
  "algorithm": "pso",
  "tasks": [
    {
      "TaskID": 1,
      "Duration": 25,
      "priority": 1
    },
    {
      "TaskID": 2,
      "Duration": 30,
      "priority": 2
    }
  ],
  "parameters": {
    "num_default_agents": 3,
    "n_iterations": 100,
    "n_particles": 30,
    "w": 0.5,
    "c1": 1.5,
    "c2": 1.5
  }
}
```

**Response:**
```json
{
  "success": true,
  "algorithm": "ACO",
  "makespan": 15.7,
  "computing_time": 0.234,
  "executionTime": 0.234,
  "loadBalanceIndex": 0.15,
  "loadbalancing": 0.15,
  "computationTime": 0.234,
  "total_execution_time": 0.234,
  "results": [...],
  "iterations": [...],
  "finalAssignment": []
}      "task_id": "task1",
      "agent_id": "Agent-1",
      "start_time": 0,
      "finish_time": 10.5
    },
    {
      "task_id": "task2",
      "agent_id": "Agent-2", 
      "start_time": 0,
      "finish_time": 5.2
    }
  ],
  "iterations": [
    {
      "iteration": 1,
      "makespan": 20.5,
      "loadBalanceIndex": 0.25
    }
  ]
}
```

## Catatan Penting

1. **Agent ID bersifat opsional**: Jika tidak disediakan, sistem akan otomatis membuat agent dengan jumlah sesuai `num_default_agents`

2. **Format Task**: Setiap task harus memiliki minimal:
   - `task_id` atau sesuai dengan `task_id_col` parameter
   - `length` (waktu eksekusi)
   - `priority` (opsional, default: 1)

3. **Port**: API berjalan di port 5001 untuk menghindari konflik dengan layanan macOS

4. **CORS**: Sudah diaktifkan untuk semua origin (development only)

## Contoh Penggunaan dengan cURL

```bash
# Test ACO algorithm
curl -X POST http://localhost:5001/ren_scheduling \
  -H "Content-Type: application/json" \
  -d '{
    "algorithm": "aco",
    "tasks_data": [
      {"TaskID": 1, "Duration": 25, "Cost": 100},
      {"TaskID": 2, "Duration": 30, "Cost": 150}
    ],
    "parameters": {
      "num_default_agents": 2,
      "n_iterations": 50,
      "n_ants": 10,
      "alpha": 1,
      "beta": 2,
      "evaporation_rate": 0.5
    }
  }'

# Test PSO algorithm
curl -X POST http://localhost:5001/ren_scheduling \
  -H "Content-Type: application/json" \
  -d '{
    "algorithm": "pso",
    "tasks_data": [
      {"TaskID": 1, "Duration": 25, "Weight": 10},
      {"TaskID": 2, "Duration": 30, "Weight": 15}
    ],
    "parameters": {
      "num_default_agents": 2,
      "n_iterations": 50,
      "n_particles": 10,
      "w": 0.5,
      "c1": 1.5,
      "c2": 1.5
    }
  }'

# Test ACOPSO algorithm
curl -X POST http://localhost:5001/ren_scheduling \
  -H "Content-Type: application/json" \
  -d '{
    "algorithm": "acopso",
    "tasks": [
      {"TaskID": "T1", "Duration": 10},
      {"TaskID": "T2", "Duration": 15},
      {"TaskID": "T3", "Duration": 20}
    ],
    "parameters": {
      "num_default_agents": 3,
      "n_iterations": 100
    }
  }'
```