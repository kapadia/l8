
import os
import sys
import numpy as np
import rasterio as rio
import pyproj
from skimage.exposure import rescale_intensity
from PIL import Image

import matplotlib.pyplot as plt
import seaborn as sns

from l8 import BANDS

sns.set()


def extract(scene_directory, longitude, latitude, bands=[], imgpath=None):
    """
    Extract pixel values at a specified geographic location.
    
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
        The band(s) for which the timeseries will be extracted. Default is
        an empty list representing all bands.
    
    :param imgpath:
        Path to an output image of a 101x101 patch surrounding the given longitude/latitude.
    """
    
    if len(bands) == 0:
        bands = BANDS.keys()
    
    padding = 50 if imgpath else 0
    
    scene = {
        "directory": scene_directory,
        "id": os.path.basename(os.path.normpath(scene_directory))
    }
    
    src_proj = pyproj.Proj(init='epsg:4326')
    
    def get_value_from_band(scene, band):
        
        file_params = { "id": scene["id"], "bidx": BANDS[band] }
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
            
            x0, y0 = xc - padding, yc - padding
            x1, y1 = xc + padding + 1, yc + padding + 1
            
            s0, t0 = src.ul(x0, y0)
            s1, t1 = src.ul(x1, y1)
            
            smin, tmin = min(s0, s1), min(t0, t1)
            smax, tmax = max(s0, s1), max(t0, t1)
            
            window = src.window(smin, tmin, smax, tmax)
            band = src.read_band(1, window=window)
            return band
        
    with rio.drivers():
        
        spectral_images = map(lambda band: get_value_from_band(scene, band), bands)
        
        # Create image plots for the patch surrounding the given coordinates
        if imgpath:
            ridx = bands.index("Red")
            gidx = bands.index("Green")
            bidx = bands.index("Blue")
            r, g, b = spectral_images[ridx], spectral_images[gidx], spectral_images[bidx]
            
            img = rescale_intensity(
                np.dstack((r, g, b)),
                in_range=(0, 20000),
                out_range=(0, 255)
            ).astype(np.uint8)
            
            im = Image.fromarray(img)
            im.save(imgpath)
        
        spectral_values = map(lambda img: img[padding][padding], spectral_images)
        return spectral_values
