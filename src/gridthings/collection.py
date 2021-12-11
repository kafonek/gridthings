import collections
from typing import Any, List

from .cell import Cell, OutOfBoundsCell

# A Collection is a list of Cells.  They may be represent a single row
# or column of a grid, such as coming from grid.rows(0), or grid.columns(0).
# A Collection might also be a linear sequence of Cells going horizontal,
# vertical, or diagonally across a grid.  Still more flexibly, a Collection
# could be any arbitrary set of Cells like the return value of grid.peek_all(),
# which would give the 8 cells surrounding the grid active cell


class Collection(collections.abc.Sequence):
    def __init__(self, cells: List[Cell]):
        self.cells = cells

    def __len__(self) -> int:
        return len(self.cells)

    def __repr__(self):
        return f"<Collection [{repr(self.cells)}]>"

    # mypy says: Signature of "__getitem__" incompatible with supertype "Sequence" ??
    def __getitem__(self, index: int):  # type: ignore
        return self.cells[index]

    def __iter__(self):
        return self.cells.__iter__()

    def __add__(self, other):
        return Collection(cells=self.cells + other.cells)

    def __eq__(self, other):
        if isinstance(other, Collection):
            return self.cells == other.cells
        return False

    # mypy says: Signature of "__getitem__" incompatible with supertype "Sequence" ??
    def index(self, value: Any) -> int:  # type: ignore
        for i, cell in enumerate(self.cells):
            if cell.value == value:
                return i
        raise ValueError(f"{value} is not in row")

    def values(self) -> List[Any]:
        return [cell.value for cell in self.cells]

    def extends_out_of_bounds(self):
        return any(isinstance(cell, OutOfBoundsCell) for cell in self.cells)
