
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
                print ((ymin, ymax), (xmin, xmax))
                arr = src.read_band(1, window=((ymin, ymax), (xmin, xmax)))
        
        return arr
    
    spectrum = []
    for band in bands:
        bidx = BAND_INDEX[band]
        
        srcpath = os.path.join(scene_directory, "%s_B%s.TIF" % (sceneid, bidx))
        arr = get_pixels(srcpath, window)
        spectrum.append(arr)
    
    return np.dstack(spectrum)


def extract(scene_directory, longitude, latitude, neighborhood=0):
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
    
    """
    
    scene = {
        "directory": scene_directory,
        "id": os.path.basename(os.path.normpath(scene_directory))
    }
    
    src_proj = pyproj.Proj(init='epsg:4326')
    
    def get_value_from_band(scene, band):
        
        file_params = { "id": scene["id"], "bidx": band['bidx'] }
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
            
            x0, y0 = xc - neighborhood, yc - neighborhood
            x1, y1 = xc + neighborhood + 1, yc + neighborhood + 1
            
            s0, t0 = src.ul(x0, y0)
            s1, t1 = src.ul(x1, y1)
            
            smin, tmin = min(s0, s1), min(t0, t1)
            smax, tmax = max(s0, s1), max(t0, t1)
            
            window = src.window(smin, tmin, smax, tmax)
            return np.median(src.read_band(1, window=window))
    
    
    with rio.drivers():
        spectral_values = np.array(map(lambda band: get_value_from_band(scene, band), BANDS))
        return spectral_values