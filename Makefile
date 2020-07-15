build:
	docker-compose build

run:
	docker-compose up -d

start:
	make build; make run; make upgrade

freeze:
	pip freeze > requirements.txt

migrate_n_upgrade:
	docker-compose exec taxibot_bot alembic revision --autogenerate -m "$(message)"; alembic upgrade head

upgrade:
	docker exec taxibot_bot alembic upgrade head
