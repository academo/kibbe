import subprocess
from threading import Thread
import os
import sys
import signal
import psutil

import click
from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from termcolor import colored

from src.config import get_config, persist_config
from src.util import merge_params, unparsed_to_map
from src.util import wait_for_elastic_search

this = sys.modules[__name__]


@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
    )
)
@click.option(
    "--wait",
    "-w",
    default=False,
    is_flag=True,
    help=(
        "If passed. It will wait for an elastic search instance in the default port"
        " (9200) to be ready before starting kibana"
    ),
)
@click.option(
    "--alt",
    default=False,
    is_flag=True,
    help="Shows an alterantive kibana loading log. Based on text parsing and regex.",
)
@click.option(
    "--save-config",
    default=False,
    is_flag=True,
    help=(
        "If passed it will write your kibbe configuration with all the current passed"
        " parameters. This will not modify your kibana repo clone."
    ),
)
@click.argument("unparsed_args", nargs=-1, type=click.UNPROCESSED)
def kibana(save_config, unparsed_args, wait, alt):
    """
    Runs Kibana from the current clone.

    You can pass the same parameters as you'd pass to `node scritps/kibana`

    You can persist some parameters by using a configuration file `~/.kibbe`.
    with the [kibana.params] section.

    See more about the configuration file here:
    https://github.com/academo/kibbe#configuration-file
    """

    if wait:
        click.echo(
            colored("Waiting for elasticsearch in port 9200. Timeout in 60s", "blue")
        )
        wait_for_elastic_search()

    config_params = []
    config = get_config()
    if "kibana.params" in config:
        config_params = config.items("kibana.params", raw=True)

    params = merge_params(config_params, unparsed_args, useEqual=True)

    if save_config:
        persist_config({"kibana.params": unparsed_to_map(params)})
        exit()

    command = ["node", "scripts/kibana", "--dev"] + params
    click.echo("Will run kibana search as: " + colored(" ".join(command), "yellow"))

    if alt:
        run_kibana_alt(command)
    else:
        subprocess.run(command)


kb = KeyBindings()


@kb.add("c-c")
def exit_(event):
    """
    Pressing Ctrl-Q will exit the user interface.

    Setting a return value means: quit the event loop that drives the user
    interface and return this value from the `Application.run()` call.
    """
    event.app.exit()

    current_process = psutil.Process()
    children = current_process.children(recursive=True)
    for child in children:
        try:
            child.terminate()
        except:
            pass

    sys.exit()


def run_kibana_alt(command):

    buffer = Buffer()  # Editable buffer.

    main_window = Window(content=BufferControl(buffer=buffer))
    status_window = Window(height=1, content=FormattedTextControl(text="Status Bar"))

    root_container = HSplit([main_window, status_window])

    # command = ["ls -la"]
    layout = Layout(root_container)
    thread = Thread(target=run_command_in_thread, args=(command, buffer), daemon=True)
    thread.start()

    app = Application(key_bindings=kb, layout=layout, full_screen=True)
    app.run()
    print(os.getcwd())


def run_command_in_thread(command, buffer):
    process = subprocess.Popen(
        " ".join(command),
        shell=True,
        stdout=subprocess.PIPE,
    )

    if process.stdout:
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                buffer.insert_text(str(output.strip()))
                buffer.insert_line_below()
    exit()
