.PHONY: tests
tests: ## run tests with poetry
	poetry run isort .\logging_server\
	poetry run black .\logging_server\
	poetry run pflake8 .\logging_server\
	poetry run mypy .\logging_server\
	poetry run pytest
