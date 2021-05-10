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

package-install:
	pip install --user --force-reinstall dist/hexlet_code-0.1.0-py3-none-any.whl