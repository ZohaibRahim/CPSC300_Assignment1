from scheduler import schedule
from departure import Departure
from admission import admission_enqueue, try_start_admission

def route_after_treatment(patient, t_now: int) -> None:
    """
    Called by TreatmentCompleted handler (Part C).
    If Priority 1 → enter admission flow.
    Else (Priority 2–5) → depart at t_now + 1.
    """
    if patient.priority == 1:
        admission_enqueue(patient, t_now)
        try_start_admission(t_now)
    else:
        schedule(Departure(t_now + 1, patient))
