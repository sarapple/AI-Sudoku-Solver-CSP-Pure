import queue as q
import math
import numpy as np

from functools import reduce
from algorithms import Algorithms
from operator import itemgetter

class Sudoku:
  @staticmethod
  def draw(puzzle):
    output = ""
    horizontal = "-------------------"
    for row in range(9):
      output += horizontal
      output += "\n|"
      for col in range(9):
        output += puzzle[(row * 9) + col]
        output += ("|" if col != 8 else "")
      output += "|\n"
    
    output += horizontal

    return output

  @staticmethod
  def solve(puzzle, solver):
    if (solver == "AC3"):
      return Sudoku.ac3(puzzle)
    elif (solver == "BTS"):
      return Sudoku.backtracking_search(puzzle)

    return puzzle

  @staticmethod
  def get_all_neighbor_locations_for_index(puzzle_state, index):
    return set(
      Sudoku.get_subsection_locations(puzzle_state, index)
      + Sudoku.get_horizontal_locations(puzzle_state, index)
      + Sudoku.get_vertical_locations(puzzle_state, index)
    )

  @staticmethod
  def get_neighbors_for_index(puzzle_state, index):
    all_arc_locations = Sudoku.get_all_neighbor_locations_for_index(puzzle_state, index)

    return set([
      Sudoku.get_index(location) for location in all_arc_locations
    ])

  @staticmethod
  def get_value(puzzle, location):
    (row, column) = location
    index = (row * 9) + column

    return int(puzzle[index])

  @staticmethod
  def get_location(index):
    row = math.floor(index / 9)
    column = index % 9

    return (row, column)

  @staticmethod
  def get_index(location):
    (row, column) = location

    return (row * 9) + column

  @staticmethod
  def get_subsection_locations(puzzle_state, index):
    (row, column) = Sudoku.get_location(index)

    distance_from_subsection_row_start = (row % 3)
    distance_from_subsection_col_start = (column % 3)

    row_start = row - distance_from_subsection_row_start
    col_start = column - distance_from_subsection_col_start

    return (
      [(row_start, col) for col in range(col_start, col_start + 3)]
      + [(row_start + 1, col) for col in range(col_start, col_start + 3)]
      + [(row_start + 2, col) for col in range(col_start, col_start + 3)]
    )

  @staticmethod
  def get_subsection_indexes(puzzle_state, index):
    return [Sudoku.get_index(location) for location in Sudoku.get_subsection_locations(puzzle_state, index)]

  @staticmethod
  def get_horizontal_indexes(puzzle_state, index):
    return [Sudoku.get_index(location) for location in Sudoku.get_horizontal_locations(puzzle_state, index)]
  
  @staticmethod
  def get_vertical_indexes(puzzle_state, index):
    return [Sudoku.get_index(location) for location in Sudoku.get_vertical_locations(puzzle_state, index)]

  @staticmethod
  def get_horizontal_locations(puzzle_state, index):
    (row, _) = Sudoku.get_location(index)

    return [(row, col_index) for col_index in range(9)]

  @staticmethod
  def get_vertical_locations(puzzle_state, index):
    (_, column) = Sudoku.get_location(index)

    return [(row_index, column) for row_index in range(9)]

  @staticmethod
  def is_assigned(puzzle_state, index):
    return int(puzzle_state[index]) > 0
  
  @staticmethod
  def get_remaining_unassigned_neighbor_indexes(puzzle_state, index):
    subsection_indexes = Sudoku.get_subsection_indexes(puzzle_state, index)
    horizontal_indexes = Sudoku.get_horizontal_indexes(puzzle_state, index)
    vertical_indexes = Sudoku.get_vertical_indexes(puzzle_state, index)

    neighbor_indexes = set([
      int(neighbor_index)
      for neighbor_index in (subsection_indexes + horizontal_indexes + vertical_indexes)
      if int(puzzle_state[neighbor_index]) == 0 and neighbor_index != index
    ])

    return set(sorted(neighbor_indexes))

  @staticmethod
  def get_remaining_domains_in_neighborhood(puzzle_state, indexes):
    existing_options = set([1, 2, 3, 4, 5, 6, 7, 8, 9])

    for index in indexes:
      taken_domain = int(puzzle_state[index])
      existing_options.discard(taken_domain)

    return existing_options

  @staticmethod
  def get_domains_for_index(puzzle_state, index):
    subsection_indexes = Sudoku.get_subsection_indexes(puzzle_state, index)
    subsection_indexes.remove(index)
    subsection_remaining = Sudoku.get_remaining_domains_in_neighborhood(puzzle_state, subsection_indexes)

    horizontal_indexes = Sudoku.get_horizontal_indexes(puzzle_state, index)
    horizontal_indexes.remove(index)
    horizontal_remaining = Sudoku.get_remaining_domains_in_neighborhood(puzzle_state, horizontal_indexes)

    vertical_indexes = Sudoku.get_vertical_indexes(puzzle_state, index)
    vertical_indexes.remove(index)
    vertical_remaining = Sudoku.get_remaining_domains_in_neighborhood(puzzle_state, vertical_indexes)

    return set(subsection_remaining).intersection(horizontal_remaining).intersection(vertical_remaining)

  @staticmethod
  def revise_domains(puzzle_state, i, j):
    all_domains_i = Sudoku.get_domains_for_index(puzzle_state, i)
    all_domains_i_arc_inconsistent = set()
    is_revised = False

    for domain_chosen_i in all_domains_i:
      all_domains_j = Sudoku.get_domains_for_index(puzzle_state, j)
      domain_j_after_i_is_taken = all_domains_j.difference(set([domain_chosen_i]))
      # if a given domain is chosen for i, it no longer becomes an option for j
      # if that domain used by i becomes unavailable to j AND there is no domain left in j
      # (i.e., dead end, will need to be removed from possible domains for i)
      if (not domain_j_after_i_is_taken):
        all_domains_i_arc_inconsistent.add(domain_chosen_i)
        is_revised = True
  
    return (all_domains_i.difference(all_domains_i_arc_inconsistent), is_revised)

  @staticmethod
  def is_puzzle_complete(puzzle_state):
    return ("0" not in puzzle_state)

  @staticmethod
  def does_puzzle_follow_constraints(puzzle_state, unassigned_value):
    for row in range(9):
      indexes = Sudoku.get_horizontal_indexes(puzzle_state, row * 9)
      indexes_unassigned = [i for i in indexes if puzzle_state[i] == unassigned_value]
      remaining = Sudoku.get_remaining_domains_in_neighborhood(puzzle_state, indexes)
      if (len(remaining) != len(indexes_unassigned)):
        return False

    for column in range(9):
      indexes = Sudoku.get_vertical_indexes(puzzle_state, column)
      indexes_unassigned = [i for i in indexes if puzzle_state[i] == unassigned_value]
      remaining = Sudoku.get_remaining_domains_in_neighborhood(puzzle_state, indexes)
      if (len(remaining) != len(indexes_unassigned)):
        return False
    
    for subsection_start_index in [0, 3, 6, 27, 30, 33, 54, 57, 60]:
      indexes = Sudoku.get_subsection_indexes(puzzle_state, subsection_start_index)
      indexes_unassigned = [i for i in indexes if puzzle_state[i] == unassigned_value]
      remaining = Sudoku.get_remaining_domains_in_neighborhood(puzzle_state, indexes)
      if (len(remaining) != len(indexes_unassigned)):
        return False

    return True 

  @staticmethod
  def ac3(initial_puzzle_state):
    if (len(initial_puzzle_state) != 81):
      raise Exception("Puzzle must be 81 characters long")

    return Algorithms.ac3(
      initial_puzzle_state = initial_puzzle_state,
      client_defined_revise_domains = Sudoku.revise_domains,
      client_defined_get_domains_for_index = Sudoku.get_domains_for_index,
      client_defined_get_neighbors_for_index = Sudoku.get_neighbors_for_index,
      client_defined_is_puzzle_complete = Sudoku.is_puzzle_complete,
      client_defined_unassigned_value = "0"
    )

  @staticmethod
  def backtracking_search(initial_puzzle_state):
    puzzle_state = initial_puzzle_state

    return Algorithms.backtracking_search(
      puzzle_state = puzzle_state,
      client_defined_get_domains_for_index = Sudoku.get_domains_for_index,
      client_defined_get_neighbors_for_index = Sudoku.get_neighbors_for_index,
      client_defined_is_puzzle_complete = Sudoku.is_puzzle_complete,
      client_defined_unassigned_value = "0",
      client_defined_does_puzzle_follow_constraints = Sudoku.does_puzzle_follow_constraints,
    )
