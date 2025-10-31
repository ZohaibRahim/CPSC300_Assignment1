from Event import Event

class AdmissionEvent(Event):
    """Priority 1 patient is admitted to hospital (completes at this time)"""
    
    def process(self, hospital):
        patient = self.patient
        hospital.admission_nurse_busy = False
        
        print(f"Time {self.time}: {patient.patient_id} (Priority {patient.priority}) admitted to hospital")
        
        # Depart at same time
        from DepartureEvent import DepartureEvent
        events = [DepartureEvent(self.time, patient)]
        
        # Check if another patient waiting for admission
        if hospital.can_start_admission():
            hospital.admission_nurse_busy = True
            next_patient = hospital.admission_queue.pop(0)
            wait_time = self.time - next_patient.treatment_end_time
            next_patient.wait_for_admission = wait_time
            
            events.append(AdmissionEvent(self.time + 3, next_patient))
        
        return events