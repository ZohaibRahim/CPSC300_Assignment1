from Event import Event

class AdmissionEvent(Event):
    """Event that occurs when a Priority 1 patient is admitted to the hospital."""
    
    def process(self, hospital):
        patient = self.patient
        hospital.admission_nurse_busy = False
        
        # Calculate admission wait time
        patient.wait_for_admission = self.time - patient.admission_queue_entry_time - 3
        
        print(f"Time {self.time}: {patient.patient_id} (Priority {patient.priority}, waited {patient.wait_for_admission}) admitted to Hospital")
        
        new_events = []
        
        # Schedule departure immediately
        from DepartureEvent import DepartureEvent
        new_events.append(DepartureEvent(self.time, patient))
        
        # Schedule next admission if patients waiting
        if hospital.admission_queue:
            next_patient = hospital.get_next_admission_patient()
            if next_patient:
                hospital.admission_nurse_busy = True
                new_events.append(AdmissionEvent(self.time + 3, next_patient))
        
        return new_events