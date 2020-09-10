import math
from collections import defaultdict
from typing import Dict

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

    Args:
        list: An iterable representing a Sudoku board
        blank: The value used to represent a blank cell
    """

    __slots__ = tuple()

    def is_solved(self) -> bool:
        """
        Check whether puzzle is solved
        """
        return not any(c.is_blank() for c in self.cells)

    def solve(self) -> Dict[str, int]:
        """
        Solve the puzzle with strategies
        """
        candidate_eliminations = defaultdict(int)

        if self.has_conflicts():
            return None

        while not self.is_solved():
            changed = False
            for strategy in strategies(self.order):
                eliminations = strategy(self)

                if eliminations > 0:
                    candidate_eliminations[strategy.name] += eliminations
                    changed = True
                    break
            if not changed:
                return dict(candidate_eliminations)

        return dict(candidate_eliminations)

    def has_solution(self) -> bool:
        """
        Return whether the puzzle can be solved using strategies
        """
        return bool(Puzzle(self.to_string(), self.tokens[0]).solve())

    def rate(self) -> float:
        """
        Calculate the difficulty of solving the puzzle

        Returns:
            float: A difficulty score between 0 and 1
        """
        if self.is_solved():
            return 0

        candidate_eliminations = Puzzle(self.to_1D(), self.tokens[0]).solve()
        if not candidate_eliminations:
            return -1

        difficulties = dict()
        for strat in strategies(self.order):
            difficulties[strat.name] = strat.difficulty

        difficulty = 0
        for strat in candidate_eliminations.keys():
            ds = difficulties[strat]
            cs = candidate_eliminations[strat]
            difficulty += ds * (cs / self.order ** 2)

        return difficulty
