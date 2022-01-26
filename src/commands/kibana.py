import subprocess
import sys

import click
import re
import atexit
import psutil
import enlighten
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
    "--prod",
    "-p",
    default=False,
    is_flag=True,
    help="Runs Kibana in production mode (omits the '--dev' argument).",
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
def kibana(save_config, unparsed_args, wait, alt, prod):
    """
    Runs Kibana from the current clone.

    You can pass the same parameters as you'd pass to `node scripts/kibana`

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

    command = ["node", "scripts/kibana"]
    if not prod:
        command.append("--dev")
    command.extend(params)
    click.echo("Will run kibana search as: " + colored(" ".join(command), "yellow"))

    if alt:
        run_kibana_alt(command)
    else:
        subprocess.run(command)


def run_kibana_alt(command):
    # command = ["node test.js"]

    manager = enlighten.get_manager()

    pbar = manager.counter(
        total=100, desc="Optimizer", unit="bundles", color="blue_on_green"
    )
    status = manager.status_bar(
        fields={"kibana_status": "Initializing"},
        status_format="Kibana is {kibana_status}",
        color="white_on_black",
    )

    process = subprocess.Popen(
        "FORCE_COLOR=1 " + " ".join(command),
        shell=True,
        stdout=subprocess.PIPE,
    )

    pbar.count = int(0)
    pbar.refresh()

    if process.stdout:
        while True:
            # exit kibbe if the node process died
            if process.poll() is not None or process.returncode:
                sys.exit()
            output = process.stdout.readline()
            if output:
                line = output.decode("utf-8")
                sys.stdout.write(line)
                parse_line(line, pbar, status)


optimizerProgressRe = re.compile(r"^.*?@kbn\/optimizer.*?\[(\d+)\/(\d+)\]\s.*$")
optimizerSuccessRe = re.compile(r"^.*?success.*?kbn\/optimizer.*")

kibanaServerRunning = re.compile(r".*http\.server\.Kibana.*?http server running")
kibanaServerStatus = re.compile(r".*?status.*?\sKibana\sis\snow\s(.+)(?:\s|$)")


def parse_line(line: str, pbar: enlighten.Counter, status: enlighten.StatusBar):
    progressMatch = optimizerProgressRe.match(line)
    if progressMatch:
        current = int(progressMatch.group(1))
        total = int(progressMatch.group(2))
        pbar.total = total
        pbar.count = current
        pbar.refresh()
        return
    successMatch = optimizerSuccessRe.match(line)
    if successMatch:
        pbar.clear()
        return

    if kibanaServerRunning.match(line):
        status.fields["kibana_status"] = "⌛ Server loading"
        status.refresh()
        return

    kibanaStatusMatch = kibanaServerStatus.match(line)
    if kibanaStatusMatch:
        message = str(kibanaStatusMatch.group(1))
        message = get_kibana_icon(message) + message
        status.fields["kibana_status"] = message
        status.refresh()
        return


def get_kibana_icon(message):
    if "available" in message:
        return "✅ "

    if "degraded" in message:
        return "⌛ "

    return ""


def exit_():
    """
    Makes sure that when exiting kibbe any remaining subprocess is killed.
    This is useful because if kibbe starts a nodejs process it might spawn
    more sub-proceses but they will not be terminated if the parent is asked to
    do so.
    """
    current_process = psutil.Process()
    children = current_process.children(recursive=True)
    for child in children:
        try:
            child.terminate()
        except:
            pass


atexit.register(exit_)


"""
const fs = require('fs');
const lines = fs.readFileSync('output.log').toString().split('\n');

let current = 0;

const int = setInterval(() => {
  console.log(lines[current]);
  current++;
  if (lines[current] === undefined) {
    clearInterval(int);
  }
});

"""
