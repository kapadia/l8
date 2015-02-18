
import os
import numpy as np
import rasterio as rio
import pyproj
from skimage.exposure import rescale_intensity

import l8
from l8 import BANDS

import matplotlib.pyplot as plt
import seaborn as sns


def subimage(scene_directory, longitude, latitude, bands=[4, 3, 2], size=50):
    """
    Get a subimage around the given coordinates to visualize in a notebook.
    
    :param scene_directory:
        Directory point to Landsat 8 images. The path is 
        is assumed to be composed of a Landsat8 scene id.
        
        LXSPPPRRRYYYYDDDGSIVV
        L = Landsat
        X = Sensor
        S = Satellite
        PPP = WRS path
        RRR = WRS row
        YYYY = Year
        DDD = Julian day of year
        GSI = Ground station identifier
        VV = Archive version number
    
    :param longitude:
        The longitude to sample in each image.
    
    :param latitude:
        The latitude to sample in each image.
        
    :param bands:
        The bands that will be used for the false color image.
    """
    
    scene = {
        "directory": scene_directory,
        "id": os.path.basename(os.path.normpath(scene_directory))
    }
    
    src_proj = pyproj.Proj(init='epsg:4326')
    
    def get_value_from_band(scene, bidx):
        
        file_params = { "id": scene["id"], "bidx": bidx }
        srcpath = os.path.join(
            scene["directory"], "%(id)s_B%(bidx)s.TIF" % file_params
        )
        
        with rio.open(srcpath, "r") as src:
            
            # Get the window associated with the given longitude/latitude
            
            # Transform from longitude/latitude to the projection of the image
            dst_proj = pyproj.Proj(src.crs)
            s, t = pyproj.transform(src_proj, dst_proj, longitude, latitude)
            
            # Get the center pixel corresponding to s/t
            try:
                xc, yc = src.index(s, t)
            except ValueError:
                return np.nan
            
            x0, y0 = xc - size, yc - size
            x1, y1 = xc + size + 1, yc + size + 1
            
            s0, t0 = src.ul(x0, y0)
            s1, t1 = src.ul(x1, y1)
            
            smin, tmin = min(s0, s1), min(t0, t1)
            smax, tmax = max(s0, s1), max(t0, t1)
            
            window = src.window(smin, tmin, smax, tmax)
            band = src.read_band(1, window=window)
            
            return band
            
    with rio.drivers():
        subimg = np.dstack(
            map(lambda band: get_value_from_band(scene, band), bands)
        )
    
    return rescale_intensity(subimg, in_range=(0, 20000), out_range=(0, 255)).astype(np.uint8)
    

def timepointKDE(srcpaths, lng, lat, timeseries, timepoint):
    """
    
    :param srcpaths:
        List of Landsat scene directories.
    
    :param lng:
        Longitude
        
    :param lat:
        Latitude
        
    :param timeseries:
        Numpy array returned by l8.timeseries.extract
    
    :param timepoint:
        A date in the format YYYYDOY corresponding to a point in the timeseries.
    
    """
    
    # Sort directories by date
    srcpaths = l8.timeseries.sort_by_date(srcpaths, accessor=lambda p: os.path.basename(os.path.normpath(p)))
    
    # Get the scene path corresponding to the given timepoint
    idx = [i for i, srcpath in enumerate(srcpaths) if str(timepoint) in srcpath][0]
    srcpath = srcpaths[idx]
    
    f, axes = plt.subplots(2, 2)
    axes_iter = axes.flat
    
    ax = axes_iter.next()
    subimg = subimage(srcpath, lng, lat, size=100)
    ax.imshow(subimg)
    ax.grid(False)
    
    b = timeseries[:, 1]
    g = timeseries[:, 2]
    r = timeseries[:, 3]
    ir = timeseries[:, 4]
    
    ax = axes_iter.next()
    sns.kdeplot(b, r, shade=True, cut=5, ax=ax)
    ax.scatter(b[idx], r[idx])
    
    ax = axes_iter.next()
    sns.kdeplot(g, ir, shade=True, cut=5, ax=ax)
    ax.scatter(g[idx], ir[idx])
    
    ax = axes_iter.next()
    sns.kdeplot(b - r, g - ir, shade=True, cut=5, ax=axes_iter.next())
    ax.scatter(b[idx] - r[idx], g[idx] - ir[idx])
    
    plt.tight_layout()

