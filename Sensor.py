# Purpose: get inputs from environment

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
    

    

# sensors check current percepts of room
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
    f3 = open("nightstatus.txt", "w")
    for k, v in sensors.items():
        if v[0] == 'light':
            if k=='outside_brightness':
                # change this value to a reasonable value -- not just random -- we will use percentage of cloud cover for this
                n = 100 - int(weather.cloudiness)*0.80
                n = int(n/10)
                setSensorValue(k, n, prolog)
                flag = 0

                # december
                if date.month in [12]:
                    #average sunrise and sunset times per month
                    if (timestamp >= datetime.time(18, 40, 0) or timestamp <= datetime.time(6, 0, 0) ):
                        n = 0
                        setSensorValue(k, n, prolog)
                        flag = -1
                        f3.write("true")
                # january
                if date.month in [1]:
                    if (timestamp >= datetime.time(19, 0, 0) or timestamp <= datetime.time(6, 30, 0)):
                        n = 0
                        setSensorValue(k, n, prolog)
                        flag = -1
                        f3.write("true")
                # february
                if date.month in [2]:
                    if (timestamp >= datetime.time(19, 30, 0) or timestamp <= datetime.time(6, 0, 0)):
                        n = 0
                        setSensorValue(k, n, prolog)
                        flag = -1
                        f3.write("true")
                # march
                if date.month in [3]:
                    if (timestamp >= datetime.time(20, 0, 0) or timestamp <= datetime.time(6, 0, 0)):
                        n = 0
                        setSensorValue(k, n, prolog)
                        flag = -1
                        f3.write("true")
                # april
                if date.month in [4]:
                    if (timestamp >= datetime.time(21, 30, 0) or timestamp <= datetime.time(5, 30, 0)):
                        n = 0
                        setSensorValue(k, n, prolog)
                        flag = -1
                        f3.write("true")
                # may
                if date.month in [5]:
                    if (timestamp >= datetime.time(22, 30, 0) or timestamp <= datetime.time(4, 30, 0)):
                        n = 0
                        setSensorValue(k, n, prolog)
                        flag = -1
                        f3.write("true")
                # june
                if date.month in [6]:
                    if (timestamp >= datetime.time(23, 0, 0) or timestamp <= datetime.time(4, 0, 0)):
                        n = 0
                        setSensorValue(k, n, prolog)
                        flag = -1
                        f3.write("true")
                # july
                if date.month in [7]:
                    if (timestamp >= datetime.time(23, 0, 0) or timestamp <= datetime.time(4, 30, 0)):
                        n = 0
                        setSensorValue(k, n, prolog)
                        flag = -1
                        f3.write("true")
                # august
                if date.month in [8]:
                    if (timestamp >= datetime.time(22, 30, 0) or timestamp <= datetime.time(5, 0, 0)):
                        n = 0
                        setSensorValue(k, n, prolog)
                        flag = -1
                        f3.write("true")
                # september
                if date.month in [9]:
                    if (timestamp >= datetime.time(21, 30, 0) or timestamp <= datetime.time(5, 30, 0)):
                        n = 0
                        setSensorValue(k, n, prolog)
                        flag = -1
                        f3.write("true")
                #october
                if date.month in [10]:
                    if (timestamp >= datetime.time(20, 0, 0) or timestamp <= datetime.time(6, 0, 0)):
                        n = 0
                        setSensorValue(k, n, prolog)
                        flag = -1
                        f3.write("true")
                #november
                if date.month in [11]:
                    if (timestamp >= datetime.time(19, 0, 0) or timestamp <= datetime.time(5, 30, 0)):
                        n = 0
                        setSensorValue(k, n, prolog)
                        flag = -1
                        f3.write("true")

                if (flag != -1):
                    f3.write("false")

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
                n = 22
                setSensorValue(k, n, prolog)

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

        # write sensors to text file logActions.txt
        f.write("setSensorValue("+k+", "+str(n)+")\n")
        f2.write(k + "," + str(n) + "\n")

    f.close()
    f2.close()
    f3.close()
