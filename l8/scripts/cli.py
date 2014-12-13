
import click
from l8 import spectrum as l8spectrum
from l8 import timeseries as l8timeseries
from l8 import histogram as l8histogram


@click.group()
def l8():
    pass


@click.command('spectrum')
@click.argument('directory', type=click.Path(exists=True))
@click.option('--longitude', prompt=True)
@click.option('--latitude', prompt=True)
def spectrum(directory, longitude, latitude):
    print l8spectrum.extract(directory, longitude, latitude)


@click.command('timeseries')
@click.argument('directories', nargs=-1)
@click.option('--longitude', prompt=True)
@click.option('--latitude', prompt=True)
def timeseries(directories, longitude, latitude):
    for spectrum in l8timeseries.extract(directories, longitude, latitude):
        print spectrum


@click.command('histogram')
@click.argument('srcpath', nargs=1)
def histogram(srcpath):
    bin_edges, histogram = l8histogram.extract(srcpath)
    print list(bin_edges)
    print list(histogram)


l8.add_command(spectrum)
l8.add_command(timeseries)
l8.add_command(histogram)
