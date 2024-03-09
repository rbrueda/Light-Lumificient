from datetime import datetime
import tkinter as tk
from smart_device import SmartLight, Thermostat, SecurityCamera
from automation_system import AutomationSystem
import pandas as pd


from data_visualization import DataVisualization
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class Dashboard:
    #master -> root of UI
    def __init__(self, master, automation_system):

        self.master = master
        self.master.title("Smart Home Monitoring Dashboard")
        self.automation_system = automation_system

        # Size of the window
        self.master.geometry('1100x900')
        self.master.configure(bg="lightgrey")  # Changes the background color to light blue

        # Create a font for text widgets and labels -- change this later?
        custom_font = ("Times New Roman", 12)

        # Automation toggle button
        self.automation_button = tk.Button(master, text="Automation ON/OFF", command=self.toggle_automation, font=custom_font)
        self.automation_button.pack()
        self.Automation_status_label = tk.Label(master, text="Automation Status: OFF", font=custom_font)
        self.Automation_status_label.pack()

        self.text_status = tk.Text(master, height=10, width=40, font=custom_font)
        self.text_status.pack()

        # will show all the current plots when clicked
        self.showPlots_button = tk.Button(master, text="Show Plots", command=self.show_plots, font=custom_font)
        self.showPlots_button.pack()


        self.update_device_status()

        # SmartLight
        self.smart_light_label = tk.Label(master, text=f"{self.automation_system.devices[0].device_id} Brightness", font=custom_font)
        self.smart_light_label.pack()
        #this will effect update_brightness value that will display in text when this is changed
        self.smart_light_brightness_scale = tk.Scale(master, from_=0, to=100, orient="horizontal", command=lambda value, self=self: self.update_brightness(value), font=custom_font)
        self.smart_light_brightness_scale.pack(pady=0)
        self.smart_light_button = tk.Button(master, text="Toggle ON/OFF", command=self.toggle_smart_light, font=custom_font)
        self.smart_light_button.pack()
        self.smart_light_bright_level = tk.Label(master, text=f"Living room Light - {self.automation_system.devices[0].brightness}%", font=custom_font)
        self.smart_light_bright_level.pack()

        # Thermostat
        self.thermostat_label = tk.Label(master, text=f"{self.automation_system.devices[1].device_id} - Temperature", font=custom_font)
        self.thermostat_label.pack()
        self.thermostat_scale = tk.Scale(master, from_=0, to=50, orient="horizontal", command=self.update_temperature_label, font=custom_font)
        self.thermostat_scale.pack()
        self.thermostat_button = tk.Button(master, text="Toggle ON/OFF", command=self.toggle_thermostat, font=custom_font)
        self.thermostat_button.pack()
        self.thermostat_level_label = tk.Label(master, text=f"Living room Thermostat - {self.automation_system.devices[1].temperature}C", font=custom_font)
        self.thermostat_level_label.pack()

        # Camera
        self.motion_detect_label = tk.Label(master, text="Front door Camera Motion Detection", font=custom_font)
        self.motion_detect_label.pack()
        self.random_motion_detect = tk.Button(master, text="Random Detect Motion", command=self.random_detect, font=custom_font)
        self.random_motion_detect.pack()
        self.camera_button = tk.Button(master, text="Toggle ON/OFF", command=self.toggle_camera, font=custom_font)
        self.camera_button.pack()
        self.camera_status = tk.Label(master, text="Front door Camera - Motion: NO", font=custom_font)
        self.camera_status.pack()

        self.t_light_event = tk.Label(master, text="Brightness Events", font=custom_font)
        self.t_light_event.pack()

        self.light_event = tk.Text(master, height=10, width=80, font=custom_font)
        self.light_event.pack()

    #display the graph in the screen
    # def displayLightGraph(self):

        # chart = alt.Chart(light_df).mark_line(color='purple').encode(
        #         x=alt.X('datetime', title='Time'), 
        #         y=alt.Y('brightness', title='Brightness of Smart Light'),
        #         tooltip=['datetime', 'brightness']
        #     ).properties(
        #         title='Line Graph of Light Brightness',
        #         width=700,
        #         height=400
        #     )

        # st.write(chart)
        


    # Other methods remain the same...
        #Automation button functions -- start

    # this will write changed brightness state to the console 
    #** TO DO: show other variable changes in the console box
    def update_brightness(self, value):
        new_brightness = int(value)
        self.automation_system.devices[0].set_brightness(new_brightness)

        #this is the continuously updated smart light level
        self.smart_light_bright_level.config(text=f"Living room Light - {new_brightness}%")

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #! is this even used -- this is not used anywhere
        self.brightness_change_text = f"[{current_time}] - Brightness of {self.automation_system.devices[0].device_id} changed to {new_brightness}%"

    #** this method seems to "automate" values when lights are turned on -- this will need to be fixed using heuristics to make values make sense and not jsut random values
    def randomize_device_states(self):
        import random

        for device in self.automation_system.devices:
            if isinstance(device,SmartLight):
                    #**seems like it is randomizing the value?? -- we can make our automizations here based off the data here

                    import random
                    device.turn_on()
                    new_brightness = random.randint(1, 100)
                    device.set_brightness(new_brightness)
                    self.smart_light_brightness_scale.set(new_brightness)  # Set the scale to the new brightness
            if isinstance(device,Thermostat):
                    import random
                    device.turn_on()
                    new_temperature = random.randint(1, 100)
                    device.set_temperature(new_temperature)
                    self.thermostat_scale.set(new_temperature)  # Set the scale to the new brightness
            if isinstance(device,SecurityCamera):
                    import random
                    motion_status = random.choice(["YES", "NO"])  # Generate random motion status

                    # Assuming your front door camera is at a specific index in the devices list
                    camera = None
                    for device in self.automation_system.devices:
                        if isinstance(device, SecurityCamera) and device.device_id == "Front door camera":
                            camera = device
                            break

                    if camera:
                        camera.set_security_status("Unsafe" if motion_status == "YES" else "Safe")
                        if motion_status == "YES":
                            for device in self.automation_system.devices:
                                if isinstance(device,SmartLight):
                                    if device.status:
                                        pass
                                    else:
                                        self.toggle_smart_light()
                        self.camera_status.config(text=f"Front door Camera - Motion: {motion_status}")
                    else:
                    # Handle the case where the front door camera is not found in the devices list
                        print("Front door camera not found in the devices list.")
            else:
                pass
    

    # this will store sensor data to csv -- TO-DO modify this method with the other attributes
    def gather_and_store_sensor_data(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #save to a dataframe
        light_data = []

        # maybe: put this data in a database
        with open("sensor_data.txt","a") as file:
            for device in self.automation_system.devices:
                if isinstance (device,SmartLight):
                    #write as a csv -- makes to parse through the data later 
                    light_data.append({
                        'datetime' : current_time,
                        'device' : device.device_id,
                        'status' : device.status,
                        'brightness' : device.brightness
                    })

                    df = pd.DataFrame(light_data)
                    csv_file_path = 'light_brightness'+'.csv'

                    #writes the dataframe to the csv
                    df.to_csv(csv_file_path, mode='a', header=False, index=False)
                    
                    #update current graph
                    # self.update_plot(current_time, device.brightness)

                    #leave for now -- remove later!
                    file.write(f"{current_time} - Device: {device.device_id}, Status: {device.status}, Brightness: {device.brightness}%\n")


    # this will show the current plots when "Show Plots" button is clicked
    def show_plots(self):
        plot = DataVisualization()

    #this will display in console (bottom white box) the status of a particular device -- this data will help us in our model when know the when devices are on and off and at what times
    def update_device_status(self):
        device_status_text = ""
        for device in self.automation_system.devices:
            device_status_text += f"{device.device_id} - Status: {'ON' if device.status else 'OFF'}\n"

        self.text_status.delete(1.0, tk.END)  # Clear the existing text
        self.text_status.insert(tk.END, device_status_text)

    # this will display in console (bottom white box) the light brightness of a particular device 
    def update_light_events(self):
        light_status_text = ""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for device in self.automation_system.devices:
            if isinstance(device,SmartLight):

                #once toggle is clicked on, brightness message is updated
                light_status_text += f"[{current_time}] - {device.device_id} brightness set to {self.smart_light_brightness_scale.get()}%\n"

        # self.light_event.delete(1.0,tk.END)
        self.light_event.insert(tk.END,light_status_text)

    # this method will check if automation is activated/deactivated
    def toggle_automation(self):
        if not self.automation_system.is_automation_on:
            self.automation_system.is_automation_on = True

            #**this is what we will optimizing in our training model
            self.randomize_device_states()
            self.Automation_status_label.config(text="Automation status: ON")
        else:
            self.automation_system.is_automation_on = False
            self.Automation_status_label.config(text="Automation status: OFF")
        
        self.update_device_status()
        self.update_light_events()
        self.gather_and_store_sensor_data()
    #Automation button functions -- end

    #Smart Light -- start
    # this physically changes the smart light value using automation system -- this this function is only activated if automation is on (VERIFY THIS) 
    def toggle_smart_light(self):
        for device in self.automation_system.devices:
            if isinstance(device, SmartLight):
                #if status is currently on, turn off??
                if device.status:
                    device.turn_off()
                    device.set_brightness(0)
                    self.smart_light_brightness_scale.set(0)  # Set the scale value to 0
                # if status is off?
                else:
                    import random #**change this with heuristic stuff
                    device.turn_on()
                    new_brightness = random.randint(1, 100)
                    device.set_brightness(new_brightness)
                    self.smart_light_brightness_scale.set(new_brightness)  # Set the scale to the new brightness
        self.update_brightness_label()
        self.update_device_status()
        self.update_light_events()
        self.gather_and_store_sensor_data()
    
    #changes the text on the screen with current brightness
    def update_brightness_label(self, event=None):
        new_brightness = self.smart_light_brightness_scale.get()
        self.automation_system.devices[0].set_brightness(new_brightness)
        self.smart_light_bright_level.config(text=f"Living room Light - {new_brightness}%")
  

    #Smart Light -- end

    #Thermostat functions  --- start

    def toggle_thermostat(self):
        for device in self.automation_system.devices:
            if isinstance(device, Thermostat):
                if device.status:
                    device.turn_off()
                    device.set_temperature(0)
                    self.thermostat_scale.set(0)  # Set the scale value to 0
                else:
                    import random
                    device.turn_on()
                    new_temperature = random.randint(1, 100)
                    device.set_temperature(new_temperature)
                    self.thermostat_scale.set(new_temperature)  # Set the scale to the new brightness
        self.update_temperature_label()
        self.update_device_status()
        #**TO DO: add gather_and_store_sensor_data() function here for saving to a new csv for temperature csv
        #** make a function self.update_light_events() version for thermostat


    #updates the current toggle value in the screen
    def update_temperature_label(self, event=None):
        new_temperature = self.thermostat_scale.get()
        self.automation_system.devices[1].set_temperature(new_temperature)
        self.thermostat_level_label.config(text=f"Living room Thermostat - {new_temperature}%")

    #Thermostat functions --- end


    #Camera -- start
    def random_detect(self):
        for device in self.automation_system.devices:
            if isinstance(device,SecurityCamera):
                if device.status:
                    import random
                    #! seems like the camera starts randomly??
                    #**TO DO: (optional for now) schedule a fixed time for this to for our model 
                    motion_status = random.choice(["YES", "NO"])  # Generate random motion status

                    # Assuming your front door camera is at a specific index in the devices list
                    camera = None

                    #! Not sure the purpose of this statement
                    # this seems like it goes through all existing devices and sees if the device is the front door camera and sets camera to that
                    for device in self.automation_system.devices:
                        if isinstance(device, SecurityCamera) and device.device_id == "Front door camera":
                            camera = device
                            break

                    if camera:
                        camera.set_security_status("Unsafe" if motion_status == "YES" else "Safe")
                        if motion_status == "YES":
                            for device in self.automation_system.devices:
                                if isinstance(device,SmartLight):
                                    if device.status:
                                        pass
                                    else:
                                        self.toggle_smart_light()
                        # this seems to be detected if "Random Detect Button is clicked" -- because status is random -- you may need to click button
                        self.camera_status.config(text=f"Front door Camera - Motion: {motion_status}")
                    else:
                    # Handle the case where the front door camera is not found in the devices list
                        print("Front door camera not found in the devices list.")
                else:
                    pass

    #this is for the "Toggle ON/OFF" button for camera
                #this only changes the top console box in tk for "Front door camera - Status: "
    def toggle_camera(self):
        for device in self.automation_system.devices:
            if isinstance(device,SecurityCamera):
                #if status is on, turn off
                if device.status:
                    device.turn_off()
                #opposite for this
                else:
                    device.turn_on()
        self.update_device_status()