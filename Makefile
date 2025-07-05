.PHONY: check
check:
	uvx ruff check --fix
	uv run pyright