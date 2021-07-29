import subprocess
import ipaddress
from termcolor import colored
from src.util import is_es_running, is_kibana_running
import click
import re

_RE_COMBINE_WHITESPACE = re.compile(r"\s+")


@click.command()
@click.option(
    "--snapshot",
    default="docker.elastic.co/beats/elastic-agent:8.0.0-SNAPSHOT",
    help=(
        "If you want to specify a different snapshot. Default to"
        " docker.elastic.co/beats/elastic-agent:8.0.0-SNAPSHOT "
    ),
)
@click.option(
    "--docker-ip",
    help=(
        "The docker host IP. Kibbe will try to autodetect it but you can overwrite it"
        " with this option"
    ),
)
@click.option(
    "--run",
    is_flag=True,
    help=(
        "It will attempt to run fleet server locally. You should have kibana and"
        " elastic search running locally already"
    ),
)
def fleet(run, snapshot, docker_ip):
    """
    Utilities to work with the security solutions fleet server locally
    """
    if run:
        if not is_kibana_running():
            click.echo(
                colored(
                    "Kibana is not running. Kibana must be runnnig to run fleet via"
                    " this helper",
                    "red",
                )
            )
            raise click.ClickException("Kibana not running")
        if not is_es_running():
            click.echo(
                colored(
                    "Elasticsearch is not running. Elasticsearch  must be runnnig to"
                    " run fleet via this helper",
                    "red",
                )
            )
            raise click.ClickException("Elasticsearch not running")

        docker_ip = get_docker_ip(docker_ip)
        click.echo(" - Autodetected docker host ip: " + colored(docker_ip, "blue"))

        docker_command = """docker run \
            --restart no \
            --add-host kibana:{host_ip} \
            --add-host elasticsearch:{host_ip} \
            --add-host fleetserver:127.0.0.1 \
            -e KIBANA_HOST=http://kibana:5601 \
            -e KIBANA_USERNAME=elastic \
            -e KIBANA_PASSWORD=changeme \
            -e ELASTICSEARCH_HOST=http://elasticsearch:9200 \
            -e ELASTICSEARCH_USERNAME=elastic  \
            -e ELASTICSEARCH_PASSWORD=changeme \
            -e FLEET_SERVER_HOST=0.0.0.0 \
            -e FLEET_INSECURE=1 \
            -e KIBANA_FLEET_SETUP=1 \
            -e FLEET_SERVER_ENABLE=1 \
            -e FLEET_SERVER_INSECURE_HTTP=1 \
            -p 8220:8220 {snapshot}
        """.replace(
            "\n", ""
        )
        docker_command = docker_command.format(host_ip=docker_ip, snapshot=snapshot)
        docker_command = _RE_COMBINE_WHITESPACE.sub(" ", docker_command).strip()

        click.echo(" - Will run docker with:\n")
        click.echo(colored(docker_command, "yellow"))
        docker_command = docker_command.split(" ")
        subprocess.run(docker_command)


def get_docker_ip(default_ip):
    ip = default_ip if default_ip and len(default_ip > 0) else "172.17.0.1"
    possible_ip = subprocess.getoutput(
        "docker network inspect bridge -f '{{range .IPAM.Config}}{{.Gateway}}{{end}}'"
    )
    try:
        ipaddress.ip_address(possible_ip)
        ip = possible_ip
    except ValueError:
        pass

    return ip
