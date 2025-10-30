# tests/test_reporter_stats.py
from reporter import log_admission_complete, log_departure
from stats import add_wait, final_report

class DummyPatient:
    def __init__(self, pid, prio):
        self.id = pid
        self.priority = prio
        self.waits = {}

def test_stats_accumulation_and_print(capsys):
    p1, p2 = DummyPatient(1,1), DummyPatient(2,3)
    add_wait(p1, "assess", 4)
    add_wait(p1, "to_treat", 2)
    add_wait(p2, "assess", 3)
    final_report([p1, p2])
    out = capsys.readouterr().out
    assert "Patient Wait Summary" in out
    assert "Total patients: 2" in out
    assert "Average wait" in out
