
#Eventlist to keep track of all the incoming files
event_list = []

#reading files 
with open('data1.txt', 'r') as file:
    line = file.readline()


    if not line:
        None
    #parsing the data into parts
    parts = line.strip.split()
    arrival_time = int(parts[1])
    patient_type = parts[2]
    assessment_time = parts[3]

    #generating a patient ID starting with 28064212

    patient_id = 28064212


    #creating an arrival event
    event = (arrival_time, 'arrival', patient_id, assessment_time, patient_type)

    event_list.append(event)

print(event_list)
