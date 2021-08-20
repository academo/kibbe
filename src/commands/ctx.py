import os
from pathlib import Path
import subprocess

import click
from termcolor import colored

from src.util import get_valid_filename


@click.command()
@click.argument("name")
@click.option(
    "--branch",
    help="Branch name to use for the new worktree",
    default="",
)
@click.option(
    "--path",
    help="Custom path to use to set the new worktree. Defaults to ../CONTEXT_NAME",
    default="",
)
@click.option(
    "--source",
    help="Branch to create the worktree from. Defaults to current branch",
    default="",
)
@click.option(
    "-i",
    "--interactive",
    help="Ask questions about the new context",
    is_flag=True,
    default=False,
)
@click.option("--cd", is_flag=True, default=True)
def ctx(name, path, source, branch, interactive, cd):

    # TODO check if the worktree exists and switch to it

    if not branch:
        if interactive:
            branch = click.prompt("Git branch name fore the new worktree", default=name)
        else:
            branch = name

    if not path:
        possible_folder_name = get_valid_filename(branch)
        possible_path = os.path.join(
            Path(os.getcwd()).parent.absolute(), possible_folder_name
        )
        if interactive:
            path = click.prompt(
                "Path target for the git worktree",
                default=possible_path,
                type=click.Path(dir_okay=True, file_okay=False),
            )
        else:
            path = possible_path

    if not source:
        possible_source = subprocess.getoutput("git rev-parse --abbrev-ref HEAD")
        if interactive:
            source = click.prompt(
                "Source branch for the git worktree", default=possible_source
            )
        else:
            source = possible_source

    click.echo("Will create a new git worktree called: " + colored(name, "yellow"))
    click.echo("In this location: " + colored(path, "blue"))
    click.echo("With a new branch name: " + colored(branch, "blue"))
    click.echo("From this local branch: " + colored(source, "blue"))
