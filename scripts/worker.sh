PROPER="${DATABASE_URL//postgres/postgresql}"
python ./scripts/kill-workers.py
rework monitor $PROPER --maxworkers 6
