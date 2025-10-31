# Hospital.py - Complete Hospital Simulation Manager

from collections import deque
from queue import PriorityQueue
import random

class Hospital:
    """Manages the hospital simulation state"""
    
    def __init__(self):
        # Queue/tracking structures
        self.all_patients = []  # Track all patients for statistics
        self.assessment_queue = deque()  # FIFO for walk-in assessment
        self.waiting_room = PriorityQueue()  # Priority queue for treatment
        self.admission_queue = deque()  # FIFO for priority 1 admissions
        
        # Resources
        self.rooms_available = 3
        self.triage_nurse_busy = False
        self.admission_nurse_busy = False
        
        # Random seed for assessment priorities (matches model)
        random.seed(0)
    
    def add_patient(self, patient):
        """Add new patient to hospital tracking"""
        self.all_patients.append(patient)
    
    def can_start_assessment(self):
        """Check if triage nurse is available"""
        return not self.triage_nurse_busy
    
    def get_next_assessment_patient(self):
        """Get next patient from assessment queue"""
        if not self.assessment_queue:
            return None
        return self.assessment_queue.popleft()
    
    def add_to_waiting_room(self, patient):
        """Add patient to waiting room priority queue"""
        # Priority tuple: (priority, patient_id) - lower values sorted first
        priority_tuple = (patient.priority, patient.patient_id)
        self.waiting_room.put((priority_tuple, patient))
    
    def get_next_from_waiting_room(self):
        """Get highest priority patient from waiting room"""
        if self.waiting_room.empty():
            return None
        return self.waiting_room.get()[1]  # Return just the patient
    
    def add_to_admission_queue(self, patient):
        """Add priority 1 patient to admission queue"""
        self.admission_queue.append(patient)
    
    def get_next_admission_patient(self):
        """Get next patient waiting for admission"""
        if not self.admission_queue:
            return None
        return self.admission_queue.popleft()