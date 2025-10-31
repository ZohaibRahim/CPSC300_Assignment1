from Event import Event

class AdmissionEvent(Event):
    """Patient completes admission process"""
    
    def process(self, hospital):
        patient = self.patient
        hospital.admission_nurse_busy = False
        
        print(f"Time {self.time}: {patient.patient_id} (Priority {patient.priority}) admitted to Hospital")
        
        new_events = []
        
        # Schedule departure immediately (admission complete)
        from DepartureEvent import DepartureEvent
        new_events.append(DepartureEvent(self.time, patient))
        
        # Schedule next admission if patients waiting
        if hospital.admission_queue:
            next_patient = hospital.get_next_admission_patient()
            if next_patient:
                hospital.admission_nurse_busy = True
                new_events.append(AdmissionEvent(self.time + 3, next_patient))
        
        return new_events