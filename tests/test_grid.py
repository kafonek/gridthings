import pytest

from gridthings import Cell, Collection, Grid, IntGrid, OutOfBoundsCell

# Test grid initilization ------------------------------------------------------
# Imagine seed data generated from something like
# import pandas
# df = pandas.DataFrame([['a', 'b', 'c'],
#                        ['d', 'e', 'f'],
#                        ['x', 'y', 'z']])


def test_init_by_dict() -> None:
    # output of df.to_csv() in sample above
    data = {
        0: {0: "a", 1: "d", 2: "x"},
        1: {0: "b", 1: "e", 2: "y"},
        2: {0: "c", 1: "f", 2: "z"},
    }
    grid = Grid(data)
    assert grid.data == {
        0: {
            0: Cell(y=0, x=0, value="a"),
            1: Cell(y=0, x=1, value="b"),
            2: Cell(y=0, x=2, value="c"),
        },
        1: {
            0: Cell(y=1, x=0, value="d"),
            1: Cell(y=1, x=1, value="e"),
            2: Cell(y=1, x=2, value="f"),
        },
        2: {
            0: Cell(y=2, x=0, value="x"),
            1: Cell(y=2, x=1, value="y"),
            2: Cell(y=2, x=2, value="z"),
        },
    }


def test_init_by_list() -> None:
    # output of df.to_dict(orient='records') from sample above
    data = [
        {0: "a", 1: "b", 2: "c"},
        {0: "d", 1: "e", 2: "f"},
        {0: "x", 1: "y", 2: "z"},
    ]
    grid = Grid(data)
    assert grid.data == {
        0: {
            0: Cell(y=0, x=0, value="a"),
            1: Cell(y=0, x=1, value="b"),
            2: Cell(y=0, x=2, value="c"),
        },
        1: {
            0: Cell(y=1, x=0, value="d"),
            1: Cell(y=1, x=1, value="e"),
            2: Cell(y=1, x=2, value="f"),
        },
        2: {
            0: Cell(y=2, x=0, value="x"),
            1: Cell(y=2, x=1, value="y"),
            2: Cell(y=2, x=2, value="z"),
        },
    }


def test_init_by_str() -> None:
    data = "abc\ndef\nxyz"
    grid = Grid(data)
    assert grid.data == {
        0: {
            0: Cell(y=0, x=0, value="a"),
            1: Cell(y=0, x=1, value="b"),
            2: Cell(y=0, x=2, value="c"),
        },
        1: {
            0: Cell(y=1, x=0, value="d"),
            1: Cell(y=1, x=1, value="e"),
            2: Cell(y=1, x=2, value="f"),
        },
        2: {
            0: Cell(y=2, x=0, value="x"),
            1: Cell(y=2, x=1, value="y"),
            2: Cell(y=2, x=2, value="z"),
        },
    }


def test_init_by_str_with_whitespace() -> None:
    data = """
    abc
    def
    xyz
    """
    grid = Grid(data)
    assert grid.data == {
        0: {
            0: Cell(y=0, x=0, value="a"),
            1: Cell(y=0, x=1, value="b"),
            2: Cell(y=0, x=2, value="c"),
        },
        1: {
            0: Cell(y=1, x=0, value="d"),
            1: Cell(y=1, x=1, value="e"),
            2: Cell(y=1, x=2, value="f"),
        },
        2: {
            0: Cell(y=2, x=0, value="x"),
            1: Cell(y=2, x=1, value="y"),
            2: Cell(y=2, x=2, value="z"),
        },
    }


def test_init_by_str_with_whitespace_and_sep() -> None:
    data = """
    a,b,c
    d,e,f
    x,y,z
    """
    grid = Grid(data, sep=",")
    assert grid.data == {
        0: {
            0: Cell(y=0, x=0, value="a"),
            1: Cell(y=0, x=1, value="b"),
            2: Cell(y=0, x=2, value="c"),
        },
        1: {
            0: Cell(y=1, x=0, value="d"),
            1: Cell(y=1, x=1, value="e"),
            2: Cell(y=1, x=2, value="f"),
        },
        2: {
            0: Cell(y=2, x=0, value="x"),
            1: Cell(y=2, x=1, value="y"),
            2: Cell(y=2, x=2, value="z"),
        },
    }


# Misc grid tests --------------------------------------------------------------


def test_flatten():
    data = "abc\ndef\nxyz"
    grid = Grid(data)
    flattened = grid.flatten()
    assert grid.flatten() == Collection(
        cells=[
            Cell(y=0, x=0, value="a"),
            Cell(y=0, x=1, value="b"),
            Cell(y=0, x=2, value="c"),
            Cell(y=1, x=0, value="d"),
            Cell(y=1, x=1, value="e"),
            Cell(y=1, x=2, value="f"),
            Cell(y=2, x=0, value="x"),
            Cell(y=2, x=1, value="y"),
            Cell(y=2, x=2, value="z"),
        ]
    )


def test_values():
    data = "abc\ndef\nxyz"
    grid = Grid(data)
    assert grid.values() == [["a", "b", "c"], ["d", "e", "f"], ["x", "y", "z"]]


