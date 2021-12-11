from typing import Any, Dict, List, Optional, Tuple, Type, Union

from .cell import Cell, OutOfBoundsCell
from .collection import Collection

# A Grid represents some tabular data, the kind of thing you might analyze in Pandas
# This library is about letting you accomplish tasks that may be confusing or
# difficult in frameworks like Pandas.  For instance, getting the neighboring
# values of a specific point, or cell with minimum value in a diagonal row
#
# See typed_grids.py for Grids with data validation


class Grid:
    # These two _cls variables are here as entrypoints for customizing
    # your Grid object, plugging in your own Cell or Collection mechanism
    # They can also be inserted in init kwargs
    cell_cls = Cell
    collection_cls = Collection

    def __init__(
        self,
        data: Union[Dict[int, Dict[int, Any]], List[Dict[int, Any]], str],
        strip_whitespace: bool = True,
        line_sep: str = "\n",
        sep: Optional[str] = None,
        out_of_bounds_value: Optional[Any] = None,
        cell_cls: Type[Cell] = None,
        collections_cls: Type[Collection] = None,
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
        self.cell_cls = cell_cls or self.cell_cls
        self.collection_cls = collections_cls or self.collection_cls

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

        # Default value for OutOfBound cells when a Collection
        # extends outside the grid, which can happen with .peek() and .line()
        self.out_of_bounds_value = out_of_bounds_value

    @property
    def is_regular(self) -> bool:
        "Return True if all rows are the same length"
        return all(len(row) == len(self.data[0]) for row in self.data.values())

    @property
    def shape(self) -> Tuple[int, int]:
        "Return the shape of the grid"
        return len(self.data), len(self.data[0])

    def __repr__(self):
        if self.is_regular:
            return f"<{self.__class__.__name__} shape={self.shape}>"
        else:
            return f"<{self.__class__.__name__} shape=(irregular)>"

    def get(self, y: int, x: int) -> Cell:
        "Return a Cell object at a given y, x position"
        return self.data[y][x]

    def get_row(self, y: int) -> Collection:
        "Return the y'th row. coll = grid.get_row(0) gives the top row of the grid"
        cells = list(self.data[y].values())
        return self.collection_cls(cells=cells)

    def get_column(self, x: int) -> Collection:
        "Return the x'th column. coll = grid.get_column(0) gives the left column of the grid"
        cells = [row[x] for row in self.data.values()]
        return self.collection_cls(cells=cells)

    # Useful for iterating through every cell in the grid.  for cell in grid.flatten():
    def flatten(self) -> Collection:
        "Flatten the 2-d Grid into a 1-d Collection of cells"
        cells = []
        for row in self.data.values():
            for cell in row.values():
                cells.append(cell)
        return Collection(cells=cells)

    # Primarily useful for integration to pandas: df = pandas.DataFrame(grid.values())
    def values(self) -> List[List[Any]]:
        "Return the grid as a list of lists"
        return [[cell.value for cell in row.values()] for row in self.data.values()]

    def peek(self, y: int, x: int, y_offset: int, x_offset: int) -> Cell:
        "Return a Cell object offset from a given y, x position"
        y_out = y + y_offset
        x_out = x + x_offset
        if y_out not in self.data or x_out not in self.data[y_out]:
            return OutOfBoundsCell(y=y_out, x=x_out, value=self.out_of_bounds_value)
        return self.data[y_out][x_out]

    def peek_left(self, y: int, x: int, distance: int = 1) -> Cell:
        "Return a Cell object to the left of a given y, x position"
        return self.peek(y=y, x=x, y_offset=0, x_offset=-distance)

    def peek_right(self, y: int, x: int, distance: int = 1) -> Cell:
        "Return a Cell object to the right of a given y, x position"
        return self.peek(y=y, x=x, y_offset=0, x_offset=distance)

    def peek_up(self, y: int, x: int, distance: int = 1) -> Cell:
        "Return a Cell object above a given y, x position"
        return self.peek(y=y, x=x, y_offset=-distance, x_offset=0)

    def peek_down(self, y: int, x: int, distance: int = 1) -> Cell:
        "Return a Cell object below a given y, x position"
        return self.peek(y=y, x=x, y_offset=distance, x_offset=0)

    def peek_linear(self, y: int, x: int, distance: int = 1) -> Collection:
        "Return peek_left, peek_right, peek_up, and peek_down from a given y, x position"
        cells = [
            self.peek_left(y=y, x=x, distance=distance),
            self.peek_right(y=y, x=x, distance=distance),
            self.peek_up(y=y, x=x, distance=distance),
            self.peek_down(y=y, x=x, distance=distance),
        ]
        return self.collection_cls(cells=cells)

    def peek_diagonal(self, y: int, x: int, distance: int = 1) -> Collection:
        "Return peek diagonal up/left, up/right, down/left, down/right a given y, x position"
        cells = [
            self.peek(y=y, x=x, y_offset=-distance, x_offset=-distance),
            self.peek(y=y, x=x, y_offset=-distance, x_offset=distance),
            self.peek(y=y, x=x, y_offset=distance, x_offset=-distance),
            self.peek(y=y, x=x, y_offset=distance, x_offset=distance),
        ]
        return self.collection_cls(cells=cells)

    def peek_all(self, y: int, x: int, distance: int = 1) -> Collection:
        "Return all cells around a given y, x position"
        linear_neighbors = self.peek_linear(y=y, x=x, distance=distance)
        diag_neighbors = self.peek_diagonal(y=y, x=x, distance=distance)
        return linear_neighbors + diag_neighbors

    def line(
        self, y: int, x: int, y_step: int = 0, x_step: int = 0, distance: int = 1
    ) -> Collection:
        "Return a Collection of cells starting at a given y/x position and stepping for some distance"
        cells = []
        for offset in range(distance):
            out_cell = self.peek(
                y=y, x=x, y_offset=offset * y_step, x_offset=offset * x_step
            )
            cells.append(out_cell)
        return self.collection_cls(cells=cells)
