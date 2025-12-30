from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json
import time
import traceback
import os
import platform
import sys
import random
from datetime import datetime
import numpy as np
from models.aco import ACO_MultiAgent_Scheduler as ACOScheduler
from models.pso import PSO_MultiAgent_Scheduler as PSOScheduler
from models.utils import (
    generate_agen_default,
    safe_convert_to_float,
    normalize_id,
    parse_dependensi,
    filter_ghost_dependencies,
    fungsi_biaya_jadwal,
    buat_cost_function_untuk_scheduler,
    validasi_dependensi,
    ada_dependensi_sirkular
)

app = Flask(__name__)
app.start_time = time.time()

# Middleware Header Keamanan
@app.after_request
def add_security_headers(response):
    """
    Menambahkan header keamanan ke setiap respons HTTP.
    
    Header yang ditambahkan meliputi:
    - Content-Security-Policy (CSP): Mengontrol sumber daya yang diizinkan dimuat.
    - X-Frame-Options: Mencegah clickjacking (SAMEORIGIN).
    - X-Content-Type-Options: Mencegah MIME sniffing.
    - Strict-Transport-Security (HSTS): Memaksa HTTPS (jika di production).
    - Cache-Control: Mengatur caching berdasarkan endpoint (no-cache untuk simulasi).
    
    Args:
        response (Response): Objek respons Flask.
        
    Returns:
        Response: Objek respons yang telah dimodifikasi dengan header keamanan.
    """
    # Content Security Policy (CSP) Header
    response.headers['Content-Security-Policy'] = (
        "default-src 'self' 'unsafe-inline' 'unsafe-eval' data: blob: https:; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://unpkg.com https://*.vercel.app https://*.vanila.app; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com https://*.vercel.app https://*.vanila.app; "
        "font-src 'self' data: https://fonts.gstatic.com https://*.vercel.app https://*.vanila.app; "
        "img-src 'self' data: blob: https: http:; "
        "connect-src 'self' http://localhost:* http://127.0.0.1:* https: wss: ws:; "
        "media-src 'self' data: blob: https:; "
        "object-src 'self' data:; "
        "base-uri 'self'; "
        "form-action 'self' https:; "
        "frame-ancestors 'self'"
    )
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers.pop('Server', None)
    response.headers.pop('X-Powered-By', None)
    response.headers['Server'] = 'nginx'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=(), payment=(), usb=(), magnetometer=()'
    
    if request.endpoint:
        if 'health' in request.endpoint or request.endpoint == 'home':
            response.headers['Cache-Control'] = 'public, max-age=300'
        elif 'simulate' in request.endpoint or 'algorithm' in request.endpoint:
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
        else:
            response.headers['Cache-Control'] = 'public, max-age=60, must-revalidate'
    else:
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    
    return response

# Konfigurasi CORS
CORS(app, 
     origins=[
         'http://localhost:3000', 
         'http://127.0.0.1:3000', 
         'http://0.0.0.0:3000',
         'http://frontend:3000',
         'http://127.0.0.1:3001', 
         'http://localhost:5000', 
         'http://127.0.0.1:5000',
         'http://localhost:5001', 
         'http://127.0.0.1:5001',
         'https://swarmwave.vercel.app',
         'https://swarmwave.vanila.app',
         'https://*.vanila.app',
         'https://*.vercel.app',
         'https://swarmwave.app',
         'https://www.swarmwave.app'
     ], 
     supports_credentials=True, 
     allow_headers=['Content-Type', 'Authorization', 'Accept', 'Origin', 'X-Requested-With', 'Access-Control-Request-Method', 'Access-Control-Request-Headers'], 
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'],
     expose_headers=['Content-Range', 'X-Content-Range'],
     max_age=86400
)

