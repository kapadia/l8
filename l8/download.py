
import os
import re
from boto.s3.connection import S3Connection

from l8 import SCENE_ID_PATTERN

BUCKET = 'landsat-pds'


def get_s3_path(sceneid):
    """
    Get the path on S3 for a given Landsat 8 scene id.
    
    :param sceneid:
        Landsat 8 scene id
    """
    
    match = re.match(SCENE_ID_PATTERN, sceneid)
    
    path = match.group('path')
    row = match.group('row')
    
    return os.path.join('L8', path, row, sceneid)


def download(sceneid, dstpath, bands):
    """
    Download Landsat 8 data from a stash on S3.
    
    :param sceneid:
        Landsat 8 scene id
    
    :param dstpath:
        Local path where files will be downloaded.
        
    :param bands:
        List of bands that will be downloaded. Must be [1 ... 11, BQA]
    """
    
    s3path = get_s3_path(sceneid)
    s3keys = map(lambda b: os.path.join(s3path, sceneid + "_B%s.TIF" % b), bands)
    
    conn = S3Connection()
    bucket = conn.get_bucket(BUCKET, validate=False)
    
    for s3key in s3keys:
        key = bucket.get_key(s3key)
        if key is None: continue
        
        fpath = os.path.join(dstpath, os.path.basename(s3key))
        key.get_contents_to_filename(fpath)
        