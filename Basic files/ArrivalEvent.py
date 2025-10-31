# Arrival event - when a patient arrives at the hospital

from Event import Event

class ArrivalEvent(Event):
    # Handles patient arrival at hospital
    
    def process(self, hospital):
        patient = self.patient
        
        # Track this patient in hospital
        hospital.add_patient(patient)
        
        # Determine patient type for printing
        patient_type = 'Emergency' if patient.patient_type == 'E' else 'Walk-In'
        print(f"Time {self.time:3d}: {patient.patient_id} ({patient_type}) arrives")
        
        # Load next arrival from file
        from Main import load_next_arrival
        load_next_arrival()
        
        new_events = []
        
        if patient.patient_type == 'E':
            # Emergency patients skip assessment, go directly to waiting room
            from EnterWaitingRoomEvent import EnterWaitingRoomEvent
            new_events.append(EnterWaitingRoomEvent(self.time, patient))
        else:
            # Walk-in patients must go through assessment first
            hospital.assessment_queue.append(patient)
            patient.assessment_start_time = self.time
            
            # If triage nurse is available, start assessment immediately
            if hospital.can_start_assessment():
                from AssessmentEvent import AssessmentEvent
                hospital.triage_nurse_busy = True
                
                # Get the patient to assess (this one we just added)
                patient_to_assess = hospital.get_next_assessment_patient()
                
                if patient_to_assess:
                    # Calculate wait time (should be 0 on arrival)
                    wait = self.time - patient_to_assess.arrival_time
                    print(f"Time {self.time:3d}: {patient_to_assess.patient_id} starts assessment (waited {wait})")
                    new_events.append(AssessmentEvent(self.time + 4, patient_to_assess))
        
        return new_events