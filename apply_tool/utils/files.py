import os
import shutil

def create_directory_if_not_exists(root):
    if not os.path.isdir(root):
        os.makedirs(root)
        return True
    return False

def remove_folder(root):
    if os.path.isdir(root):
        shutil.rmtree(root)

def create_file_if_not_exists(root, name, initial_content=None):
    create_directory_if_not_exists(root)
    path = os.path.join(root, name)
    if not os.path.isfile(path):
        with open(path, 'w') as file:
            if initial_content:
                file.write(str(initial_content))
    