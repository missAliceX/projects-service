.EXPORT_ALL_VARIABLES:

POSTGRES_HOST = localhost
POSTGRES_USER = test-user
POSTGRES_PASSWORD = test-password
POSTGRES_DB = test-db

run:
	python3 main.py

resetdb:
	make removedb
	docker run --name postgres \
		-p 5432:5432 \
		-e POSTGRES_HOST=${POSTGRES_HOST} \
		-e POSTGRES_USER=${POSTGRES_USER} \
		-e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
		-e POSTGRES_DB=${POSTGRES_DB} \
		-d postgres

psql:
	docker exec -ti postgres psql \
		-d ${POSTGRES_DB} \
		-U ${POSTGRES_USER} \
		-h ${POSTGRES_HOST}

removedb:
	docker rm -f postgres || true

test:
	coverage run -m pytest
	coverage report -m *.py src/*.py

install:
	pip install pip-upgrader
	pip-upgrade *.txt
	pip install --force-reinstall -U -r requirements.txt
	pip install -r requirements.dev.txt
