from typing import Iterator

from .types import Index, PerfectSquare


class Strategy:
    """
    Also known as a [Solving Technique](http://sudopedia.enjoysudoku.com/Solving_Technique.html)
    """
    __slots__ = 'name', 'difficulty'

    name: str
    difficulty: float

    def __init__(self):
        self.name = self.__class__.__name__

    def use(self, puzzle) -> int:
        pass


class RefreshCandidates(Strategy):
    """
    Remove invalid candidates from each cell
    """

    def __init__(self):
        super().__init__()
        self.difficulty = 0.0769

    def use(self, puzzle):
        uses = 0
        for i, cell in enumerate(puzzle.cells):
            changed = False
            for p in puzzle._peers(i):
                peer = puzzle.cells[p]
                if cell.isBlank() and not peer.isBlank():
                    d = cell.candidates.delete(peer.value())
                    changed = d if d else changed
            uses += 1 if changed else 0
        return uses


class HiddenSubset(Strategy):
    """
    Apply the [Hidden Subset](http://sudopedia.enjoysudoku.com/Hidden_Subset.html) strategy
    """

    def __init__(self, size):
        super().__init__()
        self.name += f" - {size}"
        self.difficulty = 0.0163 * size

    def use(self, puzzle):
        if size <= 0 or size >= puzzle.order:
            return 0
        complement = puzzle.order - size
        if complement < size:
            return NakedSubset(complement).use(puzzle)
        uses = 0
        for b in puzzle._blank():
            changed = False
            for v in puzzle.cells[b].candidates.values():
                if any(
                    not any(puzzle.cells[p].candidates.has(v)
                            for p in puzzle._box(b)),
                    not any(puzzle.cells[p].candidates.has(v)
                            for p in puzzle._row(b)),
                    not any(puzzle.cells[p].candidates.has(v)
                            for p in puzzle._col(b)),
                ):
                    s = puzzle.cells[b].candidates.strip(v) > 0
                    changed = s if s else changed
                    break

            uses += 1 if changed else 0

        return uses


class HiddenSingle(HiddenSubset):
    """
    The [Hidden Single](http://sudopedia.enjoysudoku.com/Hidden_Single.html) strategy
    """

    def __init__(self):
        super().__init__(1)


"""
Alias for the [[HiddenSingle]] strategy
"""
PinnedDigit = HiddenSingle


class NakedSubset(Strategy):
    """
    Apply the [Naked Subset](http://sudopedia.enjoysudoku.com/Naked_Subset.html) strategy
    """

    def __init__(self, size):
        super().__init__()
        self.name += f" - {size}"
        self.difficulty = 0.0323 * size

    def use(self, puzzle):
        if size <= 1 or size >= puzzle.order:
            return 0
        complement = puzzle.order - size
        if complement < size:
            return HiddenSubset(complement).use(puzzle)
        uses = 0
        for b in puzzle._blank():
            changed = False
            candidates = puzzle.cells[b].candidates
            if candidates.size == size:
                for house in [puzzle._row, puzzle._col, puzzle._box]:
                    peers = set([c for c in house(b)])
                    for p in peers:
                        if puzzle.cells[p].candidates.size <= size and all(candidates.has(pc) for pc in puzzle.cells[p].candidates):
                            peers.delete(p)
                    if peers.size == puzzle.order - size:
                        for p in peers:
                            for c in candidates:
                                d = puzzle.cells[p].candidates.delete(c)
                                changed = d if d else changed

            uses += 1 if changed else 0

        return uses


class NakedSingle(NakedSubset):
    """
    The [Naked Single](http://sudopedia.enjoysudoku.com/Naked_Single.html) strategy
    """

    def __init__(self):
        super().__init__(1)


"""
Alias for the [[NakedSingle]] strategy
"""
ForcedDigit = NakedSingle

"""
Alias for the [[NakedSingle]] strategy
"""
SoleCandidate = NakedSingle


class NakedDouble(NakedSubset):
    """
    Apply the [Naked Double](http://sudopedia.enjoysudoku.com/Naked_Double.html) strategy
    """

    def __init__(self):
        super().__init__(2)


class NakedTriple(NakedSubset):
    """
    Apply the [Naked Triple](http://sudopedia.enjoysudoku.com/Naked_Triple.html) strategy
    """

    def __init__(self):
        super().__init__(3)


class NakedQuad(NakedSubset):
    """
    Apply the [Naked Quad](http://sudopedia.enjoysudoku.com/Naked_Quad.html) strategy
    """

    def __init__(self):
        super().__init__(4)


def strategies(order: PerfectSquare):
    """
    Generator for strategies from simple to complex with a given order
    """
    yield RefreshCandidates
    yield HiddenSingle
    for s in range(2, order // 2):
        yield NakedSubset(s)
