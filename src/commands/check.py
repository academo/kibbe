import click
import subprocess
from src.util import is_kibana_repo, get_modified_files


@click.command(help="""Run quick checks for your modified files. Useful to run before committing""")
def check():
    if not is_kibana_repo():
        raise click.ClickException("Not a kibana repo")

    modified = get_modified_files()

    if len(modified) > 0:
        # run eslint
        click.echo("Running eslint on modified files")
        subprocess.run(['node', 'scripts/eslint.js'] + modified)
