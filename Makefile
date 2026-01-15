# Makefile for Temporal OpenAI Agents SDK

.PHONY: help install check clean test

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make check      - Check if environment is set up correctly"
	@echo "  make test       - Run tests"
	@echo "  make clean      - Remove build artifacts and cache files"

install:
	pip install -r requirements.txt

install-dev:
	pip install -e ".[dev]"

check:
	python check_setup.py

test:
	pytest tests/ -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
