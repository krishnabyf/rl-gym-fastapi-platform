.PHONY: install test lint run docker

install:
	python3 -m pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check .

run:
	uvicorn app.main:app --reload

docker:
	docker compose up --build

