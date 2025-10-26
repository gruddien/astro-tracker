
'''
Horizons API provides access to key solar system data and production of ephemerides for solar system objects:
asteroids, comets, planetary satellites, 8 planets (+ Pluto), the Sun, L1, L2, select spacecraft, and system barycenters.
'''

import httpx
import urllib
import re
from dotenv import load_dotenv
from os import environ as env

URL = "https://ssd.jpl.nasa.gov/api/horizons.api"

# SOLAR SYSTEM OBJECTS
SOLAR_SYSTEM = {
    "Sun": 10,
    "Mercury": 199,
    "Venus": 299,
    "Earth": 399,
    "Mars": 499,
    "Jupiter": 599,
    "Saturn": 699,
    "Uranus": 799,
    "Neptune": 899,
    "Pluto": 999
}

def request_data(
        object: str = "Uranus",
        obj_data: str = "NO",
        make_ephem: str = "YES",
        site_coord: str = "18.55,53.09,0.029", #Torun Observatory
        start_time: str = "2025-10-25 18:00",
        stop_time: str = "2025-10-26 18:00",
        step_size: str = "1 h",
        time_zone: str = "+01:00"
        ):
    
    '''Request data about Object from NASA HORIZONS API.
    
    Data is in huge text file, even if JSON format is requested. It has to be parsed using (name of the function).
    
    Args:
    - object: e.g. Mars
    - obj_data: NO/YES, for object data, e.g. mass
    - make_ephem: NO/YES, for ephemerides of object
    - site_coord: coordinates of observer on Earth, "e-lon,lat,alt(not msl)"
    - start_time: beginning of ephem calc
    - stop_time: end of ephem calc
    - step_size: step time of ephem calc
    - time_zone: time zone
    '''

    params = {
    "format": "json",
    "COMMAND": f"'{SOLAR_SYSTEM[object]}'", #799 is Uranus
    "OBJ_DATA": f"'{obj_data}'", #NO/YES
    "MAKE_EPHEM": f"'{make_ephem}'", #NO/YES
    "EPHEM_TYPE": "'OBSERVER'",
    "CENTER": "'coord'",
    "SITE_COORD": f"'{site_coord}'", #e.g. 18.55,53.09,0.029 - e-lon, lat, alt (not msl)
    "START_TIME": f"'{start_time}'", #YYYY-MM-DD HH:MM:SS.fff
    "STOP_TIME": f"'{stop_time}'", #YYYY-MM-DD HH:MM:SS.fff
    "STEP_SIZE": f"'{step_size}'",
    "QUANTITIES": "'2,4'",
    "TIME_ZONE": f"'{time_zone}'"
    }

    encoded_params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote, safe=",@'")

    request = httpx.get(f"{URL}?{encoded_params}")
    response = request.json()

    parsed = re.search(r"\$\$SOE(.*?)\$\$EOE", response["result"], re.DOTALL)
    planet = re.search(r"Target body name:(.*?)\(", response["result"])

    return response, planet.group(1), parsed.group(1), 


if __name__ == "__main__":

    load_dotenv()

    # OBSERVER LOCATION, USED IF HORIZONS.PY IS LAUNCHED AS SINGULAR FILE
    E_LON = env["E_LON"] #degrees
    LAT = env["LAT"] #degrees
    ALT = env["ALT"] #km, with respect to the reference ellipsoid, not “mean sea level”. convert location to alt: https://geographiclib.sourceforge.io/cgi-bin/GeoidEval

    data = request_data(object="Mars", site_coord=f"{E_LON},{LAT},{ALT}")

    print(data[1])
    print(data[2])
    input("Enter to close...")
