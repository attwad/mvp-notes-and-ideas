"""This package contains a geocoder based on the former sheets VLOOKUP impl.

It uses a dump of the geo_admin sheet to csv to load all the locations in
memory and allows for fast access.
"""

from typing import NamedTuple, Dict
import csv
import logging

class Geocode(NamedTuple):
    """Geocode contains geocoding information about a location."""
    lat: float
    lng: float
    geo_resolution: str
    country_new: str
    admin_id: int
    location: str
    admin3: str
    admin2: str
    admin1: str

_INPUT_ROW = 0
_LAT_ROW = 1
_LNG_ROW = 2
_GEO_RESOLUTION_ROW = 3
_LOCATION_ROW = 4
_ADMIN3_ROW = 5
_ADMIN2_ROW = 6
_ADMIN1_ROW = 7
_COUNTRY_NEW_ROW = 8
_ADMIN_ID_ROW = 9

class CSVGeocoder:
    def __init__(self, init_csv_path: str):
        # Build a giant map of concatenated strings for fast lookup.
        # Do not try to be smart, just replicate whatever the spreadsheet was
        # doing. Data's so small it can all fit in memory and allow for fast
        # lookups.
        
        self.geocodes :Dict[str, Geocode] = {}
        with open(init_csv_path, newline="") as csvfile:
            # Delimiter is \t instead of , because google spreadsheets were
            # exporting lat,lng with commas, leading to an invalid number of
            # columns per row :(
            rows = csv.reader(csvfile, delimiter="\t")
            for i, row in enumerate(rows):
                # Some admin_ids are not set (or set to "TBD") which can't parse
                # nicely, default to 0 for those.
                try:
                    admin_id = int(row[_ADMIN_ID_ROW])
                except ValueError:
                    admin_id = 0
                geocode = Geocode(
                    float(row[_LAT_ROW]),
                    float(row[_LNG_ROW]),
                    row[_GEO_RESOLUTION_ROW],
                    row[_COUNTRY_NEW_ROW],
                    admin_id,
                    row[_LOCATION_ROW],
                    row[_ADMIN3_ROW],
                    row[_ADMIN2_ROW],
                    row[_ADMIN1_ROW])
                self.geocodes[row[_INPUT_ROW].lower()] = geocode
        logging.info("Loaded %d geocodes from %s", len(self.geocodes), init_csv_path)
        

    def Geocode(self, city :str="", province :str="", country :str="") -> Geocode:
        """Geocode matches the given locations to their Geocode information
        
        At least one of city, province, country must be set.

        Returns:
            None if no exact match were found.
        """
        key = f"{city};{province};{country}".lower()
        return self.geocodes.get(key)