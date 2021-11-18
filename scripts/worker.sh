PROPER="${DATABASE_URL//postgres/postgresql}"
rework vacuum $PROPER --workers --tasks --finished
rework monitor $PROPER --maxworkers 3
