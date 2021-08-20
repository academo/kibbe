import os
from pathlib import Path
from src.git import find_existing_worktree, get_worktree_list_flat
from src.tmux import get_current_panel, is_inside_tmux
import subprocess

import click
from termcolor import colored

from src.util import get_valid_filename


@click.command()
@click.argument(
    "name", type=click.STRING, autocompletion=get_worktree_list_flat, required=False
)
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
@click.option(
    "--cd",
    "--change-dir",
    help="Change to new context directory (Tmux only)",
    is_flag=True,
    default=True,
)
@click.option(
    "--delete",
    help="Removes the worktree if exists",
    is_flag=True,
    default=False,
    confirmation_prompt=True,
)
@click.option(
    "-l",
    "--list-worktrees",
    help="List existing worktree. Alias for `git worktree list`",
    is_flag=True,
    default=False,
)
def ctx(
    name,
    parent_path,
    source,
    branch,
    interactive,
    overwrite_branch,
    cd,
    list_worktrees,
    delete,
):
    """
    ctx is a wrapper kibbe subcommand for git worktree with some quality of life improvements.

    NAME accepts a name of the "context" you want to switch. It is a shorthand to not have to remember
    paths as is required with git worktree.

    It allows you to quickly switch and create git worktrees without having to type or memorize
    all the git worktree parameterse.

    ctx works better when you use it with tmux. In mac, if you use iterm2,
    you can start tmux with `tmux -CC`. Install it first with `brew install tmux`

    ctx is not intended to be a replacement for git worktree, if you can't perform the operation
    you want with ctx please see the git worktree manual entry https://git-scm.com/docs/git-worktree
    """

    if list_worktrees:
        subprocess.run(["git", "worktree", "list"])
        exit(0)

    if not name:
        raise click.ClickException(
            colored(
                "You must pass the NAME of the worktree you want to change to", "red"
            )
        )

    path_name = get_valid_filename(name)
    existing_worktree = find_existing_worktree(path_name)

    if delete and not existing_worktree:
        raise click.ClickException(
            "Can not remove worktree. Worktree doesn't exist: "
            + colored(path_name, "red")
        )
    elif delete:
        if click.confirm(
            "Are you sure you want to delete the wortree"
            + colored(existing_worktree["worktree"], "yellow")
        ):
            click.echo("Deleting worktree...")
            subprocess.run(["git", "worktree", "remove", existing_worktree["worktree"]])
        exit(0)

    if existing_worktree:
        return handle_existing_worktree(existing_worktree)

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

    # this must always be the last command
    if cd and is_inside_tmux():
        click.echo("Tmux session detected. Changing to worktree")
        current_pane = get_current_panel()
        current_pane.send_keys("cd %s && nvm use" % full_path)
        exit(0)
    elif not is_inside_tmux():
        click.echo(
            "Changing to a worktree is only supported if you are running inside tmux"
        )


def handle_existing_worktree(existing_worktree):
    existing_path_name = existing_worktree["worktree"]
    click.echo(
        "Existing worktree with the same name found at "
        + colored(existing_path_name, "yellow")
    )
    click.echo("Worktree branch: " + colored(existing_worktree["branch"], "blue"))
    click.echo("Head commit: " + colored(existing_worktree["HEAD"], "blue"))
    click.echo()

    if Path(existing_path_name) == Path(os.getcwd()):
        click.echo(colored("You are already on this worktree", "yellow"))
        exit(0)

    if not is_inside_tmux():
        click.echo("You can switch to it by running: ")
        click.echo(colored("cd %s" % existing_path_name, "blue"))
        click.echo()
        click.echo("Run this command inside tmux to automatically cd to it")
    else:
        click.echo("Tmux session detected. Changing to worktree")
        current_pane = get_current_panel()
        current_pane.send_keys("cd %s && nvm use" % existing_path_name)
        exit(0)
