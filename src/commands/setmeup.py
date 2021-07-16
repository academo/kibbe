import subprocess

import click
from termcolor import colored


@click.command(help="Proxy for yarn kbn bootstrap")
@click.option("--clean", "-c", is_flag=True, help="Runs bootstrap with clean")
def setmeup(clean):
    if clean:
        click.echo(colored("Running bootstrap clean first", "yellow"))
        subprocess.run(["yarn", "kbn", "bootstrap", "clean"])

    subprocess.run(["yarn", "kbn", "bootstrap"])
