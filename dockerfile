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

# install poetry and copy pipfile, pipfile.lock
RUN pip install poetry==1.1.13
COPY ./poetry.lock .
COPY ./pyproject.toml .

# RUN poetry install system
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# copy and add executable permissions to wait-for-postgres and entrypoint
COPY ./wait-for-postgres.sh .
COPY ./entrypoint.sh .
RUN chmod +x /code/wait-for-postgres.sh
RUN chmod +x /code/entrypoint.sh

COPY . .

ENTRYPOINT ["/code/entrypoint.sh"]