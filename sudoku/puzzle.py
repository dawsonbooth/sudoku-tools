import math

from .board import Board
from .strategies import strategies


# /**
#  * @typeparam T The type of the value that may exist in a cell
#  */
class Puzzle(Board):
    # /**
    #  * Check whether puzzle is solved
    #  */
    def isSolved(self) -> bool:
        return not any(c.isBlank() for c in self.cells)

    # /**
    #  * Solve the puzzle with strategies
    #  */
    def solve(self):
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

    # /**
    #  * Return whether the puzzle can be solved using strategies
    #  */
    def hasSolution(self):
        return Puzzle(self.to1D(), self.tokens[0]).solve() is not None

    # /**
    #  * Calculate the difficulty of solving the puzzle
    #  *
    #  * @returns A difficulty score between 0 and 1
    #  */
    def rate(self):
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
