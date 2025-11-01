import httpx
from datetime import datetime
from dotenv import load_dotenv
from os import environ as env

load_dotenv()
LAT = env["LAT"]
LONG = env["E_LON"]

url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": LAT,
	"longitude": LONG,
	"hourly": ["temperature_2m", "rain", "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high"],
	"current": ["temperature_2m", "cloud_cover"],
	"forecast_days": 1,
}


request = httpx.get(url, params=params)
response = request.json()

day = datetime.now().date()
temp_hourly = {k:(v,z) for (k,(v,z)) in zip(response["hourly"]["time"],zip(response["hourly"]["temperature_2m"],response["hourly"]["cloud_cover"]))}


# print(response)
print(f"\nDay: {day}\n")
print("{:<6} {:<5} {:<10}".format("Hour", "Temp", "Clouds"))
for k in temp_hourly:
    print(f"{str(k)[-5:]:<6} {temp_hourly[k][0]:<5} {temp_hourly[k][1]:<10}")


