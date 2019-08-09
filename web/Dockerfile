FROM alpine:3.10

MAINTAINER Your Name "w.lulek@gmail.com"

RUN apk update && apk add postgresql-dev gcc musl-dev
RUN apk add --no-cache python3-dev \
	&& pip3 install --upgrade pip


COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["main.py"]
