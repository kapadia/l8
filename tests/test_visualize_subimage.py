
import os
import numpy as np
from l8 import visualize
from l8 import spectrum


def test_visualize_subimage():
    
    scenedir = os.path.join(os.path.dirname(__file__), 'fixtures', 'LC80430332013115LGN02')
    lng, lat = -120.10872499999999, 38.90009722222222
    
    # print spectrum.extract(scenedir, lng, lat)
    subimg = visualize.subimage(scenedir, lng, lat, bands=[4, 3, 2])
    assert subimg.dtype == np.uint8
    
