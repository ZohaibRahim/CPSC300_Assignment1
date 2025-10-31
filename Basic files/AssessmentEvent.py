from Event import Event
import random

class AssessmentEvent(Event):
    
    def process(self, hospital):
        patient = self.patient
        hospital.triage_nurse_busy = False
        
        # Assign random priority 1-5
        patient.priority = random.randint(1, 5)
        patient.assessment_end_time = self.time
        
        print(f"Time {self.time}: {patient.patient_id} assessment completed (Priority now {patient.priority})")
        
        # Move to waiting room
        hospital.add_to_waiting_room(patient)
        
        new_events = []
        
        # Start next assessment if anyone waiting
        if hospital.assessment_queue and hospital.can_start_assessment():
            next_patient = hospital.get_next_assessment_patient()
            if next_patient:
                hospital.triage_nurse_busy = True
                next_patient.wait_for_assessment += self.time - next_patient.assessment_start_time
                print(f"Time {self.time}: {next_patient.patient_id} starts assessment (waited {next_patient.wait_for_assessment})")
                new_events.append(AssessmentEvent(self.time + 4, next_patient))
        
        # Check if treatment room available
        if not hospital.waiting_room.empty() and hospital.rooms_available > 0:
            next_patient = hospital.get_next_from_waiting_room()
            if next_patient:
                hospital.rooms_available -= 1
                from StartTreatmentEvent import StartTreatmentEvent
                new_events.append(StartTreatmentEvent(self.time, next_patient))
        
        return new_events