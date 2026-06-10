<!-- ./src/back_end/README.md -->

# `./src/back_end/` Folder

Here lives the Python code for the backend. Think of this as a repo in itself.

## Getting started

From inside the dev container:

```bash
cd src/back_end
uv sync            # install dependencies into .venv
uv run pytest      # run the test suite
uv run mypy engine # type-check
uv run ruff check  # lint
```

## Layout

- `engine/` - our package (all the real code)
- `tests/` - pytest tests, one test file per engine module
- `pyproject.toml` - dependencies and tool config (Ruff, mypy, pytest)