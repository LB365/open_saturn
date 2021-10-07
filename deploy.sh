PROPER="${DATABASE_URL//postgres/postgresql}"
tsh init-db
tsh formula-init-db $PROPER
rework init-db $PROPER
tsh register-tasks
