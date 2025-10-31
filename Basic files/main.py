from queue import PriorityQueue
from Patient import Patient
from Hospital import Hospital
from ArrivalEvent import ArrivalEvent

# Global variables
patient_id_counter = 28064212
input_file = None
event_queue = None

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
    arrival_time = int(parts[0])
    patient_type = parts[1]
    treatment_time = int(parts[2])
    
    # Create patient and arrival event
    patient = Patient(patient_id_counter, arrival_time, patient_type, treatment_time)
    arrival_event = ArrivalEvent(arrival_time, patient)
    
    event_queue.put(arrival_event)
    patient_id_counter += 1

def print_statistics(hospital):
    """Print final statistics table"""
    print("\n...All events complete.  Final Summary:\n")
    
    # Sort patients by priority, then by patient_id
    sorted_patients = sorted(hospital.all_patients, key=lambda p: (p.priority, p.patient_id))
    
    # Header
    print(f" {'Patient':<8} {'Priority':<10} {'Arrival':<10} {'Assessment':<12} {'Treatment':<10} {'Departure':<10} {'Waiting':<8}")
    print(f" {'Number':<8} {'':10} {'Time':<10} {'Time':<12} {'Required':<10} {'Time':<10} {'Time':<8}")
    print("-" * 80)
    
    # Patient data
    total_wait = 0
    for patient in sorted_patients:
        priority = patient.priority if patient.priority else "N/A"
        arrival = patient.arrival_time
        assessment = patient.assessment_end_time if patient.assessment_end_time else patient.arrival_time
        treatment_req = patient.treatment_time
        departure = patient.departure_time
        waiting = patient.total_waiting_time()
        
        total_wait += waiting
        
        print(f"{patient.patient_id:<8} {priority:<10} {arrival:<10} {assessment:<12} {treatment_req:<10} {departure:<10} {waiting:<8}")
    
    # Summary statistics
    num_patients = len(hospital.all_patients)
    avg_wait = total_wait / num_patients if num_patients > 0 else 0
    
    print("\n")
    print(f"Patients seen in total: {num_patients}")
    print(f"Average waiting time per patient : {avg_wait:.6f}")

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
    event_queue = PriorityQueue()
    
    print("\nSimulation begins...\n")
    
    # Load first arrival
    load_next_arrival(hospital)
    
    # Process all events
    while not event_queue.empty():
        event = event_queue.get()
        hospital.current_time = event.time
        
        # Process event and get new events it generates
        new_events = event.process(hospital)
        
        # Add new events to queue
        if new_events:
            for new_event in new_events:
                event_queue.put(new_event)
    
    input_file.close()
    
    # Print statistics
    print_statistics(hospital)

if __name__ == "__main__":
    main()