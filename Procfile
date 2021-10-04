worker: pip install https://hg.sr.ht/~pythonian/tshistory_refinery/archive/0.2.0.tar.gz
worker: tsh init-db DATABASE_URL
worker: tsh formula-init-db DATABASE_URL
worker: rework init-db DATABASE_URL
web: gunicorn open_saturn.wsgi: heroku_app
