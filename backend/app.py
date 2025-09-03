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
app.start_time = time.time()

# Security headers middleware
@app.after_request
def add_security_headers(response):
    # Content Security Policy (CSP) Header
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://unpkg.com; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data: https:; "
        "connect-src 'self' http://localhost:* http://127.0.0.1:* https:; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'none'"
    )
    
    # Anti-clickjacking Header (X-Frame-Options)
    response.headers['X-Frame-Options'] = 'DENY'
    
    # Remove X-Powered-By header to prevent information leakage
    response.headers.pop('Server', None)
    
    # X-Content-Type-Options Header to prevent MIME sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Additional security headers
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    
    # Cache control for sensitive endpoints
    if request.endpoint and 'health' not in request.endpoint:
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    
    return response

# CORS configuration - Enhanced for production deployment
CORS(app, 
     origins=[
         # Local development
         'http://localhost:3000', 
         'http://127.0.0.1:3000', 
         'http://0.0.0.0:3000',
         'http://frontend:3000',
         'http://127.0.0.1:3001', 
         'http://localhost:5000', 
         'http://127.0.0.1:5000',
         'http://localhost:5001', 
         'http://127.0.0.1:5001',
         # Production deployments
         'https://swarmwave.vercel.app',
         'https://swarmwave.vanila.app',
         # Wildcard for subdomains (use carefully in production)
         'https://*.vanila.app',
         'https://*.vercel.app'
     ], 
     supports_credentials=True, 
     allow_headers=[
         'Content-Type', 
         'Authorization', 
         'Accept',
         'Origin',
         'X-Requested-With',
         'Access-Control-Request-Method',
         'Access-Control-Request-Headers'
     ], 
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'],
     expose_headers=['Content-Range', 'X-Content-Range'],
     max_age=86400  # Cache preflight for 24 hours
)

