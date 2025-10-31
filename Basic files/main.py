from queue import PriorityQueue
from Patient import Patient
from Hospital import Hospital
from ArrivalEvent import ArrivalEvent
import random  # ADDED

# Global variables
patient_id_counter = 28064212
input_file = None
event_queue = None

def load_next_arrival():
    """Load the next arrival event from file (only 1 arrival in queue at a time)."""
    global patient_id_counter, input_file, event_queue
    
    if input_file is None:
        return
    
    line = input_file.readline()
    if not line:
        return
    
    # Parse arrival data
    parts = line.strip().split()
    arrival_time = int(parts[0])
    patient_type = parts[1]
    treatment_time = int(parts[2])
    
    # Create patient and arrival event
    patient = Patient(patient_id_counter, arrival_time, patient_type, treatment_time)
    arrival_event = ArrivalEvent(arrival_time, patient)
    event_queue.put(arrival_event)
    
    patient_id_counter += 1

def print_statistics(hospital):
    """Print final statistics table matching assignment format."""
    print("\n...All events complete.  Final Summary:\n")
    
    # Sort patients by priority, then by patient_id
    sorted_patients = sorted(hospital.all_patients, key=lambda p: (p.priority or 999, p.patient_id))
    
    # Header (exact match to model)
    print(" Patient Priority   Arrival Assessment   Treatment   Departure  Waiting")
    print("  Number               Time       Time    Required        Time     Time")
    print("-----------------------------------------------------------------------")
    
    # Patient data
    total_wait = 0
    
    for patient in sorted_patients:
        priority = patient.priority
        arrival = patient.arrival_time
        assessment = patient.assessment_end_time if patient.assessment_end_time else patient.arrival_time
        treatment_req = patient.treatment_time
        departure = patient.departure_time
        waiting = patient.total_waiting_time()
        
        total_wait += waiting
        
        # Format to match model exactly
        print(f"{patient.patient_id:>8} {priority:>8} {arrival:>8} {assessment:>10} {treatment_req:>10} {departure:>10} {waiting:>8}")
    
    # Summary statistics
    num_patients = len(hospital.all_patients)
    avg_wait = total_wait / num_patients if num_patients > 0 else 0
    
    print("\n")
    print(f"Patients seen in total: {num_patients}")
    print(f"Average waiting time per patient : {avg_wait:.6f}")

def main():
    global input_file, event_queue
    
    # CRITICAL: Set random seed first
    random.seed(1)
    
    # Get input file
    filename = input("Please enter input file name: ")
    try:
        input_file = open(filename, 'r')
    except FileNotFoundError:
        print(f"Error: Could not find file '{filename}'")
        return
    
    # Initialize simulation
    hospital = Hospital()
    event_queue = PriorityQueue()
    
    print("\nSimulation begins...\n")
    
    # Load first arrival
    load_next_arrival()
    
    # Main simulation loop
    while not event_queue.empty():
        event = event_queue.get()
        new_events = event.process(hospital)
        
        # Schedule any new events generated
        if new_events:
            for new_event in new_events:
                event_queue.put(new_event)
        
        # Load next arrival after processing current event
        load_next_arrival()
    
    input_file.close()
    
    # Print statistics
    print_statistics(hospital)

if __name__ == "__main__":
    main()