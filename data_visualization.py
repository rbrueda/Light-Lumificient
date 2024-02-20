import pandas as pd
import matplotlib.pyplot as plt

#this class shows al
class DataVisualization:
    def __init__(self):
        #this is where i will show all csv with different plot popups
        light_df = pd.read_csv('light_brightness.csv', encoding='utf-8')

        #To DO: plot the temperature_df, humidity_df, windspeed_df

        # TO DO: for the future, only plot data from the last 24 hours!

        # Convert 'datetime' column to datetime data type 
        light_df['datetime'] = pd.to_datetime(light_df['datetime'])

        plt.plot(light_df['datetime'].values, light_df['brightness'].values)
        plt.title('Light Brightness Display')
        plt.xlabel('Time Stamp')
        plt.ylabel('Light brightness')

        plt.show()

