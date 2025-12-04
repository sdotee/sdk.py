# Makefile for SEE Python SDK

.PHONY: help install install-dev test test-cov lint format type-check clean build publish

help:
	@echo "SEE Python SDK - Available commands:"
	@echo "  make install       - Install package dependencies"
	@echo "  make install-dev   - Install package with development dependencies"
	@echo "  make test          - Run tests"
	@echo "  make test-cov      - Run tests with coverage report"
	@echo "  make lint          - Run linters (ruff)"
	@echo "  make format        - Format code with black"
	@echo "  make type-check    - Run type checking with mypy"
	@echo "  make clean         - Remove build artifacts"
	@echo "  make build         - Build distribution packages"
	@echo "  make publish       - Publish to PyPI"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest

test-cov:
	pytest --cov=see --cov-report=term-missing --cov-report=html --cov-report=xml

lint:
	ruff check src/ tests/ examples/

format:
	black src/ tests/ examples/
	ruff check --fix src/ tests/ examples/

type-check:
	mypy src/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

publish: build
	python -m twine upload dist/*
