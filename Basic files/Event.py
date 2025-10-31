class Event:
    """Base class for all simulation events"""
    
    def __init__(self, time, patient):
        self.time = time
        self.patient = patient
    
    def __lt__(self, other):
        """
        Compare events for priority queue ordering:
        1. Earlier time first
        2. If times equal, higher priority first (lower number = higher priority)
        3. If priorities equal or unknown, earlier patient_id first
        """
        if self.time != other.time:
            return self.time < other.time
            
        # Get priorities safely (use 999 if None/unknown)
        self_priority = getattr(self.patient, 'priority', None) or 999
        other_priority = getattr(other.patient, 'priority', None) or 999
        
        if self_priority != other_priority:
            return self_priority < other_priority
            
        # Break ties by patient ID
        return self.patient.patient_id < other.patient.patient_id
    
    def process(self, hospital):
        """
        Process this event and return list of new events to be scheduled.
        Must be implemented by subclasses.
        """
        raise NotImplementedError