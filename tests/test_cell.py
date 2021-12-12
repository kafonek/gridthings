import pytest

from gridthings import Cell

# Cells represent individual data points in a grid
# They implement a variety of mathematical dunder methods
# so that they can be compared, sorted, and manipulated


def test_cell_when_equal():
    c1 = Cell(y=0, x=0, value="foo")
    c2 = Cell(y=0, x=1, value="foo")
    # using ==, cell values are equal but actual
    # cell objects are not considered equal
    assert c1.value == c2.value
    assert c1 != c2
    # When > and < operators are used, it's
    # a pure comparison on values
    # so c1 == c2 is False, but c1 >= c2 is True
    assert c1 >= c2
    assert c2 >= c1
    assert c1 <= c2
    assert c2 <= c1


def test_cell_when_unequal():
    c1 = Cell(y=0, x=0, value=1)
    c2 = Cell(y=0, x=1, value=2)
    assert c1 != c2
    assert c1 < c2
    assert c1 <= c2
    assert c2 > c1
    assert c2 >= c1


def test_cell_against_non_cells():
    cell = Cell(y=0, x=0, value=2)
    # __eq__
    assert cell == 2
    assert 2 == cell
    # __ne__
    assert cell != 0
    assert 0 != cell
    # __gte__ / __lte__
    assert 3 >= cell
    assert cell <= 3
    assert 1 <= cell
    assert cell >= 1
    # __gt__ / __lt__
    assert 3 > cell
    assert cell < 3
    assert 1 < cell
    assert cell > 1
    # __add__
    assert cell + 2 == 4
    assert 2 + cell == 4
    # __sub__
    assert 2 - cell == 0
    assert cell - 2 == 0
    # __mul__
    assert 3 * cell == 6
    assert cell * 3 == 6
    # __truediv__
    assert cell / 2 == 1
    # __pow__
    assert cell ** 3 == 8


def test_cell_when_mismatched_datatype():
    c1 = Cell(y=0, x=0, value="foo")
    c2 = Cell(y=0, x=0, value=1)
    assert c1 != c2
    with pytest.raises(TypeError):
        # < not supported between instances of 'str' and 'int'
        assert c1 < c2


def test_cell_str_concat():
    c1 = Cell(y=0, x=0, value="foo")
    c2 = Cell(y=0, x=1, value="bar")
    assert c1 + c2 == "foobar"
    assert c2 + c1 == "barfoo"
    assert c1 + "baz" == "foobaz"
    assert "baz" + c2 == "bazbar"


def test_cell_int_math():
    c1 = Cell(y=0, x=0, value=2)
    c2 = Cell(y=0, x=0, value=4)
    c3 = Cell(y=0, x=0, value=6)
    assert c1 + c2 == 6
    assert c2 + c1 == 6
    assert c1 + 2 == 4
    assert 2 + c1 == 4
    assert c1 + c2 + c3 == 12

    assert c2 - c1 == 2
    assert 4 - c1 == 2
    assert c3 - c2 - c1 == 0

    assert c1 * c2 == 8
    assert 2 * c2 == 8
    assert c1 * c2 * c3 == 48

    assert c1 / c2 == 0.5
    assert 4 / c1 == 2

    assert c1 ** 3 == 8
    assert c2 ** c1 == 16
    assert 2 ** c1 == 4


def test_subclass_cell():
    class MyCell(Cell):
        extra_arg: bool = True

    cell = MyCell(y=0, x=0, value=1)
    assert cell.dict() == {"y": 0, "x": 0, "value": 1, "extra_arg": True}

    cell2 = MyCell(y=0, x=0, value=1, extra_arg=False)
    assert cell2.dict() == {"y": 0, "x": 0, "value": 1, "extra_arg": False}
