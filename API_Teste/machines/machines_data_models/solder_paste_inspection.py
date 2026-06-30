import random


class SolderPasteInspection():
    def __init__(self, machine_id):
        self.machine_id = machine_id
        self.inspection_result = None
        self.defect_count = None
        self.inspection_speed = None
        self.status = 'Inspecting'
        self.data_dict = {}

    def set_inspection_result(self, inspection_result):
        self.inspection_result = inspection_result
        return self
    
    def get_inspection_result(self):
        return self.inspection_result
    
    def set_defect_count(self, defect_count):
        self.defect_count = defect_count
        return self
    
    def get_defect_count(self):
        return self.defect_count
    
    def set_inspection_speed(self, inspection_speed):
        self.inspection_result = inspection_speed
        return self
    
    def get_inspection_speed(self):
        return self.inspection_speed
    
    def get_data_dict(self):
        return self.data_dict
    
    def mount_dict(self):
        self.data_dict = {
            'machine_id': self.machine_id,
            'inspection_result': self.inspection_result,
            'defect_count': self.defect_count,
            'inspection_speed': self.inspection_speed,
            'status': self.status,
        }
        return self
    
    def generate_data(self):
        inspect_result_list = ['PASS', 'FAILED']
        
        max_inspection_speed = 0.1
        min_inspection_speed = 200

        min_defect_count = 0
        max_defect_count = 100

        random_result = random.randint(0, 1)
        random_inspection_speed = random.randint(min_inspection_speed, max_inspection_speed)
        random_defect_count = random.randint(min_defect_count, max_defect_count)

        self.inspection_result = inspect_result_list[random_result]
        self.defect_count = random_defect_count
        self.inspection_speed = random_inspection_speed

        seeded_data = self.mount_dict()
        return seeded_data.data_dict

        
