import sys
import numpy as np

from sudoku import Sudoku
from reporter import Reporter
from reader import Reader

def main():
  input_csv_file_name = "sudokus_start.txt" 
  output_csv_file_name = "output.txt"

  puzzles = Reader.read(input_csv_file_name)

  Reporter.write_output(
    file_name = output_csv_file_name,
    content = "",
    should_overwrite_file = True
  )

  for puzzle in puzzles:
    solver = "AC3"
    results = Sudoku.solve(puzzle, solver)

    if (results == None):
      solver = "BTS"
      results = Sudoku.solve(puzzle, solver)
    print(solver, puzzle)

    if (results == None):
      Reporter.write_output(
        file_name = output_csv_file_name,
        content = "\n",
      )
    else:
      # write lines to output file
      Reporter.write_output(
        file_name = output_csv_file_name,
        content = " ".join([results, solver]) + "\n",
      )

if __name__ == '__main__':
    main()
