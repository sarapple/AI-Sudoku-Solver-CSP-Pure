from sudoku import Sudoku
from algorithms import Algorithms

def test_solve():
  puzzle = "000000000302540000050301070000000004409006005023054790000000050700810000080060009"
  result = Sudoku.solve(puzzle, "BTS")
  assert len(result) == 81

def test_location_and_value():
  puzzle = "123456789123456789123456789123456789123456789123456789123456789123456789123456789"
  result = Sudoku.get_location(1)
  assert result == (0, 1)

  value =  Sudoku.get_value(puzzle, result)
  assert value == 2

  result = Sudoku.get_location(9)
  assert result == (1, 0)

  value =  Sudoku.get_value(puzzle, result)
  assert value == 1

  result = Sudoku.get_location(76)
  assert result == (8, 4)

  value =  Sudoku.get_value(puzzle, result)
  assert value == 5

def test_draw():
  puzzle = "123456789223456789323456789423456789523456789623456789723456789823456789923456789"
  result = Sudoku.draw(puzzle)
  expected = (
    "-------------------"
    + "\n" + "|1|2|3|4|5|6|7|8|9|"
    + "\n" + "-------------------"
    + "\n" + "|2|2|3|4|5|6|7|8|9|"
    + "\n" + "-------------------"
    + "\n" + "|3|2|3|4|5|6|7|8|9|"
    + "\n" + "-------------------"
    + "\n" + "|4|2|3|4|5|6|7|8|9|"
    + "\n" + "-------------------"
    + "\n" + "|5|2|3|4|5|6|7|8|9|"
    + "\n" + "-------------------"
    + "\n" + "|6|2|3|4|5|6|7|8|9|"
    + "\n" + "-------------------"
    + "\n" + "|7|2|3|4|5|6|7|8|9|"
    + "\n" + "-------------------"
    + "\n" + "|8|2|3|4|5|6|7|8|9|"
    + "\n" + "-------------------"
    + "\n" + "|9|2|3|4|5|6|7|8|9|"
    + "\n" + "-------------------"
  )
  assert result == expected

def test_get_horizonatal_locations():
  puzzle = "123456789223456789323456789423456789523456789623456789723456789823456789923456789"
  index = 10
  result = Sudoku.get_horizontal_locations(puzzle, index)

  assert result == [
    (1, 0),
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5),
    (1, 6),
    (1, 7),
    (1, 8)
  ]

  assert Sudoku.get_value(puzzle, result[0]) == 2
  assert Sudoku.get_value(puzzle, result[1]) == 2
  assert Sudoku.get_value(puzzle, result[2]) == 3
  assert Sudoku.get_value(puzzle, result[8]) == 9

def test_get_vertical_locations():
  puzzle = "123456789223456789323456789423456789523456789623456789723456789823456789923456789"
  index = 27
  result = Sudoku.get_vertical_locations(puzzle, index)

  assert result == [
    (0, 0),
    (1, 0),
    (2, 0),
    (3, 0),
    (4, 0),
    (5, 0),
    (6, 0),
    (7, 0),
    (8, 0)
  ]

  assert Sudoku.get_value(puzzle, result[0]) == 1
  assert Sudoku.get_value(puzzle, result[1]) == 2
  assert Sudoku.get_value(puzzle, result[2]) == 3
  assert Sudoku.get_value(puzzle, result[8]) == 9

def test_get_subsection_locations():
  puzzle = "123456789223456789323456789423456789523456789623456789723456789823456789923456789"
  index = 0
  result = Sudoku.get_subsection_locations(puzzle, index)

  assert result == [
    (0, 0),
    (0, 1),
    (0, 2),
    (1, 0),
    (1, 1),
    (1, 2),
    (2, 0),
    (2, 1),
    (2, 2)
  ]

  assert Sudoku.get_value(puzzle, result[0]) == 1
  assert Sudoku.get_value(puzzle, result[1]) == 2
  assert Sudoku.get_value(puzzle, result[2]) == 3
  assert Sudoku.get_value(puzzle, result[8]) == 3

  index = 39
  result = Sudoku.get_subsection_locations(puzzle, index)

  assert result == [
    (3, 3),
    (3, 4),
    (3, 5),
    (4, 3),
    (4, 4),
    (4, 5),
    (5, 3),
    (5, 4),
    (5, 5)
  ]

  assert Sudoku.get_value(puzzle, result[0]) == 4
  assert Sudoku.get_value(puzzle, result[1]) == 5
  assert Sudoku.get_value(puzzle, result[2]) == 6
  assert Sudoku.get_value(puzzle, result[8]) == 6

