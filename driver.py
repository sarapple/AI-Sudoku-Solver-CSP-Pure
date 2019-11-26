import sys
import numpy as np

from sudoku import Sudoku
from reporter import Reporter
from reader import Reader

def main():
  puzzle = sys.argv[1]
  output_csv_file_name = "output.txt"

  solver = "AC3"
  results = Sudoku.solve(puzzle, solver)

  if (results == None):
    solver = "BTS"
    results = Sudoku.solve(puzzle, solver)

  # write lines to output file
  Reporter.write_output(
    file_name = output_csv_file_name,
    content = " ".join([results, solver]),
    should_overwrite_file = True
  )

if __name__ == '__main__':
    main()
