import os
import glob  
import argparse
from ortools.algorithms import pywrapknapsack_solver
from ortools.linear_solver import pywraplp
from tqdm import tqdm
import json
from icecream import ic
import time
import sys


def get_folder(dir_folder):
    folder = [list(idx) for idx in os.walk(dir_folder)]
    return folder

def get_data(folder):
    temp_lst = {}

    length_folder = get_folder(folder)
    root_folder = get_folder(folder)[0][1]
    test_case_folder = get_folder(folder)[1][1]
    temp_lst.update(((str(folder), {fld: [] for fld in test_case_folder}) for folder in root_folder))
    for i in tqdm(range(3, len(length_folder))):
        for file in length_folder[i][-1]:
            f = open(os.path.join(length_folder[i][0], file), 'r') 
            temp_lst[length_folder[i][0].split('\\')[1]][length_folder[i][0].split('\\')[2]].append(f.read())
    
    return temp_lst

def processing_str_lst(process_str_lst):
    return [idx for idx in process_str_lst.split('\n') if idx != '']

def processing_data(process_lst):
    lst_processed = processing_str_lst(process_lst)
    
    values = []
    weights = [[]]
    for i in range(2, int(lst_processed[0])):
        values.append(int(lst_processed[i].split()[1]))
        weights[0].append(int(lst_processed[i].split()[0]))
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

if __name__ == "__main__":
    print('Get all data')
    all_data = get_data('kplib')

    print('Processing')
    for folder_key in all_data:
        f = open(f'TestResults/{folder_key}.txt', 'w')
        f.write('Folder: {}\n\n'.format(folder_key))
        print('Folder: {}'.format(folder_key))
        for tmp_data in tqdm(all_data[folder_key]):
            f.write('Numbers of test case: {}\n'.format(tmp_data[1:]))
            for idx in all_data[folder_key][tmp_data]:
                values, weights, capacities = processing_data(idx)
                total_weight, packed_items, packed_weights = solver_snapback(values, weights, capacities)
                f.write('Total weight: {}\n'.format(total_weight))
                f.write('Packed items: {}\n'.format(packed_items))
                f.write('Packed_weights: {}\n\n'.format(packed_weights))
        f.close()