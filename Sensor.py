from pyswip import Prolog
import datetime 
from weather import Weather

import random

# retrieves all sensors and htier values form prolog
def getAllSensor(prolog):
    sensorList = list(prolog.query("sensor(X,Y)"))
    dictsensor = {}
    for i in range(len(sensorList)):
        dictsensor [sensorList[i]["X"]] = sensorList[i]["Y"]
        
    newdict = {}
    for k,v in dictsensor.items():
        temp = list(prolog.query("sensorValue("+str(k)+",Y)"))
        if bool(temp):
            newdict[k]= [v, temp[0]["Y"]]
    return newdict

# retrieves the value of a specific sensor
def getSensorValue(sensorID, prolog):
    query_list = list(prolog.query("sensorValue(" + sensorID +" ,X)"))
    if len(query_list) == 1:
        return str(query_list[0]["X"])
    else: return query_list 

# sets the values of a specific sensor
def setSensorValue(sensorID, value, prolog):
    old_value = str(getSensorValue(sensorID, prolog))
    list(prolog.query("replace_existing_fact(sensorValue(" + str(sensorID) +" ,"+str(old_value)+"), sensorValue(" + str(sensorID)+ ", "+str(value)+"))." ))
    
# add values from dashboard.py, and create an instance of weather.py for current weather values in python
# note: this method should activate once - change from action "simulate sensors" to "toggle ON/OFF"
def generete_random_sensors(prolog):
    sensors = getAllSensor(prolog)
    #create an http request to Weather API
    weather = Weather()
    #import the date
    date = datetime.datetime.now()

    f = open("logActions.txt", "w")

    for k, v in sensors.items():
        if v[0] == 'light':
            if k=='outside_brightness':
               # change this value to a reasonable value -- not just random -- we will use percentage of cloud cover for this
               n = 10 - int(weather.cloudiness)
               setSensorValue(k, n, prolog)
            #this is based off the most recent line from the dataset 
            else:
                # TO DO: change this value from dashboard.py
                n = 0
                setSensorValue(k, n, prolog)
        elif v[0] == 'temp':
            #instead of if cases - get the current value of temperature for Windsor
            n = weather.temperature
            setSensorValue(k, n, prolog)
        elif v[0] == 'wind':
            n = weather.wind_speed
            setSensorValue(k, n, prolog)
        elif v[0] == 'rain':
            if 'rain' in weather.weather_description:
                n = 1
                setSensorValue(k, n, prolog) #1 = true
            else:
                n = 0
                setSensorValue(k, n, prolog) #0 = false
        elif v[0] == 'humidity':
            n = weather.humidity // 10
            setSensorValue(k, n, prolog)
        
        # print in the logActionas file the string setSensorValue(k, n)
            #! what is the purpose of this??
        f.write("setSensorValue("+k+", "+str(n)+")\n")
    f.close()




