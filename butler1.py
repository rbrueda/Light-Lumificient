# this is created slightly different using different variables
# todo: check if priority queue is properly working (in this case, taking the miniumum value at INDEX 1)
# todo: play around with heurisitc numbers (add a heuristic for movie)

import queue

class Butler:
    def __init__(self):

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
        self.RESTINC = 2
        self.HEATINC = 5
        self.COOLINC = 5
        self.ENERGYCOST = 10
        self.MAXTEMP = 50
        self.MINTEMP = 0
        self.EFFICIENCY = 0.05
        
        # Magic numbers for temperature
        self.REST = 0
        self.HEAT = 1
        self.COOL = 2



#IDEA: MAKE TWO HEURISTIC INTENSITY BRIGHTNESSES -- ONE WHERE OUTSIDE BRIGHTNESS PLAYS EFFECT AND
        #-- ONE WHERE OUTSIDE BRIGHTNESS PLAYS NO EFFECT

        #based off checking the location of light relative to action
        #we are also basing off light based off outside 
        # inside brightness values -> add up to 1
        # outside brightness values -> add up to 1
        self.heuristics_sleep = {
            'L1' : 0.26,
            'L2' : 0.04,
            'L3' : 0.35,
            'L4' : 0.35,
            'W1' : 0.7, 
            'W2' : 0.3
        }

        self.heuristics_study = {
            'L1' : 0.26,
            'L2' : 0.7,
            'L3' : 0.03,
            'L4' : 0.01,
            'W1' : 0.7,
            'W2' : 0.3
        }

        #this is slightly ambiguous -- we can assume the user is listening to music in couch
        self.heuristics_music = {
            'L1' : 0.1,
            'L2' : 0.4,
            'L3' : 0.4,
            'L4' : 0.1,
            'W1' : 0.1,
            'W2' : 0.9

        }

        #another ambigous one, the user is cleaning the ENTIRE room, hence it may want the brightness to be uniform
        self.heuristics_clean = {
            'L1' : 0.4,
            'L2' : 0.2,
            'L3' : 0.2,
            'L4' : 0.2,
            'W1' : 0.5,
            'W2' : 0.5
        }

    # Light Util
    def getLightCost(self, lights):
        #the cost is based on individual light intensities, and energy consumption rate (closer to 1 -- higher consumption rate, closer to 0 -- lower consumption rate)
        cost = self.ENERGY_CONSUMPTION['L1']*lights['L1'] + self.ENERGY_CONSUMPTION['L2']*lights['L2'] + self.ENERGY_CONSUMPTION['L3']*lights['L3'] + self.ENERGY_CONSUMPTION['L4']*lights['L4']
        return cost

    def getTotalBrightness(self, lightLevels, shutter_status, outside, intensity):
        if (shutter_status) == True:
            status = 0
        else:
            status = 1

        #weighted sum with the intensities
        totalBrightness = intensity['L1']*lightLevels['L1'] + intensity['L2']*lightLevels['L2'] + intensity['L3']*lightLevels['L3'] + intensity['L4']*lightLevels['L4'] + intensity['W1']*outside*status + intensity['W2']*outside*status   
        print(f"total brightness: {totalBrightness}")
        print(f"brightness: {round(totalBrightness)}")

        # returns a array
        # array[0] = brightness rounded to 1 dp
        # array[1] = actual brightness (not rounded)
        # using min and max --> avoids values from going out of range
        return [round(min(self.MAXBRIGHTNESS, max(self.MINBRIGHTNESS, totalBrightness)), 1), totalBrightness]
    
    def heuristic_function(self, state, target_brightness, outside_brightness):
        # Calculate heuristic value actual brightness (decimal value) and target brightness
        distance_to_target = abs(target_brightness - state)
        
        print(f"distance to target: {distance_to_target}")
        return distance_to_target

    # idea: add each device by 1 until we get to goal -- this might not be as efficient but is pretty accurate (we can change this later based on other heuristics)

    # Light A*
    #this is just a modified version of UFS with the heuristics
    def AStarLight(self, initialLights, targetBrightness, outsideBrightness, option, shutter_status):
        #gets the intensity per light heuristic
        if (option == 'sleep'):
            intensity = self.heuristics_sleep
        elif (option == 'study'):
            intensity = self.heuristics_study
        elif (option == 'music'):
            intensity = self.heuristics_music
        elif (option == 'clean'):
            intensity = self.heuristics_clean


        #implementation of priority queue
        q = queue.PriorityQueue()

        # keeps track of min cost at that brightness -- our goal is to make sure that cost is min at that brightness level
        minCosts = {brightness: float('inf') for brightness in range(self.MAXBRIGHTNESS*10)}

        brightnessStats = self.getTotalBrightness(initialLights, shutter_status, outsideBrightness, intensity)
        print(f"current brightness: {brightnessStats[0]}")
        nextCost = self.getLightCost(initialLights)
        nextH = self.heuristic_function(brightnessStats[1], targetBrightness, outsideBrightness)
        totCost = nextCost+nextH 
        print(f"total cost: {totCost}")
        minCosts[brightnessStats[0]*10] = totCost
        q.put((totCost,brightnessStats[0],"", initialLights))

        #iterates until queue is empty
        while not q.empty():
            #get the min element using the priorty queue
            curr = q.get()
            print(f"current successor: {curr}")

            # round brightness to a whole number
            successor_brightness = round(curr[1])

            # case 1: lights reach target brightness
            if successor_brightness == targetBrightness:
                print(f"final queue: {curr}")
                return [curr[3], False] #gets the light fixture brightnesses and False shutter status
            
            # case 2: lights are minimized, but target brightness cannot be reached
            if successor_brightness > targetBrightness and curr[3]['L1'] == 0 and curr[3]['L2'] == 0 and curr[3]['L3'] == 0 and curr[3]['L4'] == 0:
                return [curr[3], True] #gets the light fixture brightnesses and True shutter status

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

                print(next_state)
                brightnessStats = self.getTotalBrightness(next_state, shutter_status, outsideBrightness, intensity)
                
                
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
                        q.put((totCost, brightnessStats[0],curr[2]+ " --> " +str(light), next_state))


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
    def aStar(self, goal, outside):
    
        # initialise
        minCosts = [99999 for i in range(self.MAXTEMP)]                  #value at index i will indicate minimum cost (energy+distance from goal) to reach temperature i
        q = queue.PriorityQueue()
        q.put((0, outside, 0, ""))                                     #total cost, current temp (starts at outside/initial), energy cost so far, path of choices (temp for tracing)

        # search
        while not q.empty():
            curr = q.get()                                          #dequeues lowest cost node, essentially picking best out of current options to expand

            if curr[1] == goal:
                return curr

            for i in range(3):                                      
                nextTemp = self.getTemp(i, curr[1], outside)
                nextCost = self.getCost(i)
                nextH = abs(goal-nextTemp)
                totCost = nextCost*self.EFFICIENCY+nextH                 #calculate f=g+h -> cost to reach node + additional heuristic cost. also, energy efficiency but it shouldnt have as much of an impact on the next choice as reaching the goal quickly should
                if totCost < minCosts[nextTemp]:                    #if we previously had a less effective way to reach this temperature, replace it with this way. if there is already a more effective way to reach this point, don't bother continuing this path
                    minCosts[nextTemp] = totCost
                    if nextTemp > self.MINTEMP and nextTemp < self.MAXTEMP:
                        q.put((totCost,nextTemp,nextCost,curr[3]+str(i)))


# is this main() ?
#note - these variables will change since they will be based by gui
targetBrightness = 10 
outsideBrightness = 1
initialLights = {'L1': 0, 'L2': 0, 'L3': 0, 'L4': 0} #set this as arbitrary default brightness level per fixture
option = 'study'
shutter_status = False #assume shutters are open -- these will only be true if it is night time
butler = Butler()
result = butler.AStarLight(initialLights, targetBrightness, outsideBrightness, option, shutter_status)

print("\n")
print("Total cost: {}\tFinal temp: {}\tEnergy cost: {}\tPath: {}".format(*butler.aStar(20,10)))
