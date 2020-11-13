import os
import re

root_path_name = '@app'
root_path = './src/app'
sep = os.path.sep

import_expression = re.compile(
    'import\\s*{[^}]*}\\s*from\\s*(?:\'[^\']*\'|"[^"]*")\\s*;')

path_expression = re.compile('\'[^\']*\'|"[^"]*"')


def convert_path(path_array, match):
    import_path = match.group(0)[1:-1].split(sep)
    if not import_path or import_path[0] != ('..'):
        return match.group(0)
    while import_path and import_path[0] == ('..'):
        path_array = path_array[0:-1]
        import_path = import_path[1:]
    if path_array and path_array[0] == ('.'):
        path_array = path_array[1:]
    q = match.group(0)[0]
    if path_array:
        path = os.path.join(q + root_path_name, os.path.join(*path_array))
    else:
        path = q + root_path_name
    return os.path.join(path, os.path.join(*import_path) + q)


def convert_import(path_array, match):
    return path_expression.sub(
        lambda match: convert_path(path_array, match), match.group(0))


def convert(path, file):
    path_array = path.split(sep)
    with open(os.path.join(path, file)) as f:
        content = f.read()

    with open(os.path.join(path, file), 'w') as f:
        content = import_expression.sub(
            lambda match: convert_import(path_array, match), content)
        f.write(content)


os.chdir(root_path)
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.ts'):
            convert(root, file)
