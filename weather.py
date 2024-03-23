import requests
from datetime import datetime

class Weather:
    def __init__(self):
        
        # get api key from external file
        with open('credentials.txt', 'r') as f:
            for content in f:
                API_KEY = content

        city = 'Windsor'
        country_code = 'CA'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={API_KEY}'

        # Send HTTP request
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # the description of current weather forecast
            self.weather_description = data['weather'][0]['description']
            temperature_kelvin = data['main']['temp']
            #convert to celsius and round to 1 decimal place
            self.temperature = round(temperature_kelvin - 273.15, 1) 

            # speed of wind from outside
            self.wind_speed = data['wind']['speed']

            # percentage of cloud cover
            self.cloudiness = data['clouds']['all']


        #if this happens during sensor process in smart home, use old variables
        else:
            print('Error:', response.status_code)

weather = Weather()
