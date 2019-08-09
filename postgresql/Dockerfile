FROM postgres:9.6

# Set environment variables
ENV POSTGRES_USER admin
ENV POSTGRES_PASSWORD admin1234
ENV POSTGRES_DB post_db


COPY ./sql-scripts/ /docker-entrypoint-initdb.d/

#|id BIGINT AUTOINCREMENT|name VARCHAR(32)NOT NULL|available BOOLEAN|
