from arrival_manager import open_input_file, next_arrival_if_due
from scheduler_queues_rooms import create_all_resources
from treatment import TreatmentController, set_controller
from departure import register_backfill_callback
from events import TreatmentCompleted
from stats import final_report
from patient import all_patients_list

def run_simulation(filename: str):
    # Build fresh shared resources for this run
    res = create_all_resources()
    scheduler = res["scheduler"]
    rooms     = res["rooms"]
    waiting   = res["waiting_room"]

    # Wire treatment controller (C) and give D a backfill hook
    controller = TreatmentController(rooms, waiting, scheduler)
    set_controller(controller)  # lets events call on_enter_waiting_room(now)
    register_backfill_callback(controller.try_start_treatment)

    # Open arrivals and prime exactly one Arrival
    fh = open_input_file(filename)
    first = next_arrival_if_due(fh, now=0)
    if first:
        scheduler.schedule(first)

    # Main event loop
    while not scheduler.is_empty():
        ev = scheduler.pop_next()
        now = ev.time
        ev.process()

        # Route treatment completions via controller (rooms free later on Departure)
        if isinstance(ev, TreatmentCompleted):
            controller.handle_treatment_completed(ev)

        # Maintain the “one pending arrival” invariant
        nxt = next_arrival_if_due(fh, now)
        if nxt:
            scheduler.schedule(nxt)

    # End-of-run stats
    final_report(all_patients_list)

if __name__ == "__main__":
    for name in ["data1.txt", "data2.txt", "data3.txt"]:
        print(f"\n--- Running {name} ---")
        run_simulation(f"data/{name}")
