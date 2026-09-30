.PHONY: setup test lint fmt scan docs
setup:            ## install deps and git hooks
	uv sync
	uv run pre-commit install
test:
	uv run pytest
lint:
	uv run ruff check . && uv run ruff format --check .
fmt:
	uv run ruff check --fix . && uv run ruff format .
scan:             ## scan full git history for secrets
	scripts/scan.sh
docs:             ## preview the docs site locally
	uv run --group docs mkdocs serve
