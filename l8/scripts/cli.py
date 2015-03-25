
import click


@click.group()
def l8():
    pass


@click.command('spectrum')
@click.argument('directory', type=click.Path(exists=True))
@click.option('--longitude', prompt=True)
@click.option('--latitude', prompt=True)
def spectrum(directory, longitude, latitude):
    from l8 import spectrum
    
    print spectrum.extract(directory, longitude, latitude)


@click.command('timeseries')
@click.argument('directories', nargs=-1)
@click.option('--longitude', prompt=True)
@click.option('--latitude', prompt=True)
def timeseries(directories, longitude, latitude):
    from l8 import timeseries
    
    for spectrum in timeseries.extract(directories, longitude, latitude):
        print spectrum


@click.command('histogram')
@click.argument('srcpath', nargs=1)
def histogram(srcpath):
    from l8 import histogram
    
    bin_edges, hist = histogram.extract(srcpath)
    print list(bin_edges)
    print list(hist)


@click.command('download')
@click.argument('sceneid')
@click.argument('dstpath', default=None, type=click.Path(exists=True))
@click.argument('bands', nargs=-1, type=click.Choice([ '%d' % i for i in range(1, 12)] + ['BQA']))
def download(sceneid, dstpath, bands):
    from l8.download import download
    
    download(sceneid, dstpath, bands)


@click.command('cloudmask')
@click.argument('srcpath', type=click.Path(exists=True))
@click.argument('dstpath')
def cloudmask(srcpath, dstpath):
    from l8 import cloudmask
    
    cloudmask.get_from_level1(srcpath, dstpath)


@click.command('cfmask')
@click.argument('srcpath', type=click.Path(exists=True))
@click.argument('dstpath')
def cfmask(srcpath, dstpath):
    from l8 import cfmask
    
    cfmask.get_cloud_mask(srcpath, dstpath)



@click.command('mapbox')
@click.argument('sceneid')
@click.argument('band', type=click.Choice([ '%d' % i for i in range(1, 12)] + ['BQA']))
@click.argument('username')
@click.argument('mapid')
@click.argument('access_token')
def mapbox(sceneid, band, username, mapid, access_token):
    from l8 import mapbox
    
    mapbox.mapbox(sceneid, band, username, mapid, access_token)


l8.add_command(spectrum)
l8.add_command(timeseries)
l8.add_command(histogram)
l8.add_command(download)
l8.add_command(cfmask)
l8.add_command(mapbox)
l8.add_command(cloudmask)
