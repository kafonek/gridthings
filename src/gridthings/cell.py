from typing import Any

from pydantic import BaseModel

# A cell represents a single item in the grid
# Each cell knows its position (y/x) and its value
# Cells implement a variety of comparison operators
# so that you can do things like Cell + 'foo' if Cell.value is a string
# or Cell * Cell, Cell ** 3 if Cell.value is an int/float
#
# Additionally, Row objects will take a sequence of Cells and
# offer things like min(Row), max(Row) and math.prod(Row)


class Cell(BaseModel):
    y: int
    x: int
    value: Any

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Cell):
            return self.dict() == other.dict()
        return self.value == other

    def __ne__(self, other: Any) -> bool:
        if isinstance(other, Cell):
            return self.dict() != other.dict()
        return self.value != other

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Cell):
            return self.value < other.value
        return self.value < other

    def __le__(self, other: Any) -> bool:
        if isinstance(other, Cell):
            return self.value <= other.value
        else:
            return self.value <= other

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, Cell):
            return self.value > other.value
        else:
            return self.value > other

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, Cell):
            return self.value >= other.value
        else:
            return self.value >= other

    def __add__(self, other: Any) -> Any:
        if isinstance(other, Cell):
            return self.value + other.value
        else:
            return self.value + other

    def __radd__(self, other: Any) -> Any:
        return other + self.value

    def __sub__(self, other: Any) -> Any:
        if isinstance(other, Cell):
            return self.value - other.value
        else:
            return self.value - other

    def __rsub__(self, other: Any) -> Any:
        return other - self.value

    def __mul__(self, other: Any) -> Any:
        if isinstance(other, Cell):
            return self.value * other.value
        else:
            return self.value * other

    def __rmul__(self, other: Any) -> Any:
        return other * self.value

    def __pow__(self, other: Any) -> Any:
        if isinstance(other, Cell):
            return self.value ** other.value
        else:
            return self.value ** other

    def __rpow__(self, other: Any) -> Any:
        return other ** self.value

    def __truediv__(self, other: Any) -> Any:
        if isinstance(other, Cell):
            return self.value / other.value
        else:
            return self.value / other

    def __rtruediv__(self, other: Any) -> Any:
        return other / self.value


class OutOfBoundsCell(Cell):
    """
    Returned when active calls like .peek(y_offset, x_offset)
    reach outside the bounds of the Grid.
    """

    pass
