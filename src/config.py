from pathlib import Path, PurePath
import configparser
from click.termui import confirm
from termcolor import colored

import click


def get_config_path():
    return str(PurePath(Path.home()).joinpath('.kibbe'))


def get_config():
    config = configparser.ConfigParser()
    try:
        config.read(get_config_path())
    except ValueError:
        click.echo(colored('Error reading your configuration file.', 'red'))
        pass
    return config


def persist_config(config_map):
    try:
        if click.confirm("Are you sure you want to save this configuration?\nAll existing configuration will be overwritten"):
            config = get_config()
            for config_key in config_map:
                if config_key not in config:
                    config.add_section(config_key)

                data = config_map[config_key]
                if type(data) is dict:
                    for key in data:
                        wkey = key
                        if wkey.startswith('--'):
                            wkey = wkey[2:]
                        config.set(config_key, wkey, data[key])
                else:
                    for value in data:
                        value = value.split('=')
                        if len(value) > 1:
                            config.set(config_key, value[0], value[1])
                        else:
                            config.set(config_key, value[0], '')

            config_file = open(get_config_path(), 'w')
            config.write(config_file)
            click.echo(colored('Configuration written to kibbe config', 'blue'))
        else:
            click.echo(colored("Cancelled", 'yellow'))
            exit()
    except ValueError:
        exit()
