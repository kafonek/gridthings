import math
import statistics

from gridthings import Cell, Collection

# Collections are custom collections.abc.Sequence that are aware
# the "value" in each cell is what is important when comparing
# and sorting and running operations like sum() or math.prod()
# on the data inside it


def test_collection_equality():
    cells = [
        Cell(y=0, x=0, value="a"),
        Cell(y=0, x=1, value="b"),
    ]
    assert Collection(cells=cells) == Collection(cells=cells)
    assert Collection(cells=cells) == Collection(
        cells=[
            Cell(y=0, x=0, value="a"),
            Cell(y=0, x=1, value="b"),
        ]
    )
    assert Collection(cells=cells) != [
        Cell(y=0, x=1, value="b"),
        Cell(y=0, x=0, value="a"),
    ]


def test_collection_len():
    cells = [
        Cell(y=0, x=0, value="a"),
        Cell(y=0, x=1, value="b"),
        Cell(y=0, x=2, value="c"),
    ]
    collection = Collection(cells=cells)
    assert len(collection) == 3


def test_collection_minmax():
    cells = [
        Cell(y=0, x=0, value="b"),
        Cell(y=0, x=1, value="a"),
        Cell(y=0, x=2, value="c"),
    ]
    collection = Collection(cells=cells)
    assert min(collection) == Cell(y=0, x=1, value="a")
    assert max(collection) == Cell(y=0, x=2, value="c")


def test_collection_reversed():
    cells = [
        Cell(y=0, x=0, value="a"),
        Cell(y=0, x=1, value="b"),
        Cell(y=0, x=2, value="c"),
    ]
    collection = Collection(cells=cells)
    assert list(reversed(collection)) == [
        Cell(y=0, x=2, value="c"),
        Cell(y=0, x=1, value="b"),
        Cell(y=0, x=0, value="a"),
    ]


def test_collection_math():
    cells = [
        Cell(y=0, x=0, value=2),
        Cell(y=0, x=1, value=4),
        Cell(y=0, x=2, value=8),
    ]
    collection = Collection(cells=cells)
    assert sum(collection) == 14
    assert math.prod(collection) == 64
    assert statistics.median(collection) == 4


def test_collection_index_function():
    cells = [
        Cell(y=0, x=0, value="a"),
        Cell(y=0, x=1, value="b"),
        Cell(y=0, x=2, value="c"),
    ]
    collection = Collection(cells=cells)
    assert collection.index("b") == 1


def test_collection_slice():
    cells = [
        Cell(y=0, x=0, value="a"),
        Cell(y=0, x=1, value="b"),
        Cell(y=0, x=2, value="c"),
    ]
    collection = Collection(cells=cells)
    assert collection[0] == Cell(y=0, x=0, value="a")
    assert collection[-1] == Cell(y=0, x=2, value="c")

    assert list(collection[1:]) == [
        Cell(y=0, x=1, value="b"),
        Cell(y=0, x=2, value="c"),
    ]
    assert list(collection[:2]) == [
        Cell(y=0, x=0, value="a"),
        Cell(y=0, x=1, value="b"),
    ]
    assert list(collection[:]) == [
        Cell(y=0, x=0, value="a"),
        Cell(y=0, x=1, value="b"),
        Cell(y=0, x=2, value="c"),
    ]
