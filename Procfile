release: bash scripts/release.sh
worker: bash scripts/worker.sh
scheduler: saturn start-scheduler
web: gunicorn open_saturn.wsgi:app
