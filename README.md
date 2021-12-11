# gridthings
Python library for doing things with Grid-like structures

[![Tests](https://github.com/kafonek/gridthings/actions/workflows/run-tests.yaml/badge.svg)](https://github.com/kafonek/gridthings/actions/workflows/run-tests.yaml) [![Coverage Status](https://coveralls.io/repos/github/kafonek/gridthings/badge.svg?branch=main)](https://coveralls.io/github/kafonek/gridthings?branch=main) [![PyPI version](https://badge.fury.io/py/gridthings.svg)](https://badge.fury.io/py/gridthings)

## Use-Cases

 - Read grid-like data in multiple formats, including string, and easily export to DataFrames
 - Solve puzzles like [largest product in a grid](https://projecteuler.net/problem=11) and [low points in a grid](https://adventofcode.com/2021/day/9)
 - Build board games like tic-tac-toe, connect-four, and bingo
 - Analyze tabular data in interesting new ways

## Example

See the `./examples` directory for solutions to a few puzzles with comments about how `gridthings` helps solve them.

```python
import gridthings

data = '''
123
456
789
'''

grid = gridthings.IntGrid(data)
grid
<IntGrid shape=(3, 3)>

import pandas
df = pandas.DataFrame(grid.values())
df
>>>
        0	1	2
    0	1	2	3
    1	4	5	6
    2	7	8	9

grid.get(1, 1)
>>> IntCell(y=1, x=1, value=5)

grid.peek_linear(1, 1)
>>> <Collection [[IntCell(y=1, x=0, value=4), IntCell(y=1, x=2, value=6), IntCell(y=0, x=1, value=2), IntCell(y=2, x=1, value=8)]]>

sum(grid.peek_linear(1, 1))
>>> 20

max(grid.peek_linear(1, 1))
>>> IntCell(y=2, x=1, value=8)

max(grid.peek_diagonal(1, 1))
>>> IntCell(y=2, x=2, value=9)
```


## Development

This project uses [poetry](https://python-poetry.org/) for dependency management, [pre-commit](https://pre-commit.com/) for linting at commit, [pytest](https://docs.pytest.org/) as a test framework, and [tox](https://github.com/tox-dev/tox) for running tests locally and on Github Actions (CI/CD).  To get started developing against this library, you'll need to be able to install `poetry`, then use `poetry install` and `pre-commit install`.

1. `pip install poetry` on your system Python if it doesn't exist
2. `poetry install`, or `poetry install -E examples` to include Jupyter and pandas, used in the example notebooks
3. `poetry shell` to activate the poetry environment created at `.venv`
4. `pre-commit install --install-hooks`

All pre-commit hooks will run when you `git commit`, even without pushing to Github.  You can manually check with `pre-commit run --all-files`.  If you need to commit even with `pre-commit` throwing erros, you can override with `git commit --no-verify`.
