import httpx
from datetime import datetime
from dotenv import load_dotenv
from os import environ as env

url = "https://api.open-meteo.com/v1/forecast"

def get_data(lat: float, long: float) -> dict:
	params = {
		"latitude": lat,
		"longitude": long,
		"hourly": ["temperature_2m", "rain", "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high"],
		"current": ["temperature_2m", "cloud_cover"],
		"forecast_days": 1,
	}
      
	request = httpx.get(url, params=params)
	response = request.json()

	forecast = {k:(v,z) for (k,(v,z)) in zip(response["hourly"]["time"],zip(response["hourly"]["temperature_2m"],response["hourly"]["cloud_cover"]))}
	current = (response["current"]["temperature_2m"],response["current"]["cloud_cover"])

	return {"forecast": forecast, "current": current}



if __name__ == "__main__":

	load_dotenv()
	LAT = env["LAT"]
	LONG = env["E_LON"]

	data = get_data(LAT, LONG)
	print(data)
	day = datetime.now().date()


	forecast = data["forecast"]
	print(f"\nDay: {day}\n")
	print("{:<6} {:<5} {:<10}".format("Hour", "Temp", "Clouds"))
	for k in forecast:
		print(f"{str(k)[-5:]:<6} {forecast[k][0]:<5} {forecast[k][1]:<10}")