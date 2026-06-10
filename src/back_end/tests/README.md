<!-- ./src/back_end/tests/README.md -->

# `./src/back_end/tests/` Folder

Automated tests live here. A test is just a small function that checks your real
code does what you expect. We run them with **pytest**.

## Naming rule

- Test files start with `test_` -> `test_users.py`
- Test functions start with `test_` -> `def test_creates_account():`

pytest finds them automatically by that naming.

## A complete example you can copy

Say `engine/users.py` has this function:

```python
def add(a: int, b: int) -> int:
    """Return the sum of two numbers."""
    return a + b
```

Then `tests/test_users.py` would be:

```python
from engine.users import add


def test_add_two_positive_numbers() -> None:
    """add() should sum two positives."""
    assert add(2, 3) == 5


def test_add_with_zero() -> None:
    """Adding zero changes nothing."""
    assert add(5, 0) == 5
```

`assert` means "this must be true." If it isn't, the test fails and pytest tells
you exactly which line broke.

## Running the tests

From inside the dev container:

```bash
cd src/back_end
uv run pytest          # runs everything
uv run pytest -v       # same, but lists each test by name
```

## Why bother (TDD)

The idea behind Test-Driven Development: write the test *first*, describing what
the code should do, then write the code until the test passes. It feels backward
but it stops bugs early. You don't have to be strict about it — just having tests
at all already protects the team.