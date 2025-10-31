from Patient import Patient

#sample read file we created while building the intial logic, not used in our final code

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
    treatment_time = int(parts[2])

    patient = Patient(patient_id, arrival_time, patient_type, treatment_time)
    # Instead of a tuple, returning (arrival_time, 'arrival', Patient object)
    return (arrival_time, 'arrival', patient)

