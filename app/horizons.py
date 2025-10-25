import httpx
import urllib
import re
from dotenv import load_dotenv
from os import environ as env


load_dotenv()


URL = "https://ssd.jpl.nasa.gov/api/horizons.api"

# OBSERVER LOCATION
E_LON = env["E_LON"] #degrees
LAT = env["LAT"] #degrees
ALT = env["ALT"] #km, with respect to the reference ellipsoid, not “mean sea level”. convert location to alt: https://geographiclib.sourceforge.io/cgi-bin/GeoidEval

# TIME RANGE
START_TIME = "2025-10-25 18:00" #YYYY-MM-DD HH:MM:SS.fff
STOP_TIME = "2025-10-26 09:00" #YYYY-MM-DD HH:MM:SS.fff

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

OBJECT_TO_SEARCH = SOLAR_SYSTEM["Uranus"]

# REQUEST PARAMS
params = {
    "format": "json",
    "COMMAND": f"'{OBJECT_TO_SEARCH}'", #799 is Uranus
    "OBJ_DATA": "'NO'",
    "MAKE_EPHEM": "'YES'",
    "EPHEM_TYPE": "'OBSERVER'",
    "CENTER": "'coord'",
    "SITE_COORD": f"'{E_LON},{LAT},{ALT}'",
    "START_TIME": f"'{START_TIME}'",
    "STOP_TIME": f"'{STOP_TIME}'",
    "STEP_SIZE": "'1 h'",
    "QUANTITIES": "'2,4'",
    "TIME_ZONE": "'+02:00'"
}

encoded_params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote, safe=",@'")

result = {}

def download_data():
    global result
    r = httpx.get(f"{URL}?{encoded_params}")
    result = r.json()
    return

download_data()

parsed = re.search(r"\$\$SOE(.*?)\$\$EOE", result["result"], re.DOTALL)
planet = re.search(r"Target body name:(.*?)\(", result["result"])

print(result["signature"])
print("")
print(planet.group(1))
print(parsed.group(1))
