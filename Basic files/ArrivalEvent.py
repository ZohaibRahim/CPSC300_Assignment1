from Event import Event

class ArrivalEvent(Event):
    """Event that occurs when a patient arrives at the hospital."""
    
    def process(self, hospital):
        patient = self.patient
        
        # Add to hospital tracking
        hospital.add_patient(patient)
        
        # Print arrival
        patient_type = 'Emergency' if patient.patient_type == 'E' else 'Walk-In'
        print(f"Time {self.time:3d}: {patient.patient_id} ({patient_type}) arrives")
        
        # Load next arrival
        from Main import load_next_arrival
        load_next_arrival()
        
        new_events = []
        
        if patient.patient_type == 'E':
            # Emergency patients skip assessment, go straight to waiting room
            from EnterWaitingRoomEvent import EnterWaitingRoomEvent
            new_events.append(EnterWaitingRoomEvent(self.time, patient))
        else:
            # Walk-in patients join assessment queue
            hospital.assessment_queue.append(patient)
            patient.assessment_start_time = self.time
            
            # If nurse is available, start assessment immediately
            if hospital.can_start_assessment():
                from AssessmentEvent import AssessmentEvent
                hospital.triage_nurse_busy = True
                patient_being_assessed = hospital.get_next_assessment_patient()
                
                if patient_being_assessed:
                    print(f"Time {self.time:3d}: {patient_being_assessed.patient_id} starts assessment (waited 0)")
                    new_events.append(AssessmentEvent(self.time + 4, patient_being_assessed))
        
        return new_events