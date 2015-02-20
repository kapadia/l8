
import os
import sys
import numpy as np
import rasterio as rio
import pyproj

from l8 import BANDS, BAND_INDEX, get_sceneid_from_directory



def get(scene_directory, window, bands=map(lambda x: x['name'], BANDS)):
    """
    Get the spectrum for a given window. A (n x m x 12) ndarray will be returned
    where n, m correspond to the window size. 12 bands will be returned, including
    values from the BQA.
    
    :param scene_directories:
    :param window:
        
        ( (ulx, uly), (lrx, lry) ) format in the image's coordinate system.
        
    :param bands:
    """
    
    ((ulx, uly), (lrx, lry)) = window
    sceneid = get_sceneid_from_directory(scene_directory)
    
    def get_pixels(srcpath, window):
        
        with rio.drivers():
            with rio.open(srcpath, 'r') as src:
                
                y0, x0 = src.index(ulx, uly)
                y1, x1 = src.index(lrx, lry)
                
                xmin, xmax = min(x0, x1), max(x0, x1)
                ymin, ymax = min(y0, y1), max(y0, y1)
                
                window = ((ymin, ymax), (xmin, xmax))
                arr = src.read_band(1, window=((ymin, ymax), (xmin, xmax)))
        
        return arr
    
    spectrum = []
    for band in bands:
        bidx = BAND_INDEX[band]
        
        srcpath = os.path.join(scene_directory, "%s_B%s.TIF" % (sceneid, bidx))
        arr = get_pixels(srcpath, window)
        spectrum.append(arr)
    
    return np.dstack(spectrum)
