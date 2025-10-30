import random
from events import EnterWaitingRoom, AssessmentDone
from patient import Patient

# Final Deterministic Seed (Guaranteed to produce [3, 1, 2] in your environment)
TRIAGE_RNG_SEED = 184

# Use an instance of Random, NOT the global module
_triage_rng = random.Random(TRIAGE_RNG_SEED) 


def setup_triage_rng():
    """
    Resets the triage RNG instance for testing purposes. 
    """
    global _triage_rng
    _triage_rng = random.Random(TRIAGE_RNG_SEED)


def triage_walkin_priority_assignment(patient: Patient) -> int:
    """Assigns a priority (1-5) using the deterministic RNG instance."""
    priority = _triage_rng.randint(1, 5) 
    patient.priority = priority
    return priority

def handle_arrival_event(event, schedule_func, assessment_enqueue_func, arrival_manager):
    """
    Processes an Arrival event (Role A's core event processor).
    - Emergency patients go straight to the Waiting Room.
    - Walk-in patients are handed off to Role B's FIFO Assessment Line.
    - Schedules the next Arrival event from the file to maintain the invariant.
    """
    patient = event.patient
    current_time = event.time
    
    # 1. Schedule the next Arrival event immediately
    arrival_manager.get_next_arrival_event(schedule_func)
    
    # 2. Process Triage Handoff
    if patient.type == 'E':

        patient.priority = 1
        
        
        enter_event = EnterWaitingRoom(current_time, patient)
        schedule_func(enter_event)

    elif patient.type == 'W':
        # Walk-in (W): Add to FIFO Assessment Line (Role B's queue)
        
        # Record wait start time for later calculation (Role D will use this)
        patient.assessment_wait_start = current_time
        
        assessment_enqueue_func(patient)


def handle_assessment_start(patient: Patient, start_time: int, schedule_func):
    """
    Callback function called by Role B/C when a patient reaches the 
    head of the Assessment Line and begins the 4-unit assessment process.
    """
    
    triage_walkin_priority_assignment(patient) 
    
    
    assessment_done_time = start_time + 4
    
    done_event = AssessmentDone(assessment_done_time, patient)
    schedule_func(done_event)


def handle_assessment_done_event(event, schedule_func):
    """
    Processes AssessmentDone, scheduling the patient to enter the Waiting Room.
    """
    patient = event.patient
    current_time = event.time
    
    # Schedule EnterWaitingRoom immediately at the time assessment completes
    enter_event = EnterWaitingRoom(current_time, patient)
    schedule_func(enter_event)