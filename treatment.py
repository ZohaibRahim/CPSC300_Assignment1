from events import TreatmentCompleted
from router import route_after_treatment

_controller_singleton = None

def set_controller(ctrl):
    """Called once from main to register the TreatmentController instance."""
    global _controller_singleton
    _controller_singleton = ctrl

def on_enter_waiting_room(now):
    """Called by EnterWaitingRoom events to start treatment if room free."""
    if _controller_singleton is not None:
        _controller_singleton.try_start_treatment(now)

class TreatmentController:
    def __init__(self, rooms, waitingroom, scheduler, backfill_cb=None):
        self.rooms = rooms
        self.waitingroom = waitingroom
        self.scheduler = scheduler
        self.backfill_cb = backfill_cb

    def try_start_treatment(self, now):
        while True:
            if not self.rooms.acquire_if_available():
                break
            patient = self.waitingroom.waitingroom_pop_best()
            if patient is None:
                self.rooms.release()
                break
            print(f"t={now}: Patient {patient.id} Priority {patient.priority} START treatment")
            completion_time = now + patient.treat_time
            self.scheduler.schedule(TreatmentCompleted(time=completion_time, patient=patient))

    def handle_treatment_completed(self, event):
        now = event.time
        patient = event.patient
        print(f"t={now}: Patient {patient.id} Priority {patient.priority} COMPLETED treatment")
        route_after_treatment(patient, now)
