import re
import subprocess

from termcolor import colored
from src.config import get_config
import click
import tempfile
from pathlib import Path

pathDataRe = re.compile(r"path\.data\s?=", re.IGNORECASE)


@click.command(help="Runs elastic search from the current kibana clone. It will use parameters from the ~/.kibbe [elastic.params] section.")
@click.option('--data-dir', '-d', type=click.STRING, default="esdata", help="Path where this elastic search will store its data (path.data)")
@click.option('--no-persist', '-n', default=False, is_flag=True, help="If passed will use a disposable data dir. This option will overwrite other options related to data dir.")
@click.option('-E', multiple=True, help="Additional options to pass to elastic search. `path.data` will be ignored")
def es(data_dir, no_persist, e):

    params = process_params(data_dir, no_persist)

    # additional -E params
    for item in e:
        item = item.strip()
        # ignore path.data
        if pathDataRe.match(item):
            continue
        params.append(item)

    command = get_command(params)
    click.echo("Will run elastic search as: " + colored(' '.join(command), 'yellow'))
    subprocess.run(command)


def get_command(params):
    final_params = []
    for param in params:
        final_params.append('-E')
        final_params.append(param)

    return ['node', 'scripts/es', 'snapshot'] + final_params


def process_params(data_dir, no_persist):
    CONFIG_KEY = 'elastic.params'
    config = get_config()
    params = []
    if CONFIG_KEY in config:
        for (key, value) in config.items(CONFIG_KEY, raw=True):
            # ignore path.data if this command overwrites it
            if key == 'path.data':
                if len(data_dir) > 0:
                    value = get_data_dir(data_dir, no_persist)
                else:
                    value = get_data_dir(value, no_persist)

            if len(value) > 0:
                params.append(str(key) + '=' + str(value))
            else:
                params.append(str(key))

    return params


def get_data_dir(data_dir, no_persist):
    if no_persist or len(data_dir) == 0:
        return tempfile.mkdtemp(suffix='kibbe')

    return str(Path(data_dir).resolve())
