import requests
from datetime import datetime
def worldtime(city):
	url = "https://world-time-by-api-ninjas.p.rapidapi.com/v1/worldtime"

	querystring = {"city":city}

	headers = {
		"X-RapidAPI-Key": "Your_RapidAPI_Key",
		"X-RapidAPI-Host": "world-time-by-api-ninjas.p.rapidapi.com"
	}

	response = requests.get(url, headers=headers, params=querystring)
	data = response.json()

	datetime_str = data['datetime']
	time_str = datetime_str.split(' ')[1]
	# Convert time to datetime object
	time_obj = datetime.strptime(time_str, "%H:%M:%S")

	# Convert time to AM/PM format
	time_formatted = time_obj.strftime("%I:%M:%S %p")

	return time_formatted
