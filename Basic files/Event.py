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
        if self.time != other.time:
            return self.time < other.time
        # Priority tie-breaker when time is equal:
        # Unknown priority (None) should be treated as lowest priority (i.e., sort after known ones)
        self_pri = self.patient.priority if getattr(self.patient, "priority", None) is not None else float("inf")
        other_pri = other.patient.priority if getattr(other.patient, "priority", None) is not None else float("inf")
        if self_pri != other_pri:
            return self_pri < other_pri
        return self.patient.patient_id < other.patient.patient_id

    
    def __repr__(self):
        return f"{self.__class__.__name__}(time={self.time}, patient={self.patient.patient_id})"
