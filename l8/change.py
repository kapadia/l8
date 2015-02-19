

# Create a probability density map over a single path/row

# Given a stack of L8 scenes in a parent directory,
# analyze the stack of pixels for changes in (blue - red) vs (green - nir)

import os
import pyproj
import rasterio as rio

from l8 import BANDS, SCENE_ID_PATTERN, get_date, spectrum
from l8 import timeseries



def is_scene_directory(srcpath):
    sid = os.path.basename(os.path.normpath(srcpath))
    return re.match(SCENE_ID_PATTERN, sid) is not None


def detect_change(directory):
    """
    :param directory:
        Parent directory containing various L8 scenes corresponding to the same path/row.
    """
    
    # Iterate over all pixels in image. Ugh ...
    
    dst_proj = pyproj.Proj(init='epsg:4326')
    
    scene_directories = map(lambda d: os.path.join(directory, d), os.listdir(directory))
    
    # Probe a single image to get metadata (e.g. array shape, projection)
    srcdir = scene_directories[0]
    sceneid = os.path.basename(os.path.normpath(srcdir))
    
    srcpath = os.path.join(srcdir, "%s_B1.TIF" % sceneid)
    scene_directory = os.path.join(directory, os.listdir(directory)[0])
    
    with rio.drivers():
        with rio.open(srcpath, 'r') as src:
        
            src_proj = pyproj.Proj(src.crs)
            shape = src.shape
    
    # so dumb.
    for j in range(shape[0]):
        for i in range(shape[1]):
            
            lng, lat = pyproj.transform(src_proj, dst_proj, *src.ul(j, i))
            
            # Okay, now have lng/lat to conform to requirement of timeseries
            ts = timeseries(scene_directories, lng, lat)
            
            print ts
            
            
                    
                    
                    
                    
    
    
    
    