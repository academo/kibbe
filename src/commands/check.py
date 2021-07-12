import subprocess

import click

from src.util import find_related_plugin_folder, get_modified_files, is_kibana_repo


@click.command(help="""Run quick checks for your modified files. Useful to run before committing""")
def check():
    if not is_kibana_repo():
        raise click.ClickException("Not a kibana repo")

    modified = get_modified_files()

    configs = set()
    for file in modified:
        configs.add(find_related_plugin_folder(file))

    print(configs)

    if len(modified) > 0:
        # run eslint
        click.echo("Running eslint on modified files")
        subprocess.run(['node', 'scripts/eslint.js'] + modified)
