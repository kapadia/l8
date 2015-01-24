
import os
import json
import requests
from l8.download import get_s3_path


API = 'https://api-core-patch.tilestream.net/uploads/v1/%s?access_token=%s'
# API = 'https://api.tiles.mapbox.com/uploads/v1/%s?access_token=%s'


def to_public_uri(s3path):
    return "https://landsat-pds.s3.amazonaws.com/" + s3path


def mapbox(sceneid, band, username, mapid, access_token):
    """
    Transfer a Landsat scene to Mapbox.com.
    
    :param sceneid:
    :param band:
    :param username:
    :param mapid:
    :param access_token:
    """
    
    url = API % (username, access_token)
    
    s3path = os.path.join(get_s3_path(sceneid), sceneid + "_B%s.TIF" % band)
    s3url = to_public_uri(s3path)
    
    payload = {
        "data": "%s.%s" % (username, mapid),
        "url": s3url,
        "patch": None
    }
    headers = { 'content-type': 'application/json' }
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    
    print url
    print payload
    print r
    print r.text