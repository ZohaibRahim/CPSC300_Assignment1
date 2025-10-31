class Patient:
    """Represents a patient in the hospital simulation"""
    
    def __init__(self, patient_id, arrival_time, patient_type, treatment_time):
        self.patient_id = patient_id
        self.arrival_time = arrival_time
        self.patient_type = patient_type  # 'E' for Emergency, 'W' for Walk-in
        self.treatment_time = treatment_time
        
        # Priority is 1 for emergency, assigned during assessment for walk-ins
        self.priority = 1 if patient_type == 'E' else None
        
        # Tracking times
        self.assessment_start_time = None
        self.assessment_end_time = None
        self.waiting_room_enter_time = None
        self.treatment_start_time = None
        self.treatment_end_time = None
        self.departure_time = None
        
        # Waiting time breakdown
        self.wait_for_assessment = 0
        self.wait_for_treatment = 0
        self.wait_for_admission = 0
    
    def total_waiting_time(self):
        """Calculate total waiting time"""
        return self.wait_for_assessment + self.wait_for_treatment + self.wait_for_admission
    
    def __lt__(self, other):
        """
        Compare patients for waiting room priority queue.
        Order by: priority first (lower is higher priority), then patient_id
        """
        if self.priority != other.priority:
            return self.priority < other.priority
        return self.patient_id < other.patient_id
    
    def __repr__(self):
        return f"Patient({self.patient_id}, Priority: {self.priority}, Type: {self.patient_type})"
