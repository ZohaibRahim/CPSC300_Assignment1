from queue import PriorityQueue

class Hospital:
    """Hospital class managing resources and patient queues."""
    
    def __init__(self):
        self.all_patients = []
        self.assessment_queue = []  # FIFO queue for walk-ins waiting to be assessed
        self.waiting_room = PriorityQueue()  # Priority queue for patients waiting for treatment
        self.admission_queue = []  # Queue for Priority 1 patients waiting for admission
        self.rooms_available = 3  # 3 treatment rooms
        self.triage_nurse_busy = False  # One triage nurse
        self.admission_nurse_busy = False  # One admission nurse
    
    def add_patient(self, patient):
        """Add patient to hospital tracking."""
        self.all_patients.append(patient)
    
    def can_start_assessment(self):
        """Check if assessment can start (nurse free and patients waiting)."""
        return len(self.assessment_queue) > 0 and not self.triage_nurse_busy
    
    def get_next_assessment_patient(self):
        """Get next patient from assessment queue (FIFO)."""
        if self.assessment_queue:
            return self.assessment_queue.pop(0)
        return None
    
    def add_to_waiting_room(self, patient):
        """Add patient to waiting room (priority queue)."""
        self.waiting_room.put(patient)
    
    def get_next_from_waiting_room(self):
        """Get next patient from waiting room (highest priority first)."""
        try:
            return self.waiting_room.get_nowait()
        except:
            return None
    
    def get_next_admission_patient(self):
        """Get next patient from admission queue (FIFO)."""
        if self.admission_queue:
            return self.admission_queue.pop(0)
        return None