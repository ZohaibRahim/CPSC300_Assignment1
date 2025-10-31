class Patient:
    # Represents a patient in the hospital simulation
    
    def __init__(self, patient_id, arrival_time, patient_type, treatment_time):
        # Basic patient information
        self.patient_id = patient_id
        self.arrival_time = arrival_time
        self.patient_type = patient_type  # 'E' for Emergency, 'W' for Walk-In
        self.treatment_time = treatment_time  # How long treatment will take
        
        # Emergency patients always priority 1, walk-ins get priority during assessment
        self.priority = 1 if patient_type == 'E' else None
        
        # Track important time points for this patient
        self.assessment_start_time = None
        self.assessment_end_time = None
        self.treatment_start_time = None
        self.treatment_end_time = None
        self.admission_queue_entry_time = None
        self.departure_time = None
        
        # Track waiting times for each stage
        self.wait_for_assessment = 0
        self.wait_for_treatment = 0
        self.wait_for_admission = 0
    
    def total_waiting_time(self):
        # Calculate total time spent waiting across all stages
        return (self.wait_for_assessment +
                self.wait_for_treatment +
                self.wait_for_admission)
    
    def __lt__(self, other):
        # Used for priority queue ordering in waiting room
        # First sort by priority (lower number = higher priority = comes first)
        if self.priority != other.priority:
            return self.priority < other.priority
        # If same priority, sort by patient ID (earlier patients first)
        return self.patient_id < other.patient_id
    
    def __repr__(self):
        return f"Patient({self.patient_id}, Priority: {self.priority}, Type: {self.patient_type})"