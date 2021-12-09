import pytest

from gridthings import Cell, Grid, OutOfBoundsCell, Row


def test_enter():
    data = "abc\ndef\nxyz"
    grid = Grid(data)
    top_left_cell = grid.enter(0, 0)
    assert top_left_cell == Cell(y=0, x=0, value="a")

    top_mid_cell = grid.enter(0, 1)
    assert top_mid_cell == Cell(y=0, x=1, value="b")

    mid_left_cell = grid.enter(1, 0)
    assert mid_left_cell == Cell(y=1, x=0, value="d")


def test_not_active():
    data = "abc\ndef\nxyz"
    grid = Grid(data)
    with pytest.raises(ValueError):
        row = grid.active_row()


def test_get_active_row_and_col():
    data = "abc\ndef\nxyz"
    grid = Grid(data)
    grid.enter(0, 0)
    row = grid.active_row()
    assert row == Row(
        cells=[
            Cell(y=0, x=0, value="a"),
            Cell(y=0, x=1, value="b"),
            Cell(y=0, x=2, value="c"),
        ]
    )

    column = grid.active_column()
    assert column == Row(
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
    assert out_of_bounds_cell == OutOfBoundsCell(y=-1, x=0, value=None)
