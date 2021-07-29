from src.commands.fleet import fleet
import click

from src.commands.check import check
from src.commands.es import es
from src.commands.kibana import kibana
from src.commands.setlicense import setlicense
from src.commands.setmeup import setmeup
from src.config import set_config_file
from src.util import force_kibana_root


@click.group(
    help="""
        Kibbe is a tool that help with common tasks when developing kibana plugins.

        Some subcommands allow you to define a configuration to persist arguments for some
        specific tasks such as running kibana or elasticsearch. This configuration file will
        persis those arguments among all kibana clones and branches.

        You can create a configuration file in your home ~/.kibbe and follow the configuration
        example in the kibbe repository
"""
)
@click.option(
    "--config-file", help="Overwrites the default (~/.kibbe) config file location"
)
def cli(config_file):
    set_config_file(config_file)
    force_kibana_root()


cli.add_command(setlicense)
cli.add_command(check)
cli.add_command(es)
cli.add_command(kibana)
cli.add_command(setmeup)
cli.add_command(fleet)
