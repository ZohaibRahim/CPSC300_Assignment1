from read_file import read_next_arrival
from queue import PriorityQueue

event_list = []
waiting_room = PriorityQueue()
departure_time = 0
departure_event = []
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
        
        event_type = current_event[1]
        patient_id = current_event[2]
        current_time = current_event[0]
        
        print(f"\nProcessing {event_type} event for patient {patient_id} at time {current_time}")
        
        if event_type == 'arrival':
            print(f"Patient {patient_id} arrived, assessment time: {current_event[3]}, type: {current_event[4]}")
            waiting_room.put(current_event)
            if waiting_room.qsize() == 1:
                departure_time = current_time + current_event[3] + 1
                departure_event = (departure_time, 'departure', patient_id, current_event[3], current_event[4])
                add_event_in_order(departure_event)
                print(f"Starting treatment for patient {patient_id}, scheduled departure at time {departure_time}")

        elif event_type == 'departure':
            print(f"Patient {patient_id} treatment finished at {current_time}")
            waiting_room.get()
            if not waiting_room.empty():
                next_patient = waiting_room.queue[0]
                next_departure_time = current_time + next_patient[3] + 1
                next_departure_event = (next_departure_time, 'departure', next_patient[2], next_patient[3], next_patient[4])
                add_event_in_order(next_departure_event)
                print(f"Starting treatment for next patient {next_patient[2]}, scheduled departure at time {next_departure_time}")
        
        # Read next arrival after each event processed
        next_event = read_next_arrival(file, patient_id_counter)
        if next_event:
            add_event_in_order(next_event)
            patient_id_counter += 1
            print(f"Next patient {next_event[2]} scheduled to arrive at time {next_event[0]}")

                
