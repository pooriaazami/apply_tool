import os

__all__ = [
    'install'
]

def install():
    root = os.environ.get('DATABASE_ROOT', 'database')
    if not os.path.isdir(root):
        os.makedirs(root)

        appdata_path = os.environ.get('APPDATA_PATH', 'appdata.txt')
        appdata_path = os.path.join(root, appdata_path)
        with open(appdata_path, 'w') as file:
            file.write('last_prof_id=0\n')
