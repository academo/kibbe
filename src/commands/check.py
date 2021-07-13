import subprocess
import click
from termcolor import colored
import termcolor

from src.util import find_related_plugin_folder, find_related_test, get_modified_files, is_kibana_repo


@click.command(help="""Run quick checks for your modified files. Useful to run before committing""")
def check():
    if not is_kibana_repo():
        raise click.ClickException("Not a kibana repo")

    modified = get_modified_files()

    configs = set()
    tests = set()
    for file in modified:
        tests.add(find_related_test(file))
        configs.add(find_related_plugin_folder(file))

    tests = list(filter(None, tests))
    configs = list(filter(None, configs))

    # eslint
    if len(modified) > 0:
        click.echo(colored('>> Running eslint', 'yellow'))
        subprocess.run(['node', 'scripts/eslint.js'] + modified)

    # tests
    if (len(tests) > 0):
        click.echo(colored('>> Running related tests', 'yellow'))
        subprocess.run(['yarn', 'jest'] + tests)
