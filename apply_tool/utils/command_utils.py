import os
import glob

from .files import *
from .prof_actions import prof_menu
from .report_actions import report_menu
from .query_utils import *


__DATABASE_ROOT = os.environ.get('DATABASE_ROOT', 'database')
__COUNTRIES_ROOT = os.environ.get('COUNTRIES_ROOT', 'countries')
__APPDATA_PATH = os.environ.get('APPDATA_PATH', 'appdata.txt')
__TODO_PATH = os.environ.get('TODO_PATH', 'todo.txt')

def load_appdata():
    appdata_path = os.path.join(__DATABASE_ROOT, __APPDATA_PATH)
    appdata = {}
    with open(appdata_path, 'r') as file:
        for line in file:
            line = line.strip().split('=')
            key = line[0].strip()
            value = int(line[1].strip())

            appdata[key] = value
    
    return appdata

__APPDATA = load_appdata()

def error(message="", *args):
    print(f'There was an error parsing your command {message}')

def country_list_action():
    countries_list = glob.glob(f'{__DATABASE_ROOT}/{__COUNTRIES_ROOT}/*/')
    
    if len(countries_list) == 0:
        print('There are no countries in your database yet.')
    else:
        for i, country in enumerate(countries_list):
            country_name = country.split('\\')[-2]
            print(f'{i + 1}. {country_name}')

def country_add_action(*args):
    for country in args:
        path = os.path.join(__DATABASE_ROOT, __COUNTRIES_ROOT, country)
        create_directory_if_not_exists(path)

def country_del_action(*args):
    for country in args:
        path = os.path.join(__DATABASE_ROOT, __COUNTRIES_ROOT, country)
        remove_folder(path)

def university_list_action():
    university_list = glob.glob(f'{__DATABASE_ROOT}/{__COUNTRIES_ROOT}/*/*/')

    if len(university_list) == 0:
        print('There are no universities in your databse yet.')
    else:
        for i, university in enumerate(university_list):
            university_name = university.split('\\')[-2]
            print(f'{i + 1}. {university_name}')

def read_university_data():
    country = input('Enter the county which the iniversity is located in: ')
    state = input('Enter the state which the university is located in: ')
    university = input('Enter the name of the university: ')

    path = os.path.join(__DATABASE_ROOT, __COUNTRIES_ROOT, country, state, university)
    return path

def university_add_action(*args):
    match len(args):
        case 3:
            path = '\\'.join([__DATABASE_ROOT, __COUNTRIES_ROOT, *args])
        case _:
            path = read_university_data()

    create_directory_if_not_exists(path)

def university_del_action(*args):
    for university in args:
        path = glob.glob(f'{__DATABASE_ROOT}/{__COUNTRIES_ROOT}/*/*/{university}/')
        if len(path) != 1:
            error(f'There was an error while searching for the university "{university}" in the database.')
            continue
        remove_folder(path)

def prof_add_action():
    command = input('Do you want to add new professor to an exising university? (yes/no): ').lower()
    if command in ('yes', 'y', ''):
        university_name = input('Enter the name of the university: ')
        university_path = glob.glob(f'{__DATABASE_ROOT}/{__COUNTRIES_ROOT}/*/*/{university_name}/')

        if len(university_path) != 1:
            error(f'There was an error while searching for the university "{university_name}" in the database.')
            return
        
        university_path = university_path[0]

    elif command in ('no', 'n'):
        university_path = read_university_data()
        create_directory_if_not_exists(university_path)

    prof_name = input('Enter the name of the professor: ')
    prof_path = os.path.join(university_path, prof_name)
    create_directory_if_not_exists(prof_path)

    path = os.path.join(university_path, prof_name)
    create_directory_if_not_exists(os.path.join(path, 'threads'))
    create_file_if_not_exists(path, 'metadata.txt', f'id={__APPDATA["last_prof_id"] + 1}\nstate=new')
    create_file_if_not_exists(path, 'tags.txt')

    __APPDATA['last_prof_id'] += 1

def prof_menu_action():
    prof_name = input('Enter the name of the professor: ')
    path = glob.glob(f'{__DATABASE_ROOT}/{__COUNTRIES_ROOT}/*/*/*/{prof_name}/')

    if len(path) != 1:
        error(f'There was an error while searching for the professor "{prof_name}" in the database.')
        return
    
    path = path[0]
    prof_menu(path)
    

def prof_del_action():
    prof_name = input('Enter the name of the professor: ')
    path = glob.glob(f'{__DATABASE_ROOT}/{__COUNTRIES_ROOT}/*/*/*/{prof_name}/')
    
    if len(path) != 1:
        error(f'There was an error while searching for the university "{prof_name}" in the database.')
        return
    
    path = path[0]
    remove_folder(path)

def filter_action(*tag_query):
    result = filter_by_tags(tag_query, 'all')
    
    if len(result) == 0:
        error_tags = ' '.join(tag_query)
        print(f'There are no professors taged with "{error_tags}"')
    else:
        for i, prof in enumerate(result):
            prof_name = prof.replace('\\', '/').split('/')[5]
            print(f'{i + 1}. {prof_name}')

def todo_show_action(*args):
    path = glob.glob(f'{__DATABASE_ROOT}/{__TODO_PATH}')[0]

    if len(args) == 0:
        n = -1
    else:
        n = int(args[0])

    with open(path) as file:
        for i, line in enumerate(file):
            if i == n:
                break
            print(f'{i + 1}. {line}', end='')

        print()

def todo_count_action():
    path = glob.glob(f'{__DATABASE_ROOT}/{__TODO_PATH}')[0]
    with open(path) as file:
        count = len(file.readlines())

    print(f'There are {count} line(s) in the todo file')

def todo_dd_action(*line_numbers):
    path = glob.glob(f'{__DATABASE_ROOT}/{__TODO_PATH}')[0]
    with open(path) as file:
        data = file.readlines()

    line_numbers = list(map(lambda x: int(x), line_numbers))

    output = []
    for i, line in enumerate(data):
        if i + 1 not in line_numbers:
            output.append(line)

    with open(path, 'w') as file:
        file.write(''.join(output)) 

def todo_add_action(*args):
    path = glob.glob(f'{__DATABASE_ROOT}/{__TODO_PATH}')[0]

    with open(path, 'a') as file:
        for arg in args:
            file.write('\n' + arg)


def clear_action():
    os.system('cls')

def report_action():
    report_menu()

def exit_action():
    appdata_path = os.path.join(__DATABASE_ROOT, __APPDATA_PATH)
    with open(appdata_path, 'w') as file:
        for key, value in __APPDATA.items():
            file.write(f'{key}={value}\n')