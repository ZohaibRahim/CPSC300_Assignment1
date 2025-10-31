
all_patients_list = []     # Global list for all patient objects (used in final reporting)

class Patient:
    """
    Represents a patient moving through the emergency room simulation.
    """

    NEXT_ID = 28064212    # Class variable to ensure IDs start at 28064212 and increment globally

    def __init__(self, arrival_time, p_type, treatment_time):
        # Data Read from File
        self.id = Patient.NEXT_ID
        Patient.NEXT_ID += 1

        self.arrival_time = arrival_time
        self.type = p_type  # 'E' (Emergency) or 'W' (Walk-in)
        self.treatment_time = treatment_time # Time required in treatment room

        # Data Assigned Later by Triage/Assessment
        self.priority = None  # 1 (highest) to 5 (lowest)
        self.treatment_room_id = None # Which room they are in (optional for A)

        # Waiting Time Tracking (for Role D's final report)
        self.assessment_wait_start = None
        self.treatment_wait_start = None
        self.admission_wait_start = None

        self.total_wait_time = 0
        self.departure_time = None

    def __repr__(self):
        return (f"Patient({self.id}, Type: {self.type}, Priority: {self.priority or 'N/A'}, "
                f"T_Time: {self.treatment_time})")
