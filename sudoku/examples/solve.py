from .boards import boards
from .. import Puzzle

if __name__ == "__main__":
    for i, board in enumerate(boards):
        print(f"Board {i}: {board}")

        puzzle = Puzzle(board, ".")

        print(f"Puzzle {i}:\n{puzzle.toFormattedString()}")

        puzzle.solve()

        print(f"Solution:\n{puzzle.toFormattedString()}")
