flask:
	python3 web/main.py
build-postgres:
	docker build -t db_postgres:latest postgresql/.
run-postgres:
	docker run -d -p 5432:5432 db_postgres:latest
do-postgres:
	docker build -t db_postgres:latest postgresql/.
	docker run -d -p 5432:5432 db_postgres:latest
build-flask:
	docker build -t flask-app:latest web/.
run-flask:
	docker run -it -p 8903:8903 flask-app:latest
do-flask:
	docker build -t flask-app:latest web/.
	docker run -it -p 8903:8903 flask-app:latest
