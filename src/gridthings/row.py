import collections
from typing import Any, List

from pydantic import BaseModel

from .cell import Cell


class Row(BaseModel, collections.abc.Sequence):
    cells: List[Cell]

    def __len__(self) -> int:
        return len(self.cells)

    # mypy: Signature of "__getitem__" incompatible with supertype "Sequence" ??
    def __getitem__(self, index: int):  # type: ignore
        return self.cells[index]

    def __iter__(self):
        return self.cells.__iter__()

    # mypy: Signature of "__getitem__" incompatible with supertype "Sequence" ??
    def index(self, value: Any) -> int:  # type: ignore
        for i, cell in enumerate(self.cells):
            if cell.value == value:
                return i
        raise ValueError(f"{value} is not in row")

    def values(self) -> List[Any]:
        return [cell.value for cell in self.cells]
