from .tree_command_parser import *
from .command_utils import *

__all__ = [
    'build_command_parser'
]

def build_command_parser():
    parser = CommandTree(error)

    country_parser = TreeNode('country')
    country_parser.add_child(TreeNode('list', country_list_action))
    country_parser.add_child(TreeNode('add', country_add_action))
    country_parser.add_child(TreeNode('remove', country_del_action))
    country_parser.add_child(TreeNode('del', country_del_action))
    parser.add_command(country_parser)

    university_parser = TreeNode('university')
    university_parser.add_child(TreeNode('list', university_list_action))
    university_parser.add_child(TreeNode('add', university_add_action))
    university_parser.add_child(TreeNode('remove', university_del_action))
    university_parser.add_child(TreeNode('del', university_del_action))
    parser.add_command(university_parser)

    prof_parser = TreeNode('prof')
    prof_parser.add_child(TreeNode('add', prof_add_action))
    prof_parser.add_child(TreeNode('menu', prof_menu_action))
    prof_parser.add_child(TreeNode('remove', prof_del_action))
    prof_parser.add_child(TreeNode('del', prof_del_action))
    parser.add_command(prof_parser)

    parser.add_command(TreeNode('filter', filter_action))
    parser.add_command(TreeNode('report', report_action))

    parser.add_command(TreeNode('exit', exit_action))

    return parser