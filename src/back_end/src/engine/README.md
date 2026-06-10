<!-- ./src/back_end/src/engine/README.md -->

# `./src/back_end/src/engine/` Folder

This is the heart of the backend, all our Python code goes here. It's a
"package," which just means a folder Python treats as one importable unit (that's
what the `__init__.py` file marks).

## How code is organized

Put each piece of functionality in its own file (a "module"). For example, the
code for user accounts might live in `users.py`, products in `products.py`, and
so on. Keep files focused: one topic per file.

- `__init__.py` - marks this folder as a package; leave it in place
- `users.py` - (example) account creation, login
- `products.py` - (example) product catalog

## How other files use your code

From a test or another module, you import through the package name `engine`:

```python
from engine.users import create_account
```

## Where the tests go

Every file here should have matching tests in `../tests/`. If you write
`engine/users.py`, write `tests/test_users.py`. See the tests README for a
copy-paste example.