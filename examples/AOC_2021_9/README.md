# AOC 2021 day 9

In [Advent of Code 2021](https://adventofcode.com/2021), the [day 9 puzzle](https://adventofcode.com/2021/day/9) involved analyzing a grid.  From their page, the instructions read,

```
Consider the following heightmap:

2199943210
3987894921
9856789892
8767896789
9899965678

Each number corresponds to the height of a particular location, where 9 is the highest and 0 is the lowest a location can be.

Your first goal is to find the low points - the locations that are lower than any of its adjacent locations. Most locations have four adjacent locations (up, down, left, and right); locations on the edge or corner of the map have three or two adjacent locations, respectively. (Diagonal locations do not count as adjacent.)

In the above example, there are four low points: two are in the first row (a 1 and a 0), one is in the third row (a 5), and one is in the bottom row (also a 5). All other locations on the heightmap have some lower adjacent location, and so are not low points.
```

A second part to the problem, only seen on the Advent of Code page if you solve the first problem, is to map out "basins" around the low points.  I've edited the text from their page since I do not have the numbers highlighted.

```
A basin is all locations that eventually flow downward to a single low point. Therefore, every low point has a basin, although some basins are very small. Locations of height 9 do not count as being in any basin, and all other locations will always be part of exactly one basin.

The size of a basin is the number of locations within the basin, including the low point. The example above has four basins.

The top-left basin, size 3, contain points 1, 2, and 3:

2199943210
3987894921
9856789892
8767896789
9899965678

The top-right basin (starting with low-point 0) is size 9.  The middle basin starting with low-point 5 is size 14.  The bottom-right basin starting with low-point 5 is size 9.
```


The Notebook in this directory shows how `gridthings` can be used to answer those puzzle questions.

## Notebook

To launch the Notebook in this folder on your own machine, clone this repository and follow the developer steps on the main README to set up `poetry`.  Once `poetry` is available on your system Python, you can run `poetry install` -> `poetry shell` -> `jupyter`.
