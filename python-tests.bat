poetry run pflake8 .\logging_server &^
poetry run black .\logging_server &^
poetry run isort .\logging_server &^
poetry run mypy .\logging_server &^
poetry run pytest .\tests