import httpx
import urllib
from dotenv import load_dotenv
from os import environ as env

load_dotenv()

URL = "https://ssd.jpl.nasa.gov/api/horizons.api"
E_LON = env["E_LON"] #degrees
LAT = env["LAT"] #degrees
ALT = env["ALT"] #km, with respect to the reference ellipsoid, not “mean sea level”. convert location to alt: https://geographiclib.sourceforge.io/cgi-bin/GeoidEval

params = {
    "format": "json",
    "COMMAND": "'799'", #799 is Uranus
    "OBJ_DATA": "'NO'",
    "MAKE_EPHEM": "'YES'",
    "EPHEM_TYPE": "'OBSERVER'",
    "CENTER": "'coord'",
    "SITE_COORD": f"'{E_LON},{LAT},{ALT}'",
    "START_TIME": "'2025-10-22'",
    "STOP_TIME": "'2025-10-27'",
    "STEP_SIZE": "'1 d'",
    "QUANTITIES": "'2,4'"
}

encoded_params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote, safe=",@'")

result = ""

def download_data():
    global result
    r = httpx.get(f"{URL}?{encoded_params}")
    result = r.json()
    return

download_data()

print(result["result"])
