
import click
from l8 import spectrum as l8spectrum


@click.group()
def l8():
    pass


@click.command('spectrum')
@click.argument('directory', type=click.Path(exists=True))
@click.option('--longitude')
@click.option('--latitude')
def spectrum(directory, longitude, latitude):
    l8spectrum.extract(directory, longitude, latitude)


l8.add_command(spectrum)