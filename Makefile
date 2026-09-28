.PHONY: setup test lint fmt run build scan docs
setup:            ## install deps and git hooks
	uv sync
	uv run pre-commit install
test:
	uv run pytest
lint:
	uv run ruff check . && uv run ruff format --check .
fmt:
	uv run ruff check --fix . && uv run ruff format .
run:
	uv run python -m app.main
build:
	docker build -t app:dev .
scan:             ## scan full git history for secrets
	docker run --rm -v "$$(pwd):/repo" zricethezav/gitleaks:latest git /repo
docs:             ## preview the docs site locally
	uv run --group docs mkdocs serve
