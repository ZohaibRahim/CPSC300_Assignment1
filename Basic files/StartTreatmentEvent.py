from Event import Event

class StartTreatmentEvent(Event):
    """Patient starts receiving treatment"""
    
    def process(self, hospital):
        patient = self.patient
        
        # Treatment completes in the future
        from TreatmentCompletedEvent import TreatmentCompletedEvent
        complete_time = self.time + patient.treatment_time
        
        return [TreatmentCompletedEvent(complete_time, patient)]