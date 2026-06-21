# Hospital Simulation System - CPSC300_Assignment1 

A simulation of a hospital's patient admission, treatment, and discharge
pipeline for CPSC 300, modeling priority-based event scheduling across
patient arrival, triage, treatment, and departure.

## Team

Four-person project: Jayesh Sethi, Ahad Ali Baig, Sara Surani, Zohaib Rahim

## Contributions by Role

- **Role A (Jayesh Sethi):** Event handling and triage logic
  (`events.py`, `triage_logic.py`, `test_triage.py`)

- **Role B (Ahad Ali Baig):** Patient data structures, treatment
  simulation, and overall integration (`patient.py`, `treatment.py`)

- **Role C - Treatment & scheduling support (Sara Surani):** Core scheduling and
  queue logic, treatment test suite, and edge-case testing for waiting
  room priority and room management

- **Role D (Zohaib Rahim):** Patient admission, departure, and routing
  logic (`admission.py`, `departure.py`, `router.py`); event scheduling
  and queue/room management (`scheduler.py`, `scheduler_queues_rooms.py`);
  reporting and statistics (`reporter.py`, `stats.py`); and the test
  suites for scheduling, reporting, and post-treatment flow
  (`test_scheduler_queues_rooms.py`, `tests_reporter.py`,
  `tests_post_treat.py`, `test_reporter_stats.py`)

## How to Run

1. Clone the repo and install any dependencies listed in the project files.
2. Run `main.py` to start the simulation.
3. Run the test suites (`test_*.py`) individually to verify each subsystem.
