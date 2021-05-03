from utils import processing_str_lst
from ortools.algorithms import pywrapknapsack_solver
from ortools.linear_solver import pywraplp

def processing_data_or(process_lst):
    lst_processed = processing_str_lst(process_lst)
    
    values = []
    weights = [[]]
    for i in range(2, int(lst_processed[0]) + 2):
        values.append(int(lst_processed[i].split()[0]))
        weights[0].append(int(lst_processed[i].split()[1]))
    capacities = [int(lst_processed[1])]

    return values, weights, capacities


def solver_snapback(values, weights, capacities):
    # Create the solver.
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')

    solver.Init(values, weights, capacities)
    computed_value = solver.Solve()

    packed_items = []
    packed_weights = []
    total_weight = 0

    # print('Total value =', computed_value)
    for i in range(len(values)):
        if solver.BestSolutionContains(i):
            packed_items.append(i)
            packed_weights.append(weights[0][i])
            total_weight += weights[0][i]

    # print('Total weight:', total_weight)
    # print('Packed items:', packed_items)
    # print('Packed_weights:', packed_weights)
    return total_weight, packed_items, packed_weights