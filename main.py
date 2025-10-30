from arrival_manager import open_input_file, next_arrival_if_due
from scheduler_queues_rooms import scheduler_instance
from treatment import on_enter_waiting_room
from reporter import final_report
from stats import collect_stats  # optional if you accumulate waits
from patient import all_patients_list  # if you store them globally

def run_simulation(filename: str):
    fh = open_input_file(filename)
    scheduler = scheduler_instance()

    # Prime the first arrival (only one pending)
    first = next_arrival_if_due(fh, now=0)
    if first:
        scheduler.schedule(first)

    while not scheduler.is_empty():
        event = scheduler.pop_next()
        now = event.time
        event.process()

        # ask A for next arrival when time advances
        next_event = next_arrival_if_due(fh, now)
        if next_event:
            scheduler.schedule(next_event)

    # After all events are processed
    final_report(all_patients_list)

if __name__ == "__main__":
    # Try each of the three sample files
    for name in ["data1.txt", "data2.txt", "data3.txt"]:
        print(f"\n--- Running {name} ---")
        run_simulation(f"data/{name}")
