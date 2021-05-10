#Makefile

install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

lint:
	poetry run flake8 gendiff

reps:
	poetry show --tree

run:
	poetry run gendiff

run_help:
	poetry run gendiff -h

test:
	poetry run pytest