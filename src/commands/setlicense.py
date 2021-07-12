import click
import subprocess
from src.util import is_tool

valid_licenses = ['trial', 'basic', 'gold', 'platinum', 'enterprise']


@click.command(help="""This command is a proxy for @pzl setlicense tool
        https://github.com/elastic/pzl-es-tools""")
@click.argument('license_type')
@click.option('-e', '--elastic', default="http://localhost:9200",
              help="Elastic search host. Default to localhost:9200")
@click.option('-p', '--password', default="changeme",
              help="Password to connect. Default to changeme")
@click.option('-u', '--user', default="elastic",
              help="Username to connect. Default to elastic.")
def setlicense(license_type, elastic, password, user):
    license_type = license_type.lower()

    toolInstalled = is_tool('setlicense')

    if not toolInstalled:
        raise click.ClickException("""
            This command is a proxy for @pzl setlicense tool
            setlicense is not installed in your system.
            You can download it from https://github.com/elastic/pzl-es-tools/releases/
            Make it available in your $PATH and try again.
            """)

    subprocess.run(['setlicense', '-u', user, '-p',
                   password, '-e', elastic, license_type])
