# Constraint Satisfaction Problems (CSP)

# Summary

Implement AC-3 and backtracking algorithms to solve Sudoku puzzles. The objective of the game is to fill a 9 x 9 grid with numerical digits so that each column, each row, and each of the 3 x 3 sub-grids (also called boxes) contains one of all the digits 1 through 9. 

# Sudoku

- 81 variables in total, and tiles to be filled with digits.
- Variables A1 through A9 are the top row (form left to right)
- I1 through I9 are the bottom row

# Task

Write a `driver.py` that intelligently solves Sudoku puzzles

To run:

```
python3 driver.py <input_string>
```

Provided beforehand is sudoku_start.txt, containing hundreds of Sudoku puzzles. Each Sudoku puzzle is represented as a single line of text, starting from top-left corner of the board and enumerates the digits in each tile, row by row.  `0` is used to indicate tiles that have not yet been filled.  

When executed with an input string, the program will generate an `output.txt` containing a single line of text representing the finished Sudoku board and the algorithm name which solved the Sudoku board.

The program can be solved extensively using `sudokus_finish.txt` which contain the solved versions of all the same puzzles.

# AC-3 Algorithm (AC3)

Implement the AC-3 Algorithm. Of the solutions in `sudokus_finish.txt`, there are only 2/400 Sudoku board which can be solved with AC3 alone.

# Backtracking Algorithm (BTS)

Implement backtracking using the `minimum remaining value` heuristic. The order of values to be attempted for each variable is _add here_.  When a variable is assigned, apply forward checking to reduce variable domains. 

# Specific Requirements

1. This should show a comparison of how powerful BTS is compared to AC3. Execute the AC-3 algorithm before Backtracking Search algorithm. 
2. The program will be tested against 20 test cases.
3. Correctly implemented backtracking should take well under a minute per puzzle.
