from Event import Event

class TreatmentCompletedEvent(Event):
    """Patient completes treatment"""
    
    def process(self, hospital):
        patient = self.patient
        patient.treatment_end_time = self.time
        
        print(f"Time {self.time}: {patient.patient_id} (Priority {patient.priority}) treatment completed")
        
        if patient.priority == 1:
            # Priority 1 goes to admission queue
            hospital.admission_queue.append(patient)
            
            # Start admission if nurse available
            if hospital.can_start_admission():
                from AdmissionEvent import AdmissionEvent
                hospital.admission_nurse_busy = True
                patient_to_admit = hospital.admission_queue.pop(0)
                wait_time = self.time - patient_to_admit.treatment_end_time
                patient_to_admit.wait_for_admission = wait_time
                
                return [AdmissionEvent(self.time + 3, patient_to_admit)]
            return []
        else:
            # Priority 2-5 depart after 1 time unit
            from DepartureEvent import DepartureEvent
            return [DepartureEvent(self.time + 1, patient)]