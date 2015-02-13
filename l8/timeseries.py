
import os
import re
import numpy as np
import rasterio as rio
import pyproj

import matplotlib.pyplot as plt
import seaborn as sns

from l8 import BANDS, SCENE_ID_PATTERN, spectrum

sns.set()


def sort_by_date(items, accessor=None):
    
    def get_date(sceneid):
        return sceneid[9:16]
    
    if accessor is not None:
        
        def key(item):
            sceneid = accessor(item)
            return get_date(sceneid)
    
    else:
        key=get_date
    
    
    return sorted(items, key=key)


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
    
    def is_scene_directory(srcpath):
        sid = os.path.basename(os.path.normpath(srcpath))
        return re.match(SCENE_ID_PATTERN, sid) is not None
    
    print scene_directories
    scene_directories = filter(is_scene_directory, scene_directories)
    print scene_directories
    
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
    
    scenes = sort_by_date(items, accessor=lambda x: x["id"])
    
    # Directories are now sorted by date.
    # Proceed to extract pixels from each image.
    spectra = []
    for scene in scenes:
        spectra.append(
            spectrum.extract(scene["directory"], longitude, latitude, bands=bands)
        )
    return np.array(spectra)
    