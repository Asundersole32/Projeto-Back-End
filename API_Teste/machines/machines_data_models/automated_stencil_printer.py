import random


class AutomatedStencilPrinter():
    def __init__(self, machine_id):
        self.machine_id = machine_id
        self.cycle_time = None
        self.paste_remaining = None
        self.cleaning_interval = 5 
        self.status = 'Printing'
        self.data_dict = {}

    def set_cycle_time(self, cycle_time):
        self.cycle_time = cycle_time
        return self
    
    def get_cycle_time(self):
        return self.cycle_time
    
    def set_paste_remaining(self, paste_remaining):
        self.paste_remaining = paste_remaining
        return self
    
    def get_paste_remaining(self):
        return self.paste_remaining
    
    def set_cleaning_interval(self, cleaning_interval):
        self.cleaning_interval = cleaning_interval
        return self
    
    def get_cleaning_interval(self):
        return self.cleaning_interval
    
    def get_data_dict(self):
        return self.data_dict
    
    def mount_dict(self):
        self.data_dict = {
            'machine_id': self.machine_id,
            'cycle_time': self.cycle_time,
            'paste_remaining': self.paste_remaining,
            'cleaning_interval': self.cleaning_interval,
            'status': self.status,
        }
        return self
    
    def generate_data(self):
        min_cycle_time = 1.0
        max_cycle_time = 100.0

        random_cycle_time = random.uniform(min_cycle_time, max_cycle_time)
        random_paste_remaining = random.uniform(0.0, 100.0)

        self.cycle_time = random_cycle_time
        self.paste_remaining = random_paste_remaining

        seeded_data = self.mount_dict()
        return seeded_data.data_dict
    