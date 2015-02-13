
__version__ = '0.1.0'

BANDS = {
    "Coastal aerosol": 1,
    "Blue": 2,
    "Green": 3,
    "Red": 4,
    "NIR": 5,
    "SWIR 1": 6,
    "SWIR 2": 7,
    "Panchromatic": 8,
    "Cirrus": 9,
    "TIRS 1": 10,
    "TIRS 2": 11
}

SCENE_ID_PATTERN = "[A-Z]{2}8(?P<path>[0-9]{3})(?P<row>[0-9]{3})(?P<year>[0-9]{4})(?P<doy>[0-9]{3})[A-Z]{3}[0-9]{2}"