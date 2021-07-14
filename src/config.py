from pathlib import Path, PurePath
import configparser
from termcolor import colored

import click


def get_config():
    config = configparser.ConfigParser()
    try:
        config_file_path = PurePath(Path.home()).joinpath('.kibbe')
        config.read(config_file_path)
    except ValueError:
        click.echo(colored('Error reading your configuration file.', 'red'))
        pass
    return config
