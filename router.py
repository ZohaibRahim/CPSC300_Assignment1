from scheduler import schedule
from departure import Departure
from admission import admission_enqueue, try_start_admission

def route_after_treatment(patient, now):
    if patient.priority == 1:
        admission_enqueue(patient, now)
        try_start_admission(now)
    else:
        schedule(Departure(now + 1, patient))
