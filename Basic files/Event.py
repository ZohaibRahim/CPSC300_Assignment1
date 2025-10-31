class Event:
    """Base Event class for the hospital simulation."""
    
    def __init__(self, time, patient=None):
        self.time = time
        self.patient = patient
    
    def __lt__(self, other):
        """
        Comparison for PriorityQueue ordering.
        Primary: sort by time (earlier times first)
        Secondary: sort by patient_id (lower patient numbers first when times are equal)
        """
        if self.time != other.time:
            return self.time < other.time
        
        # Handle case where one or both events don't have patients
        if self.patient is None and other.patient is None:
            return False
        if self.patient is None:
            return True
        if other.patient is None:
            return False
        
        # Both have patients - compare by patient ID
        return self.patient.patient_id < other.patient.patient_id
    
    def process(self, hospital):
        """Process the event. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement process()")