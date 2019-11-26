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
  def get_all_neighbor_indexes_for_index(puzzle_state, index):
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
  def ac3(initial_puzzle_state):
    if (len(initial_puzzle_state) != 81):
      raise Exception("Puzzle must be 81 characters long")

    return Algorithms.ac3(
      initial_puzzle_state = initial_puzzle_state,
      client_defined_revise_domains = Sudoku.revise_domains,
      client_defined_get_domains_for_index = Sudoku.get_domains_for_index,
      client_defined_get_neighbors_for_index = Sudoku.get_all_neighbor_indexes_for_index,
      client_defined_is_puzzle_complete = Sudoku.is_puzzle_complete,
      client_defined_unassigned_value = "0"
    )

  @staticmethod
  def backtracking_search(initial_puzzle_state):
    puzzle_state = initial_puzzle_state

    return Sudoku.backtracking_search_inner(puzzle_state)
  
  @staticmethod
  def get_all_domains(puzzle_state, client_defined_get_domains_for_index, client_defined_unassigned_value):
    # print("in get all domains")
    puzzle_state_length = len(puzzle_state)
    puzzle_state_indexes = range(puzzle_state_length)
    puzzle_state_domains = [(
      client_defined_get_domains_for_index(puzzle_state, i) if puzzle_state[i] == client_defined_unassigned_value else set([int(puzzle_state[i])])
    ) for i in puzzle_state_indexes]

    return puzzle_state_domains

  @staticmethod
  def resolve_puzzle(puzzle_state):
    is_changed = True

    while (is_changed):
      is_changed = False
      for i, domain in enumerate(Sudoku.get_all_domains(puzzle_state, Sudoku.get_domains_for_index, "0")):
        if (len(domain) == 0):
          return None
        elif (puzzle_state[i] == "0" and len(domain) == 1):
          domain_as_string = str(list(domain)[0])
          puzzle_state = puzzle_state[0:i] + domain_as_string + puzzle_state[i+1:]
          is_changed = True

    return puzzle_state

  @staticmethod
  def select_unassigned_variable(puzzle_state):
    all_domains = Sudoku.get_all_remaining_domains(Sudoku.resolve_puzzle(puzzle_state), "0")

    if (not all_domains):
      return None

    most_promising_unassigned = all_domains[0]
    (index, domains) = most_promising_unassigned

    return (index, domains)

  @staticmethod
  def backtracking_search_inner(puzzle_state):
    puzzle_state = Sudoku.resolve_puzzle(puzzle_state)
    if (Sudoku.is_puzzle_complete(puzzle_state)):
      return puzzle_state
    
    unassigned = Sudoku.select_unassigned_variable(puzzle_state)
    if (unassigned == None):
      return None

    (i, domains) = unassigned
    if (domains == None):
      return None

    for (_, _, child_puzzle_state) in Sudoku.get_ordered_domain_values(puzzle_state, i):
      is_inference_safe = Sudoku.inference(child_puzzle_state, i)

      if (is_inference_safe):
        found_solution = Sudoku.backtracking_search_inner(child_puzzle_state)

        if (found_solution):
          return found_solution
 
    return None
  
  # checks to see if the neighbors of an index are still viable with the value added into the index (reflected in puzzle_state)
  @staticmethod
  def inference(puzzle_state, index):
    neighbors = Sudoku.get_all_neighbor_indexes_for_index(puzzle_state, index)

    for neighbor_j in neighbors:
      domain_j = Sudoku.get_domains_for_index(puzzle_state, neighbor_j)
      
      if (len(domain_j) < 1):
        return False

    return True

  @staticmethod
  def get_all_remaining_domains(puzzle_state, unassigned_value):
    all_domains = Sudoku.get_all_domains(puzzle_state, Sudoku.get_domains_for_index, unassigned_value)
    all_domains_with_options = [
      {
        "index": index,
        "domains": domains,
        "heuristics": Sudoku.get_heuristics_for_space(puzzle_state, index, domains),
      } for index, domains in enumerate(all_domains)
      if (len(domains) > 1)
    ]

    return [
      (container["index"], container["domains"])
      for container in sorted(all_domains_with_options, key=itemgetter("heuristics"), reverse=True)
    ]

  @staticmethod
  def get_ordered_domain_values(puzzle_state, index):
    domains = Sudoku.get_domains_for_index(puzzle_state, index)
    domain_and_puzzle_states = [
      (domain, Sudoku.resolve_puzzle(puzzle_state[0:index] + str(domain) + puzzle_state[index+1:])) for domain in domains
    ]
    # put in dict to sort. Find a better way
    domain_and_heuristics = [
      {
        "index": index,
        "domain": domain,
        "heuristics": Sudoku.get_heuristics_for_domains_in_space(puzzle_state),
        "puzzle_state": child_puzzle
      } for (domain, child_puzzle) in domain_and_puzzle_states
      if child_puzzle != None
    ]

    return [
      (index, container["domain"], container["puzzle_state"])
      for container in sorted(domain_and_heuristics, key=itemgetter("heuristics"), reverse=True)
    ]

  @staticmethod
  def get_heuristics_for_space(puzzle_state, index, domains):
    return 1 / len(domains)

  @staticmethod
  def get_heuristics_for_domains_in_space(puzzle_state):
    filled_sqares = len(puzzle_state) - puzzle_state.count("0")

    all_domains = Sudoku.get_all_remaining_domains(puzzle_state, "0")
    minimum_domain_length = len(all_domains[0])

    for domains in all_domains:
      if (len(domains) < minimum_domain_length):
        minimum_domain_length = len(domains)
    
    return filled_sqares + 1/minimum_domain_length
