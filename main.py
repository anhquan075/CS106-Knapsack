import time
import schedule
from threading import Thread
import time
import signal
import os
from utils import get_data, create_folder
from tqdm import tqdm
from or_algorithm_knapsack import processing_data_or, solver_snapback
from genetic_knapsack import processing_data_genetic_algorithm, run
import argparse


# You can change time stop in here
TIME_STOP = 300
BLACK_LIST_TEST_CASE = ['02000', '05000', '10000']

def run_OR(TIME_STOP, data):
    print(f'Processing OR Algorithms in {TIME_STOP} seconds')
    for folder_key in data:
        f = open(f'TestResults/{TIME_STOP}_s/OR_{TIME_STOP}s/{folder_key}.txt', 'w')
        f.write('Folder: {}\n\n'.format(folder_key))
        print('Folder: {}'.format(folder_key))
        for tmp_data in tqdm(data[folder_key]):
            if tmp_data[1:] in BLACK_LIST_TEST_CASE:
                break

            f.write('Numbers of test case: {}\n'.format(tmp_data[1:]))
            
            counting_test_case = 1
            for idx in data[folder_key][tmp_data]:
                f.write(f'{counting_test_case} times:\n')
                
                values, weights, capacities = processing_data_or(idx)
                total_weight, computed_value, packed_weights = solver_snapback(values, weights, capacities)
                
                f.write('Total weight: {}\n'.format(total_weight))
                f.write('Total value: {}\n'.format(computed_value))
                f.write('Packed_weights: {}\n\n'.format(packed_weights))

                counting_test_case = counting_test_case + 1

        f.close()

def run_Genetic(TIME_STOP, data):
    print(f'Processing Genetic Algorithms in {TIME_STOP} seconds')
    for folder_key in data:
        f = open(f'TestResults/{TIME_STOP}_s/Genetic_{TIME_STOP}s/{folder_key}.txt', 'w') 
        f.write('Folder: {}\n\n'.format(folder_key))
        print('Folder: {}'.format(folder_key))
        for tmp_data in tqdm(data[folder_key]):
            if tmp_data[1:] in BLACK_LIST_TEST_CASE:
                break
            
            f.write('Numbers of test case: {}\n'.format(tmp_data[1:]))

            counting_test_case = 1
            for idx in data[folder_key][tmp_data]:
                f.write(f'{counting_test_case} times:\n')

                items , capacities = processing_data_genetic_algorithm(idx)
                bestFitnessValues, totalWeight, totalValue = run(items, capacities)

                f.write(f'Best Ever Fitness: {bestFitnessValues}\n')
                f.write(f'Total Weights: {totalWeight}\n')
                f.write(f'Total values: {totalValue}\n\n')

                counting_test_case = counting_test_case + 1

        f.close()


def exit_data():
    print('\nExiting process\n')
    # sys.exit()
    os.kill(os.getpid(), signal.SIGTERM)

def exit_data_thread(time_to_exit=TIME_STOP):
    schedule.every(time_to_exit).seconds.do(exit_data)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Create folder test results for or and genetic algorithm
    create_folder('TestResults')
    create_folder(f'TestResults/{TIME_STOP}_s')
    create_folder(f'TestResults/{TIME_STOP}_s/OR_{TIME_STOP}s/')
    create_folder(f'TestResults/{TIME_STOP}_s/Genetic_{TIME_STOP}s/')

    # Argparse argument
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--option", help="Choose 1 to run OR Algorithm or 2 to run Genetic Algorithm", type=int)
    args = parser.parse_args()

    # Get data from folder kplib
    print('Get data')
    all_data = get_data('kplib')
    

    if args.option == 1:
        # Create a process with TIME_STOP  
        Thread(target=exit_data_thread).start()
        run_OR(TIME_STOP=TIME_STOP, data=all_data)
    elif args.option == 2:
        Thread(target=exit_data_thread).start()
        run_Genetic(TIME_STOP=TIME_STOP, data=all_data)
    else:
        raise TypeError("Only choose 1 or 2 option to run program. You can type python main.py -h to show helping command.")