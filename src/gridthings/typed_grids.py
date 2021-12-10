from .cell import Cell
from .grid import Grid

# Typed Grids are Grids that apply data validation while reading the data
# thanks to subclassed Cell pydantic models


class IntCell(Cell):
    value: int


class IntGrid(Grid):
    cell_cls = IntCell
