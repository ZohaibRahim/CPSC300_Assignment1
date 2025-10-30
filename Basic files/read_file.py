
#Eventlist to keep track of all the incoming files

from main import event_list

#reading files 
def read_next_arrival(file, patient_id):
    line = file.readline()
    if not line:
        # no more arrivals
        return None  
    #parsing the data
    parts = line.strip().split()
    arrival_time = int(parts[0])
    patient_type = parts[1]
    assessment_time = int(parts[2])

    event = (arrival_time, 'arrival', patient_id, assessment_time, patient_type)
    return event

print(event_list)
