from os.path import join, abspath
from os import walk
import re

root_path = join('src', 'app')

import_expression = re.compile(
    'import\\s*(?:{[^}]*}|\\*\\s+as\\s+\\w+\\s)\\s*from\\s*(?:\'[^\']*\'|"[^"]*")\\s*;')

path_expression = re.compile('\'[^\']*\'|"[^"]*"')

aliases = [
    {'key': '@core', 'value': join('src', 'app', 'core')},
    {'key': '@environment', 'value': join('src', 'environments', 'environment')}
]

def convert_path(path, match):
    import_path = match.group(0)[1:-1]
    if not import_path.startswith('..'):
        return match.group(0)
    full_import_path = abspath(join(path, import_path))
    for alias in aliases:
        full_alias_path = abspath(alias['value'])
        q = match.group(0)[0]
        if full_import_path.startswith(full_alias_path):
            return q + alias['key'] + full_import_path[len(full_alias_path):] + q
    return match.group(0)


def convert_import(path, match):
    return path_expression.sub(
        lambda match: convert_path(path, match), match.group(0))


def convert(path, file):
    with open(join(path, file)) as f:
        content = f.read()

    content = import_expression.sub(
        lambda match: convert_import(path, match), content)
    with open(join(path, file), 'w') as f:
        f.write(content)


for root, dirs, files in walk(root_path):
    for file in files:
        if file.endswith('.ts'):
            convert(root, file)
