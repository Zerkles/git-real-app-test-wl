# Docker service with Flask web application using Redis and PostgreSQL database.

## To run whole service use:
```
$ docker-compose build
$ docker-compose up
```
## To run one container ("flask" or "postgres") use:
```
$ make build-<container name>
$ make run-<container name>
```
## Basic configuration
* To make postgres and flask run separately, remember to change in flask application host address to localhost. 
* You can also edit initial tables and sample inputs in /postgresql/sql-scripts/
