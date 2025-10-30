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
        print("Processing event:", current_event)

        if(current_event[1] == 'arrival'):
            waiting_room.put(current_event)
            departure_time = current_event[0] + current_event[3] + 1
            departure_event = (departure_time, 'departure', current_event[2], current_event[3], current_event[4])
            
            add_event_in_order(departure_event)

