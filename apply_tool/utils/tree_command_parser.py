class TreeNode:
    def __init__(self, value, action=None):
        self.__value = value
        self.__action = action
        self.__children = {}

    def add_child(self, child):
        self.__children[child.value] = child

    def get_child(self, value):
        return self.__children.get(value)

    @property
    def value(self):
        return self.__value
    
    def __call__(self, *args):
        return self.__action(*args)

    def __str__(self):
        return f'TreeNode(value={self.__value})'
        

class CommandTree:
    def __init__(self, error_handler):
        self.__root = TreeNode(value='', action=error_handler)

    def __traverse(self, command_segments):
        idx = 0
        child = self.__root

        while True:
            temp = child.get_child(command_segments[idx])

            if temp is None:
                break

            child = temp
            idx += 1
            if idx == len(command_segments):
                break

            
        return child, command_segments[idx:]

    def parse(self, command):
        command_segments = command.split(' ')
        
        node, command_segments = self.__traverse(command_segments)
        return node(*command_segments)

    def add_command(self, command):
        self.__root.add_child(command)

        