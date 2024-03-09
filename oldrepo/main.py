import tkinter as tk
from dashboard import Dashboard
from automation_system import AutomationSystem
from smart_device import SmartLight, Thermostat, SecurityCamera
from data_visualization import DataVisualization


if __name__ == "__main__":
    light1 = SmartLight("Living room Light", brightness=40)
    thermostat1 = Thermostat("Living room Thermostat")
    camera1 = SecurityCamera("Front door camera")

    # these are the different devices being used -- add ceiling fan (air conditioner) and humidity detector
    automation_system = AutomationSystem()
    automation_system.add_device(light1)
    automation_system.add_device(thermostat1)
    automation_system.add_device(camera1)

    #creates an instance of tkinter
    root = tk.Tk()

    #creates an instance of Daskboard that contains all tkinter pop ups
    dashboard = Dashboard(root, automation_system)

    #will look through tkinter component values until close button handler is clicked (at least as of what i think)
    root.mainloop()