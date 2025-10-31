# Hospital.py - Complete Hospital Simulation Manager

import random
from queue import PriorityQueue

class Hospital:
    """Manages the hospital simulation state"""
    
    def __init__(self):
        # Queues for different stages
        self.assessment_queue = []  # FIFO queue for walk-ins waiting for triage
        self.waiting_room = PriorityQueue()  # Priority queue for patients waiting for treatment
        self.admission_queue = []  # FIFO queue for priority 1 patients waiting for admission nurse
        
        # Resources
        self.available_treatment_rooms = 3
        self.triage_nurse_busy = False
        self.admission_nurse_busy = False
        
        # Tracking
        self.all_patients = []
        self.current_time = 0
        
        # Set random seed for consistent priority assignment
        random.seed(42)
    
    def get_available_rooms_text(self):
        """Return text showing available rooms in format 'X rm(s) remain'"""
        rooms = self.available_treatment_rooms
        if rooms == 1:
            return "1 rm(s) remain"
        else:
            return f"{rooms} rm(s) remain"
    
    def can_start_treatment(self):
        """Check if a patient can start treatment"""
        return self.available_treatment_rooms > 0 and not self.waiting_room.empty()
    
    def can_start_assessment(self):
        """Check if triage nurse is available and patients are waiting"""
        return not self.triage_nurse_busy and len(self.assessment_queue) > 0
    
    def can_start_admission(self):
        """Check if admission nurse is available and patients are waiting"""
        return not self.admission_nurse_busy and len(self.admission_queue) > 0