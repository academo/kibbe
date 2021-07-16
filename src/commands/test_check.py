import click
from click.testing import CliRunner


@click.command()
@click.argument("name")
def hello(name):
    click.echo(f"Hello {name}!")


def test_hello_world():
    runner = CliRunner()
    result = runner.invoke(hello, ["Peter"])
    assert result.exit_code == 0
    assert result.output == "Hello Peter!\n"
