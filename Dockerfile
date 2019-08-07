FROM python:2.7

MAINTAINER Your Name "youremail@domain.tld"

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["main.py"]



