from arrival_manager import open_input_file, next_arrival_if_due
from scheduler_queues_rooms import scheduler_instance
from treatment import TreatmentController, set_controller, on_enter_waiting_room
from departure import register_backfill_callback
from stats import final_report
from patient import all_patients_list  # if you store them globally

controller = TreatmentController(rooms, waiting, scheduler)
set_controller(controller)
register_backfill_callback(controller.try_start_treatment)

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
