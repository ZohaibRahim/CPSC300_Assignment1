from events import Event
from rooms import release, available_count
from reporter import log_departure

# Backfill callback, to be set by whoever constructs TreatmentController
_BACKFILL_CB = None
def register_backfill_callback(fn):
    global _BACKFILL_CB
    _BACKFILL_CB = fn

class Departure(Event):
    def process(self):
        p, now = self.patient, self.time
        release()  # room becomes free ONLY now
        log_departure(p, now, available_count())
        if _BACKFILL_CB is not None:
            _BACKFILL_CB(now)
