import os   
from .tree_command_parser import *

__all__ = [
    'prof_menu'
]

__PATH = None

def error(message="", *args):
    print(f'There was an error parsing your command {message}')

def read_tags_action():
    path = os.path.join(__PATH, 'tags.txt')
    with open(path) as file:
        tags = file.read()

    tags = tags.replace('\n', '\t')
    return tags

def show_action():
    _, _, country, state, university, name, _ = __PATH.split('/')

    print(f'Country: {country}')
    print(f'State: {state}')
    print(f'University : {university}')
    print(f'Name: {name}')
    print()
    print(read_tags_action())

def add_action(key, value):
    path = os.path.join(__PATH, 'metadata.txt')
    with open(path, 'a') as file:
        file.write(f'\n{key}={value}')

def get_action(key):
    path = os.path.join(__PATH, 'metadata.txt')
    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            line_key, line_value = line.split('=')
            if line_key == key:
                print(line_value)
                break
        else:
            print(f'There is no value assigned for the key {key} in the database')

def update_action(key, value):
    path = os.path.join(__PATH, 'metadata.txt')
    
    with open(path) as file:
        content = file.read()
        key_values = map(lambda x: x.split('='), content.split('\n'))
        meta_data = {key: value for key, value in key_values}

    meta_data[key] = value

    with open(path, 'w') as file:
        line = [f'{key}={value}' for key, value in meta_data.items()]
        content = '\n'.join(line)
        file.write(content)

def tag_action(value):
    path = os.path.join(__PATH, 'tags.txt')

    with open(path, 'a') as file:
        file.write(value + '\n')

def untag_action(value):
    path = os.path.join(__PATH, 'tags.txt')

    with open(path, 'r') as file:
        tags = file.read()

    tags = tags.split('\n')
    tags = filter(lambda x: len(x) > 0, tags)
    tags = filter(lambda x: x != value, tags)
    tags = '\n'.join(tags)

    with open(path, 'w') as file:
        file.write(tags)
        file.write('\n')

def quit_action():
    pass

def build_prof_menu_parser():
    parser = CommandTree(error)

    parser.add_command(TreeNode('show', show_action))
    parser.add_command(TreeNode('add', add_action))
    parser.add_command(TreeNode('update', update_action))
    parser.add_command(TreeNode('get', get_action))
    parser.add_command(TreeNode('tag', tag_action))
    parser.add_command(TreeNode('untag', untag_action))
    parser.add_command(TreeNode('q', quit_action))

    return parser

def prof_menu(path):
    global __PATH
    __PATH = path.replace('\\', '/')
    parser = build_prof_menu_parser()
    while True:
        command = input('>> ').strip()
        parser.parse(command)

        if command.lower() == 'q':
            break