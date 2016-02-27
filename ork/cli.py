import click

from .config import load_config


@click.group(context_settings={'auto_envvar_prefix': 'ORK'})
def cli():
    pass


@cli.command(help='Start the ork server.')
@click.option('--config', help='Configuration file path')
def start(config):
    config = load_config(config)
    print(config)
