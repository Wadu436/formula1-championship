#!/bin/bash

# Adapted from: 
# https://stackoverflow.com/questions/24718706/backup-restore-a-dockerized-postgresql-database
# https://stackoverflow.com/questions/19331497/set-environment-variables-from-file-of-key-value-pairs/30969768#30969768
# https://unix.stackexchange.com/questions/511127/bash-list-possible-files-and-select-one

set -o allexport
source .env.prod.db
set +o allexport

CONTAINER=$(docker-compose -f docker-compose.prod.yml ps -q db)

backups=( "./backup/"*.pg_bak )

PS3='Select file to upload, or 0 to exit: '
select backup in "${backups[@]}"; do
    if [[ $REPLY == "0" ]]; then
        echo 'Bye!' >&2
        exit
    elif [[ -z $backup ]]; then
        echo 'Invalid choice, try again' >&2
    else
        break
    fi
done

docker cp $backup $CONTAINER:/db.dump
docker exec -ti $CONTAINER pg_restore -U $POSTGRES_USER -c -d $POSTGRES_DB db.dump