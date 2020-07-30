import pytest

from .. import Puzzle

prompts = {
    "boards": [
        "1.34.41..3.14.23",
        ".234.6789.567.9123.891.3456.345.7891.678.1234.912.4567.456.8912.789.2345.123.5678",
        "...1.5...14....67..8...24...63.7..1.9.......3.1..9.52...72...8..26....35...4.9...",
        ".....4.284.6.....51...3.6.....3.1....87...14....7.9.....2.1...39.....5.767.4.....",
        "72..96..3...2.5....8...4.2........6.1.65.38.7.4........3.8...9....7.2...2..43..18"
    ],
    "solutions": [
        "1234341223414123",
        "123456789456789123789123456234567891567891234891234567345678912678912345912345678",
        "672145398145983672389762451263574819958621743714398526597236184426817935831459267",
        "735164928426978315198532674249381756387256149561749832852617493914823567673495281",
        "725196483463285971981374526372948165196523847548617239634851792819762354257439618"
    ],
    "unsolvable": [
        "12341...2341....",
        ".234.6789.267.9123.891.3456.345.7891.678.1234.912.4567.456.8912.789.2345.123.5679"
    ]
}


def test_solve():
    for i in range(len(prompts["boards"])):
        puzzle = Puzzle(prompts["boards"][i], ".")
        assert(puzzle.hasSolution(), True)
        assert(puzzle.isSolved(), False)
        assert(puzzle.solve(), True)
        assert(puzzle.isSolved(), True)
        assert(puzzle.toString() == prompts["solutions"][i], True)


def test_unsolvable():
    for i in range(len(prompts["unsolvable"])):
        puzzle = Puzzle(prompts["unsolvable"][i], ".")
        assert(not puzzle.isSolved(), False)
        assert(not puzzle.hasSolution(), False)
        assert(not puzzle.solve(), False)
