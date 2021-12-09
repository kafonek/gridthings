# gridthings
Python library for doing things with Grid-like structures


## Development

This project uses [poetry](https://python-poetry.org/) for dependency management, [pre-commit](https://pre-commit.com/) for linting at commit, [pytest](https://docs.pytest.org/) as a test framework, and [tox](https://github.com/tox-dev/tox) for running tests locally and on Github Actions (CI/CD).  To get started developing against this library, you'll need to be able to install `poetry`, then use `poetry install` and `pre-commit install`.

1. `pip install poetry` on your system Python if it doesn't exist
2. `poetry install`
3. `poetry shell` to activate the poetry environment created at `.venv`
4. `pre-commit install --install-hooks`

All pre-commit hooks will run when you `git commit`, even without pushing to Github.  You can manually check with `pre-commit run --all-files`.  If you need to commit even with `pre-commit` throwing erros, you can override with `git commit --no-verify`.
