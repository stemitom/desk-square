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

# install project dependencies
COPY poetry.lock pyproject.toml ./
# RUN poetry install --no-dev --no-root
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# copy entrypoint and script to confirm postgres and rabbit are healthy
COPY ./wait-for-postgres.sh .
COPY ./entrypoint.sh .
RUN chmod +x /code/wait-for-postgres.sh
RUN chmod +x /code/entrypoint.sh

# copy project
COPY . .
RUN poetry install --no-dev

ENTRYPOINT ["/code/entrypoint.sh"]