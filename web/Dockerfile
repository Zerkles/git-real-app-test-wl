FROM alpine:3.10

MAINTAINER Your Name "w.lulek@gmail.com"

RUN apk update && apk add postgresql-dev gcc musl-dev
RUN apk add --no-cache python3-dev \
	&& pip3 install --upgrade pip

ENV HOST 0.0.0.0
ENV WEB_PORT 8903
ENV DEBUG True

ENV DB_USER admin
ENV DB_PASSWORD admin1234
ENV DB_HOST database
ENV DB_PORT 5432
ENV DB_NAME post_db

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["main.py"]
