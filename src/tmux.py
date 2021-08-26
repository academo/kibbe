import os
from pathlib import Path
import platform
from shutil import which
import subprocess
import random
import sys

import click
import libtmux
from termcolor import colored


def setup_tmux_client():
    if is_inside_tmux():
        # nothing to do
        return True

    tmux_installed = False

    try:
        tmux_bin = which("tmux")
        if tmux_bin and Path(tmux_bin).exists():
            tmux_installed = True
    except ValueError:
        pass

    if tmux_installed:
        click.echo(
            "You are not inside a tmux session. Create a new session first by"
            " running: \n"
        )

        tmux_command = ["tmux"]
        if platform.system() == "Darwin" and os.getenv("TERM_PROGRAM") == "iTerm.app":
            tmux_command.append("-CC")

        session_name = "kibbe_" + str(random.randint(0, 100))

        tmux_command = tmux_command + ["new-session", "-A", "-s", session_name]

        click.echo(colored(" ".join(tmux_command), "yellow"))

        if click.confirm("Do you want kibbe to run all for you?"):
            tmux_command.append("-d")
            subprocess.run(tmux_command)

            try:
                server = libtmux.Server()
                if not server.has_session(session_name):
                    raise Exception("no tmux session kibbe created")

                session = next(
                    session
                    for session in server.list_sessions()
                    if session.name == session_name
                )
                pane = session.attached_pane

                current_dir = os.getcwd()
                pane.send_keys("cd %s && nvm use" % current_dir)

                current_command = " ".join(sys.argv)
                pane.send_keys(current_command)

                # attach the current terminal to that session
                server.attach_session(session_name)
            except ValueError:
                raise click.ClickException(
                    colored(
                        "There was an error connecting to the tmux session. Check your"
                        " tmux installation and configuration",
                        "red",
                    )
                )

    else:
        click.echo("You don't have tmux installed. To install it:\n")

        if platform.system() == "Darwin":
            click.echo(colored("brew install tmux", "yellow"))
        elif platform.system() == "Linux":
            version = platform.version().lower()
            if "ubuntu" in version or "debian" in version:
                click.echo(colored("sudo apt install tmux", "yellow"))
            elif "fedora" in version:
                click.echo(colored("sudo yum install tmux", "yellow"))
            else:
                click.echo("Visit https://github.com/tmux/tmux/wiki/Installing")

        # no tmux detected
        exit(1)


def is_inside_tmux():
    return os.getenv("TMUX") is not None


def get_current_panel():
    current_window = get_current_window()
    current_pane_id = os.getenv("TMUX_PANE")
    current_pane = current_window.get_by_id(current_pane_id)
    return current_pane


def get_current_window():
    tmux_panel = os.getenv("TMUX_PANE")
    tmux_session = os.getenv("TMUX")
    if not tmux_panel or not tmux_session:
        raise click.ClickException("Not inside a tmux session")

    tmux_session_id = "$" + tmux_session.split(",")[-1]
    server = libtmux.Server()

    session = server.get_by_id(tmux_session_id)
    if not session:
        raise click.ClickException("Could not interact with Tmux. Wrong tmux version")

    return session.attached_window


def clean_tmux_window(current_window):

    if len(current_window.panes) > 1:
        if not click.confirm(
            colored(
                "The current window has more than 1 pane. Do you want to close them all"
                " and start new ones?",
                "yellow",
            )
        ):
            raise click.ClickException(
                colored(
                    "Close all panes or create a new window to continue and run kibbe"
                    " again",
                    "red",
                )
            )
        current_pane_id = os.getenv("TMUX_PANE")
        current_pane = current_window.get_by_id(current_pane_id)
        panes = iter(current_window.panes)
        for pane in panes:
            if pane != current_pane:
                pane.cmd("kill-pane")
