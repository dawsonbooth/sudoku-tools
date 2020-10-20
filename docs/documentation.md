<a name="sudoku"></a>
# sudoku

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
## ForcedDigit Objects

```python
class ForcedDigit(NakedSingle)
```

Alias for the [[NakedSingle]] strategy

<a name="sudoku.strategies.SoleCandidate"></a>
## SoleCandidate Objects

```python
class SoleCandidate(NakedSingle)
```

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
strategies(order: int)
```

Generator for strategies from simple to complex with a given order

<a name="sudoku.puzzle"></a>
# sudoku.puzzle

<a name="sudoku.puzzle.Puzzle"></a>
## Puzzle Objects

```python
class Puzzle(Generic[T])
```

The base class for a sudoku puzzle.
```

Args:
    Generic (T): The base type for each token in the sudoku puzzle

Attributes:
    tokens (Tokens): A list of the tokens in use in the sudoku puzzle as identified by their integer aliases,
        which are the respective indices of this list.
    order (int): The number of unique tokens in use in the puzzle. For the common 9x9 sudoku puzzle,
        this value is 9.
    cells (List[Cell]): A list of all the cells in the sudoku puzzle.

<a name="sudoku.puzzle.Puzzle.Tokens"></a>
## Tokens Objects

```python
class Tokens(List[T])
```

A list of the tokens in use in the sudoku puzzle as identified by their integer aliases,
which are the respective indices of this list.

**Arguments**:

- `List` _[type]_ - [description]

<a name="sudoku.puzzle.Puzzle.Tokens.swap"></a>
#### swap

```python
 | swap(i: Value, j: Value)
```

Switch the positions of two sets of tokens in the puzzle by switching their respective aliases.

**Arguments**:

- `i` _Value_ - The integer alias value associated with a token
- `j` _Value_ - The integer alias value associated with a token

<a name="sudoku.puzzle.Puzzle.Tokens.shuffle"></a>
#### shuffle

```python
 | shuffle()
```

Randomly swap the tokens in the puzzle by randomizing their integer aliases.

<a name="sudoku.puzzle.Puzzle.Cell"></a>
## Cell Objects

```python
class Cell()
```

The class for an individual cell in the sudoku puzzle

**Attributes**:

- `puzzle` _Puzzle[T]_ - The corresponding sudoku puzzle
- `candidates` _Set[Value]_ - A set of the cell's remaining candidates
- `value` _Value_ - The value of the sudoku cell or 0 if it is blank.

<a name="sudoku.puzzle.Puzzle.Cell.is_blank"></a>
#### is\_blank

```python
 | is_blank() -> bool
```

Check whether the cell is blank or has a value.

**Returns**:

- `bool` - A boolean value for whether the cell is blank.

<a name="sudoku.puzzle.Puzzle.has_conflicts"></a>
#### has\_conflicts

```python
 | has_conflicts() -> bool
```

A method to determine if the board has any conflicting cells

**Returns**:

- `bool` - True if the board has conflicts, False otherwise

<a name="sudoku.puzzle.Puzzle.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(iterable: Iterable[T], blank: T)
```

The object can be constructed with a 1-dimensional board:
... or with a 2-dimensional board:

```python
arr_1d = [1, 0, 3, 4, 0, 4, 1, 0, 0, 3, 0, 1, 4, 0, 2, 3]
puzzle = Puzzle(arr_1d, 0)
```
```python
arr_2d = [[1, 0, 3, 4],
        [0, 4, 1, 0],
        [0, 3, 0, 1],
        [4, 0, 2, 3]]
puzzle = Puzzle(arr_2d, 0)
```

**Arguments**:

- `iterable` _Iterable[T]_ - An iterable representing a Sudoku board
- `blank` _T_ - The value used to represent a blank cell

<a name="sudoku.puzzle.Puzzle.reflect"></a>
#### reflect

```python
 | reflect(direction: str = "horizontal") -> None
