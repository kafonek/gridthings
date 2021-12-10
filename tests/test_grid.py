import pytest

from gridthings import Cell, Grid, IntGrid, OutOfBoundsCell, Row

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
    assert grid.flatten() == [
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


def test_values():
    data = "abc\ndef\nxyz"
    grid = Grid(data)
    assert grid.values() == ["a", "b", "c", "d", "e", "f", "x", "y", "z"]


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


# Functions that require an active context ------------------------------------


def test_enter():
    data = "abc\ndef\nxyz"
    grid = Grid(data)
    top_left_cell = grid.enter(0, 0)
    assert top_left_cell == Cell(y=0, x=0, value="a")

    top_mid_cell = grid.enter(0, 1)
    assert top_mid_cell == Cell(y=0, x=1, value="b")

    mid_left_cell = grid.enter(1, 0)
    assert mid_left_cell == Cell(y=1, x=0, value="d")


def test_raise_error_when_missing_active_context():
    data = "abc\ndef\nxyz"
    grid = Grid(data)
    with pytest.raises(ValueError):
        grid.active_row()


def test_get_active_row_and_col():
    data = "abc\ndef\nxyz"
    grid = Grid(data)
    grid.enter(0, 0)
    assert grid.active_row() == Row(
        cells=[
            Cell(y=0, x=0, value="a"),
            Cell(y=0, x=1, value="b"),
            Cell(y=0, x=2, value="c"),
        ]
    )

    assert grid.active_column() == Row(
        cells=[
            Cell(y=0, x=0, value="a"),
            Cell(y=1, x=0, value="d"),
            Cell(y=2, x=0, value="x"),
        ]
    )


def test_peek():
    data = "abc\ndef\nxyz"
    grid = Grid(data)
    grid.enter(1, 1)
    assert grid.peek(y_offset=0, x_offset=0) == Cell(y=1, x=1, value="e")
    assert grid.peek_left() == Cell(y=1, x=0, value="d")
    assert grid.peek_right() == Cell(y=1, x=2, value="f")
    assert grid.peek_up() == Cell(y=0, x=1, value="b")
    assert grid.peek_down() == Cell(y=2, x=1, value="y")
    assert grid.peek_linear() == [
        Cell(y=1, x=0, value="d"),
        Cell(y=1, x=2, value="f"),
        Cell(y=0, x=1, value="b"),
        Cell(y=2, x=1, value="y"),
    ]

    assert grid.peek(y_offset=-1, x_offset=-1) == Cell(y=0, x=0, value="a")

    out_of_bounds_cell = grid.peek(y_offset=-2, x_offset=0)
    assert isinstance(out_of_bounds_cell, OutOfBoundsCell)
    assert out_of_bounds_cell == OutOfBoundsCell(y=-1, x=1, value=None)


def test_default_out_of_bounds_value():
    data = "abc\ndef\nxyz"
    grid = Grid(data, out_of_bounds_value="default")
    grid.enter(0, 0)
    out_of_bounds_cell = grid.peek_left()
    assert isinstance(out_of_bounds_cell, OutOfBoundsCell)
    assert out_of_bounds_cell == OutOfBoundsCell(y=0, x=-1, value="default")
