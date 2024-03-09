import smart_device as SmartLight
#this class contains all the devices in the smart home environment
class AutomationSystem:
    def __init__(self):
        self.devices = []
        self.is_automation_on = False

    def __init__(self):
        self.devices = []
        self.is_automation_on = False

    # add the list of devices from main to the attribute devices in AutomationSystem
    def add_device(self, device):
        self.devices.append(device)

    # will turn on device is instance (toggle button) is handled
    def execute_automation_states(self, task):
        if task == "Turn on lights when motion is detected":
            for device in self.devices:
                if isinstance(device, SmartLight):
                    device.turn_on()