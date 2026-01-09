export COMPOSE_FILE := docker-compose.yml

build:
	docker compose up -d --build
down:
	docker compose down
test:
	docker compose exec web pytest
migrate:
	docker compose exec web python manage.py migrate
createsuperuser:
	docker compose exec web python manage.py createsuperuser
loaddata:
	docker compose exec web python manage.py import_dataset --path data/dataset/dataset_annonces.csv
lint:
	flake8 .
pre_commit_run:
	pre-commit run --all-files
format:
	isort .
	black .