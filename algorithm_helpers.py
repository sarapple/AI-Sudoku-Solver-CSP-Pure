import queue as q
from functools import reduce
from operator import itemgetter

class AlgorithmHelpers:
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
  def simplify_puzzle(puzzle_state, client_defined_get_domains_for_index, client_defined_unassigned_value):
    is_changed = True

    while (is_changed):
      is_changed = False
      all_domains = AlgorithmHelpers.get_all_domains(puzzle_state, client_defined_get_domains_for_index, client_defined_unassigned_value)

      for i, domain in enumerate(all_domains):
        if (len(domain) == 0):
          return None
        elif (puzzle_state[i] == client_defined_unassigned_value and len(domain) == 1):
          domain_as_string = str(list(domain)[0])
          puzzle_state = puzzle_state[0:i] + domain_as_string + puzzle_state[i+1:]
          is_changed = True

    return puzzle_state

  @staticmethod
  def select_unassigned_variable(puzzle_state, client_defined_get_domains_for_index, client_defined_unassigned_value):
    simplified_puzzle_state = AlgorithmHelpers.simplify_puzzle(puzzle_state, client_defined_get_domains_for_index, client_defined_unassigned_value)
    all_domains = AlgorithmHelpers.get_all_remaining_domains(simplified_puzzle_state, client_defined_unassigned_value, client_defined_get_domains_for_index)

    if (not all_domains):
      return None

    most_promising_unassigned = all_domains[0]
    (index, domains) = most_promising_unassigned

    return (index, domains)

  # checks to see if the neighbors of an index are still viable with the value added into the index (reflected in puzzle_state)
  @staticmethod
  def inference(puzzle_state, index, client_defined_get_neighbors_for_index, client_defined_get_domains_for_index):
    neighbors = client_defined_get_neighbors_for_index(puzzle_state, index)

    for neighbor_j in neighbors:
      domain_j = client_defined_get_domains_for_index(puzzle_state, neighbor_j)
      
      if (len(domain_j) < 1):
        return False

    return True

  @staticmethod
  def get_all_remaining_domains(puzzle_state, client_defined_unassigned_value, client_defined_get_domains_for_index):
    all_domains = AlgorithmHelpers.get_all_domains(puzzle_state, client_defined_get_domains_for_index, client_defined_unassigned_value)
    all_domains_with_options = [
      {
        "index": index,
        "domains": domains,
        "heuristics": AlgorithmHelpers.get_heuristics_for_space(puzzle_state, index, domains),
      } for index, domains in enumerate(all_domains)
      if (len(domains) > 1)
    ]

    return [
      (container["index"], container["domains"])
      for container in sorted(all_domains_with_options, key=itemgetter("heuristics"), reverse=True)
    ]

  @staticmethod
  def get_ordered_domain_values(puzzle_state, index, client_defined_get_domains_for_index, client_defined_unassigned_value):
    domains = client_defined_get_domains_for_index(puzzle_state, index)
    domain_and_puzzle_states = [
      (
        domain,
        AlgorithmHelpers.simplify_puzzle(
          puzzle_state[0:index] + str(domain) + puzzle_state[index+1:],
          client_defined_get_domains_for_index,
          client_defined_unassigned_value
        )
      ) for domain in domains
    ]
    # Putting in dict to sort. Find a better way.
    domain_and_heuristics = [
      {
        "index": index,
        "domain": domain,
        "heuristics": AlgorithmHelpers.get_heuristics_for_domains_in_space(puzzle_state, client_defined_get_domains_for_index, client_defined_unassigned_value),
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
  def get_heuristics_for_domains_in_space(puzzle_state, client_defined_get_domains_for_index, client_defined_unassigned_value):
    filled_sqares = len(puzzle_state) - puzzle_state.count(client_defined_unassigned_value)

    all_domains = AlgorithmHelpers.get_all_remaining_domains(puzzle_state, client_defined_unassigned_value, client_defined_get_domains_for_index)
    minimum_domain_length = len(all_domains[0])

    for domains in all_domains:
      if (len(domains) < minimum_domain_length):
        minimum_domain_length = len(domains)
    
    return filled_sqares + 1/minimum_domain_length
 