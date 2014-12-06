
import os
import sys
import numpy as np
import rasterio as rio
import pyproj

import matplotlib.pyplot as plt
import seaborn as sns

from l8 import BANDS, spectrum

sns.set()


def extract(scene_directories, longitude, latitude, bands=[]):
    """
    Extract values from a list of scene directories at a specified location.
    
    :param scene_directories:
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
    
    # Get scene ids from scene directories
    scene_ids = map(lambda x: os.path.basename(os.path.normpath(x)), scene_directories)
    items = [
        {
            "directory": scene_directories[index],
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
    
    for scene in scenes:
        spectrum.extract(scene["directory"], longitude, latitude, bands=bands)
    