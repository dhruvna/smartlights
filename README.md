Full Install:
python -m pip install -e ".[dev]"

Validation:
ruff format .
ruff check --fix .
python -m pytest
ruff check .
ruff format --check .
mypy

