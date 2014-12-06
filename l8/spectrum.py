
import os
import sys
import numpy as np
import rasterio as rio
import pyproj

import matplotlib.pyplot as plt
import seaborn as sns

from l8 import BANDS

sns.set()


def extract(scene_directory, longitude, latitude, bands=[]):
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
    """
    
    if len(bands) == 0:
        bands = BANDS.keys()
    
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
            
            dst_proj = pyproj.Proj(src.crs)
            x0, y0 = pyproj.transform(src_proj, dst_proj, longitude, latitude)
            
            # Get the incremented pixel with respect to x/y
            try:
                pixel = map(lambda p: p[0] + 1, src.window(x0, y0, x0, y0))
            except ValueError:
                return np.nan
            
            x1, y1 = src.ul(*pixel)
            
            xmin, ymin = min(x0, x1), min(y0, y1)
            xmax, ymax = max(x0, x1), max(y0, y1)
            
            window = src.window(xmin, ymin, xmax, ymax)
            
            return src.read_band(1, window=window)[0][0]
        
    with rio.drivers():
        scene_values = map(lambda band: get_value_from_band(scene, band), bands)
        print scene_values
