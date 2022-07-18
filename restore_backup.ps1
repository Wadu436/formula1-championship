$File = ".\backup\dump_13-02-2022_22_48_29.pg_bak"

docker cp $File namr1-formula1-db-1:/db.dump
docker exec -it namr1-formula1-db-1 pg_restore -U formula1 -O  -c -d dev db.dump