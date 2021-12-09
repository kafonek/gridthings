import pandas

from gridthings import Grid

data = "abc\ndef\nxyz"
grid = Grid(data)
df = pandas.DataFrame(grid.data)


def test_dataframe():

    assert df.shape == (3, 3)
    assert df.iloc[0, 0] == "a"
    assert (
        df.applymap(lambda cell: cell.value).to_string()
        == "   0  1  2\n0  a  d  x\n1  b  e  y\n2  c  f  z"
    )
