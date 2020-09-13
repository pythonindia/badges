PG_DATABASE=badges

initdb:
	createdb $(PG_DATABASE)
	flask db migrate
	flask db upgrade

dropdb:
	dropdb $(PG_DATABASE)

insert-sample-data:
	python -c "from badges.utils import bulk_insert_attendees; bulk_insert_attendees('sample.csv')"

refreshdb: dropdb initdb insert-sample-data

init-dev:
	pip install -r requirements.txt -r requirements-dev.txt

lint:
	black .

dev:
	python run.py
