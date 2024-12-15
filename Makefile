.PHONY: install format lint test build-image deploy clean

install:
	pip install -e ".[dev]"

format:
	black src tests
	isort src tests

lint:
	mypy src tests
	pylint src tests

test:
	pytest tests -v --cov=src

build-image:
	./scripts/build_image.sh

deploy:
	./scripts/deploy.sh

clean:
	rm -rf build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
