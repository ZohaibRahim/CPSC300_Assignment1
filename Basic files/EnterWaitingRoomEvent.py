from Event import Event

class EnterWaitingRoomEvent(Event):
    """Event that occurs when a patient enters the waiting room."""
    
    def process(self, hospital):
        patient = self.patient
        
        # Print FIRST - this must always happen
        print(f"Time {self.time}: {patient.patient_id} (Priority {patient.priority}) enters waiting room")
        
        # Add to waiting room
        hospital.add_to_waiting_room(patient)
        
        new_events = []
        
        # If treatment room available, start treatment immediately
        if hospital.rooms_available > 0:
            next_patient = hospital.get_next_from_waiting_room()
            if next_patient:
                from StartTreatmentEvent import StartTreatmentEvent
                new_events.append(StartTreatmentEvent(self.time, next_patient))
                hospital.rooms_available -= 1
        
        return new_events