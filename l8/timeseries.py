
import os
import sys
import numpy as np
import rasterio as rio
import pyproj

import matplotlib.pyplot as plt
import seaborn as sns

sns.set()


BANDS = {
    "Coastal aerosol": 1,
    "Blue": 2,
    "Green": 3,
    "Red": 4,
    "NIR": 5,
    "SWIR 1": 6,
    "SWIR 2": 7,
    "Panchromatic": 8,
    "Cirrus": 9,
    "TIRS 1": 10,
    "TIRS 2": 11
}


def extract(scene_dirs, lng, lat, bands=[]):
    """
    Extract values from a list of scene directories at a specified location.
    
    :param scene_dir:
        List of paths pointing to Landsat 8 directories. Each path
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
    
    :param lng:
        The longitude to sample in each image.
    
    :param lat:
        The latitude to sample in each image.
        
    :param bands:
        The band(s) for which the timeseries will be extracted. Default is
        an empty list representing all bands.
    """
    
    if len(bands) == 0:
        bands = BANDS.keys()
    
    # Get scene ids from scene directories
    scene_ids = map(lambda x: os.path.basename(os.path.normpath(x)), scene_dirs)
    items = [
        {
            "directory": scene_dirs[index],
            "id": scene_id
        } for index, scene_id in enumerate(scene_ids)
    ]
    
    def get_year(scene_id):
        return scene_id[9:13]
    
    def get_doy(scene_id):
        return scene_id[13:16]
    
    scenes = sorted(items, key=lambda x: (get_year(x["id"]), get_doy(x["id"])))
    
    # Directories are now sorted by date.
    # Proceed to extract pixels from each image.
    
    src_proj = pyproj.Proj(init='epsg:4326')
    
    def get_value_from_band(scene, band):
        
        file_params = { "id": scene["id"], "bidx": BANDS[band] }
        srcpath = os.path.join(
            scene["directory"], "%(id)s_B%(bidx)s.TIF" % file_params
        )
        
        with rio.open(srcpath, "r") as src:
            
            # Get the window associated with the given lng/lat
            
            dst_proj = pyproj.Proj(src.crs)
            x0, y0 = pyproj.transform(src_proj, dst_proj, lng, lat)
            
            # Get the incremented pixel with respect to x/y
            pixel = map(lambda p: p[0] + 1, src.window(x0, y0, x0, y0))
            
            x1, y1 = src.ul(*pixel)
            
            xmin, ymin = min(x0, x1), min(y0, y1)
            xmax, ymax = max(x0, x1), max(y0, y1)
            
            window = src.window(xmin, ymin, xmax, ymax)
            
            return src.read_band(1, window=window)[0][0]
    
    for scene in scenes:
        
        with rio.drivers():
            scene_values = map(lambda band: get_value_from_band(scene, band), bands)
            print scene_values
