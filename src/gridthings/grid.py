from typing import Any, Dict, List, Optional, Tuple, Union

from .cell import Cell, OutOfBoundsCell
from .row import Row

# A Grid represents some tabular data, the kind of thing you might analyze in Pandas
# This library is about letting you accomplish tasks that may be confusing or
# difficult in frameworks like Pandas.  For instance, getting the neighboring
# values of a specific point, or cell with minimum value in a diagonal row
#
# See typed_grids.py for Grids with data validation


class Grid:
    cell_cls = Cell

    def __init__(
        self,
        data: Union[Dict[int, Dict[int, Any]], List[Dict[int, Any]], str],
        strip_whitespace: bool = True,
        line_sep: str = "\n",
        sep: Optional[str] = None,
        out_of_bounds_value: Optional[Any] = None,
    ) -> None:
        """
        Instantiate a Grid object from one of several data formats.

        1. a dictionary of dictionaries, e.g. from df.to_dict()
        2. a list of dictionaries, e.g. from df.to_dict(orient='records')
        3. a string with line breaks, e.g. 'abc\ndef'
        4. a string with line breaks and in-line separator, e.g. 'a,b,c\nd,e,f'

        line_sep and sep only apply when data is a string.
        line_sep is for the break between lines
        sep is for any in-line separator
        """
        self.data: Dict[int, Dict[int, Cell]] = {}

        # data is stored internally as y:x:value, following pandas style
        # can also think of it like row-data goes to the y position
        # and column data goes to the x position
        if isinstance(data, dict):
            for x_pos, row_data in data.items():
                for y_pos, value in row_data.items():
                    if y_pos not in self.data:
                        self.data[y_pos] = {}
                    self.data[y_pos][x_pos] = self.cell_cls(
                        y=y_pos, x=x_pos, value=value
                    )

        elif isinstance(data, list):
            for y_pos, column_data in enumerate(data):
                if y_pos not in self.data:
                    self.data[y_pos] = {}
                for x_pos, value in column_data.items():
                    self.data[y_pos][x_pos] = self.cell_cls(
                        y=y_pos, x=x_pos, value=value
                    )

        elif isinstance(data, str):
            if strip_whitespace:
                data = data.strip()
            for y_pos, line in enumerate(data.split(line_sep)):
                if y_pos not in self.data:
                    self.data[y_pos] = {}
                if strip_whitespace:
                    line = line.strip()
                if sep:
                    # mypy doesn't like that line becomes a List[str]
                    # although it should recognize I just care about it being Iterable...
                    line = line.split(sep)  # type: ignore
                for x_pos, value in enumerate(line):
                    self.data[y_pos][x_pos] = self.cell_cls(
                        y=y_pos, x=x_pos, value=value
                    )

        # -- done data init --
        # these two variables are used in conjunction with "active" methods
        # like self.enter(x, y) / self.xrows() / self.peek()
        self.active_x: Optional[int] = None
        self.active_y: Optional[int] = None

        # Default value for OutOfBound cells
        # returned from active methods like .peek()
        self.out_of_bounds_value = out_of_bounds_value

    @property
    def shape(self) -> Tuple[int, int]:
        "Return the shape of the grid"
        return len(self.data), len(self.data[0])

    def __repr__(self):
        return f"<{self.__class__.__name__} shape={self.shape}>"

    def flatten(self) -> List[Cell]:
        "Flatten the grid into a list of Cells going left to right (rows) then top to bottom (columns)"
        cells = []
        for row in self.data.values():
            for cell in row.values():
                cells.append(cell)
        return cells

    def values(self) -> List[Any]:
        "Return just the values of Cells going left to right (rows) then top to bottom (columns)"
        return [cell.value for cell in self.flatten()]

    def enter(self, y: int, x: int) -> Cell:
        "Set x and y position to x and y"
        self.active_x = x
        self.active_y = y
        return self.data[y][x]

    def active(func):
        def wrapper(self, *args, **kwargs):
            if self.active_x is None or self.active_y is None:
                raise ValueError("Active position must be set first with .enter(x, y)")
            return func(self, *args, **kwargs)

        return wrapper

    # Not sure how to make mypy okay with decorators
    @active  # type: ignore
    def active_row(self) -> Row:
        "Return a list of all cells on the same row as the active position"
        cells = list(self.data[self.active_y].values())  # type: ignore
        return Row(cells=cells)

    @active  # type: ignore
    def active_column(self) -> Row:
        "Return a list of all cells on the same column as the active position"
        cells = [self.data[y][self.active_x] for y in self.data]  # type: ignore
        return Row(cells=cells)

    @active  # type: ignore
    def peek(self, y_offset: int, x_offset: int) -> Cell:
        "Return a Cell object at the active position plus the offsets"
        # mypy thinks this is None + int because it doesn't understand that
        # this can only occur after self.active_x/y are set (from @active decorator)
        y = self.active_y + y_offset  # type: ignore
        x = self.active_x + x_offset  # type: ignore
        if y not in self.data or x not in self.data[y]:
            return OutOfBoundsCell(y=y, x=x, value=self.out_of_bounds_value)
        return self.data[y][x]

    @active  # type: ignore
    def peek_left(self, distance: int = 1) -> Cell:
        "Return a Cell object to the left of the active position"
        return self.peek(y_offset=0, x_offset=-distance)

    @active  # type: ignore
    def peek_right(self, distance: int = 1) -> Cell:
        "Return a Cell object to the right of the active position"
        return self.peek(y_offset=0, x_offset=distance)

    @active  # type: ignore
    def peek_up(self, distance: int = 1) -> Cell:
        "Return a Cell object above the active position"
        return self.peek(y_offset=-distance, x_offset=0)

    @active  # type: ignore
    def peek_down(self, distance: int = 1) -> Cell:
        "Return a Cell object below the active position"
        return self.peek(y_offset=distance, x_offset=0)

    @active  # type: ignore
    def peek_linear(self, distance: int = 1) -> List[Cell]:
        "Return peek_left, peek_right, peek_up, and peek_down"
        return [
            self.peek_left(distance),
            self.peek_right(distance),
            self.peek_up(distance),
            self.peek_down(distance),
        ]

    @active  # type: ignore
    def peek_diagonal(self, distance: int = 1) -> List[Cell]:
        "Return peek diagonal up/left, up/right, down/left, down/right"
        return [
            self.peek(y_offset=-distance, x_offset=-distance),
            self.peek(y_offset=-distance, x_offset=distance),
            self.peek(y_offset=distance, x_offset=-distance),
            self.peek(y_offset=distance, x_offset=distance),
        ]

    @active  # type: ignore
    def line(self, y_step: int = 0, x_step: int = 0, distance: int = 1) -> Row:
        "Return a Row of cells in a line from the active position"
        cells = []
        for offset in range(distance):
            cells.append(self.peek(y_offset=offset * y_step, x_offset=offset * x_step))
        return Row(cells=cells)
