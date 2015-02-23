
import os
import numpy as np
from l8 import spectrum


def test_spectrum():
    
    datadir = os.path.join(os.path.dirname(__file__), 'fixtures')
    
    expected_path = os.path.join(datadir, 'npy', 'LC80430332013115LGN02-spectrum.npy')
    expected_spectrum = np.load(expected_path)
    
    scene_directory = os.path.join(datadir, 'LC80430332013115LGN02')
    
    window = ((2, 12), (2, 12))
    arr = spectrum.get(scene_directory, window, bands=['Coastal aerosol', 'Blue'])
    
    
    print expected_spectrum
    print "============"
    print arr
    assert np.array_equal(expected_spectrum, arr)
    