

# Create a probability density map over a single path/row

# Given a stack of L8 scenes in a parent directory,
# analyze the stack of pixels for changes in (blue - red) vs (green - nir)

import os
import re
import pyproj
import rasterio as rio

from sklearn.neighbors import KernelDensity

from l8 import BANDS, SCENE_ID_PATTERN, get_date, spectrum
from l8 import timeseries


# Empirically found for demo.
log_probability_threshold = -3000000


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
    
    sceneids = filter(lambda sid: re.match(SCENE_ID_PATTERN, sid), os.listdir(directory))
    sceneids = timeseries.sort_by_date(sceneids)
    
    srcdirs = map(lambda d: os.path.join(directory, d), sceneids)
    
    # Probe a single image to get metadata (e.g. array shape, projection)
    srcdir = srcdirs[0]
    sceneid = os.path.basename(os.path.normpath(srcdir))
    
    srcpath = os.path.join(srcdir, "%s_B1.TIF" % sceneid)
    
    with rio.drivers():
        with rio.open(srcpath, 'r') as src:
        
            src_proj = pyproj.Proj(src.crs)
            shape = src.shape
            metadata = src.meta.copy()
    
    # Instantiate probability density maps
    # Since 20 time points are used to fit the KDE below, will
    # instantiate the remaining number of files
    with rio.drivers():
        
        for srcdir in srcdirs[20:]:
            
            sid = os.path.basename(os.path.normpath(srcdir))
            date = str(get_date(sid))
            
            with rio.open("%s.tif" % date, 'w', **metadata) as dst:
                pass
    
    # so dumb.
    for j in range(shape[0]):
        for i in range(shape[1]):
            
            lng, lat = pyproj.transform(src_proj, dst_proj, *src.ul(j, i))
            
            # Okay, now have lng/lat to conform to requirement of timeseries
            ts = timeseries.extract(srcdirs, lng, lat)
            kde = KernelDensity(kernel='gaussian', bandwidth=1.0, algorithm='ball_tree')
            
            # For now we just look at b-r vs. g-ir
            bl = ts[:, 1]
            gr = ts[:, 2]
            rd = ts[:, 3]
            ir = ts[:, 4]
            
            blrd = bl - rd
            grir = gr - ir
            
            x = np.vstack((blrd, grir)).transpose()
            
            # Fit about 1/2 the data
            kde.fit(x[0:20])
            
            # Get the scores for the remaining time points
            logprob = kde.score_samples(x[20:])
            
            # Log probabilities aren't good for visualizing within an image
            # so convert to 16bit integer range
            
            probabilities = logprob / log_probability_threshold
            values = (65535 * probabilities).astype(np.uint16)
            
            # Write value to maps
            window = ((j, j+1), (i, i+1))
            for idx, srcdir in enumerate(srcdirs[20:]):
                
                sid = os.path.basename(os.path.normpath(srcdir))
                date = str(get_date(sid))
            
                with rio.open("%s.tif" % date, 'r+') as dst:
                    value = values[idx]
                    src.write_band(1, value, window=window)

