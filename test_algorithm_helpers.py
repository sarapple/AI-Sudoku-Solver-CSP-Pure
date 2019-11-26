from algorithm_helpers import AlgorithmHelpers
from sudoku import Sudoku

def test_simplify_puzzle():
  puzzle = (""
    + "035009781"
    + "682571493"
    + "197034562"
    + "826195347"
    + "374682915"
    + "951743628"
    + "519326874"
    + "248957136"
    + "763418259"
  ) 
  result = AlgorithmHelpers.simplify_puzzle(puzzle, Sudoku.get_domains_for_index, "0")
  expected = "435269781682571493197834562826195347374682915951743628519326874248957136763418259"

  assert result == expected
