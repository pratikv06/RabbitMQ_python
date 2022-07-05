.PHONY: up sh build db

up: db
	docker-compose up

build:
	sudo docker-compose up --build

sh:
	docker-compose exec backend sh

db:
	docker-compose up -d db