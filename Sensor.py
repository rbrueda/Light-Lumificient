from pyswip import Prolog
import datetime 
from weather import Weather
import time

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
    timestamp = datetime.datetime.now().time()
    print(f"time: {timestamp}")

    f = open("logActions.txt", "w")
    f2 = open("sensorvals.txt", "w")
    for k, v in sensors.items():
        if v[0] == 'light':
            if k=='outside_brightness':
                # change this value to a reasonable value -- not just random -- we will use percentage of cloud cover for this
                n = 100 - int(weather.cloudiness)*0.80
                n = int(n/10)
                setSensorValue(k, n, prolog)

                # december
                if date.month in [12]:
                    #average night time
                    if (timestamp >= datetime.time(18, 40, 0)):
                        n = 0
                        setSensorValue(k, n, prolog)
                # january
                if date.month in [1]:
                    if (timestamp >= datetime.time(19, 0, 0)):
                        n = 0
                        setSensorValue(k, n, prolog)
                # february
                if date.month in [2]:
                    if (timestamp >= datetime.time(19, 30, 0)):
                        n = 0
                        setSensorValue(k, n, prolog)
                # march
                if date.month in [3]:
                    if (timestamp >= datetime.time(20, 30, 0)):
                        print("here")
                        n = 0
                        setSensorValue(k, n, prolog)
                # april
                if date.month in [4]:
                    if (timestamp >= datetime.time(21, 30, 0)):
                        n = 0
                        setSensorValue(k, n, prolog)
                # may
                if date.month in [5]:
                    if (timestamp >= datetime.time(22, 30, 0)):
                        n = 0
                        setSensorValue(k, n, prolog)
                # june
                if date.month in [6]:
                    if (timestamp >= datetime.time(23, 0, 0)):
                        n = 0
                        setSensorValue(k, n, prolog)
                # july
                if date.month in [7]:
                    if (timestamp >= datetime.time(23, 0, 0)):
                        n = 0
                        setSensorValue(k, n, prolog)
                # august
                if date.month in [8]:
                    if (timestamp >= datetime.time(22, 30, 0)):
                        n = 0
                        setSensorValue(k, n, prolog)
                # september
                if date.month in [9]:
                    if (timestamp >= datetime.time(21, 30, 0)):
                        n = 0
                        setSensorValue(k, n, prolog)
                #october
                if date.month in [10]:
                    if (timestamp >= datetime.time(20, 30, 0)):
                        n = 0
                        setSensorValue(k, n, prolog)
                #november
                if date.month in [11]:
                    if (timestamp >= datetime.time(19, 0, 0)):
                        n = 0
                        setSensorValue(k, n, prolog)



            else: #inside brightness
                n = 5 #default value - 50%
                setSensorValue(k, n, prolog)
        elif v[0] == 'temp':
            if k=='outside_temperature':
                #to represent temperature in 0-30 range
                n = round((weather.temperature + 25) * 0.5)
                #for extreme cases -- below/above lowest/highest:
                if n < 0:
                    n = 0
                if n > 30:
                    n = 30
                setSensorValue(k, n, prolog)
            else:
                n = 0
                setSensorValue(k, n, prolog)
        # todo: fix speed of wind
        elif v[0] == 'wind':
            n = int(weather.wind_speed)
            setSensorValue(k, n, prolog)
        elif v[0] == 'rain':
            if 'rain' in weather.weather_description:
                n = 1
                setSensorValue(k, n, prolog) #1 = true
            else:
                n = 0
                setSensorValue(k, n, prolog) #0 = false
        # elif v[0] == 'humidity':
        #     n = weather.humidity // 10
        #     setSensorValue(k, n, prolog)
        
        # print in the logActionas file the string setSensorValue(k, n)
            #! what is the purpose of this??
        f.write("setSensorValue("+k+", "+str(n)+")\n")
        f2.write(k + "," + str(n) + "\n")

    f.close()
    f2.close()
