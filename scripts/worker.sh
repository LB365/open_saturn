PROPER="${DATABASE_URL//postgres/postgresql}"
rework monitor $PROPER --maxruns 1 --maxworkers 1 --minworkers 0
