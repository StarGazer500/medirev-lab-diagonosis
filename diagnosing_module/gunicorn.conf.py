# # gunicorn.conf.py
# from uvicorn.workers import UvicornWorker
# import multiprocessing
# import json

# # Worker Configuration
# worker_class = "uvicorn.workers.UvicornWorker"
# workers = multiprocessing.cpu_count() * 2 + 1  # Common pattern for worker count
# worker_connections = 1000
# timeout = 30
# keepalive = 2

# # Listening
# bind = "0.0.0.0:8000"
# backlog = 2048

# # Logging
# loglevel = "info"
# accesslog = "/var/log/gunicorn/access.log"
# errorlog = "/var/log/gunicorn/error.log"
# access_log_format = json.dumps({
#     "timestamp": "%(t)s",
#     "requestline": "%(r)s",
#     "status": "%(s)s",
#     "body_bytes": "%(b)s",
#     "request_time": "%(L)s",
#     "remote_addr": "%(h)s"
# })

# # Process Naming
# # proc_name = "myproject"
# # pythonpath = "/path/to/your/project"

# # SSL (if terminating SSL at Gunicorn)
# # keyfile = "/path/to/keyfile"
# # certfile = "/path/to/certfile"

# # Worker Tuning
# max_requests = 1000
# max_requests_jitter = 50
# graceful_timeout = 30


from uvicorn.workers import UvicornWorker
import multiprocessing
import json

# Worker Configuration
worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count() * 2 + 1  # Common pattern for worker count
worker_connections = 1000
timeout = 30
keepalive = 2

# Listening
bind = "0.0.0.0:8000"
backlog = 2048

# Logging (Log to stdout)
loglevel = "info"
accesslog = "-"  # Log access requests to stdout
errorlog = "-"   # Log errors to stdout
access_log_format = json.dumps({
    "timestamp": "%(t)s",
    "requestline": "%(r)s",
    "status": "%(s)s",
    "body_bytes": "%(b)s",
    "request_time": "%(L)s",
    "remote_addr": "%(h)s"
})

# Process Naming
# proc_name = "myproject"
# pythonpath = "/path/to/your/project"

# SSL (if terminating SSL at Gunicorn)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Worker Tuning
max_requests = 1000
max_requests_jitter = 50
graceful_timeout = 30
