import os

import click
import libtmux
from termcolor import colored


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
