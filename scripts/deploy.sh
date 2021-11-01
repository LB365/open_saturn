saturn template-config-file
PROPER="${DATABASE_URL//postgres/postgresql}"
tsh init-db --no-dry-run
tsh formula-init-db $PROPER
rework init-db $PROPER
