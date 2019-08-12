FROM postgres:9.6

ENV POSTGRES_USER admin
ENV POSTGRES_PASSWORD admin1234
ENV POSTGRES_DB post_db

COPY ./sql-scripts/ /docker-entrypoint-initdb.d/
