#!/usr/bin/env bash

set -a
cat > .env.test << EOT
POSTGRES_HOST=0.0.0.0
POSTGRES_PORT=5433
POSTGRES_DB=test
POSTGRES_USER=user
POSTGRES_PASSWORD=password
EOT
docker run -d --rm --name test-timescale -p 5433:5432 --env-file .env.test timescale/timescaledb:1.7.2-pg12
docker exec test-timescale bash -c 'until pg_isready; do sleep 1; done'
sleep 3
source .env.test
alembic upgrade heads
sleep 1
pytest
status=$?
docker stop test-timescale
set +a
[ $status -eq 0 ] || exit 1
