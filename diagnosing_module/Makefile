
# Collect static files
collect-static:
	python manage.py collectstatic --noinput

start-dev-server: collect-static
	@kill -9 $(shell lsof -t -i :8000) || true
	@gunicorn --worker-class uvicorn.workers.UvicornWorker \
	--workers 2 \
	--bind 127.0.0.1:8000 \
	--log-level debug \
	--reload \
	--error-logfile - \
	--access-logfile - \
	diagnosing_module.asgi:application

# Migrate the database
migrate-db:
	python manage.py makemigrations
	python manage.py migrate



# Create a superuser
create-superuser:
	python manage.py createsuperuser

# Start production server
start-prod-server:
	gunicorn -c gunicorn.conf.py diagnosing_module.asgi:application