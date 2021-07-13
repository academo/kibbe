from src.util import force_kibana_root
import click
from src.commands.setlicense import setlicense
from src.commands.functional import functional
from src.commands.check import check


@click.group()
def cli():
    force_kibana_root()


cli.add_command(setlicense)
cli.add_command(functional)
cli.add_command(check)
