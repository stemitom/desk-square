LINT_PATHS = ./ manage.py
ISORT_PARAMS = --ignore-whitespace  $(LINT_PATHS)
ISORT_CHECK_PARAMS = --diff --check-only
BLACK_CHECK_PARAMS = --diff --color --check

lint:
	isort $(ISORT_PARAMS) $(ISORT_CHECK_PARAMS)
	flake8 $(LINT_PATHS)
	black $(BLACK_CHECK_PARAMS) ./

force-lint:
	isort $(ISORT_PARAMS)
	flake8 $(LINT_PATHS)
	black ./


run-dev:
	python manage.py runserver

test:
	python manage.py test