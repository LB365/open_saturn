PROPER="${DATABASE_URL//postgres/postgresql}"
python ./scripts/kill-workers.py
rework vacuum $PROPER --workers
rework monitor $PROPER --maxworkers 2
