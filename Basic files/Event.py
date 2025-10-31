from Event import Event

class EnterWaitingRoomEvent(Event):
    """Patient enters waiting room and waits for treatment"""
    
    def process(self, hospital):
        patient = self.patient
        priority_text = f"Priority {patient.priority}" if patient.priority else ""
        print(f"Time {self.time:3d}: {patient.patient_id} ({priority_text}) enters waiting room")
        
        # Add to waiting room priority queue
        hospital.waiting_room.put(patient)
        patient.waiting_room_enter_time = self.time
        
        # Try to start treatment if room available
        if hospital.can_start_treatment():
            from StartTreatmentEvent import StartTreatmentEvent
            next_patient = hospital.waiting_room.get()
            wait_time = self.time - next_patient.waiting_room_enter_time
            next_patient.wait_for_treatment = wait_time
            next_patient.treatment_start_time = self.time
            
            hospital.available_treatment_rooms -= 1
            rooms_text = hospital.get_available_rooms_text()
            
            print(f"Time {self.time:3d}: {next_patient.patient_id} (Priority {next_patient.priority}) starts treatment (waited {wait_time}, {rooms_text})")
            
            return [StartTreatmentEvent(self.time, next_patient)]
        
        return []