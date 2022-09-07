.PHONY: install format lint 

install:
	poetry install --no-root
format:
	blue .
	isort .
lint:
	blue --check .
	isort --check .
	prospector