import random


class PickAndPlace():
    def __init__(self, machine_id):
        self.machine_id = machine_id
        self.placement_speed = None
        self.feeder_utilization = None
        self.placement_accuracy = None
        self.status = 'Running'
        self.data_dict = {}

    def set_placement_speed(self, placement_speed):
        self.placement_speed = placement_speed
        return self
    
    def get_placement_speed(self):
        return self.placement_speed
    
    def set_feeder_utilization(self, feeder_utilization):
        self.feeder_utilization = feeder_utilization
        return self
    
    def get_feeder_utilization(self):
        return self.feeder_utilization
    
    def set_placement_accuracy(self, placement_accuracy):
        self.placement_accuracy = placement_accuracy
        return self
    
    def get_placement_accuracy(self):
        return self.placement_accuracy
    
    def get_data_dict(self):
        return self.data_dict
    
    def mount_dict(self):
        self.data_dict = {
            'machine_id': self.machine_id,
            'placement_speed': self.placement_speed,
            'feeder_utilization': self.feeder_utilization,
            'placement_accuracy': self.placement_accuracy,
            'status': self.status,
        }
        return self

    def generate_data(self):
        min_placement_speed = 1
        max_placement_speed = 100000

        min_placement_accuracy = 0.001
        max_placement_accuracy = 1

        random_placement_speed = random.randint(min_placement_speed, max_placement_speed)
        random_feeder_utilization = random.uniform(0.0, 100.0)
        random_placement_accuracy = random.uniform(min_placement_accuracy, max_placement_accuracy)

        self.placement_speed = random_placement_speed
        self.feeder_utilization = random_feeder_utilization
        self.placement_accuracy = random_placement_accuracy

        seeded_data = self.mount_dict()
        return seeded_data.data_dict
