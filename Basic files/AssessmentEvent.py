import random
from Event import Event

class AssessmentEvent(Event):
    """Walk-in patient completes triage assessment"""
    
    def process(self, hospital):
        patient = self.patient
        hospital.triage_nurse_busy = False
        
        # Assign random priority 2-5
        patient.priority = random.randint(2, 5)
        patient.assessment_end_time = self.time
        
        print(f"Time {self.time:3d}: {patient.patient_id} assessment completed  (Priority now {patient.priority})")
        
        # Patient enters waiting room
        from EnterWaitingRoomEvent import EnterWaitingRoomEvent
        events = [EnterWaitingRoomEvent(self.time, patient)]
        
        # Check if another patient is waiting for assessment
        if hospital.can_start_assessment():
            hospital.triage_nurse_busy = True
            next_patient = hospital.assessment_queue.pop(0)
            wait_time = self.time - next_patient.assessment_start_time
            next_patient.wait_for_assessment = wait_time
            print(f"Time {self.time:3d}: {next_patient.patient_id} starts assessment (waited {wait_time})")
            events.append(AssessmentEvent(self.time + 4, next_patient))
        
        return events