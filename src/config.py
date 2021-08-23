import configparser
import os
from pathlib import Path
from src.util import get_valid_filename

import click
from termcolor import colored


def get_config_file(first=False):

    default_config_file = str(Path.home().joinpath(".kibbe"))

    config_files = []

    current_dir = os.getcwd()

    possible_paths = [
        default_config_file,
        str(Path.home().joinpath(".kibberc")),
        os.path.join(current_dir, ".kibbe"),
        os.path.join(current_dir, ".kibberc"),
    ]
    for path in possible_paths:
        possible_path = Path(path)
        if possible_path.exists():
            config_files.append(str(path))

    if len(config_files) == 0:
        config_files.append(default_config_file)

    if first:
        return config_files[0]

    return possible_paths


def make_config_files(config):
    for section in config.sections():
        if section.startswith("file-") and "content" in config[section]:
            try:

                current_dir = os.getcwd()
                filename = get_valid_filename(section[5:])
                filepath = os.path.join(current_dir, filename)
                content = config[section]["content"].lstrip()

                try:

                    # if the file exists, check they don't have different content
                    if Path(filepath).exists():
                        current_file = open(filepath, "r")
                        current_content = current_file.read()

                        # if the current content and future content are the same continue
                        if current_content == content:
                            continue
                        else:
                            if not click.confirm(
                                "File "
                                + colored(filename, "yellow")
                                + " already exists and has a different content."
                                " Overwrite?"
                            ):
                                continue
                except ValueError:
                    pass

                # write the config file
                click.echo("Writing config file " + colored(filename, "yellow"))
                file = open(filepath, "w")
                file.write(content)
                file.close()
            except ValueError:
                pass


def get_config():
    config = configparser.ConfigParser()
    try:
        config.optionxform = str  # type: ignore
    except ValueError:
        pass
    try:
        config.read(get_config_file())
    except ValueError:
        click.echo(colored("Error reading your configuration file.", "red"))
        pass
    return config


def persist_config(config_map):

    config = get_config_to_save(config_map)

    try:
        click.echo(colored("Config to save:\n ", "yellow"))
        print_config(config)
        if click.confirm(
            "Are you sure you want to save this configuration?\nAll existing"
            " configuration will be overwritten"
        ):
            config_file = open(str(get_config_file(first=True)), "w")
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

    click.echo(config_string)
