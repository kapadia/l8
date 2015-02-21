
import os

__version__ = '0.1.0'


BANDS = [
    { "name": "Coastal aerosol", "bidx": 1 },
    { "name": "Blue", "bidx": 2 },
    { "name": "Green", "bidx": 3 },
    { "name": "Red", "bidx": 4 },
    { "name": "NIR", "bidx": 5 },
    { "name": "SWIR 1", "bidx": 6 },
    { "name": "SWIR 2", "bidx": 7 },
    { "name": "Panchromatic", "bidx": 8 },
    { "name": "Cirrus", "bidx": 9 },
    { "name": "TIRS 1", "bidx": 10 },
    { "name": "TIRS 2", "bidx": 11 },
    { "name": "BQA", "bidx": "QA" },
]

BAND_INDEX = {
    "Coastal aerosol": "1",
    "Blue": "2",
    "Green": "3",
    "Red": "4",
    "NIR": "5",
    "SWIR 1": "6",
    "SWIR 2": "7",
    "Panchromatic": "8",
    "Cirrus": "9",
    "TIRS 1": "10",
    "TIRS 2": "11",
    "BQA": "QA"
}

SCENE_ID_PATTERN = "[A-Z]{2}8(?P<path>[0-9]{3})(?P<row>[0-9]{3})(?P<year>[0-9]{4})(?P<doy>[0-9]{3})[A-Z]{3}[0-9]{2}"

def get_date(sceneid):
    return int(sceneid[9:16])

def get_sceneid_from_directory(scene_directory):
    return os.path.basename(os.path.normpath(scene_directory))
    
def is_scene_directory(srcpath):
    sid = os.path.basename(os.path.normpath(srcpath))
    return re.match(SCENE_ID_PATTERN, sid) is not None