from queue import PriorityQueue
from Patient import Patient
from Hospital import Hospital
from ArrivalEvent import ArrivalEvent

# Global variables
patient_id_counter = 28064212
input_file = None

def load_next_arrival(hospital):
    """Load the next arrival event from file (only 1 arrival in queue at a time)"""
    global patient_id_counter, input_file, event_queue
    
    if input_file is None:
        return
    
    line = input_file.readline()
    if not line:
        # End of file
        return
    
    # Parse arrival data
    parts = line.strip().split()
    arrival_time = int(parts)
    patient_type = parts
    treatment_time = int(parts)
    
    # Create patient and arrival event
    patient = Patient(patient_id_counter, arrival_time, patient_type, treatment_time)
    arrival_event = ArrivalEvent(arrival_time, patient)
    
    event_queue.put(arrival_event)
    patient_id_counter += 1

def print_statistics(hospital):
    """Print final statistics table"""
    print("\n" + "="*60)
    print("FINAL STATISTICS")
    print("="*60)
    print(f"{'Patient ID':<15} {'Total Wait Time':<20}")
    print("-"*60)
    
    total_wait = 0
    for patient in hospital.all_patients:
        wait = patient.total_waiting_time()
        total_wait += wait
        print(f"{patient.patient_id:<15} {wait:<20}")
    
    print("-"*60)
    num_patients = len(hospital.all_patients)
    avg_wait = total_wait / num_patients if num_patients > 0 else 0
    
    print(f"\nTotal patients: {num_patients}")
    print(f"Average waiting time: {avg_wait:.2f} time units")
    print("="*60)

def main():
    global input_file, event_queue
    
    # Get input file
    filename = input("Please enter input file name: ")
    
    try:
        input_file = open(filename, 'r')
    except FileNotFoundError:
        print(f"Error: Could not find file '{filename}'")
        return
    
    # Initialize simulation
    hospital = Hospital()
   
