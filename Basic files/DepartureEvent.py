from Event import Event

class DepartureEvent(Event):
    # Handles patient departure from hospital
    
    def process(self, hospital):
        patient = self.patient
        patient.departure_time = self.time
        
        # Free up the treatment room
        hospital.rooms_available += 1
        
        # Print departure
        print(f"Time {self.time}: {patient.patient_id} (Priority {patient.priority}) departs, {hospital.rooms_available} rm(s) remain")
        
        new_events = []
        
        # If patients waiting for treatment and room is now available, start next treatment
        if not hospital.waiting_room.empty() and hospital.rooms_available > 0:
            next_patient = hospital.get_next_from_waiting_room()
            if next_patient:
                hospital.rooms_available -= 1
                from StartTreatmentEvent import StartTreatmentEvent
                new_events.append(StartTreatmentEvent(self.time, next_patient))
        
        return new_events