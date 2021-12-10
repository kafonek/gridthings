import pytest

from gridthings import Cell

# Cells are a mixin of Pydantic object and functools.total_ordering
# Tests here prove that Cells compare with each other using their .value


def test_cell_when_equal():
    c1 = Cell(y=0, x=0, value="foo")
    c2 = Cell(y=0, x=1, value="foo")
    assert c1 != c2
    assert c1 >= c2
    assert c2 >= c1
    assert c1 <= c2
    assert c2 <= c1


def test_cell_when_unequal():
    c1 = Cell(y=0, x=0, value="bar")
    c2 = Cell(y=0, x=1, value="foo")
    assert c1 != c2
    assert c1 < c2
    assert c1 <= c2
    assert c2 > c1
    assert c2 >= c1


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
