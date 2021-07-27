import os
import subprocess
import sys

import click
from termcolor import colored

import libtmux


@click.command(help="Proxy for yarn kbn bootstrap")
@click.option("--clean", "-c", is_flag=True, help="Runs bootstrap with clean")
@click.option(
    "--tmux",
    is_flag=True,
    help=(
        "If you run kibbe inside a tmux session it will divide the current window, run"
        " elasticsearch (kibbe es) and kibana (kibbe kibana)"
    ),
)
@click.option(
    "--flush",
    is_flag=True,
    default=False,
    help="If passed will pass the flush flag to ES when initializing",
)
def setmeup(clean, tmux, flush):

    commands = []
    if clean:
        commands.append(["yarn", "kbn", "bootstrap", "clean"])

    commands.append(["yarn", "kbn", "bootstrap"])

    for command in commands:
        subprocess.run(command)

    if tmux:
        setup_tmux(flush=flush)


def setup_tmux(flush=False):

    current_window = get_current_window()
    clean_tmux_window(current_window)
    current_pane_id = os.getenv("TMUX_PANE")
    current_pane = current_window.get_by_id(current_pane_id)

    es_pane = current_window.split_window(vertical=False)
    start_es(es_pane, flush=flush)

    click.echo(colored("Starting kibana and closing this pane", "yellow"))
    kibana_pane = current_window.split_window(vertical=False)
    start_kibana(kibana_pane)

    # close this pane. This will also kill the python process
    current_pane.cmd("kill-pane")
    exit()


def start_kibana(kibana_pane):
    current_dir = os.getcwd()
    kibbe_command = sys.argv[0]

    kibana_pane.send_keys("cd %s" % current_dir)
    kibana_pane.send_keys("nvm use")
    kibana_pane.send_keys("%s kibana --wait" % kibbe_command)


def start_es(es_pane, flush=False):
    current_dir = os.getcwd()
    kibbe_command = sys.argv[0]

    params = ""
    if flush:
        params = "--flush"

    es_pane.send_keys("cd %s" % current_dir)
    es_pane.send_keys("nvm use")
    es_pane.send_keys("%s es %s" % (kibbe_command, params))


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
