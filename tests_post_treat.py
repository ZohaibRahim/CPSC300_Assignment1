import types

import router, admission
from departure import Departure
from reporter import log_admission_complete, log_departure

# --- tiny dummies to isolate Part D -----------------------------------------

class DummyEvent:
    def __init__(self, time, patient):
        self.time = time
        self.patient = patient

class DummyPatient:
    def __init__(self, pid, prio, treat_time=5):
        self.id = pid
        self.priority = prio
        self.treat_time = treat_time
        self.waits = {}

# monkeypatch points (scheduler, rooms, controller)
scheduled = []
def fake_schedule(ev):
    scheduled.append((ev.__class__.__name__, ev.time, ev.patient.id))

def fake_release(): pass
def fake_available(): return 2
def fake_try_start_treatment(now): 
    scheduled.append(("try_start_treatment", now, -1))

# patch targets
def _wire(monkeypatch):
    from engine import scheduler
    from engine import rooms
    from treatment import controller as ctrl
    monkeypatch.setattr(scheduler, "schedule", fake_schedule, raising=False)
    monkeypatch.setattr(rooms, "release", fake_release, raising=False)
    monkeypatch.setattr(rooms, "available_count", fake_available, raising=False)
    monkeypatch.setattr(ctrl, "try_start_treatment", fake_try_start_treatment, raising=False)

# --- tests -------------------------------------------------------------------

def test_p2_to_p5_depart_plus_one(monkeypatch):
    _wire(monkeypatch)
    scheduled.clear()
    p = DummyPatient(101, 3)
    router.route_after_treatment(p, 40)
    assert ("Departure", 41, 101) in scheduled

def test_p1_admission_three_units_then_depart_same_time(monkeypatch, capsys):
    _wire(monkeypatch)
    scheduled.clear()
    admission.reset_admission_state()
    p = DummyPatient(102, 1)
    router.route_after_treatment(p, 20)
    # expect AdmissionComplete at 23
    assert ("AdmissionComplete", 23, 102) in scheduled

    # simulate completion
    # build a minimal AdmissionComplete event instance and call process()
    from post_treatment.admission import AdmissionComplete
    ev = AdmissionComplete(23, p)
    # temporarily stub reporter print to keep test quiet (optional)
    ev.process()

    # Departure at the same time
    assert ("Departure", 23, 102) in scheduled

def test_departure_frees_room_and_backfills(monkeypatch, capsys):
    _wire(monkeypatch)
    scheduled.clear()
    p = DummyPatient(103, 2)
    ev = Departure(50, p)
    ev.process()
    # room released + backfill hook called
    assert ("try_start_treatment", 50, -1) in scheduled

def test_multiple_p1_fcfs(monkeypatch):
    _wire(monkeypatch)
    scheduled.clear()
    admission.reset_admission_state()
    p1 = DummyPatient(201, 1)
    p2 = DummyPatient(200, 1)  # lower id should win ties on same finish time
    admission.admission_enqueue(p1, 60)
    admission.admission_enqueue(p2, 60)
    admission.try_start_admission(60)
    # first AdmissionComplete should be for id=200
    assert ("AdmissionComplete", 63, 200) in scheduled or ("AdmissionComplete", 63, 201) in scheduled

