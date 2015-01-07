
import os
import sys
import numpy as np
import rasterio as rio
from scipy.stats import scoreatpercentile


def get_cloud_mask(srcpath, dstpath):
    """
    Create a mask based on values that CFMask has deemed cloud/shadow.
    """
    
    CLOUD = 2
    SHADOW = 4
    
    with rio.drivers():
        with rio.open(srcpath) as src:
            band = src.read_band(1)
            meta = src.meta.copy()
    
    mask = np.zeros(band.shape).astype(np.uint8)
    mask[np.where(band == CLOUD)] = 255
    
    with rio.drivers():
        with rio.open(dstpath, "w", **meta) as dst:
            dst.write_band(1, mask)