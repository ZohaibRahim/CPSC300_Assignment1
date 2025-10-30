import heapq
from dataclasses import dataclass
from typing import List, Tuple

from event import Event    # Base Event
from scheduler import schedule    #Part-B
from reporter import log_admission_complete
from departure import Departure

# INTERNAL STATE
class _AdmItem:
    # FCFS by treatment-finish time, tie-break by patient id
    treat_finish_time: int
    patient_id: int
    patient: "Patient"  # forward type

nurse_busy: bool = False    # Single admission nurse shared by all P1 patients
_adm_heap: list[tuple[int, int, "Patient"]] = []    ## Heap items are tuples: (treat_finish_time, patient_id, patient_obj)

# HELPERS - FOR TESTS
def reset_admission_state() -> None:
    """Helper for tests; safe to call anytime."""
    global nurse_busy, _adm_heap
    nurse_busy = False
    _adm_heap.clear()
    
# PUBLIC API
def admission_enqueue(patient, treat_finish_time: int) -> None:
    """Queue a priority-1 patient for admission while they remain in the room."""
    heapq.heappush(_adm_heap, (treat_finish_time, patient.id, patient))
    
def try_start_admission(t_now: int) -> None:
    """
    If the nurse is idle and a P1 is waiting, start an admission.
    Admission takes 3 time units and prints at completion.
    """
    global nurse_busy
    if nurse_busy or not _adm_heap:
        return
    nurse_busy = True
    _, _, p = heapq.heappop(_adm_heap)
    schedule(AdmissionComplete(t_now + 3, p))

class AdmissionComplete(Event):
    """
    Occurs exactly 3 time units after an admission starts.
    Print admission at completion, then schedule same-time Departure.
    """
    def process(self) -> None:
        global nurse_busy
        p, now = self.patient, self.time
        log_admission_complete(p, now)                  # print at completion
        schedule(Departure(now, p))                     # depart same tick
        nurse_busy = False
        try_start_admission(now)                        # immediately serve next P1, if any
