from src.config import get_config, make_config_files
import click

from src.commands.check import check
from src.commands.config import config
from src.commands.ctx import ctx
from src.commands.es import es
from src.commands.fleet import fleet
from src.commands.kibana import kibana
from src.commands.setlicense import setlicense
from src.commands.setmeup import setmeup
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
def cli():
    force_kibana_root()
    config = get_config()
    make_config_files(config)


cli.add_command(setlicense)
cli.add_command(check)
cli.add_command(es)
cli.add_command(kibana)
cli.add_command(setmeup)
cli.add_command(fleet)
cli.add_command(ctx)
cli.add_command(config)
