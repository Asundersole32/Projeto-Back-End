class PickAndPlace():
    def __init__(self):
        self.placement_speed = None
        self.feeder_utilization = None
        self.placement_accuracy = None
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
            'placement_speed': self.placement_speed,
            'feeder_utilization': self.feeder_utilization,
            'placement_accuracy': self.placement_accuracy
        }
        return self.data_dict

    def generate_data(self):
        pass