"""
Gunicorn configuration for Swarm Wave Backend
Optimized for real-time SSE streaming
"""
import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"
backlog = 2048

# Worker processes
workers = int(os.getenv('GUNICORN_WORKERS', '2'))
worker_class = 'gthread'  # Use threaded workers for better streaming support
threads = int(os.getenv('GUNICORN_THREADS', '4'))
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100

# Timeouts (increased for long-running streaming)
timeout = 600  # 10 minutes for long simulations
graceful_timeout = 30
keepalive = 5

# Logging
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log to stderr
loglevel = os.getenv('LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'swarm-wave-backend'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (if needed in production)
keyfile = os.getenv('SSL_KEY_FILE', None)
certfile = os.getenv('SSL_CERT_FILE', None)

# Performance tuning for streaming
worker_tmp_dir = '/dev/shm'  # Use shared memory for better performance

# Preload application for better memory usage
preload_app = False  # Set to False to avoid issues with streaming

# Server hooks for debugging
def on_starting(server):
    """Called just before the master process is initialized."""
    print("🚀 Swarm Wave Backend is starting...")

def on_reload(server):
    """Called to recycle workers during a reload via SIGHUP."""
    print("♻️  Reloading workers...")

def when_ready(server):
    """Called just after the server is started."""
    print(f"✅ Server is ready. Listening on {bind}")
    print(f"   Workers: {workers} | Threads per worker: {threads}")
    print(f"   Timeout: {timeout}s | Worker class: {worker_class}")

def worker_int(worker):
    """Called just after a worker exited on SIGINT or SIGQUIT."""
    print(f"⚠️  Worker received INT or QUIT signal: pid={worker.pid}")

def worker_abort(worker):
    """Called when a worker receives the SIGABRT signal."""
    print(f"❌ Worker received ABORT signal: pid={worker.pid}")
