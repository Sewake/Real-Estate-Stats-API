export COMPOSE_FILE := docker-compose.yml

build:
	docker compose up -d --build
down:
	docker compose down
migrate:
	docker compose exec web python manage.py migrate