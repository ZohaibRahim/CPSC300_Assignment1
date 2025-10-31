from Event import Event

class EnterWaitingRoomEvent(Event):
    """Patient enters waiting room and waits for treatment"""
    
    def process(self, hospital):
        patient = self.patient
        print(f"Time {self.time}: {patient.patient_id} (Priority {patient.priority}) enters waiting room")
        
        # Add to waiting room
        hospital.add_to_waiting_room(patient)
        
        # If treatment room available, start treatment immediately
        new_events = []
        if hospital.rooms_available > 0:
            next_patient = hospital.get_next_from_waiting_room()
            if next_patient:
                from StartTreatmentEvent import StartTreatmentEvent
                new_events.append(StartTreatmentEvent(self.time, next_patient))
                hospital.rooms_available -= 1
        
        return new_events