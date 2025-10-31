from Event import Event

class ArrivalEvent(Event):
    """Patient arrives at hospital"""
    
    def process(self, hospital):
        patient = self.patient
        hospital.all_patients.append(patient)
        
        # Print arrival with proper formatting
        patient_type = 'Emergency' if patient.patient_type == 'E' else 'Walk-In'
        print(f"Time {self.time:3d}: {patient.patient_id} ({patient_type}) arrives")
        
        # Load next arrival from file if not at end
        from Main import load_next_arrival
        load_next_arrival(hospital)
        
        if patient.patient_type == 'E':
            # Emergency patients skip assessment, go to waiting room
            from EnterWaitingRoomEvent import EnterWaitingRoomEvent
            return [EnterWaitingRoomEvent(self.time, patient)]
        else:
            # Walk-in patients join assessment queue
            hospital.assessment_queue.append(patient)
            patient.assessment_start_time = self.time
            
            # Start assessment if nurse is available
            if hospital.can_start_assessment():
                from AssessmentEvent import AssessmentEvent
                hospital.triage_nurse_busy = True
                patient_being_assessed = hospital.assessment_queue.pop(0)
                wait_time = self.time - patient_being_assessed.assessment_start_time
                patient_being_assessed.wait_for_assessment = wait_time
                print(f"Time {self.time:3d}: {patient_being_assessed.patient_id} starts assessment (waited {wait_time})")
                return [AssessmentEvent(self.time + 4, patient_being_assessed)]
            
            return []