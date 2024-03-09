# this is created slightly different using different variables

import queue

class Butler:
    def __init__(self):

        # Constants for energy consumption (adjust as needed)
        self.ENERGY_CONSUMPTION = {
            'L1': 0.5,  # Energy consumption rate for light fixture L1
            'L2': 0.7,  # Energy consumption rate for light fixture L2
            'L3': 0.6,  # Energy consumption rate for light fixture L3
            'L4': 0.8   # Energy consumption rate for light fixture L4
        }

        # Constants, we can change later -- best way for now is increase or decrease certain light by 1
        # RESTINC = 2
        # BRIGHTINC = 3
        # DIMC = 5
        self.MAXBRIGHTNESS = 10
        self.MINBRIGHTNESS = 0
        self.EFFICIENCY = 0.05 # use later

        self.lights = ['L1', 'L2', 'L3', 'L4']

        #based off checking the location of light relative to action
        #we are also basing off light based off outside 
        self.heuristics_sleep = {
            'L1' : 0.26,
            'L2' : 0.04,
            'L3' : 0.35,
            'L4' : 0.35,
            'W1' : 0.7, 
            'W2' : 0.4
        }

        #all values should add up to 1
        self.heuristics_study = {
            'L1' : 0.35,
            'L2' : 0.5,
            'L3' : 0.1,
            'L4' : 0.05,
            'W1' : 0.9,
            'W2' : 0.5
        }

        #this is slightly ambiguous -- we can assume the user is listening to music in couch
        self.heuristics_music = {
            'L1' : 0.1,
            'L2' : 0.4,
            'L3' : 0.4,
            'L4' : 0.1,
            'W1' : 0.5,
            'W2' : 1

        }

        #another ambigous one, the user is cleaning the ENTIRE room, hence it may want the brightness to be uniform
        self.heuristics_clean = {
            'L1' : 0.4,
            'L2' : 0.2,
            'L3' : 0.2,
            'L4' : 0.2,
            'W1' : 0.7,
            'W2' : 0.7
        }

    def getCost(self, lights):
        #the cost is based on individual light intensities, and energy consumption rate (closer to 1 -- higher consumption rate, closer to 0 -- lower consumption rate)
        cost = self.ENERGY_CONSUMPTION['L1']*lights[0] + self.ENERGY_CONSUMPTION['L2']*lights[1] + self.ENERGY_CONSUMPTION['L3']*lights[2] + self.ENERGY_CONSUMPTION['L4']*lights[3]
        return cost

    def getTotalBrightness(self, lightLevels, shutter_status, outside, intensity):
        if (shutter_status) == True:
            status = 0
        else:
            status = 1
        # figure out intensity scaling such that maxTotal brightness is no greater than 10 because no less that 0
        totalBrightness = intensity['L1']*lightLevels[0] + intensity['L2']*lightLevels[1] + intensity['L3']*lightLevels[2] + intensity['L4']*lightLevels[3] + intensity['W1']*outside*status + intensity['W2']*outside*status   
        print(f"brightness: {int(totalBrightness)}")
        return int(totalBrightness)

    # idea: add each device by 1 until we get to goal -- this might not be as efficient but is pretty accurate (we can change this later based on other heuristics)

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
        minCosts = [99999 for i in range(self.MAXBRIGHTNESS)]

        nextBrightness = self.getTotalBrightness(initialLights, shutter_status, outsideBrightness, intensity)
        nextCost = self.getCost(initialLights)
        q.put((nextBrightness,nextCost,"", initialLights))


        while not q.empty():
            #get the min element using the priorty queue -> use the heapq library
            curr = q.get()
            if curr[0] == targetBrightness:
                print(f"final queue: {curr}")
                return curr[3] #gets the light fixture brightnesses
            
            #traverse through all the lights in the smart home
            for i in range(4):

                # we are going to assume next brightness will get -- for now curr[3] = listOfLights -- we are going to increase one of the lights by 1 or -1 depending on current status
                if curr[0] < targetBrightness:
                    curr[3][i] += 1
                if curr[0] > targetBrightness:
                    curr[3][i] -= 1
                nextBrightness = self.getTotalBrightness(curr[3], shutter_status, outsideBrightness, intensity)
                print(f"brightness at {i}: {nextBrightness}")
                nextCost = self.getCost(curr[3])  
                nextH = abs(targetBrightness-nextBrightness)
                totCost = nextCost+nextH                 #calculate f=g+h -> cost to reach node + additional heuristic cost. also, energy efficiency but it shouldnt have as much of an impact on the next choice as reaching the goal quickly should
                print(totCost)
                # where totCost = f(n), nextH = remaining brightness, (lets not use efficiency yet)
                if totCost < minCosts[nextBrightness]:                    #if we previously had a less effective way to reach this temperature, replace it with this way. if there is already a more effective way to reach this point, don't bother continuing this path
                    minCosts[nextBrightness] = totCost
                    if nextBrightness > self.MINBRIGHTNESS and nextBrightness < self.MAXBRIGHTNESS:
                        #to do - make a list of values to add and subtract in order to get total cost
                        # priority queue:
                        # value 1: current brightness
                        # value 2: current cost -- this should get the min every time
                        # value 3: path for queue
                        # value 4: light values
                        q.put((nextBrightness,nextCost,curr[2]+ "--" +str(i), curr[3]))

#note - these variable will change since they will be based by gui
targetBrightness = 5 #this is will change later
outsideBrightness = 1 
initialLights = [1, 0, 0, 0]
option = 'study'
shutter_status = False #assume shutters are open -- 
butler = Butler()
result = butler.AStarLight(initialLights, targetBrightness, outsideBrightness, option, shutter_status)
print(result)

