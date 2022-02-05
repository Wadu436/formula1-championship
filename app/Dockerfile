## BASE IMAGE
FROM python:3.10-slim as base

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN adduser --system --group app 

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN chown app:app $APP_HOME
WORKDIR $APP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN pip install pipenv
RUN apt update && apt install -y netcat

COPY Pipfile Pipfile.lock ./
RUN pipenv sync --system

# Copy project
COPY leaderboard leaderboard
COPY project project
COPY manage.py .

## DEVELOPMENT IMAGE
FROM base as develop

RUN pipenv sync --system --dev

COPY data_entry.py entrypoint.sh ./

RUN sed -i 's/\r$//g' ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

USER app

ENTRYPOINT ["./entrypoint.sh"]

## PRODUCTION IMAGE
FROM base as production

COPY entrypoint.prod.sh ./

RUN sed -i 's/\r$//g' ./entrypoint.prod.sh
RUN chmod +x ./entrypoint.prod.sh

USER app

RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles

ENTRYPOINT ["./entrypoint.prod.sh"]