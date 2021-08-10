import configparser
from pathlib import Path, PurePath

import click
from termcolor import colored

config_path = ""


def set_config_file(path):
    global config_path
    if path and len(path) > 0:
        config_path = str(PurePath(path))
    else:
        config_path = str(PurePath(Path.home()).joinpath(".kibbe"))


def get_config_file():
    global config_path
    return config_path


def get_config():
    config = configparser.ConfigParser()
    config.optionxform = str
    try:
        config.read(get_config_file())
    except ValueError:
        click.echo(colored("Error reading your configuration file.", "red"))
        pass
    return config


def persist_config(config_map):

    config = get_config_to_save(config_map)

    try:
        print_config(config)
        if click.confirm(
            "Are you sure you want to save this configuration?\nAll existing"
            " configuration will be overwritten"
        ):
            config_file = open(get_config_file(), "w")
            config.write(config_file)
            click.echo(colored("Configuration written to kibbe config", "blue"))
        else:
            click.echo(colored("Cancelled", "yellow"))
            exit()
    except ValueError:
        exit()


def get_config_to_save(config_map):
    config = get_config()
    for config_key in config_map:
        if config_key not in config:
            config.add_section(config_key)

        data = config_map[config_key]
        if type(data) is dict:
            for key in data:
                wkey = key
                if wkey.startswith("--"):
                    wkey = wkey[2:]
                config.set(config_key, wkey, data[key])
        else:
            for value in data:
                value = value.split("=")
                if len(value) > 1:
                    config.set(config_key, value[0], value[1])
                else:
                    config.set(config_key, value[0], "")

    return config


def print_config(config):
    config_string = "--start--\n"
    sections = config.sections()
    for section in sections:
        config_string = config_string + "[%s]\n" % (section)
        items = config.items(section)
        for item, value in items:
            config_string = config_string + "%s = %s\n" % (item, value)
        config_string = config_string + "\n"
    config_string = config_string + "---end---"

    click.echo(colored("Config to save:\n ", "yellow"))
    click.echo(config_string)
