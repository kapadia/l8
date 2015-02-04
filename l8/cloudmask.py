
import click
import numpy as np
import rasterio as rio


def get_from_level1(srcpath, dstpath):
    """
    Read the Landsat 8 BQA mask to extract a cloud mask.
    
    http://landsat.usgs.gov/L8QualityAssessmentBand.php
    """
    
    high_confidence_binary = '1100000000000000'
    medium_confidence_binary = '1000000000000000'
    
    high_confidence_integer = int(high_confidence_binary, 2)
    medium_confidence_integer = int(medium_confidence_binary, 2)
    
    with rio.drivers():
        
        with rio.open(srcpath, "r") as src:
            meta = src.meta.copy()
            
            bqa = src.read_band(1)
            
            nodata = np.where(bqa == 1)
            mask1 = np.bitwise_and(high_confidence_integer, bqa)
            mask2 = np.bitwise_and(medium_confidence_integer, bqa)
            
            # TODO: bitwise these operations
            mask1[mask1 != high_confidence_integer] = 65535
            mask1[mask1 == high_confidence_integer] = 0
            
            mask2[mask2 != medium_confidence_integer] = 65535
            mask2[mask2 == medium_confidence_integer] = 0
            
            mask = np.bitwise_or(mask1, mask2)
            mask[nodata] = 0
        
        with rio.open(dstpath, "w", **meta) as dst:
            dst.write_band(1, mask)

def get_from_surface_reflectance(srcpath, dstpath):
    """
    
    Bit | Interpretation
    ----+------------------
    0   | Cirrus cloud
    ----+------------------
    1   | Cloud
    ----+------------------
    2   | Adjacent to cloud
    ----+------------------
    3   | Cloud shadow
    ----+------------------
    4   | Aerosol
    ----+------------------
    5   | Aerosol
    ----+------------------
    6   | Unused
    ----+------------------
    7   | Internal test
    """
    
    

def get_from_cfmask(srcpath, dstpath):
    pass



def get_cloud_mask(srcpath, dstpath):
    """
    Various products exist to decipher clouds in Landsat8 imagery.
    
     * Level 1 BQA
     * SR Cloud Mask
     * CFMask product
    """
    
    # Determine which data product
    pass

if __name__ == '__main__':
    get_mask()