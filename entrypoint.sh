#!/bin/sh
bash ./wait-for-postgres.sh

# poetry run python manage.py flush --no-input
# poetry run python manage.py migrate

exec "$@"