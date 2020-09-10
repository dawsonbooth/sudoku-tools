import random
from typing import List

import numpy as np

from .types import ArrayLike, Index, PerfectSquare, Value


class Tokens(list):
    __slots__ = tuple()

    def swap(self, i: Value, j: Value):
        self[i], self[j] = self[j], self[i]

    def shuffle(self):
        tokens = self[1:]
        random.shuffle(tokens)
        self[1:] = tokens


class Candidates(set):
    __slots__ = tuple()

    def strip(self, *candidates):
        before = len(self)
        self.clear()
        for c in candidates:
            self.add(c)
        return before - len(self)


class Cell:
    __slots__ = 'candidates',

    candidates: Candidates

    def __init__(self, order: PerfectSquare, value: Value):
        self.candidates = Candidates(i + 1 for i in range(order))
        if value != 0:
            self.candidates.strip(value)

    def value(self) -> Value:
        if len(self.candidates) > 1:
            return 0
        return next(iter(self.candidates))

    def is_blank(self) -> bool:
        return len(self.candidates) > 1


class Board:
    __slots__ = 'order', 'tokens', 'cells'

    order: PerfectSquare
    tokens: Tokens
    cells: List[Cell]

    def _box(self, index: Index):
        boxWidth = int(self.order ** .5)
        row = index // self.order
        col = index % self.order
        edgeRow = boxWidth * (row // boxWidth)
        edgeCol = boxWidth * (col // boxWidth)

        for i in range(self.order):
            r = edgeRow + i // boxWidth
            c = edgeCol + (i % boxWidth)
            if not (r == row and c == col):
                p = int(self.order * r + c)
                yield p, self.cells[p]

    def _row(self, index: Index):
        row = index // self.order
        col = index % self.order

        for i in range(self.order):
            if i != col:
                p = int(self.order * row + i)
                yield p, self.cells[p]

    def _col(self, index: Index):
        row = index // self.order
        col = index % self.order

        for i in range(self.order):
            if i != row:
                p = int(self.order * i + col)
                yield p, self.cells[p]

    def _peers(self, index: Index):
        boxWidth = int(self.order ** .5)
        row = index // self.order
        col = index % self.order
        edgeM = boxWidth * (row // boxWidth)
        edgeN = boxWidth * (col // boxWidth)

        peers = set()

        for i in range(self.order):
            r = edgeM + i // boxWidth
            c = edgeN + i % boxWidth
            if i != col:
                p = int(self.order * row + i)
                if p not in peers:
                    yield p, self.cells[p]
                    peers.add(p)
            if i != row:
                p = int(self.order * i + col)
                if p not in peers:
                    yield p, self.cells[p]
                    peers.add(p)
            if not (r == row and c == col):
                p = int(self.order * r + c)
                if p not in peers:
                    yield p, self.cells[p]
                    peers.add(p)

    def _blank(self, indices=None):
        if indices is None:
            indices = range(self.order ** 2)
        for i in indices:
            cell = self.cells[i]
            if cell.is_blank():
                yield i, cell

    def has_conflicts(self) -> bool:
        """
        A method to determine if the board has any conflicting cells
        """
        for i, cell in enumerate(self.cells):
            if not cell.is_blank():
                for _, peer in self._peers(i):
                    if not peer.is_blank() and cell.value() == peer.value():
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

    def _shift_indices(self, *indices: List[Index]) -> None:
        tmp = self.cells[indices[0]]
        for i in range(1, len(indices)):
            self.cells[indices[i - 1]] = self.cells[indices[i]]
        self.cells[indices[-1]] = tmp

    def reflect(self, direction="horizontal") -> None:
        """
        Reflect the Sudoku board horizontally or vertically

        @param direction The direction in reflection
        """
        n = self.order
        x = n // 2
        y = n - 1
        if direction == "horizontal":
            for i in range(n):
                for j in range(x):
                    self._shift_indices(n * i + j, n * i + (y - j))
        else:
            for i in range(x):
                for j in range(n):
                    self._shift_indices(n * i + j, n * (y - i) + j)

    def rotate(self, rotations=1) -> None:
        """
        Rotate the Sudoku board clockwise a given number in times.

        @param rotations The number in clockwise rotations to be performed. self value may be negative and will be rounded.
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
                    self._shift_indices(
                        n * i + j,
                        n * (y - j) + i,
                        n * (y - i) + y - j,
                        n * j + y - i
                    )

            self.rotate(rotations - 1)

    def transpose(self) -> None:
        """
        Switch the rows and columns in the Sudoku board
        """
        n = self.order
        for i in range(n):
            for j in range(i + 1, n):
                self._shift_indices(n * i + j, n * j + i)

    def shuffle(self) -> None:
        """
        Shuffle the board using rotations, reflections, and token-swapping
        """
        self.tokens.shuffle()
        for _ in range(self.order // 2):
            self.reflect(random.choice(("horizontal", "vertical")))
            self.rotate(random.choice(range(4)))

    def to_1D(self):
        """
        A method for getting back the Sudoku board as a 1-dimensional array

        @returns A 1D array in the Sudoku board
        """
        return [self.tokens[c.value()] for c in self.cells]

    def to_2D(self):
        """
        A method for getting back the Sudoku board as a 2-dimensional array

        @returns A 2D array in the Sudoku board
        """
        return np.reshape(self.to_1D(), (self.order, self.order)).tolist()

    def to_string(self) -> str:
        """
        A method for getting back the Sudoku board as a string

        @returns A string representation in the Sudoku board
        """
        return "".join(self.to_1D())

    def to_formatted_string(self,
                            cell_corner="┼",
                            box_corner="╬",
                            top_left_corner="╔",
                            top_right_corner="╗",
                            bottom_left_corner="╚",
                            bottom_right_corner="╝",
                            inner_top_tower_corner="╦",
                            inner_bottom_tower_corner="╩",
                            inner_left_floor_corner="╠",
                            inner_right_floor_corner="╣",
                            cell_horizontal_border="─",
                            box_horizontal_border="═",
                            cell_vertical_border="│",
                            box_vertical_border="║",
                            blank=" ") -> str:
        """
        A method for getting back the Sudoku board as a formatted string

        @returns A formatted string representing the Sudoku board
        """
        unit = int(self.order ** .5)
        token_width = max([len(str(t)) for t in self.tokens])

        cell_width = token_width + 2
        box_width = unit * (cell_width + 1) - 1

        top_border = top_left_corner + box_horizontal_border * \
            (box_width) + (inner_top_tower_corner + box_horizontal_border *
                           (box_width)) * (unit - 1) + top_right_corner
        bottom_border = bottom_left_corner + box_horizontal_border * \
            (box_width) + (inner_bottom_tower_corner + box_horizontal_border *
                           (box_width)) * (unit - 1) + bottom_right_corner
        floor_border = inner_left_floor_corner + box_horizontal_border * \
            (box_width) + (box_corner + box_horizontal_border *
                           (box_width)) * (unit - 1) + inner_right_floor_corner
        bar_border = (box_vertical_border + cell_horizontal_border * (cell_width) + (cell_corner +
                                                                                     cell_horizontal_border * (cell_width)) * (unit - 1)) * (unit) + box_vertical_border

        formatted_str = f"{top_border}\n{box_vertical_border} "
        for i, c in enumerate(self.cells):
            v = c.value()
            formatted_str += f"{self.tokens[v] if not c.is_blank() else blank} "
            if (i + 1) % (self.order * unit) == 0:
                if i + 1 == len(self.cells):
                    formatted_str += f"{box_vertical_border}\n{bottom_border}"
                else:
                    formatted_str += f"{box_vertical_border}\n{floor_border}\n{box_vertical_border} "
            elif (i + 1) % self.order == 0:
                formatted_str += f"{box_vertical_border}\n{bar_border}\n{box_vertical_border} "
            elif (i + 1) % unit == 0:
                formatted_str += f"{box_vertical_border} "
            else:
                formatted_str += f"{cell_vertical_border} "

        return formatted_str
