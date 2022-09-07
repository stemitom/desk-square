FROM python:3.9-slim-buster

# set work directory
WORKDIR /code

# environmental variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2-binary
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && apt-get -y install netcat

# install poetry
RUN pip install poetry==1.1.13

# copy project
COPY . .

# add executable permissions to wait-for-postgres and entrypoint
RUN chmod +x /code/wait-for-postgres.sh
RUN chmod +x /code/entrypoint.sh

# RUN poetry install system
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

ENTRYPOINT ["/code/entrypoint.sh"]