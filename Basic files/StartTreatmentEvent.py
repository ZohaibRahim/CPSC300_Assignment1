from Event import Event

class StartTreatmentEvent(Event):
    """Patient starts treatment"""
    
    def process(self, hospital):
        patient = self.patient
        patient.treatment_start_time = self.time
        
        print(f"Time {self.time}: {patient.patient_id} (Priority {patient.priority}) enters treatment room ({hospital.rooms_available} rm(s) remain)")
        
        # Schedule treatment completion
        from TreatmentCompletedEvent import TreatmentCompletedEvent
        return [TreatmentCompletedEvent(self.time + patient.treatment_time, patient)]