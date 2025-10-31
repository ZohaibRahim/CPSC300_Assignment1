from Read_file import read_next_arrival
from queue import PriorityQueue
from Patient import Patient

event_list = []
waiting_room = PriorityQueue()
patient_id_counter = 28064212


def add_event_in_order(event):
    index = 0
    while index < len(event_list) and event_list[index][0] <= event[0]:
        index += 1
    event_list.insert(index, event)


with open('data1.txt', 'r') as file:

    first_event = read_next_arrival(file, patient_id_counter)
    if first_event:
        add_event_in_order(first_event)
        patient_id_counter += 1

    while event_list:
        current_event = event_list.pop(0)
        current_time = current_event[0]
        event_type = current_event[1]
        patient = current_event[2]

        print(f"\nProcessing {event_type} for Patient ID {patient.patient_id} (Type: {patient.patient_type}) at time {current_time}")

        # Arrival event
        if event_type == 'arrival':
            waiting_room.put(patient)
            if waiting_room.qsize() == 1:
                departure_time = current_time + patient.treatment_time + 1
                departure_event = (departure_time, 'departure', patient)
                add_event_in_order(departure_event)

        # Departure event
        elif event_type == 'departure':
            waiting_room.get()
            if not waiting_room.empty():
                next_patient = waiting_room.queue[0]
                next_departure_time = current_time + next_patient.treatment_time + 1
                next_departure_event = (next_departure_time, 'departure', next_patient)
                add_event_in_order(next_departure_event)

        # Read next arrival after processing current event
        next_event = read_next_arrival(file, patient_id_counter)
        if next_event:
            add_event_in_order(next_event)
            patient_id_counter += 1

        # Debug print statements
        print("Events in queue:")
        for event in event_list:
            e_time, e_type, e_patient = event
            print(f"  Time {e_time} - {e_type} - Patient {e_patient.patient_id} (Type: {e_patient.patient_type})")

        print("Waiting room queue:")
        for p in waiting_room.queue:
            print(f"  Patient {p.patient_id} (Priority: {p.priority}, Type: {p.patient_type})")
