from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..puzzle import Puzzle, T


class Solver:
    def solve(self, puzzle: Puzzle[T]) -> None:
        """
        Solve the puzzle in place.

        Args:
            puzzle (Puzzle): The puzzle to be solved.
        """
