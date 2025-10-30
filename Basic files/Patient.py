class Patient:
     def __init__(self, patient_id, arrival_time, patient_type, assessment_time):
        # 'E' for Emergency, 'W' for Walk-in
        # default priority; can be upgraded later
        self.patient_id = patient_id
        self.arrival_time = arrival_time
        self.patient_type = patient_type 
        
        self.assessment_time = assessment_time
        self.priority = 1 if patient_type == 'E' else 3  
        self.waiting_time = 0
        self.treatment_start_time = None
        self.treatment_end_time = None
        self.admission_time = None
    
    #Defines comparison based on priority for PriorityQueue
     def __lt__(self, other):
       
        return self.priority < other.priority
     
     def __repr__(self):
        return f"Patient({self.patient_id}, Priority: {self.priority}, Type: {self.patient_type})"