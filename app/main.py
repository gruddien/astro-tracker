from datetime import datetime
import horizons
import weather
from dotenv import load_dotenv
from os import environ as env
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from enum import Enum


load_dotenv()

# OBSERVER LOCATION
E_LON = env["E_LON"] #degrees
LAT = env["LAT"] #degrees
ALT = env["ALT"] #km, with respect to the reference ellipsoid, not “mean sea level”. convert location to alt: https://geographiclib.sourceforge.io/cgi-bin/GeoidEval

class SolarObjects(Enum):
    sun = "Sun"
    mercury = "Mercury"
    venus = "Venus"
    mars = "Mars"
    jupiter = "Jupiter"
    saturn = "Saturn"
    uranus = "Uranus"
    neptune = "Neptune"
    pluto = "Pluto"

app = FastAPI()

@app.get("/")
def root():
    print("Root called")
    weather_data = weather.get_data(LAT, E_LON)
    day = datetime.now().date()
    return  day, weather_data["current"]

@app.get("/solar/{obj}", response_class=HTMLResponse)
def get_data(obj: SolarObjects):
    print("Get solar object called")
    data = horizons.request_data(object=obj.value, site_coord=f"{E_LON},{LAT},{ALT}")
    formatted_data = str(data[2]).replace("\n", "<br>")
    return f"<h2>{obj.value}</h2><pre>{formatted_data}</pre>"