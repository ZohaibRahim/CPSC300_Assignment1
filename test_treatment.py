import sys


class MockPatient:
    """Mock patient for testing"""
    next_id = 28064212
    
    def __init__(self, priority, treat_time, arrive_time=0):
        self.id = MockPatient.next_id
        MockPatient.next_id += 1
        self.priority = priority
        self.treat_time = treat_time
        self.arrive_time = arrive_time
        
        # Timestamps
        self.enter_waiting_time = None
        self.treatment_start = None
        self.treatment_end = None
        self.treatment_wait = 0
    
    def __repr__(self):
        return f"Patient({self.id}, P{self.priority}, T{self.treat_time})"


class MockRooms:
    """Mock rooms manager (Member B's interface)"""
    def __init__(self, total=3):
        self.total = total
        self.occupied = 0
    
    def acquire_if_available(self):
        """Try to acquire a room. Returns True if successful."""
        if self.occupied < self.total:
            self.occupied += 1
            return True
        return False
    
    def release(self):
        """Release a room back to the pool."""
        if self.occupied > 0:
            self.occupied -= 1
    
    def get_available_count(self):
        """Get number of available rooms."""
        return self.total - self.occupied


class MockWaitingRoom:
    """Mock waiting room (Member B's interface)"""
    def __init__(self):
        self.patients = []
    
    def add_patient(self, patient):
        """Add patient, sorted by priority then ID"""
        self.patients.append(patient)
        self.patients.sort(key=lambda p: (p.priority, p.id))
    
    def waitingroom_pop_best(self):
        """Pop highest priority patient (lowest priority number)"""
        if self.patients:
            return self.patients.pop(0)
        return None
    
    def is_empty(self):
        return len(self.patients) == 0


class MockScheduler:
    """Mock event scheduler (Member B's interface)"""
    def __init__(self):
        self.events = []
    
    def schedule(self, event):
        """Schedule an event"""
        self.events.append(event)
        # Sort by time
        self.events.sort(key=lambda e: e.time)


class MockRouter:
    """Mock router (Member D's interface)"""
    def __init__(self):
        self.routed_patients = []
    
    def route_after_treatment(self, patient, now):
        """Route patient after treatment (admission or departure)"""
        self.routed_patients.append((patient, now))
        print(f"  [Router] Patient {patient.id} routed at time {now}")


class MockTreatmentCompleted:
    """Mock TreatmentCompleted event"""
    def __init__(self, time, patient):
        self.time = time
        self.patient = patient


# Mock the events module
from types import ModuleType
mock_events = ModuleType('events')
mock_events.TreatmentCompleted = MockTreatmentCompleted
sys.modules['events'] = mock_events

# Now import the actual treatment module
from treatment import TreatmentController


# Test Functions

def test_immediate_start_single_patient():
    """
    TEST 1: Immediate start when rooms available
    
    Scenario: 1 patient waiting, 3 rooms available
    Expected: Patient starts treatment immediately
    """
    print("\n" + "="*70)
    print("TEST 1: Immediate Start - Single Patient")
    print("="*70)
    
    # Setup
    rooms = MockRooms(3)
    waitingroom = MockWaitingRoom()
    scheduler = MockScheduler()
    router = MockRouter()
    controller = TreatmentController(rooms, waitingroom, scheduler, router)
    
    # Add patient to waiting room
    patient = MockPatient(priority=2, treat_time=15)
    patient.enter_waiting_time = 10
    waitingroom.add_patient(patient)
    
    print(f"Setup: {patient} in waiting room at time 10")
    print(f"       3 rooms available")
    print()
    
    # Try to start treatment
    print("Action: try_start_treatment(10)")
    controller.try_start_treatment(10)
    
    # Verify
    assert rooms.get_available_count() == 2, "Should have 2 rooms remaining"
    assert waitingroom.is_empty(), "Waiting room should be empty"
    assert len(scheduler.events) == 1, "Should have 1 scheduled event"
    assert scheduler.events[0].time == 25, f"Treatment should complete at 25, got {scheduler.events[0].time}"
    assert patient.treatment_start == 10, "Treatment should start at time 10"
    assert patient.treatment_wait == 0, f"Should have 0 wait time, got {patient.treatment_wait}"
    
    print()
    print("Patient started treatment immediately")
    print("Room acquired (2 remaining)")
    print("TreatmentCompleted scheduled at time 25")
    print("Wait time = 0 (immediate start)")
    print("TEST PASSED")


