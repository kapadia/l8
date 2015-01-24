
import click
from l8 import spectrum as l8spectrum
from l8 import timeseries as l8timeseries
from l8 import histogram as l8histogram
from l8 import download as l8download


@click.group()
def l8():
    pass


@click.command('spectrum')
@click.argument('directory', type=click.Path(exists=True))
@click.option('--longitude')
@click.option('--latitude')
@click.option('--image', default=None)
def spectrum(directory, longitude, latitude, image):
    print l8spectrum.extract(directory, longitude, latitude, imgpath=image)


@click.command('timeseries')
@click.argument('directories', nargs=-1)
@click.option('--longitude')
@click.option('--latitude')
def timeseries(directories, longitude, latitude):
    for spectrum in l8timeseries.extract(directories, longitude, latitude):
        print spectrum


@click.command('histogram')
@click.argument('srcpath', nargs=1)
def histogram(srcpath):
    bin_edges, histogram = l8histogram.extract(srcpath)
    print list(bin_edges)
    print list(histogram)

@click.command('download')
@click.argument('sceneid')
@click.argument('dstpath', default=None, type=click.Path(exists=True))
@click.argument('bands', nargs=-1, type=click.Choice([ '%d' % i for i in range(1, 12)] + ['BQA', 'MTL']))
def download(sceneid, dstpath, bands):
    l8download.download(sceneid, dstpath, bands)


l8.add_command(spectrum)
l8.add_command(timeseries)
l8.add_command(histogram)
l8.add_command(download)