@app.before_request
def handle_preflight():
    """
    Menangani request OPTIONS untuk keperluan CORS Preflight.
    
    Browser modern mengirim request OPTIONS sebelum request actual (POST/PUT/DELETE)
    untuk memverifikasi izin CORS.
    
    Returns:
        Response: Respons kosong dengan header Access-Control-Allow-* yang sesuai.
    """
    if request.method == "OPTIONS":
        response = Response()
        response.headers.add("Access-Control-Allow-Origin", request.headers.get('Origin', '*'))
        response.headers.add('Access-Control-Allow-Headers', "Content-Type, Authorization, Accept, Origin, X-Requested-With")
        response.headers.add('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS, PATCH")
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

@app.errorhandler(Exception)
def handle_cors_error(e):
    """
    Global Error Handler yang tetap menyertakan header CORS.
    
    Memastikan bahwa jika terjadi error 500/400, browser tetap menerima header CORS
    sehingga pesan error bisa dibaca oleh frontend (tidak terblokir CORS policy).
    
    Args:
        e (Exception): Exception yang terjadi.
        
    Returns:
        tuple: (JSON Response, HTTP Status Code)
    """
    response = jsonify({
        "error": "Internal server error",
        "message": "An error occurred while processing your request",
        "status": "error"
    })
    origin = request.headers.get('Origin')
    allowed_origins = [
        'http://localhost:3000', 'http://127.0.0.1:3000', 'http://0.0.0.0:3000',
        'http://frontend:3000', 'https://swarmwave.vercel.app', 'https://swarmwave.vanila.app'
    ]
    if origin in allowed_origins:
        response.headers.add("Access-Control-Allow-Origin", origin)
    return response, 500

@app.route('/')
def home():
    """
    Endpoint root untuk pengecekan sederhana apakah server berjalan.
    
    Returns:
        JSON: Pesan status server.
    """
    return jsonify({"message": "Multi-Agent Task Scheduling API is running"})

@app.route('/health')
def health_check():
    """
    Endpoint Health Check untuk monitoring status sistem.
    
    Memberikan informasi mendalam tentang:
    - Status server & Uptime.
    - Info Sistem (OS, Python version).
    - Status ketersediaan algoritma (ACO, PSO) dengan melakukan test run dummy.
    
    Returns:
        JSON: Laporan kesehatan sistem lengkap.
    """
    try:
        current_time = time.time()
        uptime = current_time - app.start_time if hasattr(app, 'start_time') else 0
        
        system_info = {
            "platform": platform.system(),
            "architecture": platform.machine(),
            "python_version": platform.python_version()[:3],
        }
        
        app_info = {
            "name": "Swarm Wave Backend API",
            "version": "1.0.0",
            "status": "healthy",
            "timestamp": current_time,
            "datetime": datetime.fromtimestamp(current_time).isoformat(),
            "uptime_seconds": round(uptime, 2),
            "environment": os.getenv('FLASK_ENV', 'production'),
        }
        
        algorithms_status = {}
        try:
            test_tasks = [{"id": "test", "length": 1}]
            test_agents = [{"id": "test-agent"}]
            ACOScheduler(tasks=test_tasks, agents=test_agents, cost_function=lambda x, y: y, heuristic_function=lambda x: 1.0, n_iterations=1)
            algorithms_status["ACO"] = {"available": True, "status": "operational"}
        except Exception as e:
            algorithms_status["ACO"] = {"available": False, "error": str(e)}
        
        try:
            PSOScheduler(tasks=test_tasks, agents=test_agents, cost_function=lambda x, y: y, n_iterations=1)
            algorithms_status["PSO"] = {"available": True, "status": "operational"}
        except Exception as e:
            algorithms_status["PSO"] = {"available": False, "error": str(e)}
        
        response_data = {
            "status": "healthy",
            "health_score": 100,
            "timestamp": current_time,
            "application": app_info,
            "system": system_info,
            "algorithms": algorithms_status
        }
        
        response = jsonify(response_data)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
        
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route('/stream_scheduling', methods=['POST'])
def stream_scheduling():
    """
    Endpoint utama untuk menjalankan simulasi penjadwalan dengan Streaming Response (SSE).
    
    Menerima data tugas dan parameter, melakukan normalisasi, validasi dependensi,
    dan menjalankan algoritma optimasi (ACO/PSO) secara real-time.
    
    Proses:
    1. Parsing Input: Normalisasi nama kolom dan tipe data.
    2. Auto-Detect Dependencies: Mengaktifkan mode dependensi jika data ditemukan.
    3. Validasi Dependensi: Cek circular dependency (return 400 jika ada).
    4. Inisialisasi Scheduler: Setup ACO atau PSO dengan parameter yang sesuai.
    5. Streaming: Mengirim update progress per iterasi ke klien menggunakan generator.
    
    Args (JSON Body):
        tasks (list): Daftar tugas (task_id, duration, priority, dependencies, dll).
        parameters (dict): Konfigurasi simulasi (num_agents, n_iterations, algorithm-specific params).
        algorithm (str): 'ACO' atau 'PSO'.
        
    Returns:
        Response: Stream text/event-stream berisi update JSON per baris.
    """
    try:
        data = request.get_json()
        if not data: return jsonify({"error": "No data provided"}), 400
        
        tasks = data.get('tasks', data.get('tasks_data', []))
        parameters = data.get('parameters', {})
        if not tasks: return jsonify({"error": "No tasks provided"}), 400
        
        print(f"🔍 DEBUG: Received {len(tasks)} tasks from frontend")
        
        algorithm = data.get('algorithm', '').upper()
        if not algorithm: return jsonify({"error": "Algorithm not specified"}), 400

        # Ekstraksi Parameter
        num_default_agents = parameters.get('num_default_agents', 10)
        n_iterations = parameters.get('n_iterations', 100)
        task_id_col_for_scheduler = parameters.get('task_id_col', 'id')
        task_id_col_for_scheduler = parameters.get('task_id_col', 'id')
        agent_id_col_for_scheduler = parameters.get('agent_id_col', 'id')
        dependency_col_for_scheduler = parameters.get('dependency_col', '')
        
        # Pengaturan Random Seed
        random_seed = parameters.get('random_seed', 42)
        random.seed(random_seed)
        np.random.seed(random_seed)
        
        # Parameter Spesifik Algoritma
        n_ants = parameters.get('n_ants', 50)
        alpha = parameters.get('alpha', 0.9)
        beta = parameters.get('beta', 2)
        evaporation_rate = parameters.get('evaporation_rate', 0.3)
        pheromone_deposit = parameters.get('pheromone_deposit', 100)
        
        n_particles = parameters.get('n_particles', 50)
        w = parameters.get('w', 0.3)
        c1 = parameters.get('c1', 0.3)
        c2 = parameters.get('c2', 0.4)
        
        enable_dependencies = parameters.get('enable_dependencies', None)

        # --- NORMALISASI DATA TUGAS ---
        formatted_tasks = []
        flexible_task_id_candidates = ['Task_ID', 'TaskID', 'task_id', 'id', 'ID', 'name', 'Name']

        for i, task in enumerate(tasks):
            # Normalisasi ID
            task_id_value = None
            for field in flexible_task_id_candidates:
                if field in task and task[field] is not None:
                    raw_val = task[field]
                    if str(raw_val).strip():
                        task_id_value = normalize_id(raw_val)
                        break
            
            # Fallback ID (Pakai index+1 agar lebih aman untuk dataset numerik)
            if not task_id_value: 
                task_id_value = str(i + 1)

            # Field Numerik
            task_length = None
            for field in ['Duration', 'duration', 'length', 'Length', 'Weight', 'weight', 'execution_time', 'Execution_Time (s)']:
                if field in task:
                    task_length = safe_convert_to_float(task[field])
                    if task_length > 0: break
            if task_length is None or task_length <= 0: task_length = 1.0
            
            cost = 0.0
            for field in ['Cost', 'cost', 'price', 'Price']:
                if field in task:
                    cost = safe_convert_to_float(task[field])
                    if cost >= 0: break
            
            priority = safe_convert_to_float(task.get('Priority', task.get('priority', 1)), 1)
            cpu_usage = safe_convert_to_float(task.get('CPU_Usage', task.get('cpu_usage', 0)), 0)
            ram_usage = safe_convert_to_float(task.get('RAM_Usage', task.get('ram_usage', 0)), 0)
            
            # Normalisasi Dependensi (menggunakan utils)
            dependencies = None
            
            # Prioritas Utama: Gunakan kolom yang dipilih user
            if dependency_col_for_scheduler and dependency_col_for_scheduler in task:
                 dependencies = task[dependency_col_for_scheduler]
            
            # Alternatif: Cari otomatis jika belum ketemu
            # Alternatif: Cari otomatis jika belum ketemu, TAPI hanya jika user tidak mematikan dependensi
            if dependencies is None and enable_dependencies is not False:
                for field in ['dependencies', 'Dependencies', 'depends_on', 'prerequisites', 'requires', 'dependensi', 'Dependensi']:
                    if field in task and task[field] is not None:
                        dependencies = task[field]
                        break
            
            # Gunakan parse_dependensi untuk list, atau handle langsung
            if isinstance(dependencies, str):
                normalized_deps = parse_dependensi(dependencies)
            elif isinstance(dependencies, (list, tuple)):
                normalized_deps = [normalize_id(d) for d in dependencies 
                                   if d is not None and str(d).lower() not in ['null', 'nan', 'none', '']]
            elif isinstance(dependencies, (int, float)):
                normalized_deps = [normalize_id(dependencies)]
            else:
                normalized_deps = []
            
            formatted_task = {
                task_id_col_for_scheduler: task_id_value,
                'length': task_length, 
                'cost': cost,
                'priority': priority,
                'cpu_usage': cpu_usage,
                'ram_usage': ram_usage,
                'dependencies': normalized_deps
            }
            
            # Salin field yang tersisa
            for key, value in task.items():
                if key not in formatted_task:
                    if isinstance(value, (int, float)):
                        formatted_task[key] = safe_convert_to_float(value, 0)
                    else:
                        formatted_task[key] = str(value).strip() if value else ''
            
            formatted_tasks.append(formatted_task)
        
        # --- DETEKSI OTOMATIS DEPENDENSI ---
        # Jika ada data dependensi, kita PAKSA nyalakan, karena user sudah memilih kolomnya.
        has_dependencies = any(len(t['dependencies']) > 0 for t in formatted_tasks)
        
        if has_dependencies:
            if not enable_dependencies:
                print("Auto-enabling dependencies (Force) because dependency data was found.")
            enable_dependencies = True
        
        # Pastikan boolean
        enable_dependencies = bool(enable_dependencies)
        
        # Filter ghost dependencies menggunakan fungsi dari utils
        if enable_dependencies and len(formatted_tasks) > 0:
            count_removed = filter_ghost_dependencies(formatted_tasks, task_id_col_for_scheduler)

            # --- VALIDASI DEPENDENSI SIRKULAR ---
            is_valid, masalah_dependensi = validasi_dependensi(formatted_tasks, task_id_col_for_scheduler)
            if not is_valid:
                error_msg = "Dependency Error: " + "; ".join(masalah_dependensi)
                print(f"{error_msg}")
                return jsonify({"error": error_msg}), 400
        
        # --- GENERASI AGEN DETERMINISTIK ---
        agents = parameters.get('agents')
        
        if not agents:
            agents = generate_agen_default(num_default_agents, agent_id_col_for_scheduler)
            print(f"DEBUG: Generated {len(agents)} deterministic agents.")
        
        # Fungsi Biaya (menggunakan utils)
        bobot_waktu = parameters.get('bobot_waktu', 1.0)
        bobot_keseimbangan_beban = parameters.get('bobot_keseimbangan_beban', 1.0)
        cost_function = buat_cost_function_untuk_scheduler(bobot_waktu, bobot_keseimbangan_beban)

        def heuristic_function(task):
            duration = max(task.get('length', 1), 0.1)
            priority = max(task.get('priority', 1), 1.0)
            return (1.0 / duration) * priority
        
        # Inisialisasi Scheduler
        scheduler = None
        if algorithm == 'ACO':
            scheduler = ACOScheduler(
                tasks=formatted_tasks, cost_function=cost_function,
                heuristic_function=heuristic_function, agents=agents,
                n_ants=n_ants, n_iterations=n_iterations, alpha=alpha, beta=beta,
                evaporation_rate=evaporation_rate, pheromone_deposit=pheromone_deposit,
                task_id_col=task_id_col_for_scheduler, agent_id_col=agent_id_col_for_scheduler,
                enable_dependencies=enable_dependencies, random_seed=random_seed,
                num_default_agents=num_default_agents
            )
        elif algorithm == 'PSO':
            scheduler = PSOScheduler(
                tasks=formatted_tasks, agents=agents, cost_function=cost_function,
                n_particles=n_particles, n_iterations=n_iterations, w=w, c1=c1, c2=c2,
                task_id_col=task_id_col_for_scheduler, agent_id_col=agent_id_col_for_scheduler,
                enable_dependencies=enable_dependencies, random_seed=random_seed,
                num_default_agents=num_default_agents
            )
        else:
            return jsonify({"error": f"Unsupported algorithm: {algorithm}"}), 400

        # Fungsi Generator dengan penanganan diskoneksi klien
        def generate():
            start_time = time.time()
            final_result = None
            algorithm_computation_time = 0
            cancelled = False
            
            try:
                initial_data = {"type": "start", "message": f"Starting {algorithm} simulation..."}
                yield f"data: {json.dumps(initial_data)}\n\n"
                
                iteration_count = 0

                for data_chunk in scheduler.run():
                    yield f"data: {data_chunk}\n\n"
                    
                    iteration_count += 1
                    if iteration_count % 10 == 0:
                        yield f": keepalive {iteration_count}\n\n"
                    
                    try:
                        chunk_obj = json.loads(data_chunk)
                        if chunk_obj.get("type") == "done":
                            final_result = chunk_obj
                            algorithm_computation_time = chunk_obj.get('computation_time', 0)
                    except json.JSONDecodeError:
                        continue
            except GeneratorExit:
                # Klien terputus - hentikan proses
                cancelled = True
                print(f"[INFO] Client disconnected, stopping {algorithm} simulation")
                return
            
            if cancelled:
                return
            
            try:
                total_execution_time = time.time() - start_time
                load_balance_index = final_result.get('load_balance_index', 0)

                schedule_data = final_result.get('schedule', [])
                full_schedule_table = {
                    "columns": ["task_id", "agent_id", "start_time", "finish_time"],
                    "data": [[item.get('task_id'), item.get('agent_id'), 
                             round(item.get('start_time', 0), 2), 
                             round(item.get('finish_time', 0), 2)] 
                            for item in schedule_data],
                    "total_rows": len(schedule_data)
                }
                
                agent_finish_times = final_result.get('agent_finish_times', {})
                agent_info_table = {
                    "columns": ["agent_id", "type", "capacity", "efficiency", "total_tasks", "finish_time"],
                    "data": []
                }
                
                for agent in agents:
                    agent_id = agent.get(agent_id_col_for_scheduler)
                    agent_tasks = [s for s in schedule_data if s.get('agent_id') == agent_id]
                    agent_info_table["data"].append([
                        agent_id,
                        agent.get('type', 'N/A'),
                        round(agent.get('capacity', 1.0), 2),
                        round(agent.get('efficiency', 1.0), 2),
                        len(agent_tasks),
                        round(agent_finish_times.get(agent_id, 0), 2)
                    ])
                agent_info_table["total_rows"] = len(agent_info_table["data"])
                
                final_metrics = {
                    "type": "final_metrics",
                    "total_execution_time": round(total_execution_time * 1000, 2),
                    "computation_time": algorithm_computation_time,
                    "load_balance_index": load_balance_index,
                    "full_schedule_table": full_schedule_table,
                    "agent_info_table": agent_info_table,
                    "full_result": {
                        "algorithm": algorithm,
                        "schedule": schedule_data,
                        "makespan": final_result.get('makespan', 0),
                        "load_balance_index": load_balance_index,
                        "computation_time": algorithm_computation_time,
                        "agent_finish_times": final_result.get('agent_finish_times', {}),
                        "iteration_history": final_result.get('iteration_history', []),
                        "total_tasks": len(schedule_data),
                        "total_agents": len(final_result.get('agent_finish_times', {})),
                        "timestamp": datetime.now().isoformat(),
                        "parameters": {
                            "enable_dependencies": enable_dependencies,
                            "random_seed": random_seed,
                            "n_iterations": n_iterations,
                            "num_agents": num_default_agents
                        }
                    }
                }
                
                if algorithm == 'ACO':
                    final_metrics["full_result"]["parameters"].update({
                        "n_ants": n_ants, "alpha": alpha, "beta": beta,
                        "evaporation_rate": evaporation_rate, "pheromone_deposit": pheromone_deposit
                    })
                elif algorithm == 'PSO':
                    final_metrics["full_result"]["parameters"].update({
                        "n_particles": n_particles, "w": w, "c1": c1, "c2": c2
                    })
                
                yield f"data: {json.dumps(final_metrics)}\n\n"
            except GeneratorExit:
                print(f"[INFO] Client disconnected during final metrics")
                return

        response = Response(generate(), mimetype='text/event-stream')
        response.headers['Cache-Control'] = 'no-cache, no-transform'
        response.headers['X-Accel-Buffering'] = 'no'
        response.headers['Connection'] = 'keep-alive'
        return response

    except Exception as e:
        error_details = {"type": "error", "message": str(e), "traceback": traceback.format_exc()}
        return Response(f"data: {json.dumps(error_details)}\n\n", mimetype='text/event-stream')

@app.route('/health/simple')
def simple_health_check():
    return jsonify({"status": "ok", "timestamp": time.time()})

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
    port = int(os.getenv('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port, threaded=True)