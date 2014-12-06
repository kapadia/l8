
import click
from l8 import spectrum as l8spectrum
from l8 import timeseries as l8timeseries


@click.group()
def l8():
    pass


@click.command('spectrum')
@click.argument('directory', type=click.Path(exists=True))
@click.option('--longitude')
@click.option('--latitude')
def spectrum(directory, longitude, latitude):
    l8spectrum.extract(directory, longitude, latitude)


@click.command('timeseries')
@click.argument('directories', nargs=-1)
@click.option('--longitude')
@click.option('--latitude')
def timeseries(directories, longitude, latitude):
    l8timeseries.extract(directories, longitude, latitude)


l8.add_command(spectrum)
l8.add_command(timeseries)