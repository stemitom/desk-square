# desk-square
 API for an event management tool (ex. Meetup and EventBrite) written in drf django.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with%20Django-ff69b4.svg?logo=cookiecutter)](/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# Getting Up and Running Locally with Docker

The steps below will get you up and running with a local development environment. All of these commands assume you are in the root of your generated project.

## Prerequisites
- Docker
- Docker-Compose

## Steps
- Clone the repo `git clone https://github.com/stemitom/desk-square`
- Navigate to repo directory `cd desk-square`
- Build and run the docker-compose file `docker-compose up -d build`
- Create a superuser `docker-compose exec web poetry run python manage.py createsuperuser`


# Postman Documentation

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/1f81891a63eb37a94a5e?action=collection%2Fimport)