def test_immediate_start_multiple_patients():
    """
    TEST 2: Multiple rooms free should start multiple patients
    
    Scenario: 4 patients waiting, 3 rooms available
    Expected: Top 3 priority patients start, 1 waits
    """
    print("\n" + "="*70)
    print("TEST 2: Immediate Start - Multiple Patients")
    print("="*70)
    
    # Setup
    rooms = MockRooms(3)
    waitingroom = MockWaitingRoom()
    scheduler = MockScheduler()
    router = MockRouter()
    controller = TreatmentController(rooms, waitingroom, scheduler, router)
    
    # Add 4 patients with different priorities
    patients = [
        MockPatient(priority=1, treat_time=20),
        MockPatient(priority=3, treat_time=10),
        MockPatient(priority=2, treat_time=15),
        MockPatient(priority=4, treat_time=25),
    ]
    
    for p in patients:
        p.enter_waiting_time = 10
        waitingroom.add_patient(p)
    
    print(f"Setup: 4 patients in waiting room")
    print(f"       Priorities: 1, 3, 2, 4")
    print(f"       3 rooms available")
    print()
    
    # Try to start treatments
    print("Action: try_start_treatment(10)")
    controller.try_start_treatment(10)
    
    # Verify
    assert rooms.get_available_count() == 0, "All rooms should be occupied"
    assert not waitingroom.is_empty(), "1 patient should still be waiting"
    assert len(scheduler.events) == 3, "Should have 3 scheduled events"
    
    # Check that lowest priority patient is still waiting
    remaining = waitingroom.waitingroom_pop_best()
    assert remaining.priority == 4, f"Priority 4 should be waiting, got {remaining.priority}"
    
    print()
    print("3 patients started (priorities 1, 2, 3)")
    print("All 3 rooms occupied")
    print("Priority 4 patient still waiting")
    print("3 TreatmentCompleted events scheduled")
    print("TEST PASSED")


def test_chained_start_after_departure():
    """
    TEST 3: Chained starts after departures
    
    Scenario: All rooms occupied, patient waiting, then treatment completes
    Expected: Waiting patient starts immediately after completion
    """
    print("\n" + "="*70)
    print("TEST 3: Chained Start After Completion")
    print("="*70)
    
    # Setup
    rooms = MockRooms(3)
    waitingroom = MockWaitingRoom()
    scheduler = MockScheduler()
    router = MockRouter()
    controller = TreatmentController(rooms, waitingroom, scheduler, router)
    
    # Occupy all 3 rooms
    for _ in range(3):
        rooms.acquire_if_available()
    
    # Add waiting patient
    waiting_patient = MockPatient(priority=2, treat_time=10)
    waiting_patient.enter_waiting_time = 20
    waitingroom.add_patient(waiting_patient)
    
    print(f"Setup: All 3 rooms occupied")
    print(f"       {waiting_patient} waiting since time 20")
    print()
    
    # Simulate treatment completion at time 30
    completed_patient = MockPatient(priority=1, treat_time=20)
    event = MockTreatmentCompleted(time=30, patient=completed_patient)
    
    print("Action: handle_treatment_completed(event) at time 30")
    controller.handle_treatment_completed(event)
    
    # Verify
    assert rooms.get_available_count() == 2, f"Should have 2 rooms, got {rooms.get_available_count()}"
    assert waitingroom.is_empty(), "Waiting room should be empty"
    assert waiting_patient.treatment_start == 30, "Waiting patient should start at time 30"
    assert waiting_patient.treatment_wait == 10, f"Wait time should be 10, got {waiting_patient.treatment_wait}"
    assert len(router.routed_patients) == 1, "Completed patient should be routed"
    
    print()
    print("Completed patient's room released")
    print("Waiting patient started immediately (chained)")
    print("Wait time = 10 (waited from 20 to 30)")
    print("Completed patient routed to Member D")
    print("TEST PASSED")


