# Purpose: perform a search algorithm to find the most optimal combinations for fixtures optimizing energy efficiency

import queue
from contributionValues import Contribution 
import random

class Butler:
    def __init__(self):

        f = open("sensorvals.txt")
        lines = f.readlines()

        sensor_values = {}

        for line in lines:
            k, v = line.strip().split(',')
            sensor_values[k] = int(v)

        f.close()

        f = open("profilevals.txt")
        lines = f.readlines()

        study_values = {}
        movie_values = {}
        sleep_values = {}
        clean_values = {}
        music_values = {}

        constribution_values = {}

        for line in lines:
            act, k, v = line.strip().split(',')
            if act == "study":
                study_values[k] = int(v)
            elif act == "movie":
                movie_values[k] = int(v)
            elif act == "sleep":
                sleep_values[k] = int(v)
            elif act == "clean":
                clean_values[k] = int(v)
            elif act == "music":
                music_values[k] = int(v)

        f.close()

        self.outside_brightness = sensor_values['outside_brightness']
        self.outside_temperature = sensor_values['outside_temperature']

        self.study_brightness = study_values['light']
        self.movie_brightness = movie_values['light']
        self.sleep_brightness = sleep_values['light']
        self.clean_brightness = clean_values['light']
        self.music_brightness = music_values['light']

        self.study_temperature = study_values['temp']
        self.movie_temperature = movie_values['temp']
        self.sleep_temperature = sleep_values['temp']
        self.clean_temperature = clean_values['temp']
        self.music_temperature = music_values['temp']

        # Constants for light energy consumption (adjust as needed)
        self.ENERGY_CONSUMPTION = {
            'L1': 0.5,  # Energy consumption rate for light fixture L1
            'L2': 0.7,  # Energy consumption rate for light fixture L2
            'L3': 0.6,  # Energy consumption rate for light fixture L3
            'L4': 0.8   # Energy consumption rate for light fixture L4
        }

        self.MAXBRIGHTNESS = 10
        self.MINBRIGHTNESS = 0
        self.EFFICIENCY = 0.05

        self.lights = ['L1', 'L2', 'L3', 'L4']


        # Constants for temperature
        self.RESTINC = 0.5
        self.HEATINC = 1
        self.COOLINC = 1
        self.ENERGYCOST = 10
        self.MAXTEMP = 50
        self.MINTEMP = 0
        self.EFFICIENCY = 0.05
        
        # Magic numbers for temperature
        self.REST = 0
        self.HEAT = 1
        self.COOL = 2

    # Light Util
    def getLightCost(self, lights):
        #the cost is based on individual light intensities, and energy consumption rate (closer to 1 -- higher consumption rate, closer to 0 -- lower consumption rate)
        cost = self.ENERGY_CONSUMPTION['L1']*lights['L1'] + self.ENERGY_CONSUMPTION['L2']*lights['L2'] + self.ENERGY_CONSUMPTION['L3']*lights['L3'] + self.ENERGY_CONSUMPTION['L4']*lights['L4']
        return cost

    # this weight is calculated to find the weights of outside and inside brightness 
    # weights are favoured from 2 factors:
    #   - outside brightness contribution to total light brightness (calculated in Cotribution class)
    #   - current outside brightness
    def findAdditionalWeights(self, outside, intensity):
        # check inside contribution values based off what the current state of outside brightness is and outside contribution
        T1 = 10 - (outside*intensity['outsideContribution'])
        # remainder of T1
        T2 = (10-T1)/10
        #scale the values from 0 to 1
        T1 = T1/10
        return [T1, T2]


    def getTotalBrightness(self, lightLevels, shutter_status, outside, intensity):
        #check shutter status
        if (shutter_status) == True:
            status = 0
        else:
            status = 1

        #weights for contribution to outside brightness and inside brightness (separately)
        [T1, T2] = self.findAdditionalWeights(outside, intensity)

        #weighted sum with the intensities
        totalBrightness = T1*(intensity['L1']*lightLevels['L1'] + intensity['L2']*lightLevels['L2'] + intensity['L3']*lightLevels['L3'] + intensity['L4']*lightLevels['L4']) + T2*(outside*status)   
        print(f"current totalBrightness: {totalBrightness}")

        # returns a array
        # array[0] = brightness rounded to 1 dp
        # array[1] = actual brightness (not rounded)
        # using min and max --> avoids values from going out of range
        return [round(min(self.MAXBRIGHTNESS, max(self.MINBRIGHTNESS, totalBrightness)), 1), totalBrightness]
    
    def heuristic_function(self, state, target_brightness, outside_brightness):
        # Calculate heuristic value actual brightness (decimal value) and target brightness
        distance_to_target = abs(target_brightness - state)
        
        return distance_to_target

    # Light A*
    def AStarLight(self, initialLights, targetBrightness, outsideBrightness, option, shutter_status):

        #gets intensity heuristics
        contribution = Contribution(option)
        intensity = contribution.getValues()

        print(f"A* light brightness results:")

        #implementation of priority queue
        q = queue.PriorityQueue()

        # keeps track of min cost at that brightness -- our goal is to make sure that cost is min at that brightness level
        minCosts = {brightness: float('inf') for brightness in range(self.MAXBRIGHTNESS*10 + 1)}

        brightnessStats = self.getTotalBrightness(initialLights, shutter_status, outsideBrightness, intensity)
        nextCost = self.getLightCost(initialLights)
        nextH = self.heuristic_function(brightnessStats[1], targetBrightness, outsideBrightness)
        totCost = nextCost+nextH 
        #keep track of successor result if queue becomes empty before exhausting possibilities
        successorResult = [initialLights, 0]
        closestToGoal = nextH

        minCosts[brightnessStats[0]*10] = totCost
        q.put((totCost,brightnessStats[0],"", initialLights))

        #iterates until queue is empty
        while not q.empty():
            #get the min element using the priority queue
            curr = q.get()
            print(f"current successor: {curr}")

            # case 1 --> keep track of closest result (for case if queue becomes empty before finding result)
            if (targetBrightness - curr[1] < closestToGoal):
                successorResult = [curr[3], 0]
                closestToGoal = targetBrightness - curr[1]
                print(f"current closest result: {successorResult}")

            # round brightness to a whole number
            successor_brightness = round(curr[1])

            # case 2 --> lights reach target brightness
            if successor_brightness == targetBrightness:
                return [curr[3], 0] #gets the light fixture brightnesses and False shutter status
            
            # case 3 --> lights are minimized, but target brightness cannot be reached
            if successor_brightness > targetBrightness and curr[3]['L1'] == 0 and curr[3]['L2'] == 0 and curr[3]['L3'] == 0 and curr[3]['L4'] == 0:
                if 2 > successor_brightness - targetBrightness: #slightly off
                    shutter_value = 2

                elif 4 > successor_brightness - targetBrightness: #somewhat off
                    shutter_value = 4

                elif 6 > successor_brightness - targetBrightness: # pretty off
                    shutter_value = 6

                elif 8 > successor_brightness - targetBrightness: # very off
                    shutter_value = 8

                elif 10 >= successor_brightness - targetBrightness: # super off
                    shutter_value = 10
   
                return [curr[3], shutter_value] #gets the light fixture brightnesses and shutter status at a particular setting

            
            #traverse through all the lights in the smart home
            for light, brightness in curr[3].items():

                # make a copy of light fixture brightnesses
                next_state = dict(curr[3])

                # we are going to increase one of the lights by 1 or -1 depending on current status
                if successor_brightness < targetBrightness:
                    if (next_state[light] > 9):
                        continue
                    next_state[light] += 1
                elif successor_brightness > targetBrightness:
                    if (next_state[light] < 1):
                        continue
                    next_state[light] -= 1

                brightnessStats = self.getTotalBrightness(next_state, shutter_status, outsideBrightness, intensity)

                #edge case --> brightness is slightly above 10
                if (brightnessStats[0] > 10):
                    brightnessStats[0] = 10 
        
                nextCost = self.getLightCost(next_state)  
                nextH = self.heuristic_function(brightnessStats[1], targetBrightness, outsideBrightness)
                totCost = nextCost+nextH                 #calculate f=g+h -> cost to reach node + additional heuristic cost. also, energy efficiency but it shouldnt have as much of an impact on the next choice as reaching the goal quickly should
                
                #checks if totcost is less than the current min cost that the brightness level
                if totCost < minCosts[brightnessStats[0]*10]:                    
                    minCosts[brightnessStats[0]*10] = totCost
                    # check if total brightness value are in range
                    if round(brightnessStats[0]) >= self.MINBRIGHTNESS and round(brightnessStats[0]) <= self.MAXBRIGHTNESS:
                        # priority queue:
                        # value 1: total cost -- this should get min every time
                        # value 2: current brightness
                        # value 3: path for queue
                        # value 4: light values
                        q.put((totCost, brightnessStats[0], curr[2]+ " --> " +str(light), next_state))

        return successorResult


    # Temperature Util
    def getTemp(self, choice, current, outside):
        if choice == self.REST:
            return current-self.RESTINC if current>outside else current+self.RESTINC
        elif choice == self.HEAT:
            return current+self.HEATINC
        else: 
            return current-self.COOLINC
    
    def getCost(self, choice):
        return 0 if choice == self.REST else self.ENERGYCOST
                        
    # Temperature A*
    def AStarTemp(self, goal, outside):  
        goal = round(goal * (50/30))
        outside = round(outside * (50/30))

        # edge case --> so we can output a result from 1-50
        if (goal == 0):
            goal = 1
        
        if (outside == 0):
            outside = 1
        

        # initialise
        minCosts = [99999 for i in range(self.MAXTEMP*2)]                  #value at index i will indicate minimum cost (energy+distance from goal) to reach temperature i
        q = queue.PriorityQueue()
        q.put((0, outside, 0, ""))                                     #total cost, current temp (starts at outside/initial), energy cost so far, path of choices (temp for tracing)

        # search
        while not q.empty():
            curr = q.get()                                          #dequeues lowest cost node, essentially picking best out of current options to expand

            #goal temperature is found at lowest cost
            if curr[1] == goal:
                return curr

            for i in range(3):                                      
                nextTemp = self.getTemp(i, curr[1], outside)
                print(f"nextTemp: {nextTemp}")
                nextCost = self.getCost(i)
                nextH = abs(goal-nextTemp)
                totCost = nextCost*self.EFFICIENCY+nextH                 #calculate f=g+h -> cost to reach node + additional heuristic cost. also, energy efficiency but it shouldnt have as much of an impact on the next choice as reaching the goal quickly should
                if totCost < minCosts[int(nextTemp*2)]:                    #if we previously had a less effective way to reach this temperature, replace it with this way. if there is already a more effective way to reach this point, don't bother continuing this path
                    minCosts[int(nextTemp*2)] = totCost
                    if nextTemp > self.MINTEMP and nextTemp < self.MAXTEMP:
                        q.put((totCost,nextTemp,nextCost,curr[3]+str(i)))


#note - these variables will change since they will be based by gui
print("Random run -- without sensor percepts")
targetBrightness = random.randint(0, 10)
outsideBrightness = random.randint(0, 10)
initialLights = {'L1': 0, 'L2': 0, 'L3': 0, 'L4': 0} #set this as arbitrary default brightness level per fixture
#random option
optionNumber = random.randint(0,4)
if (optionNumber == 0):
    option = 'study'
if (optionNumber == 1):
    option = 'movie'
if (optionNumber == 2):
    option = 'music'
if (optionNumber == 3):
    option = 'sleep'
if (optionNumber == 4):
    option = 'clean'

shutter_status = False #assume shutters are open -- these will only be true if it is night time
butler = Butler()
result = butler.AStarLight(initialLights, targetBrightness, outsideBrightness, option, shutter_status)
print(f"final result: {result}")

print("\n")
print("Total cost: {}\tFinal temp: {}\tEnergy cost: {}\tPath: {}".format(*butler.AStarTemp(20,10)))