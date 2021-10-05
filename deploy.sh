pip install -e.
pip install -e ".[remote]"
export INSTALL_ON_LINUX=1;pip install -e ".[xl]"
tsh init-db DATABASE_URL --no-dry-run