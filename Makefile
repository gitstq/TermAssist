.PHONY: install test clean build publish lint format

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -e .

# Testing
test:
	python -m pytest tests/ -v

test-coverage:
	python -m pytest tests/ --cov=termassist --cov-report=html

# Linting and formatting
lint:
	flake8 termassist/ tests/
	pylint termassist/

format:
	black termassist/ tests/
	isort termassist/ tests/

# Building
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

build: clean
	python -m build

# Publishing
publish-test: build
	python -m twine upload --repository testpypi dist/*

publish: build
	python -m twine upload dist/*

# Running
run:
	python -m termassist

# Development
dev:
	python -m termassist

# Build executables
build-exe:
	pyinstaller --onefile --name termassist termassist/main.py

build-exe-all:
	pyinstaller --onefile --name termassist-linux termassist/main.py
	pyinstaller --onefile --name termassist-windows --hidden-import=termassist termassist/main.py
	pyinstaller --onefile --name termassist-macos termassist/main.py
