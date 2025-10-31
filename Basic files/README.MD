# CPSC 300 Assignment 1: Event-Driven Hospital Simulatio

his is CPSC 300 Assignment 1, an event-driven simulation of a hospital system. The simulation models patient arrivals, assessments, treatments, and departures using a priority-based event queue. It demonstrates key concepts in discrete event simulation, including resource management (nurses, treatment rooms) and patient prioritization.

## How to Run

1. Ensure you have Python installed (tested with Python 3.13).
2. Navigate to the CPSC300_ASSIGNMENT1 folder in your terminal:

```bash
cd USER...\..\CPSC300_Assignment1\
```
3. Run the main simulation file:
```bash
python Main.py
```
4. When prompted, enter the input file name (e.g., data1.txt).

## Input Files

The folder includes sample input files:

1. data1.txt: Example with 7 patients (mix of emergencies and walk-ins).
2. data2.txt: Another test case.
3. data3.txt: Additional test case.

```# Example input from data1.txt
18 E 2
18 W 3
19 E 28
20 W 19
20 E 36
21 W 1
24 E 10
```

## Output

The simulation prints:

Real-time event logs (e.g., "Time 18: 28064212 (Emergency) arrives").

Final summary table with patient details and wait times.

Total patients seen and average waiting time.

Example output snippet:

```
Simulation begins...

Time  18: 28064212 (Emergency) arrives
Time 18: 28064212 (Priority 1) enters waiting room
...

...All events complete.  Final Summary:

 Patient Priority   Arrival Assessment   Treatment   Departure  Waiting
  Number               Time       Time    Required        Time     Time
----------------------------------------------------------------------
28064212        1        18         18           2          23        0
...

Patients seen in total: 7
Average waiting time per patient : 8.285714

```

