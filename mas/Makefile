# Makefile
.PHONY:
install:
	poetry run pip install 'cython<3.0.0'
	poetry run pip install wheel
	poetry run pip install pyyaml==5.4.1 --no-build-isolation -v
	poetry install --no-root


.PHONY: clean
clean: clean-build clean-pyc clean-test clean-docs

.PHONY: clean-build
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr deployments/build/
	rm -fr deployments/Dockerfiles/open_aea/packages
	rm -fr pip-wheel-metadata
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +
	find . -name '*.svn' -exec rm -fr {} +
	find . -name '*.db' -exec rm -fr {} +
	rm -fr .idea .history
	rm -fr venv

.PHONY: clean-docs
clean-docs:
	rm -fr site/

.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '.DS_Store' -exec rm -fr {} +

.PHONY: clean-test
clean-test:
	rm -fr .tox/
	rm -f .coverage
	find . -name ".coverage*" -not -name ".coveragerc" -exec rm -fr "{}" \;
	rm -fr coverage.xml
	rm -fr htmlcov/
	rm -fr .hypothesis
	rm -fr .pytest_cache
	rm -fr .mypy_cache/
	find . -name 'log.txt' -exec rm -fr {} +
	find . -name 'log.*.txt' -exec rm -fr {} +

.PHONY: hashes
hashes: clean
	poetry run autonomy packages lock
	poetry run adev -v -n 0 lint

lint:
	poetry run adev -v -n 0 lint -co

fmt: 
	poetry run adev -n 0 fmt -co

test:
	poetry run adev -v test

all: fmt lint test hashes

metadata:
	adev metadata generate . contract/eightballer/pwn_simple_loan/0.1.0 01 && adev -v metadata validate mints/01.json
	adev metadata generate . skill/eightballer/collateralisation_station_abci/0.1.0 02 && adev -v metadata validate mints/02.json
	adev metadata generate . skill/eightballer/chained_collateralisation/0.1.0 03 && adev -v metadata validate mints/03.json
	adev metadata generate . agent/eightballer/collateralisation_station/0.1.0 04 && adev -v metadata validate mints/04.json
	adev metadata generate . service/eightballer/collateralisation_station/0.1.0 05 && adev -v metadata validate mints/05.json


