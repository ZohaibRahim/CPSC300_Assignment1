# Tiny accumulator for end-of-run summary.
def add_wait(patient, bucket: str, delta: int) -> None:
    """
    bucket in {"assess", "to_treat", "admit"}.
    """
    waits = getattr(patient, "waits", None)
    if waits is None:
        patient.waits = {}
        waits = patient.waits
    waits[bucket] = waits.get(bucket, 0) + int(delta)

def final_report(patients: list) -> None:
    print("\nPatient Wait Summary")
    total = 0
    for p in patients:
        waits = getattr(p, "waits", {})
        tw = waits.get("assess", 0) + waits.get("to_treat", 0) + waits.get("admit", 0)
        total += tw
        print(f"{p.id}\t{tw}")
    n = len(patients)
    avg = (total / n) if n else 0
    print(f"\nTotal patients: {n}")
    print(f"Average wait: {avg:.2f}")
