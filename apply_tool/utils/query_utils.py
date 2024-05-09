import os
import glob

__DATABASE_ROOT = os.environ.get('DATABASE_ROOT', 'database')
__COUNTRIES_ROOT = os.environ.get('COUNTRIES_ROOT', 'countries')

def filter_by_tags(tag_query, strategy='any'):
    if isinstance(tag_query, tuple):
        tag_query = list(tag_query)
    else:
        tag_query = [tag_query]

    paths = glob.glob(f'{__DATABASE_ROOT}/{__COUNTRIES_ROOT}/*/*/*/*/tags.txt')
    result = []

    for path in paths:
        with open(path) as file:
            content = file.read().split('\n')
        
        if strategy == 'any' and any([tag in content for tag in tag_query]):
            result.append(path)
        elif strategy == 'all' and all([tag in content for tag in tag_query]):
            result.append(path)

    return result

def filter_by_metadata(key, value):
    if not isinstance(value, list):
        value = [value]

    paths = glob.glob(f'{__DATABASE_ROOT}/{__COUNTRIES_ROOT}/*/*/*/*/metadata.txt')
    result = []

    for path in paths:
        with open(path) as file:
            content = file.read().split('\n')
            content = map(lambda x: x.split('='), content)
            content = {key: value for key, value in content}
            
            if content[key] in value:
                result.append(path)

    return result