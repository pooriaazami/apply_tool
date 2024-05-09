from .tree_command_parser import *
from .query_utils import *

__all__ = [
    'report_menu'
]

def quit_action():
    pass

def error(message="", *args):
    print(f'There was an error parsing your command {message}')

def status_action(status='waiting'):
    result = filter_by_metadata('state', status)
    if len(result) == 0:
        print(f'There are no professors in the databadse with status: "{status}"')
    else:
        for i, prof in enumerate(result):
            prof_name = prof.replace('\\', '/').split('/')[5]
            print(f'{i + 1}. {prof_name}')

def stats_action():
    ...
    # Number of active professors

def build_report_menu_parser():
    parser = CommandTree(error)

    parser.add_command(TreeNode('q', quit_action))
    parser.add_command(TreeNode('status', status_action))

    return parser

def report_menu():
    parser = build_report_menu_parser()
    while True:
        command = input('>> ').strip()
        parser.parse(command)

        if command.lower() == 'q':
            break