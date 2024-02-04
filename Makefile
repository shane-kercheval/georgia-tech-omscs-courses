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

docker_bash:
	docker compose -f docker-compose.yml up --build bash

docker_open: notebook mlflow_ui zsh

notebook:
	open 'http://127.0.0.1:8888/?token=d4484563805c48c9b55f75eb8b28b3797c6757ad4871776d'

zsh:
	docker exec -it data-science-template-bash-1 /bin/zsh

docker_all:
	docker compose run --no-deps --entrypoint "make all" bash

####
# Project
####
linting:
	ruff check cli.py

unittests:

tests: linting unittests

open_coverage:
	open 'htmlcov/index.html'

data_extract:
	python source/entrypoints/cli.py extract

data_transform:
	python source/entrypoints/cli.py transform

data: data_extract data_transform

explore:
	jupyter nbconvert --execute --to html source/notebooks/datasets.ipynb
	mv source/notebooks/datasets.html output/data/datasets.html
	jupyter nbconvert --execute --to html source/notebooks/data-profile.ipynb
	mv source/notebooks/data-profile.html output/data/data-profile.html

remove_logs:
	rm -f output/log.log

## Run entire workflow.
all: tests remove_logs data explore

## Delete all generated files (e.g. virtual)
clean:
	rm -f data/raw/*.pkl
	rm -f data/raw/*.csv
	rm -f data/processed/*






scape_omscs_courses:
	python source/cli.py scrape-omscs-courses

scape_omscs_specializations:
	python source/cli.py scrape-omscs-specializations

scrape: scape_omscs_courses scape_omscs_specializations
