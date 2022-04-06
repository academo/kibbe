import click
import os
import subprocess
import re

from termcolor import colored

from src.config import get_kibbe_config


@click.command()
@click.argument("testfile", type=click.Path(exists=True), required=False)
@click.option(
    "--watch", "-w", default=False, is_flag=True, help="Run jest in watch mode"
)
def jest(testfile, watch):
    """
    Helper for kibana's jest runner script.

    If TESTFILE is passed. It will run jest for it.

    If TESTFILE is not passed it will prompt you to select a test file
    from `git status`
    """
    if testfile:
        run_for_file(testfile, watch)
        return

    file_re = re.compile(r"\.test\.(t|j)sx?$")

    status = subprocess.getoutput("git status --porcelain")
    modifiedlist = status.split("\n")

    selectable = []
    for entry in modifiedlist:
        try:
            file = entry.split(" ")[-1]
            if file_re.search(file):
                selectable.append(file)
        except Exception:
            pass

    if len(selectable) == 0:
        click.echo("No test files modified")
        return

    counter = 1
    choices = []
    click.echo(colored("Select a file to test", "blue"))
    for file in selectable:
        click.echo("%d. %s" % (counter, file))
        choices.append(str(counter))
        counter = counter + 1

    file_nr = click.prompt(
        text="File list number",
        default="1",
        show_choices=False,
        type=click.Choice(choices),
    )

    run_for_file(selectable[int(file_nr) - 1], watch)


def run_for_file(testfile: str, watch: bool):
    command_args = ""
    max_workers = get_kibbe_config("jest-max-workers")

    if max_workers:
        command_args = command_args + " --maxWorkers=%s" % max_workers

    if watch:
        command_args = command_args + " --watch"

    command = "node scripts/jest.js %s %s" % (command_args, testfile)
    click.echo(colored(command, "yellow"))
    os.system("node scripts/jest.js %s %s" % (command_args, testfile))
