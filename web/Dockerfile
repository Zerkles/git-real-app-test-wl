FROM alpine:3.10
MAINTAINER Your Name "w.lulek@gmail.com"

#Variables for setting up Flask
ENV HOST 0.0.0.0
ENV WEB_PORT 8903
ENV DEBUG False

#Variables used to connect with Postgresql database
ENV DB_USER admin
ENV DB_PASSWORD admin1234
ENV DB_HOST 0.0.0.0
ENV DB_PORT 5432
ENV DB_NAME post_db

RUN apk update && apk add postgresql-dev gcc musl-dev
RUN apk add --no-cache python3-dev && apk add make

WORKDIR /app
COPY . /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install -r requirements-dev.txt

#RUN make code-quality-check

CMD python3 main.py
