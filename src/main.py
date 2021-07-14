import click

from src.commands.check import check
from src.commands.es import es
from src.commands.setlicense import setlicense
from src.util import force_kibana_root


@click.group()
def cli():
    force_kibana_root()


cli.add_command(setlicense)
cli.add_command(check)
cli.add_command(es)
