import random
from typing import List

import numpy as np

from .types import ArrayLike, Index, PerfectSquare, Value


class Tokens(list):
    def swap(self, i: Value, j: Value):
        self[i], self[j] = self[j], self[i]

    def shuffle(self):
        tokens = self[1:]
        random.shuffle(tokens)
        self[1:] = tokens


class Candidates(set):
    def strip(self, v: Value):
        before = len(self)
        self.clear()
        self.add(v)
        return before - 1


class Cell:
    candidates: Candidates

    def __init__(self, order: PerfectSquare, value: Value):
        self.candidates = Candidates(i + 1 for i in range(order))
        if value != 0:
            self.candidates.strip(value)

    def value(self) -> Value:
        return next(iter(self.candidates), 0)

    def isBlank(self) -> bool:
        return len(self.candidates) > 1


class Board:
    order: PerfectSquare
    tokens: Tokens
    cells: List[Cell]

    def _box(self, index: Index):
        boxWidth = self.order ** .5
        row = index // self.order
        col = index % self.order
        edgeRow = boxWidth * row // boxWidth
        edgeCol = boxWidth * col // boxWidth
        for i in range(self.order):
            r = edgeRow + i // boxWidth
            c = edgeCol + (i % boxWidth)
            if not (r == row and c == col):
                yield self.order * r + c

    def _row(self, index: Index):
        row = (index / self.order) >> 0
        col = index % self.order
        for i in range(self.order):
            if i != col:
                yield self.order * row + i

    def _col(self, index: Index):
        row = index // self.order
        col = index % self.order
        for i in range(self.order):
            if i != row:
                yield self.order * i + col

    def _peers(self, index: Index):
        boxWidth = self.order ** .5
        row = index // self.order
        col = index % self.order
        edgeM = boxWidth * row // boxWidth
        edgeN = boxWidth * col // boxWidth
        for i in range(self.order):
            r = edgeM + i // boxWidth
            c = edgeN + i % boxWidth
            if i != col:
                yield int(self.order * row + i)
            if i != row:
                yield int(self.order * i + col)
            if not (r == row and c == col):
                yield int(self.order * r + c)

    def _blank(self, indices=None):
        if indices is None:
            indices = self.order ** 2
        for i in indices:
            if self.cells[i].isBlank():
                yield i

    def hasConflicts(self) -> bool:
        """
        A method to determine if the board has any conflicting cells
        """
        for i, cell in enumerate(self.cells):
            if not cell.isBlank():
                for p in self._peers(i):
                    peer = self.cells[p]
                    if not peer.isBlank() and cell.value() == peer.value():
                        return True
        return False

    def __init__(self, arr: ArrayLike, blank):
        arr = np.array(list(arr)).flatten()

        self.order = int(len(arr) ** .5)
        self.tokens = Tokens(blank)
        self.cells = np.empty(len(arr), dtype=object)

        for i, token in enumerate(arr):
            try:
                v = self.tokens.index(token)
            except ValueError:
                self.tokens.append(token)
                v = len(self.tokens) - 1
            self.cells[i] = Cell(self.order, v)

    def _shiftIndices(self, *indices: List[Index]):
        tmp = self.cells[indices[0]]
        for i in range(1, len(indices)):
            self.cells[indices[i - 1]] = self.cells[indices[i]]
        self.cells[indices[-1]] = tmp

    def reflect(self, direction="horizontal"):
        """
        Reflect the Sudoku board horizontally or vertically

        @ param direction The direction in reflection
        """
        n = self.order
        x = n // 2
        y = n - 1
        if direction == "horizontal":
            for i in range(n):
                for j in range(x):
                    self._shiftIndices(n * i + j, n * i + (y - j))
        else:
            for i in range(x):
                for j in range(n):
                    self._shiftIndices(n * i + j, n * (y - i) + j)

    def rotate(self, rotations=1):
        """
        Rotate the Sudoku board clockwise a given number in times.

        @ param rotations The number in clockwise rotations to be performed. self value may be negative and will be rounded.
        """
        if not isinstance(rotations, int):
            rotations = round(rotations)
        if rotations % 4 == 0:
            return
        elif rotations % 2 == 0:
            self.cells = np.flip(self.cells)
            return
        elif rotations < 0:
            self.rotate(-1 * rotations + 2)
        else:
            n = self.order
            x = n // 2
            y = n - 1
            for i in range(x):
                for j in range(i, y-i):
                    self._shiftIndices(
                        n * i + j,
                        n * (y - j) + i,
                        n * (y - i) + y - j,
                        n * j + y - i
                    )

            self.rotate(rotations - 1)

    def transpose(self):
        """
        Switch the rows and columns in the Sudoku board
        """
        n = self.order
        for i in range(n):
            for j in range(i + 1, n):
                self._shiftIndices(n * i + j, n * j + i)

    def shuffle(self):
        """
        Shuffle the board using rotations, reflections, and token-swapping
        """
        self.tokens.shuffle()
        for i in range(self.order // 2):
            self.reflect(random.choice(("horizontal", "vertical")))
            self.rotate(random.choice(range(4)))

    def to1D(self):
        """
        A method for getting back the Sudoku board as a 1-dimensional array

        @ returns A 1D array in the Sudoku board
        """
        return [self.tokens[c.value()] for c in self.cells]

    def to2D(self):
        """
        A method for getting back the Sudoku board as a 2-dimensional array

        @ returns A 2D array in the Sudoku board
        """
        return np.reshape(self.to1D(), (self.order, self.order)).tolist()

    def toString(self) -> str:
        """
        A method for getting back the Sudoku board as a string

        @ returns A string representation in the Sudoku board
        """
        return "".join(self.to1D())

    def toFormattedString(self,
                          cellCorner="┼",
                          boxCorner="╬",
                          topLeftCorner="╔",
                          topRightCorner="╗",
                          bottomLeftCorner="╚",
                          bottomRightCorner="╝",
                          innerTopTowerCorner="╦",
                          innerBottomTowerCorner="╩",
                          innerLeftFloorCorner="╠",
                          innerRightFloorCorner="╣",
                          cellHorizontalBorder="─",
                          boxHorizontalBorder="═",
                          cellVerticalBorder="│",
                          boxVerticalBorder="║",
                          blank=" "):
        """
        A method for getting back the Sudoku board as a formatted string

        @ returns A formatted string representing the Sudoku board
        """
        unit = int(self.order ** .5)
        tokenWidth = max([len(str(t)) for t in self.tokens])

        cellWidth = tokenWidth + 2
        boxWidth = unit * (cellWidth + 1) - 1

        topBorder = topLeftCorner + boxHorizontalBorder * \
            (boxWidth) + (innerTopTowerCorner + boxHorizontalBorder *
                          (boxWidth)) * (unit - 1) + topRightCorner
        bottomBorder = bottomLeftCorner + boxHorizontalBorder * \
            (boxWidth) + (innerBottomTowerCorner + boxHorizontalBorder *
                          (boxWidth)) * (unit - 1) + bottomRightCorner
        floorBorder = innerLeftFloorCorner + boxHorizontalBorder * \
            (boxWidth) + (boxCorner + boxHorizontalBorder *
                          (boxWidth)) * (unit - 1) + innerRightFloorCorner
        barBorder = (boxVerticalBorder + cellHorizontalBorder * (cellWidth) + (cellCorner +
                                                                               cellHorizontalBorder * (cellWidth)) * (unit - 1)) * (unit) + boxVerticalBorder

        formattedString = f"{topBorder}\n{boxVerticalBorder} "
        for i, c in enumerate(self.cells):
            v = c.value()
            formattedString += f"{self.tokens[v] if not c.isBlank() else blank} "
            if ((i + 1) % (self.order * unit) == 0):
                if (i + 1 == len(self.cells)):
                    formattedString += f"{boxVerticalBorder}\n{bottomBorder}"
                else:
                    formattedString += f"{boxVerticalBorder}\n{floorBorder}\n{boxVerticalBorder} "
            elif ((i + 1) % self.order == 0):
                formattedString += f"{boxVerticalBorder}\n{barBorder}\n{boxVerticalBorder} "
            elif ((i + 1) % unit == 0):
                formattedString += f"{boxVerticalBorder} "
            else:
                formattedString += f"{cellVerticalBorder} "

        return formattedString
