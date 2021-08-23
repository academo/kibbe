import click
from termcolor import colored

from src.config import get_config, print_config


@click.command("config")
def config():
    """
    Prints the current kibbe configuration and where is it taking it from
    """
    click.echo(colored("Configuration to use", "yellow"))
    config = get_config()
    print_config(config)