def test_get_all_arcs():
  puzzle = "123456789223456789323456789423456789523456789623456789723456789823456789923456789"
  index = 80
  result = Sudoku.get_all_neighbor_locations_for_index(puzzle, index)
  assert result == set([
    (6, 6),
    (6, 7),
    (6, 8),
    (7, 6),
    (7, 7),
    (7, 8),
    (8, 6),
    (8, 7),
    (8, 8),
    (8, 0),
    (8, 1),
    (8, 2),
    (8, 3),
    (8, 4),
    (8, 5),
    (0, 8),
    (1, 8),
    (2, 8),
    (3, 8),
    (4, 8),
    (5, 8),
  ])

def test_get_all_arc_indexes():
  puzzle = "123456789223456789323456789423456789523456789623456789723456789823456789923456789"
  index = 80
  result = Sudoku.get_neighbors_for_index(puzzle, index)
  assert result == set([
    60,
    61,
    62,
    69,
    70,
    71,
    78,
    79,
    80,
    72,
    73,
    74,
    75,
    76,
    77,
    8,
    17,
    26,
    35,
    44,
    53
  ])

def test_get_remaining_domains_in_neighborhood():
  puzzle = "123056080223456789323456789423456789523456789623456789723456789823456789923456789"

  result = Sudoku.get_remaining_domains_in_neighborhood(puzzle, [0, 1, 2, 3, 4, 5, 6, 7, 8])
  assert result == set([4, 7, 9])

def test_get_available_domains_for_index():
  puzzle = (
    ""
    + "675913482"
    + "482657931"
    + "391248075"
    + "817362549"
    + "263594718"
    + "954781326"
    + "749125863"
    + "528436197"
    + "136879254"
  )

  index = Sudoku.get_index((2, 6))

  assert index == 24

  result = Sudoku.get_domains_for_index(puzzle, index)
  assert result == set([6])


def test_get_available_domains_for_index_2():
  puzzle = (
    ""
    + "675913482"
    + "482657031"
    + "391248075"
    + "817362549"
    + "263594718"
    + "954781326"
    + "749125863"
    + "528436197"
    + "136879254"
  )

  index = Sudoku.get_index((2, 6))

  assert index == 24

  result = Sudoku.get_domains_for_index(puzzle, index)
  assert result == set([6])

def test_get_available_domains_for_index_3():
  puzzle = (
    ""
    + "675913482"
    + "482657031"
    + "301248075"
    + "817362549"
    + "263594718"
    + "954781326"
    + "749125863"
    + "528436197"
    + "136879254"
  )

  index = Sudoku.get_index((2, 6))

  assert index == 24

  result = Sudoku.get_domains_for_index(puzzle, index)
  assert result == set([6, 9])

def test_revise():
  puzzle = (
    ""
    + "000000000"
    + "000000000"
    + "000000000" # here
    + "000000000"
    + "000000000"
    + "000000000"
    + "000000000"
    + "000000000"
    + "000000000"
  )

  index = Sudoku.get_index((2, 6))
  neighbor_index = Sudoku.get_index((2, 7))
  assert index == 24

  result = Sudoku.revise_domains(puzzle, index, neighbor_index)
  assert result == (set([1, 2, 3, 4, 5, 6, 7, 8, 9]), False)

def test_revise_2():
  puzzle = (
    ""
    + "000000120"
    + "000000456"
    + "000000089" # here
    + "000000000"
    + "000000000"
    + "000000000"
    + "000000000"
    + "000000000"
    + "000000000"
  )

  index = Sudoku.get_index((2, 6))
  neighbor_index = Sudoku.get_index((2, 7))
  assert index == 24

  result = Sudoku.revise_domains(puzzle, index, neighbor_index)
  assert result == (set([3, 7]), False)

def test_revise_3():
  puzzle = (
    ""
    + "000000123"
    + "000000456"
    + "000000009" # here
    + "000000780"
    + "000000000"
    + "000000000"
    + "000000000"
    + "000000000"
    + "000000000"
  )

  index = Sudoku.get_index((2, 6))
  neighbor_index = Sudoku.get_index((2, 7))
  assert index == 24

  result = Sudoku.revise_domains(puzzle, index, neighbor_index)
  assert result == (set([8]), False)


