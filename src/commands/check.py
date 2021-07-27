import os
from pathlib import PurePath
import subprocess

import click
from termcolor import colored

from src.util import find_related_plugin_folder, find_related_test, get_modified_files


@click.command(
    help="""Runs quick checks for your modified files. Useful to run before committing"""
)
@click.option("--skip-tests", default=False, help="Skip running tests", is_flag=True)
@click.option(
    "--skip-stylescheck", default=False, help="Skip running styles check", is_flag=True
)
@click.option(
    "--types",
    default=False,
    help="Runs Typescript types check (if relevant)",
    is_flag=True,
)
def check(skip_tests, types, skip_stylescheck):

    modified = get_modified_files()

    if len(modified) == 0:
        click.echo(
            colored(
                "Kibbe check only works with uncommited files. Edit some files first",
                "yellow",
            )
        )

    configs = set()
    tests = set()
    styles = set()
    for file in modified:
        path = PurePath(file)
        if path.suffix in [".css", ".scss"]:
            styles.add(file)
        tests.add(find_related_test(file))
        configs.add(find_related_plugin_folder(file))

    tests = list(filter(None, tests))
    configs = list(filter(None, configs))
    styles = list(filter(None, styles))

    fails = []

    # style check
    if not skip_stylescheck and len(styles) > 0:
        click.echo(colored(">> Running styles check", "yellow"))
        process = subprocess.run(["node", "scripts/stylelint.js"] + styles)
        if process.returncode != 0:
            fails.append("Stylelint")

    # types check
    if types and len(configs) > 0:
        click.echo(colored(">> Finding tsconfig.json", "yellow"))
        for config in configs:
            tsconfig = os.path.join(config, "tsconfig.json")
            if os.path.isfile(tsconfig):
                click.echo(
                    colored(">>  - Running type_check for ", "cyan")
                    + colored(tsconfig, "white")
                )
                process = subprocess.run(
                    ["node", "scripts/type_check.js", "--project", tsconfig]
                )
                if process.returncode != 0:
                    fails.append("TS types check")

    # eslint
    if len(modified) > 0:
        click.echo(colored(">> Running eslint", "yellow"))
        process = subprocess.run(["node", "scripts/eslint.js"] + modified)
        if process.returncode != 0:
            fails.append("Eslint checks")

    # tests
    if not skip_tests and len(tests) > 0:
        click.echo(colored(">> Running related tests", "yellow"))
        process = subprocess.run(["node", "scripts/jest.js"] + tests)
        if process.returncode != 0:
            fails.append("Jest tests")

    if len(fails) > 0:
        click.echo("\n ------ \n")
        click.echo(colored(">> Errors found running checks:\n", "red"))
        for fail in fails:
            click.echo("      ❌ - " + str(fail))

    click.echo("kibbe check complete")
