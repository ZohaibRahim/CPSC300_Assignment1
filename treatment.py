from events import TreatmentCompleted
from router import route_after_treatment

class TreatmentController:
    def __init__(self, rooms, waitingroom, scheduler, backfill_cb=None):
        self.rooms = rooms
        self.waitingroom = waitingroom
        self.scheduler = scheduler
        # optional callback for D to call when a room frees (registered later)
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
        # DO NOT release room here; D's Departure will free it.
        route_after_treatment(patient, now)