def test_revise_4():
  puzzle = (
    ""
    + "000000123"
    + "000000456"
    + "000000009" # here
    + "000000870"
    + "000000000"
    + "000000000"
    + "000000000"
    + "000000000"
    + "000000000"
  )

  index = Sudoku.get_index((2, 6))
  neighbor_index = Sudoku.get_index((2, 7))
  assert index == 24

  result = Sudoku.revise_domains(puzzle, index, neighbor_index)
  assert result == (set([7]), False)


def test_revise_5():
  puzzle = (
    ""
    + "000000042"
    + "000000031"
    + "000000000" # here
    + "567800000"
    + "000000024"
    + "000000013"
    + "000000000"
    + "000000000"
    + "000000000"
  )

  index = Sudoku.get_index((2, 6))
  neighbor_index = Sudoku.get_index((3, 6))

  index_domains = Sudoku.get_domains_for_index(puzzle, index) 
  neighbor_domains = Sudoku.get_domains_for_index(puzzle, neighbor_index)

  assert index_domains == set([5, 6, 7, 8, 9])
  assert neighbor_domains == set([9])

  assert index == 24

  result = Sudoku.revise_domains(puzzle, index, neighbor_index)

  assert result == (set([5, 6, 7, 8]), True)

def test_get_remaining_unassigned_neighbor_indexes():
  puzzle = (
    ""
    + "000000007"
    + "060504030"
    + "000000000" # 2nd from the right
    + "000000010"
    + "000000000"
    + "000000020"
    + "000000000"
    + "000000030"
    + "000000000"
  )

  index = Sudoku.get_index((2, 7))
  neighbor_indexes = Sudoku.get_remaining_unassigned_neighbor_indexes(puzzle, index)

  assert neighbor_indexes == set([6, 7, 15, 17, 18, 19, 20, 21, 22, 23, 24, 26, 43, 61, 79])

def test_ac3_1():
  puzzle = (""
    + "035269781"
    + "682571493"
    + "197034562"
    + "826195347"
    + "374682915"
    + "951743628"
    + "519326874"
    + "248957136"
    + "763418259"
  )

  result = Sudoku.ac3(puzzle)

  assert result == (""
    + "435269781"
    + "682571493"
    + "197834562"
    + "826195347"
    + "374682915"
    + "951743628"
    + "519326874"
    + "248957136"
    + "763418259"
  )

def test_ac3_2():
  puzzle = "000260701680070090190004500820100040004602900050003028009300074040050036703018000"
  result = Sudoku.ac3(puzzle)
  expected = "435269781682571493197834562826195347374682915951743628519326874248957136763418259"

  assert result == expected

def test_ac3_3():
  puzzle = "000001000020000008691200000000000014102506003800020506005000000730000000006319405"
  result = Sudoku.ac3(puzzle)
  expected = "358471629427963158691285347569738214142596783873124596915647832734852961286319475"

  assert result == expected

def test_ac3_4():
  puzzle = "000000000302540000050301070000000004409006005023054790000000050700810000080060009"
  result = Sudoku.ac3(puzzle)
  expected = None

  assert result == expected

def test_backtracking_search():
  puzzle = (""
    + "000000000302540000050301070000000004409006005023054790000000050700810000080060009"
  ) 
  result = Sudoku.backtracking_search(puzzle)
  expected = "148697523372548961956321478567983214419276385823154796691432857735819642284765139"

  assert result == expected

def test_solve_2():
  puzzle = "040010068000000594080059000007003080304006000000100000050800703000000000800032009"
  result = Sudoku.backtracking_search(puzzle)

  assert result == "945317268173628594286459137527943681314286975698175342459861723732594816861732459"

def test_does_follow_constraints():
  puzzle_state = "945217368712368594683459172127593486394786215568124937259841723436975841871632659"
  result = Sudoku.does_puzzle_follow_constraints(puzzle_state, "0")

  assert result == False

def test_does_follow_constraints_1():
  puzzle_state = "945317268173628594286459137527943681314286975698175342459861723732594816861732459"
  result = Sudoku.does_puzzle_follow_constraints(puzzle_state, "0")

  assert result == True

def test_does_follow_constraints_2():
  puzzle_state = "794582136268931745315476982689715324432869571157243869821657493943128657576394218"
  result = Sudoku.does_puzzle_follow_constraints(puzzle_state, "0")

  assert result == True

def test_backtracking_search_2():
  puzzle_state = "094000130000000000000076002080010000032000000000200060000050400000008007006304008"
  result = Sudoku.backtracking_search(puzzle_state)
  expected = "794582136268931745315476982689715324432869571157243869821657493943128657576394218"

  assert result == expected
