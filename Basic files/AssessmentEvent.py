from Event import Event
import random

class AssessmentEvent(Event):
    """Event that occurs when assessment of a walk-in patient is completed."""
    
    def process(self, hospital):
        patient = self.patient
        hospital.triage_nurse_busy = False
        
        # Assign random priority 1-5
        patient.priority = random.randint(1, 5)
        patient.assessment_end_time = self.time
        patient.wait_for_assessment = self.time - patient.assessment_start_time
        
        print(f"Time {self.time}: {patient.patient_id} assessment completed  (Priority now {patient.priority})")
        
        # Move to waiting room
        from EnterWaitingRoomEvent import EnterWaitingRoomEvent
        new_events = [EnterWaitingRoomEvent(self.time, patient)]
        
        # Start next assessment if anyone waiting
        if hospital.assessment_queue and hospital.can_start_assessment():
            next_patient = hospital.get_next_assessment_patient()
            if next_patient:
                hospital.triage_nurse_busy = True
                next_patient.assessment_start_time = self.time
                print(f"Time {self.time}: {next_patient.patient_id} starts assessment (waited 0)")
                new_events.append(AssessmentEvent(self.time + 4, next_patient))
        
        return new_events