def test_correct_completion_timing():
    """
    TEST 4: Correct completion timing
    
    Scenario: Patient with 15 time unit treatment starts at time 10
    Expected: Completion scheduled at time 25
    """
    print("\n" + "="*70)
    print("TEST 4: Correct Completion Timing")
    print("="*70)
    
    # Setup
    rooms = MockRooms(3)
    waitingroom = MockWaitingRoom()
    scheduler = MockScheduler()
    router = MockRouter()
    controller = TreatmentController(rooms, waitingroom, scheduler, router)
    
    # Test different treatment times
    test_cases = [
        (10, 15, 25),  # Start 10, duration 15, complete 25
        (20, 30, 50),  # Start 20, duration 30, complete 50
        (0, 5, 5),     # Start 0, duration 5, complete 5
    ]
    
    for start_time, duration, expected_completion in test_cases:
        scheduler.events.clear()
        waitingroom.patients.clear()
        
        patient = MockPatient(priority=2, treat_time=duration)
        patient.enter_waiting_time = start_time
        waitingroom.add_patient(patient)
        
        print(f"Test: Start={start_time}, Duration={duration}")
        controller.try_start_treatment(start_time)
        
        assert len(scheduler.events) == 1, "Should schedule 1 event"
        actual_completion = scheduler.events[0].time
        assert actual_completion == expected_completion, \
            f"Expected completion at {expected_completion}, got {actual_completion}"
        print(f"  ✓ Completion scheduled at {actual_completion}")
        
        # Release room for next test
        rooms.release()
    
    print()
    print("TEST PASSED - All timing calculations correct")


def test_straight_to_treatment():
    """
    TEST 5: Patient goes straight from waiting room to treatment
    
    Scenario: Patient enters waiting room, room immediately available
    Expected: Zero wait time, immediate start
    """
    print("\n" + "="*70)
    print("TEST 5: Straight to Treatment (Zero Wait)")
    print("="*70)
    
    # Setup
    rooms = MockRooms(3)
    waitingroom = MockWaitingRoom()
    scheduler = MockScheduler()
    router = MockRouter()
    controller = TreatmentController(rooms, waitingroom, scheduler, router)
    
    # Patient enters waiting room at time 15
    patient = MockPatient(priority=3, treat_time=20)
    patient.enter_waiting_time = 15
    waitingroom.add_patient(patient)
    
    print(f"Setup: {patient} enters waiting room at time 15")
    print(f"       3 rooms available")
    print()
    
    # Immediately try to start treatment
    print("Action: try_start_treatment(15) - same time as entering")
    controller.try_start_treatment(15)
    
    # Verify
    assert patient.treatment_start == 15, "Should start at time 15"
    assert patient.treatment_wait == 0, f"Should have 0 wait, got {patient.treatment_wait}"
    assert waitingroom.is_empty(), "Should not remain in waiting room"
    
    print()
    print("Patient started treatment at same time as entering waiting room")
    print("Wait time = 0 (immediate)")
    print("TEST PASSED")


def test_no_rooms_available():
    """
    TEST 6: No rooms available - patient stays in waiting room
    
    Scenario: All rooms occupied, patient waiting
    Expected: Patient stays in queue, no treatment started
    """
    print("\n" + "="*70)
    print("TEST 6: No Rooms Available")
    print("="*70)
    
    # Setup
    rooms = MockRooms(3)
    waitingroom = MockWaitingRoom()
    scheduler = MockScheduler()
    router = MockRouter()
    controller = TreatmentController(rooms, waitingroom, scheduler, router)
    
    # Occupy all rooms
    for _ in range(3):
        rooms.acquire_if_available()
    
    # Add patient
    patient = MockPatient(priority=2, treat_time=15)
    patient.enter_waiting_time = 10
    waitingroom.add_patient(patient)
    
    print(f"Setup: All 3 rooms occupied")
    print(f"       {patient} waiting")
    print()
    
    print("Action: try_start_treatment(10)")
    controller.try_start_treatment(10)
    
    # Verify
    assert rooms.get_available_count() == 0, "Still no rooms available"
    assert not waitingroom.is_empty(), "Patient should still be waiting"
    assert len(scheduler.events) == 0, "No events should be scheduled"
    assert patient.treatment_start is None, "Treatment should not have started"
    
    print()
    print("Patient remains in waiting room")
    print("No treatment started")
    print("No events scheduled")
    print("TEST PASSED")


