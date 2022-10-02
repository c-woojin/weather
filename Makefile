build:
	docker-compose build

up:
	docker-compose up -d app

down:
	docker-compose down --remove-orphans

test: up
	docker-compose run --rm --no-deps --entrypoint=pytest app /tests

logs:
	docker-compose logs app | tail -100

black:
	black .

flake8:
	flake8 .

up-native:
	uvicorn src.weather.entrypoint.main:app --reload

test-native:
	pytest

compile:
	pip install -U pip pip-tools
	pip-compile

install:
	pip install -U pip pip-tools
	pip-sync
	pip install -e src
