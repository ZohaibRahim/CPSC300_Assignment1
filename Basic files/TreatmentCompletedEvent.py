from Event import Event

class TreatmentCompletedEvent(Event):
    #Patient completes treatment
    
    def process(self, hospital):
        patient = self.patient
        patient.treatment_end_time = self.time
        
        print(f"Time {self.time}: {patient.patient_id} (Priority {patient.priority}) finishes treatment")
        
        new_events = []
        
        if patient.priority == 1:
            # Priority 1 patients need admission
            hospital.add_to_admission_queue(patient)
            patient.admission_queue_entry_time = self.time
            
            # If admission nurse is free, start admission
            if not hospital.admission_nurse_busy:
                # Pop from queue
                next_patient = hospital.get_next_admission_patient()  
                if next_patient:
                    hospital.admission_nurse_busy = True
                    from AdmissionEvent import AdmissionEvent
                    new_events.append(AdmissionEvent(self.time + 3, next_patient))
        else:
            # Lower priority patients depart immediately
            from DepartureEvent import DepartureEvent
            new_events.append(DepartureEvent(self.time + 1, patient))
            
        return new_events