# Typed grids -----------------------------------------------------------------
def test_intgrid():
    data = "123\n456"
    grid = IntGrid(data)
    assert grid.data == {
        0: {
            0: Cell(y=0, x=0, value=1),
            1: Cell(y=0, x=1, value=2),
            2: Cell(y=0, x=2, value=3),
        },
        1: {
            0: Cell(y=1, x=0, value=4),
            1: Cell(y=1, x=1, value=5),
            2: Cell(y=1, x=2, value=6),
        },
    }


def test_intgrid_invalid():
    data = "a\n2\n3"
    with pytest.raises(ValueError):
        IntGrid(data)


def test_get_row_and_col():
    data = "abc\nxyz"
    grid = Grid(data)
    assert grid.get_row(0) == Collection(
        cells=[
            Cell(y=0, x=0, value="a"),
            Cell(y=0, x=1, value="b"),
            Cell(y=0, x=2, value="c"),
        ]
    )
    assert grid.get_row(1) == Collection(
        cells=[
            Cell(y=1, x=0, value="x"),
            Cell(y=1, x=1, value="y"),
            Cell(y=1, x=2, value="z"),
        ]
    )
    assert grid.get_column(0) == Collection(
        cells=[
            Cell(y=0, x=0, value="a"),
            Cell(y=1, x=0, value="x"),
        ]
    )
    assert grid.get_column(1) == Collection(
        cells=[
            Cell(y=0, x=1, value="b"),
            Cell(y=1, x=1, value="y"),
        ]
    )
    assert grid.get_column(2) == Collection(
        cells=[
            Cell(y=0, x=2, value="c"),
            Cell(y=1, x=2, value="z"),
        ]
    )


def test_peek():
    data = "abc\ndef\nxyz"
    grid = Grid(data)
    assert grid.peek(y=0, x=0, y_offset=0, x_offset=0) == "a"
    assert grid.peek(y=0, x=0, y_offset=0, x_offset=1) == "b"
    assert grid.peek_left(y=1, x=1) == "d"
    assert grid.peek_right(y=1, x=1) == "f"
    assert grid.peek_up(y=1, x=1) == "b"
    assert grid.peek_down(y=1, x=1) == "y"


def test_peek_linear():
    data = "abc\ndef\nxyz"
    grid = Grid(data)
    assert grid.peek_linear(y=1, x=1) == Collection(
        cells=[
            Cell(y=1, x=0, value="d"),
            Cell(y=1, x=2, value="f"),
            Cell(y=0, x=1, value="b"),
            Cell(y=2, x=1, value="y"),
        ]
    )


def test_peek_diagonal():
    data = "abc\ndef\nxyz"
    grid = Grid(data)
    assert grid.peek_diagonal(y=1, x=1) == Collection(
        cells=[
            Cell(y=0, x=0, value="a"),
            Cell(y=0, x=2, value="c"),
            Cell(y=2, x=0, value="x"),
            Cell(y=2, x=2, value="z"),
        ]
    )


def test_peek_out_of_bounds():
    data = "abc\ndef\nxyz"
    grid = Grid(data)
    out_of_bounds_cell = grid.peek(y=1, x=1, y_offset=-2, x_offset=0)
    assert isinstance(out_of_bounds_cell, OutOfBoundsCell)
    assert out_of_bounds_cell == OutOfBoundsCell(y=-1, x=1, value=None)


def test_line():
    data = "abc\ndef\nxyz"
    grid = Grid(data)
    assert grid.line(y=0, x=0, y_step=0, x_step=1, distance=3) == Collection(
        cells=[
            Cell(y=0, x=0, value="a"),
            Cell(y=0, x=1, value="b"),
            Cell(y=0, x=2, value="c"),
        ]
    )
    assert grid.line(y=0, x=0, y_step=1, x_step=0, distance=3) == Collection(
        cells=[
            Cell(y=0, x=0, value="a"),
            Cell(y=1, x=0, value="d"),
            Cell(y=2, x=0, value="x"),
        ]
    )
    assert grid.line(y=0, x=0, y_step=1, x_step=1, distance=3) == Collection(
        cells=[
            Cell(y=0, x=0, value="a"),
            Cell(y=1, x=1, value="e"),
            Cell(y=2, x=2, value="z"),
        ]
    )


def test_line_out_of_bounds():
    data = "abc\ndef\nxyz"
    grid = Grid(data)
    collection = grid.line(y=0, x=0, y_step=-1, distance=2)
    assert collection == Collection(
        cells=[Cell(y=0, x=0, value="a"), OutOfBoundsCell(y=-1, x=0, value=None)]
    )
    assert collection.extends_out_of_bounds()


def test_default_out_of_bounds_value():
    data = "abc\ndef\nxyz"
    grid = Grid(data, out_of_bounds_value="default")
    out_of_bounds_cell = grid.peek_left(y=0, x=0)
    assert isinstance(out_of_bounds_cell, OutOfBoundsCell)
    assert out_of_bounds_cell == OutOfBoundsCell(y=0, x=-1, value="default")
