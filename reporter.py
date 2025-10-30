def log_start(p, t, rooms_avail) -> None:
    # Part C calls this; kept here for centralized formatting
    print(f"Time {t}: {p.id} (Priority {p.priority}) starts treatment "
          f"({rooms_avail} rooms still available)")

def log_treatment_completed(p, t) -> None:
    # Part C calls this on completion (before routing)
    print(f"Time {t}: {p.id} (Priority {p.priority}) finishes treatment")

def log_admission_complete(p, t) -> None:
    # Print admission at completion time only (P1)
    print(f"Time {t}: {p.id} (Priority 1) admitted to Hospital")

def log_departure(p, t, rooms_avail) -> None:
    print(f"Time {t}: {p.id} (Priority {p.priority}) departs "
          f"({rooms_avail} rooms still available)")

def note_wait_segment(p, key: str, delta: int) -> None:
    # Optional accumulator for waits: 'assess', 'to_treat', 'admit'
    p.waits[key] = p.waits.get(key, 0) + delta

def final_report(patients: list) -> None:
    print("\nPatient Wait Summary")
    total = 0
    for p in patients:
        tw = p.waits.get("assess", 0) + p.waits.get("to_treat", 0) + p.waits.get("admit", 0)
        total += tw
        print(f"{p.id}\t{tw}")
    n = len(patients)
    avg = (total / n) if n else 0
    print(f"\nTotal patients: {n}")
    print(f"Average wait: {avg:.2f}")
