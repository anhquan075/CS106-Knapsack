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

TIME_STOP = 300

def exit_data():
    print(f'\nExiting process')
    # sys.exit()
    os.kill(os.getpid(), signal.SIGTERM)

def exit_data_thread(time_to_exit=TIME_STOP):
    schedule.every(time_to_exit).seconds.do(exit_data)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    create_folder('TestResults')
    create_folder('TestResults/OR/')
    create_folder('TestResults/Genetic/')

    print('Get data')
    all_data = get_data('kplib')

    Thread(target=exit_data_thread).start()

    print('Processing OR Algorithms in 5 minutes')
    for folder_key in all_data:
        f = open(f'TestResults/OR/{folder_key}.txt', 'w')
        f.write('Folder: {}\n\n'.format(folder_key))
        print('Folder: {}'.format(folder_key))
        for tmp_data in tqdm(all_data[folder_key]):
            f.write('Numbers of test case: {}\n'.format(tmp_data[1:]))
            for idx in all_data[folder_key][tmp_data]:
                values, weights, capacities = processing_data_or(idx)
                total_weight, packed_items, packed_weights = solver_snapback(values, weights, capacities)
                f.write('Total weight: {}\n'.format(total_weight))
                f.write('Packed items: {}\n'.format(packed_items))
                f.write('Packed_weights: {}\n\n'.format(packed_weights))

        f.close()

    Thread(target=exit_data_thread).start()
    
    print('Processing Genetic Algorithms in 5 minutes')
    for folder_key in all_data:
        f = open(f'TestResults/OR/{folder_key}.txt', 'w')
        f.write('Folder: {}\n\n'.format(folder_key))
        print('Folder: {}'.format(folder_key))
        for tmp_data in tqdm(all_data[folder_key]):
            f.write('Numbers of test case: {}\n'.format(tmp_data[1:]))
            for idx in all_data[folder_key][tmp_data]:
                items , capacities = processing_data_genetic_algorithm(idx)
                run(items, capacities)

        f.close()
                