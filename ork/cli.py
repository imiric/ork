import click


@click.group(context_settings={'auto_envvar_prefix': 'ORK'})
def cli():
    pass


@cli.command(help='Start the ork server.')
def start():
    pass
