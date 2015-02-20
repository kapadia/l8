
import os
import re
import numpy as np
import rasterio as rio
import pyproj

import matplotlib.pyplot as plt
import seaborn as sns

from l8 import BANDS, SCENE_ID_PATTERN, get_date, spectrum, get_sceneid_from_directory

sns.set()



def sort_by_date(items, accessor=None):
    
    if accessor is not None:
        
        def key(item):
            sceneid = accessor(item)
            return get_date(sceneid)
    
    else:
        key=get_date
    
    return sorted(items, key=key)


def is_scene_directory(srcpath):
    sid = os.path.basename(os.path.normpath(srcpath))
    return re.match(SCENE_ID_PATTERN, sid) is not None


def get(scene_directories, window, bands=None):
    """
    
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
    
    :param window:
        
        ( (ulx, uly), (lrx, lry) ) format in the image's coordinate system.
    
    :param bands:
    
        List of bands to extract. Bands should be specified by their name:
        
        Coastal aerosol, Blue, Green, Red, NIR, SWIR 1, SWIR 2, Panchromatic, Cirrus, TIRS 1, TIRS 2, BQA

    """
    
    # Filter out directories that do not appear to be a scene directory
    scene_directories = filter(is_scene_directory, scene_directories)
    
    # Sort directories by date
    scene_directories = sort_by_date(scene_directories, accessor=get_sceneid_from_directory)
    
    # Get a sorted list of dates
    sceneids = map(get_sceneid_from_directory, scene_directories)
    dates = map(get_date, sceneids)
    
    ts = []
    for scene_directory in scene_directories:
        ts.append(
            spectrum.get(scene_directory, window, bands)
        )
    
    return (dates, np.array(ts))


def extract(scene_directories, longitude, latitude, neighborhood=0):
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
    
    scene_directories = filter(is_scene_directory, scene_directories)
    
    # Get scene ids from scene directories
    scene_ids = map(lambda x: os.path.basename(os.path.normpath(x)), scene_directories)
    
    items = [
        {
            "directory": scene_directories[index],
            "id": scene_id
        } for index, scene_id in enumerate(scene_ids)
    ]
    
    scenes = sort_by_date(items, accessor=lambda x: x["id"])
    dates = np.array(map(get_date, scene_ids))
    
    # Directories are now sorted by date.
    # Proceed to extract pixels from each image.
    ts = []
    for scene in scenes:
        ts.append(
            spectrum.get(scene["directory"], longitude, latitude, neighborhood=neighborhood)
        )
    
    return (dates, np.array(ts))
    