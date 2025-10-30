# arrival_manager.py

from patient import Patient
from events import Arrival

class ArrivalManager:
    """
    Manages the input file stream to enforce the 'only one pending Arrival event' rule.
    """
    def __init__(self, filename: str):
        try:
            self.file_stream = open(filename, 'r')
            # Read the very first line to prime the simulation
            self.pending_arrival_data = self._read_next_line()
        except FileNotFoundError:
            print(f"Error: Input file '{filename}' not found.")
            self.file_stream = None
            self.pending_arrival_data = None
            
        self.filename = filename

    def _read_next_line(self):
        """Internal helper to read and parse one valid line."""
        if not self.file_stream:
            return None
        
        while True:
            line = self.file_stream.readline()
            if not line:
                self.file_stream.close()
                self.file_stream = None
                return None # End of file

            try:
                # Expected format: time E|W treatment_time
                parts = line.strip().split()
                if len(parts) == 3:
                    time = int(parts[0])
                    p_type = parts[1].upper()
                    treat_time = int(parts[2])
                    return (time, p_type, treat_time)
                else:
                    # Skip improperly formatted lines
                    continue 
            except ValueError:
                # Skip lines with invalid numbers
                continue


    def get_next_arrival_event(self, schedule_func):
        # ... (lines 92-100 remain the same) ...
        if self.pending_arrival_data is None:
            return False # No more arrivals left

        arrival_time, p_type, treat_time = self.pending_arrival_data
        
        # 1. Create Patient
        new_patient = Patient(arrival_time, p_type, treat_time)

        # 2. Create Arrival Event
        arrival_event = Arrival(arrival_time, new_patient)

        # Schedule the event
        schedule_func(arrival_event)
        
        # Read the subsequent line to maintain the invariant
        self.pending_arrival_data = self._read_next_line()
        
        return True # Indicate an event was successfully scheduled