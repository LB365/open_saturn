export INSTALL_ON_LINUX=1;pip install -e ".[remote, xl]"
tsh init-db DATABASE_URL --no-dry-run