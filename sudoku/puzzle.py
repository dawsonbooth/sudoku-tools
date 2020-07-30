import math

from .board import Board
from .strategies import strategies


class Puzzle(Board):
    """
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
    @param list An array-like object representing a Sudoku board
    @param blank The value used to represent a blank cell
    """

    def is_solved(self) -> bool:
        """
        Check whether puzzle is solved
        """
        return not any(c.isBlank() for c in self.cells)

    def solve(self):
        """
        Solve the puzzle with strategies
        """
        uses = dict()
        for strat in strategies(self.order):
            uses[strat.name] = 0

        if self.has_conflicts():
            return None

        while not self.is_solved():
            changed = False
            for strat in strategies(self.order):
                eliminations = strat(self)
                if eliminations > 0:
                    changed = True
                    break
                uses[strat.name] += eliminations
            if not changed:
                return None

        return uses

    def has_solution(self):
        """
        Return whether the puzzle can be solved using strategies
        """
        return Puzzle(self.to_1D(), self.tokens[0]).solve() is not None

    def rate(self):
        """
        Calculate the difficulty of solving the puzzle

        @returns A difficulty score between 0 and 1
        """
        if self.is_solved():
            return 0
        uses = Puzzle(self.to_1D(), self.tokens[0]).solve()
        if not uses:
            return -1

        difficulties = dict()
        for strat in strategies(self.order):
            difficulties[strat.name] = strat.difficulty

        S = 0
        for strat in difficulties:
            ds = difficulties[strat]
            us = uses[strat]
            S += ds * us

        k = 1 / math.e ** 2
        difficulty = (k * S) / (k * S + 1)
        return difficulty
