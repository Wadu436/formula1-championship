# Development
To start development Docker environment, run `docker-compose up -d`. The development server will run on port 8000.

When changing dependencies, it is necessary to rebuild the image. Run `docker-compose up -d --build` instead.

When the container starts, it flushes the database, applies migrations, then runs `data_entry.py` to populate the database, and finally creates a superuser account.

# Production
First, create `.env.prod` and `.env.prod.db`. Examples can be found in `.env.prod.example` and `.env.prod.db.example`.

To start the production Docker environment, run `docker-compose -f ./docker-compose.prod.yml up -d --build`. By default, the production server will run on port 80.

Don't forget to migrate and collect static files!
```sh
# Migrate
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput

# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput --clear
```

Finally, create a superuser to access the admin panel.
```
# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```
