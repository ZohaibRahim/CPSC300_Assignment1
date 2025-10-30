from Read_file import read_next_arrival
from queue import PriorityQueue
from Patient import Patient
#made global variables to keep tracking of important variables
event_list = []
waiting_room = PriorityQueue()
departure_time = 0
departure_event = []
patient_id_counter = 28064212


#a function to arrange our event_list based on time (earliest to so on)
def add_event_in_order(event):
    index = 0
    while index < len(event_list) and event_list[index][0] <= event[0]:
        index += 1
    event_list.insert(index, event)

#opens up the file using our function from read_file.py , making the program modular
with open('data1.txt', 'r') as file:

    first_event = read_next_arrival(file, patient_id_counter)
    if first_event:
        add_event_in_order(first_event)
        patient_id_counter += 1
    
    #a loop that goes through all the indexes of event_list
    while event_list:
        current_event = event_list.pop(0)
        #taking the data from the tuple and assigning it the meaningful names
        current_time = current_event[0]
        event_type = current_event[1]
        patient_id = current_event[2]
        
        #condition the check if the event type is an arrival or departure
        if event_type == 'arrival':        
            waiting_room.put(current_event)
            if waiting_room.qsize() == 1:
                departure_time = current_time + current_event[3] + 1
                departure_event = (departure_time, 'departure', patient_id, current_event[3], current_event[4])
                add_event_in_order(departure_event)
                
        #condition to deal with departures
        elif event_type == 'departure':
            waiting_room.get()
            if not waiting_room.empty():
                next_patient = waiting_room.queue[0]
                next_departure_time = current_time + next_patient[3] + 1
                next_departure_event = (next_departure_time, 'departure', next_patient[2], next_patient[3], next_patient[4])
                add_event_in_order(next_departure_event)                
        
        # Read next arrival after each event processed
        next_event = read_next_arrival(file, patient_id_counter)
        if next_event:
            add_event_in_order(next_event)
            patient_id_counter += 1
        print(event_list)
                
