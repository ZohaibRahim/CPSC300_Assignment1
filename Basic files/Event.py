class Event:
    
    def __init__(self, time, patient):
        self.time = time
        self.patient = patient
    
    
    #Compare events for priority queue ordering:
    #1. Earlier time first ,2. If times equal, higher priority first (lower number = higher priority)
    #3. If priorities equal or unknown, earlier patient_id first
    
    def __lt__(self, other):
       
        if self.time != other.time:
            return self.time < other.time
            
        # Get priorities safely (use 999 if None/unknown)
        self_priority = getattr(self.patient, 'priority', None) or 999
        other_priority = getattr(other.patient, 'priority', None) or 999
        
        if self_priority != other_priority:
            return self_priority < other_priority
            
        # Break ties by patient ID
        return self.patient.patient_id < other.patient.patient_id

    
    #Process this event and return list of new events to be scheduled.
    def process(self, hospital):
        
        raise NotImplementedError