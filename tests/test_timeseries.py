
import os
import numpy as np
from l8 import timeseries


expected = [
    'LC80430322013115LGN02',
    'LC80430332013211LGN00',
    'LC80430322013227LGN00',
    'LC80430332013259LGN00',
    'LC80430322013275LGN00',
    'LC80430322013355LGN00',
    'LC80430332013355LGN00',
    'LC80430332014102LGN00',
    'LC80430322014118LGN00',
    'LC80430322014134LGN00',
    'LC80430332014134LGN00',
    'LC80430332014214LGN00',
    'LC80430332014230LGN00',
    'LC80430332014310LGN00',
    'LC80430332014326LGN00',
    'LC80430322014342LGN00',
    'LC80430322015009LGN00',
    'LC80430332015025LGN00'
]


def test_sort_by_date_with_list_of_scene_ids():
    
    scenes = [
        'LC80430322013355LGN00',
        'LC80430322014134LGN00',
        'LC80430322013275LGN00',
        'LC80430322013115LGN02',
        'LC80430332013211LGN00',
        'LC80430332014214LGN00',
        'LC80430322013227LGN00',
        'LC80430322014118LGN00',
        'LC80430332014326LGN00',
        'LC80430332014102LGN00',
        'LC80430332015025LGN00',
        'LC80430332014134LGN00',
        'LC80430332014310LGN00',
        'LC80430332014230LGN00',
        'LC80430322015009LGN00',
        'LC80430332013355LGN00',
        'LC80430322014342LGN00',
        'LC80430332013259LGN00'
    ]
    
    scenes_sorted = timeseries.sort_by_date(scenes)
    assert scenes_sorted == expected


def test_sort_by_date_with_list_of_items():
    
    scenes = [
        {'sceneid': u'LC80430322013355LGN00', 'something': 56},
        {'sceneid': u'LC80430322014134LGN00', 'something': 20},
        {'sceneid': u'LC80430322013275LGN00', 'something': 21},
        {'sceneid': u'LC80430322013115LGN02', 'something': 95},
        {'sceneid': u'LC80430332013211LGN00', 'something': 7},
        {'sceneid': u'LC80430332014214LGN00', 'something': 75},
        {'sceneid': u'LC80430322013227LGN00', 'something': 2},
        {'sceneid': u'LC80430322014118LGN00', 'something': 32},
        {'sceneid': u'LC80430332014326LGN00', 'something': 40},
        {'sceneid': u'LC80430332014102LGN00', 'something': 0},
        {'sceneid': u'LC80430332015025LGN00', 'something': 23},
        {'sceneid': u'LC80430332014134LGN00', 'something': 12},
        {'sceneid': u'LC80430332014310LGN00', 'something': 46},
        {'sceneid': u'LC80430332014230LGN00', 'something': 5},
        {'sceneid': u'LC80430322015009LGN00', 'something': 82},
        {'sceneid': u'LC80430332013355LGN00', 'something': 81},
        {'sceneid': u'LC80430322014342LGN00', 'something': 50},
        {'sceneid': u'LC80430332013259LGN00', 'something': 36}
    ]
    
    scenes_sorted = timeseries.sort_by_date(scenes, accessor=lambda x: x["sceneid"])
    sceneids = map(lambda x: x["sceneid"], scenes_sorted)
    
    assert sceneids == expected
    
    
def test_timeseries():
    
    lng = -120.10872499999999
    lat = 38.90009722222222
    
    expected = np.array([
        [34062, 20473, 20070, 32642, 34807, 5104, 5855, 28332, 5626, 35822, 32081],
        [37562, 14776, 15506, 35895, 36769, 5401, 11218, 33318, 11152, 39184, 42101]
    ])
    
    data_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
    scene_dirs = map(lambda d: os.path.join(data_dir, d), os.listdir(data_dir))
    
    ts = timeseries.extract(scene_dirs, lng, lat)
    
    assert np.array_equal(ts, expected)
    