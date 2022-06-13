FROM python:3.9-slim-buster

# environmental variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install poetry
RUN pip install poetry==1.1.13

# install project dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev --no-root

# install project
COPY . .
RUN poetry install --no-dev