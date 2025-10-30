"""
Manages patient treatment start and completion events.
"""

from events import TreatmentCompleted  # Your event class for treatment done
from router import route_after_treatment  # Post-treatment routing from Member D


class TreatmentController:
    def __init__(self, rooms, waitingroom, scheduler):
        """
        Initialize with shared resources.
        
        :param rooms: Shared rooms manager with acquire_if_available() and release()
        :param waitingroom: Shared waiting room queue with waitingroom_pop_best()
        :param scheduler: Shared scheduler with schedule(event)
        """
        self.rooms = rooms
        self.waitingroom = waitingroom
        self.scheduler = scheduler

    def try_start_treatment(self, now):
        """
        Attempt to start treatment for patients while rooms are available.
        Schedule TreatmentCompleted events at appropriate times.
        """
        while True:
            if not self.rooms.acquire_if_available():
                # No rooms are free, stop attempting
                break

            patient = self.waitingroom.waitingroom_pop_best()
            if patient is None:
                # No patients waiting; release the room and stop
                self.rooms.release()
                break

            print(f"t={now}: Patient {patient.id} Priority {patient.priority} START treatment")

            completion_time = now + patient.treat_time
            treatment_completed_event = TreatmentCompleted(time=completion_time, patient=patient)
            self.scheduler.schedule(treatment_completed_event)

    def handle_treatment_completed(self, event):
        """
        Handle the TreatmentCompleted event:
        frees up a room, routes patient to next stage,
        and attempts to start treatments for others waiting.
        """
        now = event.time
        patient = event.patient

        print(f"t={now}: Patient {patient.id} Priority {patient.priority} COMPLETED treatment")

        self.rooms.release()
        route_after_treatment(patient, now)

        self.try_start_treatment(now)
