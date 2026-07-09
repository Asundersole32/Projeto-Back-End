import random


class AutomatedOpticalInspection():
    def __init__(self, machine_id):
        self.machine_id = machine_id
        self.inspection_result = None
        self.defected_defects = None
        self.inspection_time = None
        self.status = 'Paused'
        self.data_dict = {}

    def set_inspection_result(self, inspection_result):
        self.inspection_result = inspection_result
        return self
    
    def get_inspection_result(self):
        return self.inspection_result
    
    def set_defected_defects(self, defected_defects):
        self.defected_defects = defected_defects
        return self
    
    def get_defected_defects(self):
        return self.defected_defects
    
    def set_inspection_time(self, inspection_time):
        self.inspection_time = inspection_time
        return self
    
    def get_inspection_time(self):
        return self.inspection_time
    
    def get_data_dict(self):
        return self.data_dict
    
    def mount_dict(self):
        self.data_dict = {
            'machine_id': self.machine_id,
            'inspection_result': self.inspection_result,
            'defected_defects': self.defected_defects,
            'inspection_time': self.inspection_result,
            'status': self.status,
        }
        return self

    def generate_data(self):
        result_list = ['FAIL', 'PASS']

        defected_defects_list = [
            'Solder Bridge',
            'Component offset',
            'Component polarity',
            'Component presence',
            'Area defects',
            'Billboarding',
            'Flipped component',
            'Component absence',
            'Component skew',
            'Excessive solder joints',
            'Height defects',
            'Insufficient paste around Leads',
            'Insufficient solder Joints',
            'Lifted leads',
            'No population tests',
            'Paste registration',
            'Severely damaged components',
            'Tombstoning',
            'Volume defects',
            'Wrong part',
            'Presence of foreign material on the board'
        ]

        min_inspection_time = 1.0
        max_inspection_time = 100.0

        random_result = random.randint(0, 1)
        random_defect = random.randint(0, 19)
        random_inspection_time = random.uniform(min_inspection_time, max_inspection_time)

        self.inspection_result = result_list[random_result]
        self.defected_defects = defected_defects_list[random_defect]
        self.inspection_time = random_inspection_time

        seeded_data = self.mount_dict()
        return seeded_data.data_dict
    