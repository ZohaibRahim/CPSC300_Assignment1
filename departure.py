from models.event import Event
from engine.rooms import release, available_count
from reporter import log_departure
from controller import try_start_treatment

class Departure(Event):
    """
    For P2–P5: scheduled at treatment_complete + 1.
    For P1: scheduled at admission_complete time.
    Only here the room becomes free.
    """
    def process(self) -> None:
        p, now = self.patient, self.time
        release()                                       # room frees ONLY now
        log_departure(p, now, available_count())        # include rooms available in log
        try_start_treatment(now)                        # backfill at the same time tick
