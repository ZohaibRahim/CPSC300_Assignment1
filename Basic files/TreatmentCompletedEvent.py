from Event import Event
from AdmissionEvent import AdmissionEvent
from DepartureEvent import DepartureEvent

class TreatmentCompletedEvent(Event):
    """Patient completes treatment"""
    
    def process(self, hospital):
        patient = self.patient
        print(f"Time {self.time}: {patient.patient_id} (Priority {patient.priority}) finishes treatment")
        
        new_events = []
        
        if patient.priority == 1:
            # Priority 1 patients need admission
            hospital.add_to_admission_queue(patient)
            
            # If admission nurse is free and this is first in queue, start admission
            if not hospital.admission_nurse_busy:
                patient_to_admit = hospital.get_next_admission_patient()
                if patient_to_admit:
                    hospital.admission_nurse_busy = True
                    new_events.append(AdmissionEvent(self.time + 3, patient_to_admit))
        else:
            # Lower priority patients depart after 1 time unit
            new_events.append(DepartureEvent(self.time + 1, patient))
            
        return new_events