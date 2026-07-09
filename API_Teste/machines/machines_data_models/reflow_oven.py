import random


class ReflowOven():
    def __init__(self, machine_id):
        self.machine_id = machine_id
        self.zone_temperature = None
        self.conveyor_speed = None
        self.oxygen_level = None
        self.status = 'Heating'
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
            'machine_id': self.machine_id,
            'zone_temperature': self.zone_temperature,
            'conveyor_speed': self.conveyor_speed,
            'oxygen_level': self.oxygen_level,
            'status': self.status,
        }
        return self
    
    def generate_data(self):
        min_zone_temperature = 0
        max_zone_temperature = 250

        min_conveyor_speed = 40
        max_conveyor_speed = 200

        min_oxygen_level = 500
        max_oxygen_level = 1000

        random_zone_temperature = random.randint(min_zone_temperature, max_zone_temperature)
        random_conveyor_speed = random.randint(min_conveyor_speed, max_conveyor_speed)
        random_oxygen_level = random.randint(min_oxygen_level, max_oxygen_level)

        self.zone_temperature = random_zone_temperature
        self.conveyor_speed = random_conveyor_speed
        self.oxygen_level = random_oxygen_level

        seeded_data = self.mount_dict()
        return seeded_data.data_dict
