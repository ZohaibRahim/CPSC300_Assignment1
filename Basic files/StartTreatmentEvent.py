from Event import Event

class StartTreatmentEvent(Event):
    # Handles patient starting treatment in a treatment room
    
    def process(self, hospital):
        patient = self.patient
        patient.treatment_start_time = self.time
        
        # Calculate wait time for treatment
        if patient.assessment_end_time:
            # Walk-in patient: wait is from assessment end to treatment start
            patient.wait_for_treatment = self.time - patient.assessment_end_time
        else:
            # Emergency patient: no wait
            patient.wait_for_treatment = 0
        
        # Print treatment start
        print(f"Time {self.time}: {patient.patient_id} (Priority {patient.priority}) starts treatment (waited {patient.wait_for_treatment}, {hospital.rooms_available} rm(s) remain)")
        
        # Schedule when treatment will be completed
        from TreatmentCompletedEvent import TreatmentCompletedEvent
        return [TreatmentCompletedEvent(self.time + patient.treatment_time, patient)]