web: gunicorn app:app
heroku-postbuild: |
  echo "Creating database tables..."
  psql $DATABASE_URL < data/structure.sql