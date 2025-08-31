from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json
import time
import traceback
import os
import platform
import sys
from datetime import datetime
from models.aco import ACO_MultiAgent_Scheduler as ACOScheduler
from models.pso import PSO_MultiAgent_Scheduler as PSOScheduler

app = Flask(__name__)
app.start_time = time.time()  # Track application start time
CORS(app, origins=[
    'http://localhost:3000', 
    'http://127.0.0.1:3000', 
    'http://0.0.0.0:3000',
    'http://frontend:3000',
    'http://127.0.0.1:3001', 
    'http://localhost:5000', 
    'http://127.0.0.1:5000',
    'http://localhost:5001', 
    'http://127.0.0.1:5001',
    'https://swarm-lab.vercel.app'
], supports_credentials=True, allow_headers=['Content-Type', 'Authorization'], methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

@app.route('/')
def home():
    return jsonify({"message": "Cloud Task Scheduling API is running"})

@app.route('/health')
def health_check():
    """
    Comprehensive health check endpoint
    Returns detailed system and application health information
    """
    try:
        # Basic health info
        current_time = time.time()
        uptime = current_time - app.start_time if hasattr(app, 'start_time') else 0
        
        # System information
        system_info = {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "hostname": platform.node(),
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
        }
        
        # Application information
        app_info = {
            "name": "Swarm Lab Backend API",
            "version": "1.0.0",
            "status": "healthy",
            "timestamp": current_time,
            "datetime": datetime.fromtimestamp(current_time).isoformat(),
            "uptime_seconds": round(uptime, 2),
            "environment": os.getenv('FLASK_ENV', 'development'),
            "port": os.getenv('PORT', '5001'),
            "debug_mode": app.debug
        }
        
        # Algorithm availability check
        algorithms_status = {}
        try:
            # Test ACO import and basic functionality
            test_tasks = [{"id": "test", "length": 1}]
            test_agents = [{"id": "test-agent"}]
            aco_scheduler = ACOScheduler(
                tasks=test_tasks, 
                agents=test_agents, 
                cost_function=lambda x, y: y,
                heuristic_function=lambda x: 1.0,
                n_iterations=1
            )
            algorithms_status["ACO"] = {"available": True, "status": "operational"}
        except Exception as e:
            algorithms_status["ACO"] = {"available": False, "error": str(e)}
        
        try:
            # Test PSO import and basic functionality
            pso_scheduler = PSOScheduler(
                tasks=test_tasks, 
                agents=test_agents, 
                cost_function=lambda x, y: y,
                n_iterations=1
            )
            algorithms_status["PSO"] = {"available": True, "status": "operational"}
        except Exception as e:
            algorithms_status["PSO"] = {"available": False, "error": str(e)}
        
        # Memory and resource info (basic)
        resource_info = {
            "process_id": os.getpid(),
            "parent_process_id": os.getppid(),
            "current_working_directory": os.getcwd(),
            "python_path": sys.executable,
            "python_paths": sys.path[:3]  # First 3 paths to avoid too much data
        }
        
        # Health score calculation
        health_score = 100
        if not algorithms_status["ACO"]["available"]:
            health_score -= 40
        if not algorithms_status["PSO"]["available"]:
            health_score -= 40
        
        overall_status = "healthy" if health_score >= 80 else "degraded" if health_score >= 50 else "unhealthy"
        
        return jsonify({
            "status": overall_status,
            "health_score": health_score,
            "timestamp": current_time,
            "datetime": app_info["datetime"],
            "uptime_seconds": app_info["uptime_seconds"],
            "application": app_info,
            "system": system_info,
            "algorithms": algorithms_status,
            "resources": resource_info,
            "endpoints": {
                "health": "/health",
                "algorithms": "/algorithms", 
                "stream_scheduling": "/stream_scheduling"
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "health_score": 0,
            "timestamp": time.time(),
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/stream_scheduling', methods=['POST'])
def stream_scheduling():
    # ... (Kode parsing data dari request body tetap sama)
    try:
        data = request.get_json()
        if not data: return jsonify({"error": "No data provided"}), 400
        
        tasks = data.get('tasks', data.get('tasks_data', []))
        parameters = data.get('parameters', {})
        if not tasks: return jsonify({"error": "No tasks provided"}), 400
        
        algorithm = data.get('algorithm', '').upper()
        if not algorithm: return jsonify({"error": "Algorithm not specified"}), 400

        # Ekstrak parameter dengan nilai default (sama seperti sebelumnya)
        num_default_agents = parameters.get('num_default_agents', 3)
        n_iterations = parameters.get('n_iterations', 100)
        task_id_col_for_scheduler = parameters.get('task_id_col', 'id')
        agent_id_col_for_scheduler = parameters.get('agent_id_col', 'id')
        
        # Parameter spesifik ACO
        n_ants = parameters.get('n_ants', 10)
        alpha = parameters.get('alpha', 1.0)
        beta = parameters.get('beta', 2.0)
        evaporation_rate = parameters.get('evaporation_rate', 0.1)
        pheromone_deposit = parameters.get('pheromone_deposit', 1.0)
        
        # Parameter spesifik PSO
        n_particles = parameters.get('n_particles', 10)
        w = parameters.get('w', 0.7)
        c1 = parameters.get('c1', 1.4)
        c2 = parameters.get('c2', 1.4)

        # ... (Kode formatting tasks tetap sama)
        formatted_tasks = []
        flexible_task_id_candidates = ['TaskID', 'task_id', 'id', 'name', 'Name']
        for task in tasks:
            task_id_value = None
            for field in flexible_task_id_candidates:
                if field in task and task[field] is not None:
                    task_id_value = str(task[field])
                    break
            if task_id_value is None: task_id_value = str(len(formatted_tasks) + 1)

            task_length = None
            for field in ['Duration', 'duration', 'length', 'Length', 'Weight', 'weight', 'execution_time', 'Execution_Time (s)']:
                if field in task and task[field] is not None:
                    try: task_length = float(task[field]); break
                    except ValueError: pass
            if task_length is None: task_length = 1.0
            
            cost = 0.0
            for field in ['Cost', 'cost', 'price', 'Price']:
                if field in task and task[field] is not None:
                    try: cost = float(task[field]); break
                    except ValueError: pass
            
            formatted_task = {
                task_id_col_for_scheduler: task_id_value,
                'length': task_length, 'cost': cost
            }
            formatted_task.update(task)
            formatted_tasks.append(formatted_task)
        
        agents = parameters.get('agents')
        if not agents: agents = [{agent_id_col_for_scheduler: f"Agent-{i+1}"} for i in range(num_default_agents)]
        
        def cost_function(schedule, makespan): return makespan
        def heuristic_function(task): return 1.0 / max(task.get('length', 1), 0.1)
        
        scheduler = None
        if algorithm == 'ACO':
            scheduler = ACOScheduler(
                tasks=formatted_tasks, agents=agents, cost_function=cost_function,
                heuristic_function=heuristic_function, num_default_agents=num_default_agents,
                task_id_col=task_id_col_for_scheduler, agent_id_col=agent_id_col_for_scheduler,
                n_ants=n_ants, n_iterations=n_iterations, alpha=alpha, beta=beta,
                evaporation_rate=evaporation_rate, pheromone_deposit=pheromone_deposit
            )
        elif algorithm == 'PSO':
            scheduler = PSOScheduler(
                tasks=formatted_tasks, agents=agents, cost_function=cost_function,
                task_id_col=task_id_col_for_scheduler, agent_id_col=agent_id_col_for_scheduler,
                n_particles=n_particles, n_iterations=n_iterations, w=w, c1=c1, c2=c2
            )
        else:
            return jsonify({"error": f"Unsupported algorithm: {algorithm}"}), 400

        # Fungsi generator untuk streaming
        def generate():
            start_time = time.time()
            final_result = None
            algorithm_computation_time = 0
            
            # Mengirim data awal
            initial_data = {"type": "start", "message": f"Starting {algorithm} simulation..."}
            yield f"data: {json.dumps(initial_data)}\n\n"

            # Iterasi melalui generator scheduler
            for data_chunk in scheduler.run():
                yield f"data: {data_chunk}\n\n"
                # Simpan hasil akhir saat event 'done' diterima
                chunk_obj = json.loads(data_chunk)
                if chunk_obj.get("type") == "done":
                    final_result = chunk_obj
                    algorithm_computation_time = chunk_obj.get('computation_time', 0)
            
            total_execution_time = time.time() - start_time
            
            # Hitung load balancing dari hasil akhir
            best_schedule = final_result.get('schedule', [])
            agent_times = {}
            for assignment in best_schedule:
                agent_id = assignment['agent_id']
                finish_time = assignment['finish_time']
                agent_times[agent_id] = max(agent_times.get(agent_id, 0), finish_time)
            
            load_balance_index = 0
            if agent_times:
                max_time = max(agent_times.values())
                min_time = min(agent_times.values())
                avg_time = sum(agent_times.values()) / len(agent_times)
                if avg_time > 0:
                    load_balance_index = (max_time - min_time) / avg_time

            # Kirim data metrik final
            final_metrics = {
                "type": "final_metrics",
                "total_execution_time": round(total_execution_time * 1000, 2),  # Convert to milliseconds
                "computation_time": algorithm_computation_time,  # Already in milliseconds from algorithm
                "load_balance_index": load_balance_index
            }
            yield f"data: {json.dumps(final_metrics)}\n\n"

        return Response(generate(), mimetype='text/event-stream')

    except Exception as e:
        error_details = {"type": "error", "message": str(e), "traceback": traceback.format_exc()}
        # Walaupun ini bukan stream, kita kirim sebagai event error
        return Response(f"data: {json.dumps(error_details)}\n\n", mimetype='text/event-stream')


@app.route('/health/simple')
def simple_health_check():
    """
    Simple health check for Docker and load balancers
    Returns minimal response for quick health verification
    """
    return jsonify({
        "status": "ok",
        "timestamp": time.time()
    })
@app.route('/algorithms', methods=['GET'])
def get_algorithms():
    return jsonify({
        "algorithms": ["ACO", "PSO"],
        "descriptions": {
            "ACO": "Ant Colony Optimization for task scheduling",
            "PSO": "Particle Swarm Optimization for task scheduling"
        }
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))  # Use PORT env var, default to 5001
    app.run(debug=True, host='0.0.0.0', port=port)