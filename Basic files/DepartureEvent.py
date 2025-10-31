from Event import Event

class DepartureEvent(Event):
    """Patient leaves the hospital"""
    
    def process(self, hospital):
        patient = self.patient
        patient.departure_time = self.time
        
        # Free up treatment room
        hospital.available_treatment_rooms += 1
        rooms_text = hospital.get_available_rooms_text()
        
        # Changed format from "(X rooms still available)" to "X rm(s) remain"
        print(f"Time {self.time:3d}: {patient.patient_id} (Priority {patient.priority}) departs, {rooms_text}")
        
        # Try to start treatment for next waiting patient
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