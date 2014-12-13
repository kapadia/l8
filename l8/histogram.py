
import os
import sys
import numpy as np
import rasterio as rio
from scipy.stats import scoreatpercentile


def get_bin_size(arr):
    """
    Freedman-Diaconis' rule.
    
    .. math::
    
        w = 2 * \frac{IQR(x)}{n^{1/3}}
    
    """
    low = scoreatpercentile(arr, 25)
    high = scoreatpercentile(arr, 75)
    
    n = arr.size
    return 2 * (high - low) / np.power(n, 1./3.)


def extract(srcpath):
    """
    Compute the histogram for a given source path.
    
    :param srcpath:
        Path to an image.
    """
    
    with rio.drivers():
        with rio.open(srcpath, "r") as src:
            band = src.read_band(1).ravel()
    
    nbins = get_bin_size(band)
    histogram, bin_edges = np.histogram(band, bins=nbins)
    return bin_edges, histogram
    
    