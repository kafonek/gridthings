import math
import statistics

from gridthings import Cell, Row

# Rows are mixins of Pydantic and collections.abc.Sequence
# the purpose is to allow operations like sorted(), min(), and max()
# to use the Cell .value attribute


def test_row_len():
    cells = [
        Cell(y=0, x=0, value="a"),
        Cell(y=0, x=1, value="b"),
        Cell(y=0, x=2, value="c"),
    ]
    row = Row(cells=cells)
    assert len(row) == 3


def test_row_minmax():
    cells = [
        Cell(y=0, x=0, value="b"),
        Cell(y=0, x=1, value="a"),
        Cell(y=0, x=2, value="c"),
    ]
    row = Row(cells=cells)
    assert min(row) == Cell(y=0, x=1, value="a")
    assert max(row) == Cell(y=0, x=2, value="c")


def test_row_reversed():
    cells = [
        Cell(y=0, x=0, value="a"),
        Cell(y=0, x=1, value="b"),
        Cell(y=0, x=2, value="c"),
    ]
    row = Row(cells=cells)
    assert list(reversed(row)) == [
        Cell(y=0, x=2, value="c"),
        Cell(y=0, x=1, value="b"),
        Cell(y=0, x=0, value="a"),
    ]


def test_row_math():
    cells = [
        Cell(y=0, x=0, value=2),
        Cell(y=0, x=1, value=4),
        Cell(y=0, x=2, value=8),
    ]
    row = Row(cells=cells)
    assert sum(row) == 14
    assert math.prod(row) == 64
    assert statistics.median(row) == 4


def test_row_index_function():
    cells = [
        Cell(y=0, x=0, value="a"),
        Cell(y=0, x=1, value="b"),
        Cell(y=0, x=2, value="c"),
    ]
    row = Row(cells=cells)
    assert row.index("b") == 1


def test_row_slice():
    cells = [
        Cell(y=0, x=0, value="a"),
        Cell(y=0, x=1, value="b"),
        Cell(y=0, x=2, value="c"),
    ]
    row = Row(cells=cells)
    assert row[0] == Cell(y=0, x=0, value="a")
    assert row[-1] == Cell(y=0, x=2, value="c")

    assert list(row[1:]) == [
        Cell(y=0, x=1, value="b"),
        Cell(y=0, x=2, value="c"),
    ]
    assert list(row[:2]) == [
        Cell(y=0, x=0, value="a"),
        Cell(y=0, x=1, value="b"),
    ]
    assert list(row[:]) == [
        Cell(y=0, x=0, value="a"),
        Cell(y=0, x=1, value="b"),
        Cell(y=0, x=2, value="c"),
    ]
