from gridthings import Cell, Grid

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
            0: Cell(x=0, y=0, value="a"),
            1: Cell(x=1, y=0, value="b"),
            2: Cell(x=2, y=0, value="c"),
        },
        1: {
            0: Cell(x=0, y=1, value="d"),
            1: Cell(x=1, y=1, value="e"),
            2: Cell(x=2, y=1, value="f"),
        },
        2: {
            0: Cell(x=0, y=2, value="x"),
            1: Cell(x=1, y=2, value="y"),
            2: Cell(x=2, y=2, value="z"),
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
    print(grid.data)
    assert grid.data == {
        0: {
            0: Cell(x=0, y=0, value="a"),
            1: Cell(x=1, y=0, value="b"),
            2: Cell(x=2, y=0, value="c"),
        },
        1: {
            0: Cell(x=0, y=1, value="d"),
            1: Cell(x=1, y=1, value="e"),
            2: Cell(x=2, y=1, value="f"),
        },
        2: {
            0: Cell(x=0, y=2, value="x"),
            1: Cell(x=1, y=2, value="y"),
            2: Cell(x=2, y=2, value="z"),
        },
    }


def test_init_by_str() -> None:
    data = "abc\ndef\nxyz"
    grid = Grid(data)
    assert grid.data == {
        0: {
            0: Cell(x=0, y=0, value="a"),
            1: Cell(x=1, y=0, value="b"),
            2: Cell(x=2, y=0, value="c"),
        },
        1: {
            0: Cell(x=0, y=1, value="d"),
            1: Cell(x=1, y=1, value="e"),
            2: Cell(x=2, y=1, value="f"),
        },
        2: {
            0: Cell(x=0, y=2, value="x"),
            1: Cell(x=1, y=2, value="y"),
            2: Cell(x=2, y=2, value="z"),
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
            0: Cell(x=0, y=0, value="a"),
            1: Cell(x=1, y=0, value="b"),
            2: Cell(x=2, y=0, value="c"),
        },
        1: {
            0: Cell(x=0, y=1, value="d"),
            1: Cell(x=1, y=1, value="e"),
            2: Cell(x=2, y=1, value="f"),
        },
        2: {
            0: Cell(x=0, y=2, value="x"),
            1: Cell(x=1, y=2, value="y"),
            2: Cell(x=2, y=2, value="z"),
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
            0: Cell(x=0, y=0, value="a"),
            1: Cell(x=1, y=0, value="b"),
            2: Cell(x=2, y=0, value="c"),
        },
        1: {
            0: Cell(x=0, y=1, value="d"),
            1: Cell(x=1, y=1, value="e"),
            2: Cell(x=2, y=1, value="f"),
        },
        2: {
            0: Cell(x=0, y=2, value="x"),
            1: Cell(x=1, y=2, value="y"),
            2: Cell(x=2, y=2, value="z"),
        },
    }
