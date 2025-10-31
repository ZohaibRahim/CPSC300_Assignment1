from abc import ABC, abstractmethod

class Event(ABC):
    """Abstract base class for all events"""
    
    def __init__(self, time, patient):
        self.time = time
        self.patient = patient
    
    @abstractmethod
    def process(self, hospital):
        """Process this event - must be implemented by subclasses"""
        pass
    
    def __lt__(self, other):
        """
        Compare events for priority queue ordering.
        Order by: time first, then patient_id
        """
        if self.time != other.time:
            return self.time < other.time
        return self.patient.patient_id < other.patient.patient_id
    
    def __repr__(self):
        return f"{self.__class__.__name__}(time={self.time}, patient={self.patient.patient_id})"