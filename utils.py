import os
from tqdm import tqdm
import platform


def create_folder(dir_name):
    if os.path.exists(dir_name):
        print(f"{dir_name} is exists")
    else:
        os.mkdir(dir_name)
        print(f'{dir_name} is created')

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
            if platform.system() == "Windows":
                temp_lst[length_folder[i][0].split('\\')[1]][length_folder[i][0].split('\\')[2]].append(f.read())
            else:
                temp_lst[length_folder[i][0].split('/')[1]][length_folder[i][0].split('/')[2]].append(f.read())
    
    return temp_lst

def processing_str_lst(process_str_lst):
    return [idx for idx in process_str_lst.split('\n') if idx != '']