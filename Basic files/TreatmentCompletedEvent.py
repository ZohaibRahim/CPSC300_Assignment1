from Event import Event

class TreatmentCompletedEvent(Event):
    """Event that occurs when a patient's treatment is completed."""
    
    def process(self, hospital):
        patient = self.patient
        patient.treatment_end_time = self.time
        
        print(f"Time {self.time}: {patient.patient_id} (Priority {patient.priority}) finishes treatment")
        
        new_events = []
        
        # Priority 1 patients go to admission queue
        if patient.priority == 1:
            patient.admission_queue_entry_time = self.time
            hospital.admission_queue.append(patient)
            
            # If admission nurse is free, start admission immediately
            if not hospital.admission_nurse_busy:
                hospital.admission_nurse_busy = True
                from AdmissionEvent import AdmissionEvent
                new_events.append(AdmissionEvent(self.time + 3, patient))
        else:
            # Priority 2-5 patients depart after 1 time unit
            from DepartureEvent import DepartureEvent
            new_events.append(DepartureEvent(self.time + 1, patient))
        
        return new_events