run:
	poetry run python -m albumbot

lint:
	poetry run black -q -l 120 .
	poetry run isort .
	poetry run pyflakes .
	poetry run flake8
	poetry run mypy --ignore-missing-imports .
