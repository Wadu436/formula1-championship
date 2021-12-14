FROM python:3.10-slim

# Set workdir
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv
RUN pipenv sync --system

RUN apt update && apt install -y netcat

# copy entrypoint.sh
COPY entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Copy project
COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]