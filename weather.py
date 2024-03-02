import requests
import datetime

class Weather:
    def __init__(self):

        # get api key from external file
        API_KEY = 'e96eaabd4215318eb360de442e41444f'
        city = 'Windsor'
        country_code = 'CA'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={API_KEY}'

        # Send HTTP request
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            print(data)
            
            # Extract relevant information from the response
            # the description could also be important for training, especially to check if it is dark or sunny outside
            self.weather_description = data['weather'][0]['description']
            temperature_kelvin = data['main']['temp']
            #convert to celsius and round to 1 decimal place
            self.temperature = round(temperature_kelvin - 273.15, 1) 
            self.humidity = data['main']['humidity']
            self.wind_speed = data['wind']['speed']
            #time of sunrise - to later if time for a continuous automation system -- or for updating preferences
            sunrise = data['sys']['sunrise']
            self.sunrise_time = datetime.datetime.utcfromtimestamp(sunrise)
            sunset = data['sys']['sunset']
            self.sunset_time = datetime.datetime.utcfromtimestamp(sunset)
            self.cloudiness = data['clouds']['all']
            # # find formula to represent formula for light brightness given light brightness and 

            
            # just for tracing -  Print the weather information
            # print(f'Weather in {city}:')
            # print(f'Description: {weather_description}')
            # print(f'Temperature: {temperature} °C')
            # print(f'Humidity: {humidity}%')
            # print(f'Wind Speed: {wind_speed} m/s')
            # print(f'Cloudiness: {cloudiness}%')
            # print(f'Sunrise time: {sunrise_time}')
            # print(f'Sunset time: {sunset_time}')

            # heuristics: educated guess -- we can use Percentage of cloud cover.

        #if this happens during sensor process in smart home, use old variables
        else:
            print('Error:', response.status_code)

weather = Weather()
