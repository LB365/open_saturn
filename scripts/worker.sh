PROPER="${DATABASE_URL//postgres/postgresql}"
rework vacuum $PROPER --workers --tasks --finished
rework monitor $PROPER --maxruns 1 --maxworkers 3 --minworkers 0
