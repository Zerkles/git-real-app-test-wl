flask:
	python3 main.py
build:
	docker build -t dockerized-flask:latest .
run:
	docker run -d -p 8901:8901 dockerized-flask:latest
