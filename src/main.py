import click
from src.commands.setlicense import setlicense


@click.group()
def cli():
    # here only to create a click namespace
    pass


cli.add_command(setlicense)
