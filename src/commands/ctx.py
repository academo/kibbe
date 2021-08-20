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
    "--parent-path",
    help="Custom parent path to use to set the new worktree. Defaults to ../",
    default="",
)
@click.option(
    "--source",
    help="Branch to create the worktree from. Defaults to current branch. e.g. master",
    default="",
)
@click.option(
    "-i",
    "--interactive",
    help="Ask questions about the new context",
    is_flag=True,
    default=False,
)
@click.option(
    "-B",
    "--overwrite-branch",
    help="If the branch already exists, reset it to source",
    is_flag=True,
    default=False,
)
def ctx(name, parent_path, source, branch, interactive, overwrite_branch):

    # TODO check if the worktree exists and switch to it
    path_name = get_valid_filename(name)

    if not branch:
        if interactive:
            branch = click.prompt("Git branch name fore the new worktree", default=name)
        else:
            branch = name

    if not parent_path:
        possible_path = os.path.join(Path(os.getcwd()).parent.absolute())
        if interactive:
            parent_path = click.prompt(
                "Parent path target for the git worktree",
                default=possible_path,
                type=click.Path(dir_okay=True, file_okay=False),
            )
        else:
            parent_path = possible_path

    full_path = os.path.join(parent_path, path_name)

    if not source:
        possible_source = subprocess.getoutput("git rev-parse --abbrev-ref HEAD")
        if interactive:
            source = click.prompt(
                "Source branch for the git worktree. e.g. master",
                default=possible_source,
            )
        else:
            source = possible_source

    click.echo("Will create a new git worktree called: " + colored(path_name, "yellow"))
    click.echo("In this location: " + colored(parent_path, "blue"))
    click.echo("With a new branch name: " + colored(branch, "blue"))
    click.echo("From this branch: " + colored(source, "blue"))
    click.echo("---git output--")

    b_option = "-b" if not overwrite_branch else "-B"

    command = ["git", "worktree", "add", full_path, source, b_option, branch]
    process = subprocess.run(command)
    click.echo("--- end git output---")

    if process.returncode != 0:
        raise click.ClickException(
            colored(
                "Something went wrong with git. See git output and verify your"
                " parameters",
                "red",
            )
        )

    click.echo(
        colored("Success!", "green")
        + " a new git worktree was created in "
        + colored(full_path, "blue")
    )

    click.echo("To change to your new worktree run:")
    click.echo(colored("cd %s" % full_path, "yellow"))
