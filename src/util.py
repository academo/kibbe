import os
import json
import subprocess
from pathlib import PurePath


def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""

    # from whichcraft import which
    from shutil import which

    return which(name) is not None


def is_kibana_repo():
    if not os.path.isfile('package.json'):
        return False

    file = open('package.json')
    try:
        content = json.load(file)
        if content['name'] != 'kibana' or not content['homepage'].startswith('https://www.elastic.co/'):
            return False
    except ValueError:
        return False
    finally:
        file.close()

    return True


def get_modified_files():
    list = ""
    try:
        list = subprocess.getoutput('git diff --name-only HEAD')
    except ValueError:
        return []

    list = list.split('\n')
    return list


def find_related_test(file):
    path = PurePath(file)

    # skip if the file is a test
    if path.match('*.test.*'):
        return ""

    test_file = path.with_suffix('.test' + path.suffix)

    if os.path.isfile(test_file):
        return test_file

    return ""


def find_related_plugin_folder(file):
    path = PurePath(file)

    if not path.relative_to('x-pack/plugins'):
        return ""

    while not path.match('x-pack/plugins/*'):
        path = PurePath(path.parent)

    return str(path)
