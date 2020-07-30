import math

from .board import Board
from .strategies import strategies


class Puzzle(Board):
    """
    The object can be constructed with a 1-dimensional board:
    '''python
    arr1D = [1, 0, 3, 4, 0, 4, 1, 0, 0, 3, 0, 1, 4, 0, 2, 3]
    puzzle = Puzzle(arr1D, 0)
    '''
    ... or with a 2-dimensional board:
    '''python
    arr2D = [[1, 0, 3, 4],
            [0, 4, 1, 0],
            [0, 3, 0, 1],
            [4, 0, 2, 3]]
    puzzle = Puzzle(arr2D, 0)

    '''
    @param list An array-like object representing a Sudoku board
    @param blank The value used to represent a blank cell
    """

    def isSolved(self) -> bool:
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

        if self.hasConflicts():
            return None

        while not self.isSolved():
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

    def hasSolution(self):
        """
        Return whether the puzzle can be solved using strategies
        """
        return Puzzle(self.to1D(), self.tokens[0]).solve() is not None

    def rate(self):
        """
        Calculate the difficulty of solving the puzzle

        @returns A difficulty score between 0 and 1
        """
        if self.isSolved():
            return 0
        uses = Puzzle(self.to1D(), self.tokens[0]).solve()
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
