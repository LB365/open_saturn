release: bash deploy.sh
worker: rework monitor --maxruns 1 --maxworkers 6 --minworkers 0
web: gunicorn open_saturn.wsgi:app
