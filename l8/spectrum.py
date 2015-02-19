
import os
import sys
import numpy as np
import rasterio as rio
import pyproj

from l8 import BANDS


def extract(scene_directory, longitude, latitude, bands=[], neighborhood=0):
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
        bands = map(lambda d: d['name'], BANDS)
    
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