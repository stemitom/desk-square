# include .env

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: venv
poetry: ## Make a new virtual environment
	python -m pip install --upgrade poetry 

.PHONY: activate	
activate: ## Activate the created environment
	poetry shell	

.PHONY: install
install: activate ## Make venv and install requirements
	poetry install

.PHONY: migrate
migrate: activate## Make and run migrations
	python3 manage.py makemigrations
	python3 manage.py migrate

.PHONY: test
test: ## Run tests
	python3 manage.py test 

.PHONY: run
run: ## Run the Django server
	python3 manage.py runserver

# styling
style: ## Lint the python project
	black .
	flake8
	python3 -m isort .

start: install migrate run ## Install requirements, apply migrations, then start development server
