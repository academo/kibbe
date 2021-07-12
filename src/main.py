import click
from src.commands.setlicense import setlicense
from src.commands.functional import functional
from src.commands.check import check


@click.group()
def cli():
    # here only to create a click namespace
    pass


cli.add_command(setlicense)
cli.add_command(functional)
cli.add_command(check)
