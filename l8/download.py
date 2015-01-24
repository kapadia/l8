
import os
import re
from boto.s3.connection import S3Connection

BUCKET = 'landsat-pds'


def get_s3_path(sceneid):
    
    pattern = "[A-Z]{2}8(?P<path>[0-9]{3})(?P<row>[0-9]{3})(?P<year>[0-9]{4})(?P<doy>[0-9]{3})[A-Z]{3}[0-9]{2}"
    match = re.match(pattern, sceneid)
    
    path = match.group('path')
    row = match.group('row')
    
    s3path = os.path.join('L8', path, row, sceneid)
    return s3path


def download(sceneid, dstpath, bands):
    s3path = get_s3_path(sceneid)
    s3keys = map(lambda b: os.path.join(s3path, sceneid + "_B%s.TIF" % b), bands)
    
    conn = S3Connection()
    bucket = conn.get_bucket(BUCKET, validate=False)
    
    for s3key in s3keys:
        key = bucket.get_key(s3key)
        if key is None: continue
        
        fpath = os.path.join(dstpath, os.path.basename(s3key))
        key.get_contents_to_filename(fpath)
        