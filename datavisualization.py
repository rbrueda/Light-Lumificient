# Purpsse: compare results for both A* (new simulator) and logic (original simulator) results

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 

class DataVisualization:
    def __init__(self, value1, value2):
        
        self.value1 = value1
        self.value2 = value2

        n=10
        r = np.arange(n) 
        width = 0.25
        
        # 1st line bar graph --> logic
        plt.bar(r, self.value1, color = 'b', 
                width = width, edgecolor = 'black', 
                label='Logic Result')
        #2nd line bar graph --> A* 
        plt.bar(r + width, self.value2, color = 'pink', 
                width = width, edgecolor = 'black', 
                label='A* Result') 
        
        #x and y-axis labels
        plt.xlabel("Devices") 
        plt.ylabel("Device Level") 
        plt.title("Statistics for Different Device States") 
        
        #x-axis values
        plt.xticks(r + width/2,['AC','R','W1','W2', 'L1', 'L2', 'L3', 'L4', 'RS1', 'RS2']) 
        plt.legend() 
        
        plt.show() 