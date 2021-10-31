release: saturn register-tasks
worker: bash script/worker.sh
scheduler: saturn start-scheduler
web: gunicorn open_saturn.wsgi:app
