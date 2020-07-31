# `sudoku-tools`

[![](https://img.shields.io/pypi/v/sudoku-tools.svg?style=flat)](https://pypi.org/pypi/sudoku-tools/)
[![](https://img.shields.io/pypi/dw/sudoku-tools.svg?style=flat)](https://pypi.org/pypi/sudoku-tools/)
[![](https://img.shields.io/pypi/pyversions/sudoku-tools.svg?style=flat)](https://pypi.org/pypi/sudoku-tools/)
[![](https://img.shields.io/pypi/format/sudoku-tools.svg?style=flat)](https://pypi.org/pypi/sudoku-tools/)
[![](https://img.shields.io/pypi/l/sudoku-tools.svg?style=flat)](https://github.com/dawsonbooth/sudoku-tools/blob/master/LICENSE)

## Description

This Python package is a collection of useful tools for generating, grading, solving, and transforming sudoku puzzles.

## Installation

With [Python](https://www.python.org/downloads/) installed, simply run the following command to add the package to your project.

```bash
pip install sudoku-tools
```

## Usage

The object can be constructed with a 1-dimensional board:

```python
arr_1d = [1, 0, 3, 4, 0, 4, 1, 0, 0, 3, 0, 1, 4, 0, 2, 3]
puzzle = Puzzle(arr_1d, 0)
```
... or with a 2-dimensional board:

```python
arr_2d = [[1, 0, 3, 4],
	[0, 4, 1, 0],
	[0, 3, 0, 1],
	[4, 0, 2, 3]]
puzzle = Puzzle(arr_2d, 0)
```

Feel free to [check out the docs](https://dawsonbooth.github.io/sudoku-tools/) for more information.

## License

This software is released under the terms of [MIT license](LICENSE).
