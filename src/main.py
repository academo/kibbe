from src.util import is_kibana_repo
import click
from src.commands.setlicense import setlicense
from src.commands.functional import functional
from src.commands.check import check


@click.group()
def cli():
    if not is_kibana_repo():
        raise click.ClickException("You must run kibbe inside a kibana repo")


cli.add_command(setlicense)
cli.add_command(functional)
cli.add_command(check)
