class AutomatedOpticalInspection():
    def __init__(self):
        self.inspection_result = None
        self.defected_defects = None
        self.inspection_time = None
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
            'inspection_result': self.inspection_result,
            'defected_defects': self.defected_defects,
            'inspection_time': self.inspection_result
        }
        return self.data_dict

    def generate_data(self):
        pass