from Event import Event

class DepartureEvent(Event):
    
    def process(self, hospital):
        patient = self.patient
        # Free up treatment room
        hospital.rooms_available += 1
        print(f"Time {self.time}: {patient.patient_id} (Priority {patient.priority}) departs, {hospital.rooms_available} rm(s) remain")
        
        # Record departure time for statistics
        patient.departure_time = self.time
        
        # If patients waiting and room now available, start next treatment
        new_events = []
        if not hospital.waiting_room.empty() and hospital.rooms_available > 0:
            next_patient = hospital.get_next_from_waiting_room()
            if next_patient:
                hospital.rooms_available -= 1
                from StartTreatmentEvent import StartTreatmentEvent
                new_events.append(StartTreatmentEvent(self.time, next_patient))
        
        return new_events