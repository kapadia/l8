
import os
import numpy as np
from l8 import spectrum

# TODO: Pack up as npy file
expected = np.array([
    [
        [31094, 33338],
        [30236, 31822],
        [21234, 21355],
        [21818, 23489],
        [25623, 26648],
        [27213, 28806],
        [29610, 31389],
        [25774, 26410],
        [25462, 26162],
        [33379, 34804]
    ],

    [
        [26996, 27187],
        [21153, 21287],
        [20428, 20438],
        [22677, 22468],
        [24833, 25173],
        [30085, 31083],
        [25651, 25400],
        [23106, 22781],
        [24966, 26230],
        [27320, 28039]
    ],

    [
        [16346, 16657],
        [18568, 18445],
        [22171, 22162],
        [28189, 29936],
        [33638, 35045],
        [32810, 34365],
        [28430, 30580],
        [24724, 26159],
        [25213, 26281],
        [31493, 32408]
    ],

    [
        [16771, 16777],
        [14908, 15569],
        [17805, 18861],
        [26974, 28214],
        [30747, 32078],
        [30086, 31393],
        [33897, 35334],
        [33141, 34343],
        [32102, 32843],
        [33351, 34456]
    ],

    [
        [20618, 20616],
        [24809, 25556],
        [20792, 20768],
        [26435, 27769],
        [22682, 23137],
        [24544, 25288],
        [34441, 36168],
        [36103, 37682],
        [35496, 37332],
        [34546, 36225]
    ],

    [
        [20163, 20518],
        [26501, 27467],
        [24152, 25768],
        [26513, 26568],
        [28031, 28627],
        [26416, 27405],
        [34176, 35547],
        [36632, 38135],
        [35530, 37014],
        [34724, 36264]
    ],

    [
        [19747, 20805],
        [24974, 25337],
        [25640, 26150],
        [25514, 26478],
        [32053, 33517],
        [31878, 33359],
        [35537, 37171],
        [36335, 37968],
        [34366, 36246],
        [34965, 36544]
    ],

    [
        [16025, 15567],
        [18780, 19398],
        [21632, 22694],
        [23882, 24257],
        [29236, 30351],
        [34070, 35536],
        [35339, 37076],
        [32626, 32985],
        [31456, 32672],
        [32729, 34139]
    ],

    [
        [19045, 19129],
        [20655, 20727],
        [20356, 20745],
        [19968, 20494],
        [26420, 27584],
        [32120, 33390],
        [34283, 36039],
        [27891, 29913],
        [24314, 24765],
        [30197, 31465]
    ],

    [
        [21025, 22377],
        [21594, 22182],
        [24474, 25653],
        [21946, 22700],
        [23282, 23732],
        [26584, 28401],
        [30064, 31119],
        [30471, 31594],
        [19585, 20667],
        [27084, 27948]
    ]
])

def test_spectrum():
    
    datadir = os.path.join(os.path.dirname(__file__), 'fixtures')
    
    scene_directory = os.path.join(datadir, 'LC80430332013115LGN02')
    
    ulx, uly = 750435.000, 4309965.000
    lrx, lry = 750735.000, 4309665.000
    window = ((ulx, uly), (lrx, lry))
    
    arr = spectrum.get(scene_directory, window, bands=['Coastal aerosol', 'Blue'])
    assert np.array_equal(expected, arr)
    