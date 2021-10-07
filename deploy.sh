echo $DATABASE_URL
tsh init-db $DATABASE_URL
tsh formula-init-db $DATABASE_URL
rework init-db $DATABASE_URL
tsh register-tasks
