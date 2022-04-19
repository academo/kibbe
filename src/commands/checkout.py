import click
from src.tmux import is_inside_tmux
from src.util import is_tool
import os
import sys


@click.command()
@click.argument("tag", required=True)
def checkout(tag):
    """
    Quickly creates a new context with the passed PR tag checked out,
    then bootstrap and starts kibbe setmeup

    """
    if not is_tool("gh"):
        click.echo("You must install github cli for this feature to work")
        exit(1)

    if not is_inside_tmux():
        click.echo("You must run this command inside a tmux session")
        exit(1)

    branch = tag.replace(":", "-")

    kibbe_command = sys.argv[0]
    os.system("git branch -D %s" % branch)
    os.system("%s ctx -i %s" % (kibbe_command, branch))
    os.system("gh pr checkout %s" % tag)
    os.system("%s setmeup --tmux" % kibbe_command)
