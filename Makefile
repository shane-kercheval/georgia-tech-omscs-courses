####
# DOCKER
####
docker_build:
	docker compose -f docker-compose.yml build

docker_run: docker_build
	docker compose -f docker-compose.yml up

docker_down:
	docker compose down --remove-orphans

docker_rebuild:
	docker compose -f docker-compose.yml build --no-cache

####
# Project
####
linting:
	ruff check cli.py

scape_omscs_courses:
	python source/cli.py scrape-omscs-courses

scape_omscs_specializations:
	python source/cli.py scrape-omscs-specializations

scrape: scape_omscs_courses scape_omscs_specializations

recommendation:
	python source/cli.py recommend

recommendation_local:
	python source/cli.py recommend --use-local-server

all: scrape recommendation

all_local: scrape recommendation_local

docker_recommend:
	docker compose run --no-deps --entrypoint "make all" bash

docker_recommend_local:
	docker compose run --no-deps --entrypoint "make all_local" bash
