import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 

#this class shows al
class DataVisualization:
    def __init__(self, value1, value2):
        
        self.value1 = value1
        self.value2 = value2

        n=10
        r = np.arange(n) 
        width = 0.25
        
        
        plt.bar(r, self.value1, color = 'b', 
                width = width, edgecolor = 'black', 
                label='Logic Result') 
        plt.bar(r + width, self.value2, color = 'pink', 
                width = width, edgecolor = 'black', 
                label='A* Result') 
        
        plt.xlabel("Devices") 
        plt.ylabel("Device Level") 
        plt.title("Statics for Different Device States") 
        
        # plt.grid(linestyle='--') 
        plt.xticks(r + width/2,['AC','R','W1','W2', 'L1', 'L2', 'L3', 'L4', 'RS1', 'RS2']) 
        plt.legend() 
        
        plt.show() 


# #these values should be from effector values     
# value1 = [115, 215, 250, 200, 232, 233, 234, 234, 234, 234] 
# value2 = [114, 230, 510, 370, 343, 245, 234, 276, 222, 234] 

# data = DataVisualization(value1, value2)