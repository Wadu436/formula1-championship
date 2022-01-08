#!/bin/bash

# Adapted from: 
# https://stackoverflow.com/questions/24718706/backup-restore-a-dockerized-postgresql-database
# https://stackoverflow.com/questions/19331497/set-environment-variables-from-file-of-key-value-pairs/30969768#30969768
# https://blog.dcycle.com/blog/ae67284c/docker-compose-cp
# https://stackoverflow.com/questions/63934856/why-is-pg-restore-segfaulting-in-docker

set -o allexport
source .env.prod.db
set +o allexport

CONTAINER=$(docker-compose -f docker-compose.prod.yml ps -q db)

docker exec -ti $CONTAINER pg_dump -Fc -f /db.dump -U $POSTGRES_USER $POSTGRES_DB
docker cp $CONTAINER:/db.dump backup/dump_`date +%d-%m-%Y"_"%H_%M_%S`.pg_bak