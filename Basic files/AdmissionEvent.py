from Event import Event

class AdmissionEvent(Event):
    # Handles admission of Priority 1 patient to hospital (takes 3 time units)
    
    def process(self, hospital):
        patient = self.patient
        
        # Admission nurse is now free
        hospital.admission_nurse_busy = False
        
        # Calculate how long patient waited for admission
        # Wait is from when treatment ended until admission starts minus the 3 time units for admission
        patient.wait_for_admission = self.time - patient.admission_queue_entry_time - 3
        
        # Print admission
        print(f"Time {self.time}: {patient.patient_id} (Priority {patient.priority}, waited {patient.wait_for_admission}) admitted to Hospital")
        
        new_events = []
        
        # Schedule immediate departure
        from DepartureEvent import DepartureEvent
        new_events.append(DepartureEvent(self.time, patient))
        
        # Check if more Priority 1 patients waiting for admission
        if hospital.admission_queue:
            next_patient = hospital.get_next_admission_patient()
            if next_patient:
                hospital.admission_nurse_busy = True
                new_events.append(AdmissionEvent(self.time + 3, next_patient))
        
        return new_events