.PHONY: up sh down build buildnc db


up: db
	docker-compose up
down:
	docker-compose down

build:
	sudo docker-compose up --build
buildnc:
	docker-compose build --no-cache

sh:
	docker-compose exec backend sh


db:
	docker-compose up -d db