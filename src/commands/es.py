from pathlib import Path
import re
from shutil import rmtree
import subprocess
import tempfile

import click
from termcolor import colored

from src.config import get_config, persist_config
from src.util import get_valid_filename, merge_params, unparsed_to_map

pathDataRe = re.compile(r"path\.data\s?=", re.IGNORECASE)


@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
    )
)
@click.option(
    "--data-dir",
    "-d",
    type=click.STRING,
    default="",
    help="Path where this elastic search will store its data (path.data)",
)
@click.option(
    "--no-persist",
    "-n",
    default=False,
    is_flag=True,
    help=(
        "If passed will use a disposable data dir. This option will overwrite other"
        " options related to data dir."
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
@click.option(
    "--flush",
    is_flag=True,
    default=False,
    help="If passed will flush the ES datadir directory before starting es.",
)
@click.option(
    "-E",
    multiple=True,
    help="Additional options to pass to elastic search. `path.data` will be ignored",
)
@click.argument("unparsed_args", nargs=-1, type=click.UNPROCESSED)
def es(data_dir, no_persist, e, unparsed_args, save_config, flush):
    """
    Runs elastic search from the current kibana clone.

    You can also pass the same parameters as you'd pass to `node scritps/es`

    You can persist the -E parameters by using a configuration file `~/.kibbe`.
    with the [elastic.params] section.

    See more about the configuration file here:
    https://github.com/academo/kibbe#configuration-file
    """

    e_params = get_eparams(data_dir, no_persist)

    # additional -E params
    for item in e:
        item = item.strip()

        # ignore if passing a path.data -E param
        if pathDataRe.match(item):
            continue

        item = item.split("=")
        try:
            e_params[str(item[0])] = str(item[1]) if str(item[1]) else ""
        except ValueError:
            pass

    params = []
    config = get_config()

    config_params = []
    if "elastic.params" in config:
        config_params = config.items("elastic.params", raw=True)
    params = merge_params(config_params, unparsed_args)

    if not no_persist and "path.data" not in e_params:
        # not a path data passed. Will create one based on the current branch name
        try:
            current_branch = subprocess.getoutput("git rev-parse --abbrev-ref HEAD")
            data_dir = "../" + get_valid_filename("kibbe-esdata-" + current_branch)
            e_params["path.data"] = get_data_dir(data_dir, no_persist)
        except ValueError:
            pass

    if flush:
        for param in e_params:
            if param == "path.data":
                try:
                    dataDir = e_params[param]
                    click.echo(colored("Will remove data dir %s" % (dataDir), "red"))
                    rmtree(dataDir, ignore_errors=True)
                except ValueError:
                    pass
                finally:
                    break

    e_params = normalize_eparams(e_params)

    if save_config:
        persist_config(
            {"elastic.eparams": e_params, "elastic.params": unparsed_to_map(params)}
        )
        exit()

    command = get_command(e_params, extra_params=params)
    click.echo("Will run elastic search as: " + colored(" ".join(command), "yellow"))
    subprocess.run(command)


def get_command(e_params, extra_params):
    final_params = []
    for param in e_params:
        final_params.append("-E")
        final_params.append(param)

    return ["node", "scripts/es", "snapshot"] + final_params + extra_params


def get_eparams(data_dir, no_persist):
    CONFIG_KEY = "elastic.eparams"
    config = get_config()
    params = {}
    if CONFIG_KEY in config:
        for (key, value) in config.items(CONFIG_KEY, raw=True):
            # ignore path.data if this command overwrites it
            if key == "path.data":
                if len(data_dir) > 0:
                    value = get_data_dir(data_dir, no_persist)
                else:
                    value = get_data_dir(value, no_persist)

            params[str(key)] = str(value) if value else ""

    return params


def get_data_dir(data_dir, no_persist):
    if no_persist or len(data_dir) == 0:
        return tempfile.mkdtemp(suffix="kibbe")

    return str(Path(data_dir).resolve())


def normalize_eparams(params):
    final = []
    for param in params:
        final.append("%s=%s" % (param, params[param]))
    return final