# Additional CORS handling for preflight requests
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = Response()
        response.headers.add("Access-Control-Allow-Origin", request.headers.get('Origin', '*'))
        response.headers.add('Access-Control-Allow-Headers', "Content-Type, Authorization, Accept, Origin, X-Requested-With")
        response.headers.add('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS, PATCH")
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

# Error handler for CORS issues - Updated to be more secure
@app.errorhandler(Exception)
def handle_cors_error(e):
    response = jsonify({
        "error": "Internal server error",  # Don't expose internal error details
        "message": "An error occurred while processing your request",
        "status": "error"
    })
    # Only add CORS headers for legitimate origins
    origin = request.headers.get('Origin')
    allowed_origins = [
        'http://localhost:3000', 
        'http://127.0.0.1:3000',
        'http://0.0.0.0:3000',
        'http://frontend:3000',
        'https://swarmwave.vercel.app',
        'https://swarmwave.vanila.app'
    ]
    if origin in allowed_origins:
        response.headers.add("Access-Control-Allow-Origin", origin)
    return response, 500

@app.route('/')
def home():
    response = jsonify({"message": "Multi-Agent Task Scheduling API is running"})
    return response

@app.route('/health')
def health_check():
    """Comprehensive health check with system information"""
    try:
        current_time = time.time()
        uptime = current_time - app.start_time if hasattr(app, 'start_time') else 0
        
        # System information - Limited for security
        system_info = {
            "platform": platform.system(),
            "architecture": platform.machine(),
            "python_version": platform.python_version()[:3],  # Only major.minor version
        }
        
        # Application information
        app_info = {
            "name": "Swarm Wave Backend API",
            "version": "1.0.0",
            "status": "healthy",
            "timestamp": current_time,
            "datetime": datetime.fromtimestamp(current_time).isoformat(),
            "uptime_seconds": round(uptime, 2),
            "environment": os.getenv('FLASK_ENV', 'production'),  # Default to production
        }
        
        # Algorithm availability check
        algorithms_status = {}
        try:
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
            pso_scheduler = PSOScheduler(
                tasks=test_tasks, 
                agents=test_agents, 
                cost_function=lambda x, y: y,
                n_iterations=1
            )
            algorithms_status["PSO"] = {"available": True, "status": "operational"}
        except Exception as e:
            algorithms_status["PSO"] = {"available": False, "error": str(e)}
        
        # Resource information - Limited for security
        resource_info = {
            "process_id": os.getpid(),
            "python_path": "hidden_for_security"  # Don't expose system paths
        }
        
        # Health score calculation
        health_score = 100
        if not algorithms_status["ACO"]["available"]:
            health_score -= 40
        if not algorithms_status["PSO"]["available"]:
            health_score -= 40
        
        overall_status = "healthy" if health_score >= 80 else "degraded" if health_score >= 50 else "unhealthy"
        
        response_data = {
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
        }
        
        response = jsonify(response_data)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
        
    except Exception as e:
        error_response = jsonify({
            "status": "error",
            "health_score": 0,
            "timestamp": time.time(),
            "error": str(e),
            "traceback": traceback.format_exc()
        })
        error_response.headers.add("Access-Control-Allow-Origin", "*")
        return error_response, 500

@app.route('/stream_scheduling', methods=['POST'])
def stream_scheduling():
    """Stream-enabled scheduling endpoint with real-time progress updates"""
    try:
        data = request.get_json()
        if not data: 
            return jsonify({"error": "No data provided"}), 400
        
        tasks = data.get('tasks', data.get('tasks_data', []))
        parameters = data.get('parameters', {})
        if not tasks: 
            return jsonify({"error": "No tasks provided"}), 400
        
        algorithm = data.get('algorithm', '').upper()
        if not algorithm: 
            return jsonify({"error": "Algorithm not specified"}), 400

        # Extract parameters with default values
        num_default_agents = parameters.get('num_default_agents', 10)
        n_iterations = parameters.get('n_iterations', 100)
        task_id_col_for_scheduler = parameters.get('task_id_col', 'id')
        agent_id_col_for_scheduler = parameters.get('agent_id_col', 'id')
        
        # ACO parameters
        n_ants = parameters.get('n_ants', 10)
        alpha = parameters.get('alpha', 1.0)
        beta = parameters.get('beta', 2.0)
        evaporation_rate = parameters.get('evaporation_rate', 0.1)
        pheromone_deposit = parameters.get('pheromone_deposit', 1.0)
        
        # PSO parameters
        n_particles = parameters.get('n_particles', 10)
        w = parameters.get('w', 0.7)
        c1 = parameters.get('c1', 1.4)
        c2 = parameters.get('c2', 1.4)
        
        # Dependency settings
        enable_dependencies = parameters.get('enable_dependencies', False)

        # Task formatting with flexible ID handling
        formatted_tasks = []
        flexible_task_id_candidates = ['Task_ID', 'TaskID', 'task_id', 'id', 'ID', 'name', 'Name']
        
        def safe_convert_to_float(value, default=0.0):
            """Convert value to float safely"""
            if value is None or value == '' or str(value).lower() in ['null', 'nan', 'none']:
                return default
            try:
                return float(value)
            except (ValueError, TypeError):
                return default
        
        def safe_convert_to_string(value, default=''):
            """Convert value to string safely"""
            if value is None or str(value).lower() in ['null', 'nan', 'none']:
                return default
            return str(value).strip()
        
        for task in tasks:
            # Flexible Task ID handling
            task_id_value = None
            for field in flexible_task_id_candidates:
                if field in task and task[field] is not None and str(task[field]).strip():
                    task_id_value = safe_convert_to_string(task[field])
                    break
            if not task_id_value: 
                task_id_value = f"Task_{len(formatted_tasks) + 1}"

            # Duration/Length with null handling
            task_length = None
            for field in ['Duration', 'duration', 'length', 'Length', 'Weight', 'weight', 'execution_time', 'Execution_Time (s)']:
                if field in task:
                    task_length = safe_convert_to_float(task[field])
                    if task_length > 0:  # Only use positive values
                        break
            if task_length is None or task_length <= 0: 
                task_length = 1.0
            
            # Cost with null handling
            cost = 0.0
            for field in ['Cost', 'cost', 'price', 'Price']:
                if field in task:
                    cost = safe_convert_to_float(task[field])
                    if cost >= 0:  # Allow 0 cost
                        break
            
            # Additional fields with null handling
            priority = safe_convert_to_float(task.get('Priority', task.get('priority', 1)), 1)
            cpu_usage = safe_convert_to_float(task.get('CPU_Usage', task.get('cpu_usage', 0)), 0)
            ram_usage = safe_convert_to_float(task.get('RAM_Usage', task.get('ram_usage', 0)), 0)
            
            formatted_task = {
                task_id_col_for_scheduler: task_id_value,
                'length': task_length, 
                'cost': cost,
                'priority': priority,
                'cpu_usage': cpu_usage,
                'ram_usage': ram_usage
            }
            
            # Add all original fields, replacing null values
            for key, value in task.items():
                if key not in formatted_task:
                    if isinstance(value, (int, float)):
                        formatted_task[key] = safe_convert_to_float(value, 0)
                    else:
                        formatted_task[key] = safe_convert_to_string(value, '')
            
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
                evaporation_rate=evaporation_rate, pheromone_deposit=pheromone_deposit,
                enable_dependencies=enable_dependencies
            )
        elif algorithm == 'PSO':
            scheduler = PSOScheduler(
                tasks=formatted_tasks, agents=agents, cost_function=cost_function,
                task_id_col=task_id_col_for_scheduler, agent_id_col=agent_id_col_for_scheduler,
                n_particles=n_particles, n_iterations=n_iterations, w=w, c1=c1, c2=c2,
                enable_dependencies=enable_dependencies
            )
        else:
            return jsonify({"error": f"Unsupported algorithm: {algorithm}"}), 400

        # Generator function for streaming
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
            
            # Load balance index now comes directly from the final result
            load_balance_index = final_result.get('load_balance_index', 0)

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
        # Although this is not a stream, we send it as an error event
        return Response(f"data: {json.dumps(error_details)}\n\n", mimetype='text/event-stream')


@app.route('/health/simple')
def simple_health_check():
    """
    Simple health check for Docker and load balancers
    Returns minimal response for quick health verification
    """
    response = jsonify({
        "status": "ok",
        "timestamp": time.time()
    })
    return response
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