# Assessment completion event - when a walk-in assessment is complete

from Event import Event
import random

class AssessmentEvent(Event):
    # Handles completion of walk-in patient assessment (takes 4 time units)
    
    def process(self, hospital):
        patient = self.patient
        
        # Triage nurse is now free
        hospital.triage_nurse_busy = False
        
        # Assign random priority (1-5) to this walk-in patient
        patient.priority = random.randint(1, 5)
        patient.assessment_end_time = self.time
        patient.wait_for_assessment = self.time - patient.assessment_start_time
        
        # Print assessment completion
        print(f"Time {self.time}: {patient.patient_id} assessment completed  (Priority now {patient.priority})")
        
        new_events = []
        
        # Move completed patient to waiting room
        from EnterWaitingRoomEvent import EnterWaitingRoomEvent
        new_events.append(EnterWaitingRoomEvent(self.time, patient))
        
        # Check if more patients waiting for assessment
        if hospital.assessment_queue and hospital.can_start_assessment():
            next_patient = hospital.get_next_assessment_patient()
            if next_patient:
                hospital.triage_nurse_busy = True
                next_patient.assessment_start_time = self.time
                
                # Calculate wait (how long patient waited for assessment to start)
                wait = self.time - next_patient.arrival_time
                print(f"Time {self.time}: {next_patient.patient_id} starts assessment (waited {wait})")
                
                new_events.append(AssessmentEvent(self.time + 4, next_patient))
        
        return new_events