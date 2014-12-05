
import click
from l8 import timeseries


@click.group()
def l8():
    pass


@click.command('spectrum')
@click.argument('directory', type=click.Path(exists=True))
@click.option('--longitude')
@click.option('--latitude')
def spectrum(directory, longitude, latitude):
    timeseries.extract([directory], longitude, latitude)


l8.add_command(spectrum)
