import subprocess
import click

from src.config import get_config
from src.util import merge_params
from termcolor import colored


@click.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('unparsed_args', nargs=-1, type=click.UNPROCESSED)
def kibana(unparsed_args):
    """
    Runs Kibana from the current clone.

    You can pass the same parameters as you'd pass to `node scritps/kibana`

    You can persist some parameters by using a configuration file `~/.kibbe`.
    with the [kibana.params] section.

    See more about the configuration file here:
    https://github.com/academo/kibbe#configuration-file
    """

    config_params = []
    config = get_config()
    if 'kibana.params' in config:
        config_params = config.items('kibana.params', raw=True)

    params = merge_params(config_params, unparsed_args)
    command = ['node', 'scripts/kibana', '--dev'] + params
    click.echo("Will run kibana search as: " + colored(' '.join(command), 'yellow'))
    subprocess.run(command)
