# Main simulation driver

from queue import PriorityQueue
from Patient import Patient
from Hospital import Hospital
from ArrivalEvent import ArrivalEvent
import random

# Global variables
patient_id_counter = 28064212
input_file = None
event_queue = None

def load_next_arrival():
    # Load the next patient arrival from input file
    global patient_id_counter, input_file, event_queue
    
    if input_file is None:
        return
    
    line = input_file.readline()
    if not line:
        return
    
    # Parse the input line
    parts = line.strip().split()
    arrival_time = int(parts[0])
    patient_type = parts[1]  # 'E' or 'W'
    treatment_time = int(parts[2])
    
    # Create new patient and arrival event
    patient = Patient(patient_id_counter, arrival_time, patient_type, treatment_time)
    arrival_event = ArrivalEvent(arrival_time, patient)
    event_queue.put(arrival_event)
    
    patient_id_counter += 1

def print_statistics(hospital):
    # Print final statistics matching the expected format
    print("\n...All events complete.  Final Summary:\n")
    
    # Sort patients by priority, then by patient_id
    sorted_patients = sorted(hospital.all_patients, key=lambda p: (p.priority or 999, p.patient_id))
    
    # Print header
    print(" Patient Priority   Arrival Assessment   Treatment   Departure  Waiting")
    print("  Number               Time       Time    Required        Time     Time")
    print("-----------------------------------------------------------------------")
    
    # Print each patient's statistics
    total_wait = 0
    
    for patient in sorted_patients:
        priority = patient.priority
        arrival = patient.arrival_time
        assessment = patient.assessment_end_time if patient.assessment_end_time else patient.arrival_time
        treatment_req = patient.treatment_time
        departure = patient.departure_time
        waiting = patient.total_waiting_time()
        
        total_wait += waiting
        
        # Format output to match expected format
        print(f"{patient.patient_id:>8} {priority:>8} {arrival:>8} {assessment:>10} {treatment_req:>10} {departure:>10} {waiting:>8}")
    
    # Print summary statistics
    num_patients = len(hospital.all_patients)
    avg_wait = total_wait / num_patients if num_patients > 0 else 0
    
    print("\n")
    print(f"Patients seen in total: {num_patients}")
    print(f"Average waiting time per patient : {avg_wait:.6f}")

def main():
    global input_file, event_queue
    
    # CRITICAL: Set random seed FIRST before anything else
    random.seed(1)
    
    # Get input file from user
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
    
    # Load first arrival from file
    load_next_arrival()
    
    # Main simulation loop - process events until none remain
    while not event_queue.empty():
        # Get next event from queue
        event = event_queue.get()
        
        # Process the event (generate new events)
        new_events = event.process(hospital)
        
        # Add any newly generated events to the queue
        if new_events:
            for new_event in new_events:
                event_queue.put(new_event)
        
        # Try to load next arrival from file
        load_next_arrival()
    
    input_file.close()
    
    # Print final statistics
    print_statistics(hospital)

if __name__ == "__main__":
    main()