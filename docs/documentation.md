<a name="sudoku"></a>
# sudoku

<a name="sudoku.board"></a>
# sudoku.board

<a name="sudoku.board.Board"></a>
## Board Objects

```python
class Board()
```

<a name="sudoku.board.Board.has_conflicts"></a>
#### has\_conflicts

```python
 | has_conflicts() -> bool
```

A method to determine if the board has any conflicting cells

<a name="sudoku.board.Board.reflect"></a>
#### reflect

```python
 | reflect(direction="horizontal") -> None
```

Reflect the Sudoku board horizontally or vertically

@param direction The direction in reflection

<a name="sudoku.board.Board.rotate"></a>
#### rotate

```python
 | rotate(rotations=1) -> None
```

Rotate the Sudoku board clockwise a given number in times.

@param rotations The number in clockwise rotations to be performed. self value may be negative and will be rounded.

<a name="sudoku.board.Board.transpose"></a>
#### transpose

```python
 | transpose() -> None
```

Switch the rows and columns in the Sudoku board

<a name="sudoku.board.Board.shuffle"></a>
#### shuffle

```python
 | shuffle() -> None
```

Shuffle the board using rotations, reflections, and token-swapping

<a name="sudoku.board.Board.to_1D"></a>
#### to\_1D

```python
 | to_1D()
```

A method for getting back the Sudoku board as a 1-dimensional array

@returns A 1D array in the Sudoku board

<a name="sudoku.board.Board.to_2D"></a>
#### to\_2D

```python
 | to_2D()
```

A method for getting back the Sudoku board as a 2-dimensional array

@returns A 2D array in the Sudoku board

<a name="sudoku.board.Board.to_string"></a>
#### to\_string

```python
 | to_string() -> str
```

A method for getting back the Sudoku board as a string

@returns A string representation in the Sudoku board

<a name="sudoku.board.Board.to_formatted_string"></a>
#### to\_formatted\_string

```python
 | to_formatted_string(cell_corner="┼", box_corner="╬", top_left_corner="╔", top_right_corner="╗", bottom_left_corner="╚", bottom_right_corner="╝", inner_top_tower_corner="╦", inner_bottom_tower_corner="╩", inner_left_floor_corner="╠", inner_right_floor_corner="╣", cell_horizontal_border="─", box_horizontal_border="═", cell_vertical_border="│", box_vertical_border="║", blank=" ") -> str
```

A method for getting back the Sudoku board as a formatted string

@returns A formatted string representing the Sudoku board

<a name="sudoku.examples"></a>
# sudoku.examples

<a name="sudoku.examples.boards"></a>
# sudoku.examples.boards

<a name="sudoku.examples.rate"></a>
# sudoku.examples.rate

<a name="sudoku.examples.shuffle"></a>
# sudoku.examples.shuffle

<a name="sudoku.examples.solve"></a>
# sudoku.examples.solve

<a name="sudoku.puzzle"></a>
# sudoku.puzzle

<a name="sudoku.puzzle.Puzzle"></a>
## Puzzle Objects

```python
class Puzzle(Board)
```

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

<a name="sudoku.puzzle.Puzzle.is_solved"></a>
#### is\_solved

```python
 | is_solved() -> bool
```

Check whether puzzle is solved

<a name="sudoku.puzzle.Puzzle.solve"></a>
#### solve

```python
 | solve() -> Dict[str, int]
```

Solve the puzzle with strategies

<a name="sudoku.puzzle.Puzzle.has_solution"></a>
#### has\_solution

```python
 | has_solution() -> bool
```

Return whether the puzzle can be solved using strategies

<a name="sudoku.puzzle.Puzzle.rate"></a>
#### rate

```python
 | rate() -> float
```

Calculate the difficulty of solving the puzzle

@returns A difficulty score between 0 and 1

<a name="sudoku.strategies"></a>
# sudoku.strategies

<a name="sudoku.strategies.Strategy"></a>
## Strategy Objects

```python
class Strategy()
```

Also known as a [Solving Technique](http://sudopedia.enjoysudoku.com/Solving_Technique.html)

<a name="sudoku.strategies.RefreshCandidates"></a>
## RefreshCandidates Objects

```python
class RefreshCandidates(Strategy)
```

Remove invalid candidates from each cell

<a name="sudoku.strategies.HiddenSubset"></a>
## HiddenSubset Objects

```python
class HiddenSubset(Strategy)
```

Apply the [Hidden Subset](http://sudopedia.enjoysudoku.com/Hidden_Subset.html) strategy

<a name="sudoku.strategies.HiddenSingle"></a>
## HiddenSingle Objects

```python
class HiddenSingle(HiddenSubset)
```

The [Hidden Single](http://sudopedia.enjoysudoku.com/Hidden_Single.html) strategy

<a name="sudoku.strategies.NakedSubset"></a>
## NakedSubset Objects

```python
class NakedSubset(Strategy)
```

Apply the [Naked Subset](http://sudopedia.enjoysudoku.com/Naked_Subset.html) strategy

<a name="sudoku.strategies.NakedSingle"></a>
## NakedSingle Objects

```python
class NakedSingle(NakedSubset)
```

The [Naked Single](http://sudopedia.enjoysudoku.com/Naked_Single.html) strategy

<a name="sudoku.strategies.ForcedDigit"></a>
#### ForcedDigit

Alias for the [[NakedSingle]] strategy

<a name="sudoku.strategies.NakedDouble"></a>
## NakedDouble Objects

```python
class NakedDouble(NakedSubset)
```

Apply the [Naked Double](http://sudopedia.enjoysudoku.com/Naked_Double.html) strategy

<a name="sudoku.strategies.NakedTriple"></a>
## NakedTriple Objects

```python
class NakedTriple(NakedSubset)
```

Apply the [Naked Triple](http://sudopedia.enjoysudoku.com/Naked_Triple.html) strategy

<a name="sudoku.strategies.NakedQuad"></a>
## NakedQuad Objects

```python
class NakedQuad(NakedSubset)
```

Apply the [Naked Quad](http://sudopedia.enjoysudoku.com/Naked_Quad.html) strategy

<a name="sudoku.strategies.strategies"></a>
#### strategies

```python
strategies(order: PerfectSquare)
```

Generator for strategies from simple to complex with a given order

<a name="sudoku.test"></a>
# sudoku.test

<a name="sudoku.test.test_board"></a>
# sudoku.test.test\_board

<a name="sudoku.test.test_puzzle"></a>
# sudoku.test.test\_puzzle

<a name="sudoku.types"></a>
# sudoku.types

