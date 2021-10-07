PROPER="${DATABASE_URL//postgres/postgresql}"
echo "heroku uri: $DATABASE_URL; proper heroku uri: $PROPER"
tsh init-db
tsh formula-init-db $PROPER
rework init-db $PROPER
tsh register-tasks
