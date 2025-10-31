
# Global list for all patient objects (used in final reporting)
all_patients_list = []

class Patient:
    """
    Represents a patient moving through the emergency room simulation.
    """
    NEXT_ID = 28064212  # Start ID per assignment spec

    def __init__(self, arrival_time, p_type, treatment_time):
        self.id = Patient.NEXT_ID
        Patient.NEXT_ID += 1

        self.arrival_time = arrival_time
        self.type = p_type  # 'E' (Emergency) or 'W' (Walk-in)
        self.treatment_time = treatment_time

        # Assigned later
        self.priority = None
        self.treatment_room_id = None

        # Waiting-time tracking
        self.assessment_wait_start = None
        self.treatment_wait_start = None
        self.admission_wait_start = None
        self.total_wait_time = 0
        self.departure_time = None

        # Automatically register this patient globally
        all_patients_list.append(self)

    def __repr__(self):
        return (f"Patient({self.id}, Type: {self.type}, "
                f"Priority: {self.priority or 'N/A'}, "
                f"T_Time: {self.treatment_time})")
