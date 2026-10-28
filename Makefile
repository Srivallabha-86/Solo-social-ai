PYTHON ?= python3
PIP ?= pip

install:
	$(PIP) install -r requirements.txt

run:
	uvicorn app.main:app --reload

test:
	pytest -q

format:
	black app tests

lint:
	ruff check app tests
