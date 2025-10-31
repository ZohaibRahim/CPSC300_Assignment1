from Event import Event

class EnterWaitingRoomEvent(Event):
    # Handles patient entering the waiting room for treatment
    
    def process(self, hospital):
        patient = self.patient
        
        # Print that patient entered waiting room
        print(f"Time {self.time}: {patient.patient_id} (Priority {patient.priority}) enters waiting room")
        
        # Add patient to waiting room priority queue
        hospital.add_to_waiting_room(patient)
        
        new_events = []
        
        # Check if treatment room is available
        if hospital.rooms_available > 0:
            next_patient = hospital.get_next_from_waiting_room()
            if next_patient:
                # Immediately start treatment
                from StartTreatmentEvent import StartTreatmentEvent
                new_events.append(StartTreatmentEvent(self.time, next_patient))
                hospital.rooms_available -= 1
        
        return new_events