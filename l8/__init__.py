
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

SCENE_ID_PATTERN = "[A-Z]{2}8(?P<path>[0-9]{3})(?P<row>[0-9]{3})(?P<year>[0-9]{4})(?P<doy>[0-9]{3})[A-Z]{3}[0-9]{2}"

def get_date(sceneid):
    return int(sceneid[9:16])