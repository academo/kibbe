import subprocess
from typing import DefaultDict
import click
import os
from termcolor import colored
import termcolor

from src.util import find_related_plugin_folder, find_related_test, force_kibana_root, get_modified_files


@click.command(help="""Run quick checks for your modified files. Useful to run before committing""")
@click.option('--skip-tests', default=False, help="Skip running tests", is_flag=True)
@click.option('--check-types', default=False, help="Runs Typescript types check (if relevant)", is_flag=True)
def check(skip_tests, check_types):
    force_kibana_root()

    modified = get_modified_files()

    configs = set()
    tests = set()
    for file in modified:
        tests.add(find_related_test(file))
        configs.add(find_related_plugin_folder(file))

    tests = list(filter(None, tests))
    configs = list(filter(None, configs))

    if check_types:
        click.echo(colored('>> Finding tsconfig.json', 'yellow'))
        for config in configs:
            tsconfig = os.path.join(config, 'tsconfig.json')
            if os.path.isfile(tsconfig):
                click.echo(colored('>>  - Running type_check for ', 'yellow') + colored(tsconfig, 'white'))
                subprocess.run(['node', 'scripts/type_check.js', '--project', tsconfig])
        return

    # eslint
    if len(modified) > 0:
        click.echo(colored('>> Running eslint', 'yellow'))
        subprocess.run(['node', 'scripts/eslint.js'] + modified)

    # tests
    if not skip_tests and len(tests) > 0:
        click.echo(colored('>> Running related tests', 'yellow'))
        subprocess.run(['yarn', 'jest'] + tests)
