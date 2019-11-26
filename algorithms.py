import queue as q
from functools import reduce

class Algorithms:
  @staticmethod
  def get_puzzle_state_from_domains(puzzle_state, all_domains):
    for i, domains_i in enumerate(all_domains):
      if (int(puzzle_state[i]) == 0 and len(domains_i) == 1):
        puzzle_state = puzzle_state[0:i] + str(list(domains_i)[0]) + puzzle_state[i + 1:]
    
    return puzzle_state 
  @staticmethod
  def get_all_domains(puzzle_state, client_defined_get_domains_for_index, client_defined_unassigned_value):
    puzzle_state_length = len(puzzle_state)
    puzzle_state_indexes = range(puzzle_state_length)
    puzzle_state_domains = [(
      client_defined_get_domains_for_index(puzzle_state, i) if puzzle_state[i] == client_defined_unassigned_value else set([int(puzzle_state[i])])
    ) for i in puzzle_state_indexes]

    return puzzle_state_domains

  @staticmethod
  def get_initial_arcs(puzzle_state, client_defined_get_neighbors_for_index):
    all_arcs = [
      [
        (ref_index, neighbor_index)
        for neighbor_index in client_defined_get_neighbors_for_index(puzzle_state, ref_index) if (neighbor_index != ref_index)
      ]
      for ref_index in range(len(puzzle_state))
    ]
    all_arcs.sort()

    return set(reduce(lambda x, y: x + y, all_arcs))

  @staticmethod
  def ac3(
    initial_puzzle_state, # string of n characters
    client_defined_revise_domains, # revise the domains for an index (based on a neighbor j) and should return tuple of (updated_domains, is_revised)
    client_defined_get_domains_for_index, # given a puzzle state and an index, should return the domains for that index
    client_defined_get_neighbors_for_index, # given a puzzle state and an index, should return the neighbor indexes for that index
    client_defined_is_puzzle_complete, # given the puzzle, is it complete? Should return True/False
    client_defined_unassigned_value # unassigned value should be given this key
  ):
    puzzle_state = initial_puzzle_state
    # get the available domains for 81 squares
    all_domains = Algorithms.get_all_domains(puzzle_state, client_defined_get_domains_for_index, client_defined_unassigned_value)
    # update puzzle state where possible (domains with only one option) that haven't been set yet
    puzzle_state = Algorithms.get_puzzle_state_from_domains(puzzle_state, all_domains)

    queue = q.Queue()
    initial_arcs = Algorithms.get_initial_arcs(puzzle_state, client_defined_get_neighbors_for_index)
    for arc in initial_arcs: queue.put(arc)

    while (queue.empty() == False):
      (i, j) = queue.get()

      (revised_domains_i, is_i_domains_revised) = client_defined_revise_domains(puzzle_state, i, j)

      if (not revised_domains_i): # out of options, exit
        return False
      elif (len(revised_domains_i) == 1): # found a way to minimize to 1 domain! This is the correct answer so update the puzzle.
        domain_as_string = str(list(revised_domains_i)[0])
        puzzle_state = puzzle_state[0:i] + domain_as_string + puzzle_state[i+1:]
  
      # domains have been revised for i, add back (neighbors, i) to queue to check arc consistency
      if (is_i_domains_revised == True):
        neighbors = [
          (neighbor_index, i)
          for neighbor_index in client_defined_get_neighbors_for_index(puzzle_state, i) if (neighbor_index != i and neighbor_index != j)
        ]

        for arc in neighbors: queue.put(arc)
    
    if (client_defined_is_puzzle_complete(puzzle_state) == True):
      return puzzle_state
    else:
      return None