def test_cascade_multiple_completions():
    """
    TEST 7: Multiple completions trigger cascade of starts
    
    Scenario: 2 patients complete, 3 patients waiting
    Expected: 2 waiting patients start as rooms free up
    """
    print("\n" + "="*70)
    print("TEST 7: Cascade - Multiple Completions")
    print("="*70)
    
    # Setup
    rooms = MockRooms(3)
    waitingroom = MockWaitingRoom()
    scheduler = MockScheduler()
    router = MockRouter()
    controller = TreatmentController(rooms, waitingroom, scheduler, router)
    
    # Occupy all rooms
    for _ in range(3):
        rooms.acquire_if_available()
    
    # Add 3 waiting patients
    waiting_patients = [
        MockPatient(priority=1, treat_time=10),
        MockPatient(priority=2, treat_time=15),
        MockPatient(priority=3, treat_time=20),
    ]
    for p in waiting_patients:
        p.enter_waiting_time = 20
        waitingroom.add_patient(p)
    
    print(f"Setup: All 3 rooms occupied")
    print(f"       3 patients waiting (priorities: 1, 2, 3)")
    print()
    
    # First completion at time 30
    print("Action 1: Treatment completes at time 30")
    event1 = MockTreatmentCompleted(time=30, patient=MockPatient(priority=2, treat_time=10))
    controller.handle_treatment_completed(event1)
    
    assert waiting_patients[0].treatment_start == 30, "Priority 1 should start"
    print("Priority 1 patient started")
    
    # Second completion at time 35
    print("\nAction 2: Treatment completes at time 35")
    event2 = MockTreatmentCompleted(time=35, patient=MockPatient(priority=3, treat_time=15))
    controller.handle_treatment_completed(event2)
    
    assert waiting_patients[1].treatment_start == 35, "Priority 2 should start"
    print("Priority 2 patient started")
    
    # Verify final state
    assert not waitingroom.is_empty(), "Priority 3 should still be waiting"
    assert len(router.routed_patients) == 2, "2 patients should be routed"
    
    print()
    print("2 patients started as rooms freed up (cascade)")
    print("Priority 3 still waiting (lowest priority)")
    print("TEST PASSED")


def run_all_tests():
    """Run all test cases"""
    print("\n" + "🏥"*35)
    print(" "*20 + "TREATMENT MODULE TEST SUITE")
    print(" "*25 + "Role C - Member C")
    print("🏥"*35)
    
    tests = [
        ("Immediate Start - Single Patient", test_immediate_start_single_patient),
        ("Immediate Start - Multiple Patients", test_immediate_start_multiple_patients),
        ("Chained Start After Completion", test_chained_start_after_departure),
        ("Correct Completion Timing", test_correct_completion_timing),
        ("Straight to Treatment", test_straight_to_treatment),
        ("No Rooms Available", test_no_rooms_available),
        ("Cascade Multiple Completions", test_cascade_multiple_completions),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"\n TEST FAILED: {test_name}")
            print(f"   Error: {e}")
            failed += 1
            import traceback
            traceback.print_exc()
        except Exception as e:
            print(f"\n ERROR in {test_name}: {e}")
            failed += 1
            import traceback
            traceback.print_exc()
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print("="*70)
    
    if failed == 0:
        print("\n ALL TESTS PASSED!")
        print("\nYour treatment module is ready for integration!")
        print("\nNext steps:")
        print("1. Integrate with Member B's actual rooms/waitingroom classes")
        print("2. Integrate with Member D's route_after_treatment()")
        print("3. Test with real data files (data1.txt, data2.txt, data3.txt)")
        print("4. Verify output format matches assignment spec")
        return 0
    else:
        print("\n Some tests failed. Please review and fix.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
