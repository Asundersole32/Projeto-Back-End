class SolderPasteInspection():
    def __init__(self):
        self.inspection_result = None
        self.defect_count = None
        self.inspection_speed = None
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
            'inspection_result': self.inspection_result,
            'defect_count': self.defect_count,
            'inspection_speed': self.inspection_speed
        }
        return self.data_dict
    
    def generate_data(self):
        pass