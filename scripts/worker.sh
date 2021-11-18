PROPER="${DATABASE_URL//postgres/postgresql}"
rework vacuum $PROPER --workers
rework monitor $PROPER --maxworkers 3 --minworkers 0 --maxruns 2
