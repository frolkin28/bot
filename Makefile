freeze:
	pip freeze > requirements.txt
migrate:
	alembic revision --autogenerate -m "$(message)"; alembic upgrade head