```

Reflect the Sudoku board horizontally or vertically

**Arguments**:

- `direction` _str_ - The direction over which to reflect. Defaults to "horizontal".

<a name="sudoku.puzzle.Puzzle.rotate"></a>
#### rotate

```python
 | rotate(rotations=1) -> None
```

Rotate the Sudoku board clockwise a given number in times.

**Arguments**:

- `rotations` _int_ - The number in clockwise rotations to be performed.
  This value may be negative and is rounded to the nearest integer.
  Defaults to 1.

<a name="sudoku.puzzle.Puzzle.transpose"></a>
#### transpose

```python
 | transpose() -> None
```

Switch the rows and columns in the Sudoku board

<a name="sudoku.puzzle.Puzzle.shuffle"></a>
#### shuffle

```python
 | shuffle() -> None
```

Shuffle the board using rotations, reflections, and token-swapping

<a name="sudoku.puzzle.Puzzle.to_1D"></a>
#### to\_1D

```python
 | to_1D() -> List[T]
```

A method for getting back the Sudoku board as a 1-dimensional array

**Returns**:

- `List[T]` - A 1D array of the Sudoku board in the board's original type

<a name="sudoku.puzzle.Puzzle.to_2D"></a>
#### to\_2D

```python
 | to_2D() -> List[List[T]]
```

A method for getting back the Sudoku board as a 2-dimensional array

**Returns**:

- `List[T]` - A 2D array of the Sudoku board in the board's original type

<a name="sudoku.puzzle.Puzzle.to_string"></a>
#### to\_string

```python
 | to_string() -> str
```

A method for getting back the Sudoku board as a string

**Returns**:

- `str` - A string representation in the Sudoku board

<a name="sudoku.puzzle.Puzzle.to_formatted_string"></a>
#### to\_formatted\_string

```python
 | to_formatted_string(cell_corner="┼", box_corner="╬", top_left_corner="╔", top_right_corner="╗", bottom_left_corner="╚", bottom_right_corner="╝", inner_top_tower_corner="╦", inner_bottom_tower_corner="╩", inner_left_floor_corner="╠", inner_right_floor_corner="╣", cell_horizontal_border="─", box_horizontal_border="═", cell_vertical_border="│", box_vertical_border="║", blank=" ") -> str
```

A method for getting back the Sudoku board as a formatted string

**Returns**:

- `str` - A formatted string representing the Sudoku board

<a name="sudoku.puzzle.Puzzle.is_solved"></a>
#### is\_solved

```python
 | is_solved() -> bool
```

Check whether the puzzle is solved

**Returns**:

- `bool` - A boolean value indicating whether the puzzle is solved

<a name="sudoku.puzzle.Puzzle.solve"></a>
#### solve

```python
 | solve() -> Dict[str, int]
```

Solve the puzzle using strategies

**Returns**:

  Dict[str, int]: A dict containing the number of candidates eliminated by each strategy

<a name="sudoku.puzzle.Puzzle.has_solution"></a>
#### has\_solution

```python
 | has_solution() -> bool
```

Check whether the puzzle is able to be solved

**Returns**:

- `bool` - A boolean value indicating whether the puzzle has a solution

<a name="sudoku.puzzle.Puzzle.rate"></a>
#### rate

```python
 | rate() -> float
```

Calculate the difficulty of solving the puzzle

**Returns**:

- `float` - A difficulty rating between 0 and 1

<a name="sudoku.types"></a>
# sudoku.types

<a name="sudoku.examples"></a>
# sudoku.examples

<a name="sudoku.examples.rate"></a>
# sudoku.examples.rate

<a name="sudoku.examples.shuffle"></a>
# sudoku.examples.shuffle

<a name="sudoku.examples.solve"></a>
# sudoku.examples.solve

<a name="sudoku.examples.boards"></a>
# sudoku.examples.boards

