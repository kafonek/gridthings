from importlib_metadata import version

from .cell import Cell, OutOfBoundsCell
from .collection import Collection
from .grid import Grid
from .typed_grids import IntCell, IntGrid

# Recommended way to handle __version__ when defining it only in pyproject.toml
# https://github.com/python-poetry/poetry/issues/1036#issuecomment-489880822
__version__ = version(__package__)
