import subprocess
import click
from src.config import get_config, persist_config
from src.util import merge_params, unparsed_to_map
from src.util import wait_for_elastic_search
from termcolor import colored


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
    "--save-config",
    default=False,
    is_flag=True,
    help=(
        "If passed it will write your kibbe configuration with all the current passed"
        " parameters. This will not modify your kibana repo clone."
    ),
)
@click.argument("unparsed_args", nargs=-1, type=click.UNPROCESSED)
def kibana(save_config, unparsed_args, wait):
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

    params = merge_params(config_params, unparsed_args)

    if save_config:
        persist_config({"kibana.params": unparsed_to_map(params)})
        exit()

    command = ["node", "scripts/kibana", "--dev"] + params
    click.echo("Will run kibana search as: " + colored(" ".join(command), "yellow"))
    subprocess.run(command)
