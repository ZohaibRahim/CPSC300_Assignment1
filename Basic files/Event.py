# Event base class for the hospital simulation

class Event:
    # Base class for all events in the simulation
    
    def __init__(self, time, patient=None):
        self.time = time
        self.patient = patient
    
    def __lt__(self, other):
        # Primary sort: by time (earlier times first)
        if self.time != other.time:
            return self.time < other.time
        
        # Secondary sort: by patient_id when times are equal (lower patient ID first)
        if self.patient is None and other.patient is None:
            return False
        if self.patient is None:
            return True
        if other.patient is None:
            return False
        
        # Both have patients - compare by patient ID
        return self.patient.patient_id < other.patient.patient_id
    
    def process(self, hospital):
        # All subclasses must implement this method
        raise NotImplementedError("Subclasses must implement process()")