To start development docker environment, run `docker-compose up -d`

When changing dependencies, it is necessary to rebuild the image. Run `docker-compose up -d --build` instead.

When the container starts, it flushes the database, applies migrations, then runs `data_entry.py` to populate the database.
