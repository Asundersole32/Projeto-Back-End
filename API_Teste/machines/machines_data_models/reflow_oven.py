class ReflowOven():
    def __init__(self):
        self.zone_temperature = None
        self.conveyor_speed = None
        self.oxygen_level = None
        self.data_dict = {}

    def set_zone_temperature(self, zone_temperature):
        self.zone_temperature = zone_temperature
        return self
    
    def get_zone_temperature(self):
        return self.zone_temperature
    
    def set_conveyor_speed(self, conveyor_speed):
        self.conveyor_speed = conveyor_speed
        return self
    
    def get_conveyor_speed(self):
        return self.conveyor_speed
    
    def set_oxygen_level(self, oxygen_level):
        self.oxygen_level = oxygen_level
        return self
    
    def get_oxygen_level(self):
        return self.oxygen_level
    
    def get_data_dict(self):
        return self.data_dict
    
    def mount_dict(self):
        self.data_dict = {
            'zone_temperature': self.zone_temperature,
            'conveyor_speed': self.conveyor_speed,
            'oxygen_level': self.oxygen_level
        }
        return self.data_dict
    
    def generate_data(self):
        pass