from Event import Event

class StartTreatmentEvent(Event):
    """Event that occurs when a patient starts treatment."""
    
    def process(self, hospital):
        patient = self.patient
        patient.treatment_start_time = self.time
        
        # Calculate wait time WHEN TREATMENT STARTS
        if patient.assessment_end_time:
            # Walk-in patient - wait is from assessment completion to treatment start
            patient.wait_for_treatment = self.time - patient.assessment_end_time
        else:
            # Emergency patient - no wait
            patient.wait_for_treatment = 0
        
        print(f"Time {self.time}: {patient.patient_id} (Priority {patient.priority}) starts treatment (waited {patient.wait_for_treatment}, {hospital.rooms_available} rm(s) remain)")
        
        # Schedule treatment completion
        from TreatmentCompletedEvent import TreatmentCompletedEvent
        return [TreatmentCompletedEvent(self.time + patient.treatment_time, patient)]