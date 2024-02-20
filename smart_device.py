class SmartDevice:
    def __init__(self, device_id, status=False):
        self.device_id = device_id
        self.status = status

class SmartLight(SmartDevice):
    def __init__(self, device_id, status=False, brightness=50):
        super().__init__(device_id, status)
        self.brightness = brightness

    def turn_on(self):
        self.status = True

    def turn_off(self):
        self.status = False

    def set_brightness(self, brightness):
        self.brightness = brightness


class Thermostat(SmartDevice):
    def __init__(self, device_id, status=False, temperature=72):
        super().__init__(device_id, status)
        self.temperature = temperature

    def turn_on(self):
        self.status = True

    def turn_off(self):
        self.status = False

    def set_temperature(self, temperature):
        self.temperature = temperature


class SecurityCamera(SmartDevice):
    def __init__(self, device_id, status=False, security_status="Safe"):
        super().__init__(device_id, status)
        self.security_status = security_status

    def turn_on(self):
        self.status = True

    def turn_off(self):
        self.status = False

    def set_security_status(self, security_status):
        self.security_status = security_status