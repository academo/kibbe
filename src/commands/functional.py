import click


@click.group(help="""Utilities for functional tests""")
def functional():
    pass


@functional.command(help="""List the available projects to run functional tests""")
def list():
    print("im listing stuff")
