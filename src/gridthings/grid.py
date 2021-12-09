from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel


class Cell(BaseModel):
    x: int
    y: int
    value: Any


class Grid:
    def __init__(
        self,
        data: Union[Dict[int, Dict[int, Any]], List[Dict[int, Any]], str],
        strip_whitespace: bool = True,
        line_sep: str = "\n",
        sep: Optional[str] = None,
    ) -> None:
        """
        Instantiate a Grid object from one of several data formats.

        1. a dictionary of dictionaries, e.g. df.to_dict()
        2. a list of dictionaries, e.g. df.to_dict(orient='records')
        3. a string with line breaks, e.g. 'abc\ndef'
        4. a string with line breaks and a separator, e.g. 'a,b,c\nd,e,f'

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
                    self.data[y_pos][x_pos] = Cell(x=x_pos, y=y_pos, value=value)

        elif isinstance(data, list):
            for y_pos, column_data in enumerate(data):
                if y_pos not in self.data:
                    self.data[y_pos] = {}
                for x_pos, value in column_data.items():
                    self.data[y_pos][x_pos] = Cell(x=x_pos, y=y_pos, value=value)

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
                    self.data[y_pos][x_pos] = Cell(x=x_pos, y=y_pos, value=value)
