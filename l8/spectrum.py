
import os
import sys
import numpy as np
import rasterio as rio
import pyproj
from scipy.ndimage.interpolation import zoom

from l8 import BANDS, BAND_INDEX, get_sceneid_from_directory



def get(scene_directory, window, bands=map(lambda x: x['name'], BANDS)):
    """
    Get the spectrum for a given window. A (n x m x 12) ndarray will be returned
    where n, m correspond to the window size. 12 bands will be returned, including
    values from the BQA.
    
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
        
        ((row_start, row_stop), (col_start, col_stop))
    
    :param bands:
    
        List of bands to extract. Bands should be specified by their name:
        
        Coastal aerosol, Blue, Green, Red, NIR, SWIR 1, SWIR 2, Panchromatic, Cirrus, TIRS 1, TIRS 2, BQA
    """
    
    sceneid = get_sceneid_from_directory(scene_directory)
    
    def get_pixels(srcpath, window):
        
        with rio.drivers():
            with rio.open(srcpath, 'r') as src:
                arr = src.read_band(1, window=window)
        
        return arr
    
    spectrum = []
    for band in bands:
        bidx = BAND_INDEX[band]
        
        srcpath = os.path.join(scene_directory, "%s_B%s.TIF" % (sceneid, bidx))
        arr = get_pixels(srcpath, window)
        spectrum.append(zoom(arr, 0.20))
    
    return np.dstack(spectrum)
