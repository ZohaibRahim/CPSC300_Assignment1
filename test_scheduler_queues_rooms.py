"""
Comprehensive Test Suite for Member B - Scheduler + Queues + Rooms

Tests cover:
1. Event scheduler tie-breaks (time → priority → patient#)
2. Waiting room priority ordering
3. Room acquire/release functionality
4. Assessment line FIFO
5. Admission line FCFS

Run: python test_scheduler_queues.py
"""

import sys
from scheduler_queues_rooms import (
    EventScheduler,
    AssessmentLine,
    WaitingRoom,
    AdmissionLine,
    RoomsManager,
    create_all_resources
)


# ============================================================================
# MOCK CLASSES
# ============================================================================

class MockPatient:
    """Mock patient for testing"""
    def __init__(self, patient_id, priority=None):
        self.id = patient_id
        self.priority = priority
        self.admission_wait = 0
    
    def __repr__(self):
        return f"Patient({self.id}, P{self.priority})"


class MockEvent:
    """Mock event for testing"""
    def __init__(self, time, patient, event_type="TEST"):
        self.time = time
        self.patient = patient
        self.type = event_type
    
    def __repr__(self):
        return f"Event(t={self.time}, {self.patient})"


# ============================================================================
# TEST FUNCTIONS
# ============================================================================

def test_event_scheduler_basic():
    """TEST 1: Basic event scheduling and ordering by time"""
    print("\n" + "=" * 70)
    print("TEST 1: Event Scheduler - Basic Time Ordering")
    print("=" * 70)
    
    scheduler = EventScheduler()
    
    # Add events at different times
    p1 = MockPatient(28064212, priority=2)
    p2 = MockPatient(28064213, priority=3)
    p3 = MockPatient(28064214, priority=1)
    
    scheduler.schedule(MockEvent(time=30, patient=p2))
    scheduler.schedule(MockEvent(time=10, patient=p1))
    scheduler.schedule(MockEvent(time=20, patient=p3))
    
    print("Scheduled events at times: 30, 10, 20")
    
    # Pop in time order
    e1 = scheduler.pop_next()
    e2 = scheduler.pop_next()
    e3 = scheduler.pop_next()
    
    assert e1.time == 10, f"Expected time 10, got {e1.time}"
    assert e2.time == 20, f"Expected time 20, got {e2.time}"
    assert e3.time == 30, f"Expected time 30, got {e3.time}"
    
    print("Events popped in correct time order: 10, 20, 30")
    print("TEST PASSED")


def test_event_scheduler_priority_tiebreak():
    """TEST 2: Event scheduler tie-break by priority at same time"""
    print("\n" + "=" * 70)
    print("TEST 2: Event Scheduler - Priority Tie-Break")
    print("=" * 70)
    
    scheduler = EventScheduler()
    
    # Add events at SAME time with different priorities
    p1 = MockPatient(28064212, priority=3)
    p2 = MockPatient(28064213, priority=1)
    p3 = MockPatient(28064214, priority=2)
    
    # All at time 10
    scheduler.schedule(MockEvent(time=10, patient=p1))
    scheduler.schedule(MockEvent(time=10, patient=p2))
    scheduler.schedule(MockEvent(time=10, patient=p3))
    
    print("Scheduled 3 events at time 10")
    print("  Priorities: 3, 1, 2")
    
    # Should come out in priority order: 1, 2, 3
    e1 = scheduler.pop_next()
    e2 = scheduler.pop_next()
    e3 = scheduler.pop_next()
    
    assert e1.patient.priority == 1, f"Expected priority 1, got {e1.patient.priority}"
    assert e2.patient.priority == 2, f"Expected priority 2, got {e2.patient.priority}"
    assert e3.patient.priority == 3, f"Expected priority 3, got {e3.patient.priority}"
    
    print("Events popped in priority order: 1, 2, 3")
    print("TEST PASSED")


def test_event_scheduler_patient_id_tiebreak():
    """TEST 3: Event scheduler tie-break by patient ID when time and priority same"""
    print("\n" + "=" * 70)
    print("TEST 3: Event Scheduler - Patient ID Tie-Break")
    print("=" * 70)
    
    scheduler = EventScheduler()
    
    # Add events at SAME time with SAME priority but different patient IDs
    p1 = MockPatient(28064215, priority=2)
    p2 = MockPatient(28064212, priority=2)
    p3 = MockPatient(28064214, priority=2)
    
    # All at time 10, all priority 2
    scheduler.schedule(MockEvent(time=10, patient=p1))
    scheduler.schedule(MockEvent(time=10, patient=p2))
    scheduler.schedule(MockEvent(time=10, patient=p3))
    
    print("Scheduled 3 events at time 10, all priority 2")
    print("  Patient IDs: 28064215, 28064212, 28064214")
    
    # Should come out in patient ID order: 212, 214, 215
    e1 = scheduler.pop_next()
    e2 = scheduler.pop_next()
    e3 = scheduler.pop_next()
    
    assert e1.patient.id == 28064212, f"Expected ID 212, got {e1.patient.id}"
    assert e2.patient.id == 28064214, f"Expected ID 214, got {e2.patient.id}"
    assert e3.patient.id == 28064215, f"Expected ID 215, got {e3.patient.id}"
    
    print("Events popped in patient ID order: 212, 214, 215")
    print("TEST PASSED")


def test_event_scheduler_complex_ordering():
    """TEST 4: Complex scenario with multiple tie-break levels"""
    print("\n" + "=" * 70)
    print("TEST 4: Event Scheduler - Complex Multi-Level Ordering")
    print("=" * 70)
    
    scheduler = EventScheduler()
    
    # Create complex scenario
    events = [
        MockEvent(10, MockPatient(28064215, priority=2)),  # time=10, p=2, id=215
        MockEvent(10, MockPatient(28064212, priority=2)),  # time=10, p=2, id=212 ← should be 1st
        MockEvent(10, MockPatient(28064213, priority=1)),  # time=10, p=1, id=213 ← should be 2nd
        MockEvent(5, MockPatient(28064220, priority=5)),   # time=5, p=5, id=220  ← should be 0th
        MockEvent(10, MockPatient(28064214, priority=3)),  # time=10, p=3, id=214
    ]
    
    for e in events:
        scheduler.schedule(e)
    
    print("Scheduled 5 events with mixed times/priorities/IDs")
    
    # Expected order:
    # 1. time=5 (earliest time)
    # 2. time=10, priority=1 (highest priority at time 10)
    # 3. time=10, priority=2, id=212 (next priority, lowest ID)
    # 4. time=10, priority=2, id=215 (next priority, higher ID)
    # 5. time=10, priority=3 (lowest priority at time 10)
    
    results = []
    while not scheduler.is_empty():
        e = scheduler.pop_next()
        results.append((e.time, e.patient.priority, e.patient.id))
    
    expected = [
        (5, 5, 28064220),
        (10, 1, 28064213),
        (10, 2, 28064212),
        (10, 2, 28064215),
        (10, 3, 28064214),
    ]
    
    assert results == expected, f"Expected {expected}, got {results}"
    
    print("Complex ordering correct:")
    for i, (t, p, id) in enumerate(results, 1):
        print(f"  {i}. time={t}, priority={p}, id={id}")
    print("TEST PASSED")


def test_assessment_line_fifo():
    """TEST 5: Assessment line maintains FIFO order"""
    print("\n" + "=" * 70)
    print("TEST 5: Assessment Line - FIFO Order")
    print("=" * 70)
    
    line = AssessmentLine()
    
    # Add patients in specific order
    p1 = MockPatient(28064212, priority=None)
    p2 = MockPatient(28064213, priority=None)
    p3 = MockPatient(28064214, priority=None)
    
    line.enqueue_assessment(p1)
    line.enqueue_assessment(p2)
    line.enqueue_assessment(p3)
    
    print("Enqueued patients: 212, 213, 214")
    
    # Dequeue in FIFO order
    d1 = line.dequeue_assessment()
    d2 = line.dequeue_assessment()
    d3 = line.dequeue_assessment()
    
    assert d1.id == 28064212, f"Expected 212, got {d1.id}"
    assert d2.id == 28064213, f"Expected 213, got {d2.id}"
    assert d3.id == 28064214, f"Expected 214, got {d3.id}"
    
    print("Dequeued in FIFO order: 212, 213, 214")
    
    # Check empty
    assert line.is_empty(), "Line should be empty"
    assert line.dequeue_assessment() is None, "Should return None when empty"
    
    print("Empty queue handled correctly")
    print("TEST PASSED")


def test_waiting_room_priority_ordering():
    """TEST 6: Waiting room pops by priority then patient ID"""
    print("\n" + "=" * 70)
    print("TEST 6: Waiting Room - Priority Ordering")
    print("=" * 70)
    
    room = WaitingRoom()
    
    # Add patients with different priorities
    patients = [
        MockPatient(28064215, priority=3),
        MockPatient(28064212, priority=1),
        MockPatient(28064214, priority=2),
        MockPatient(28064213, priority=1),  # Same priority as 212
        MockPatient(28064216, priority=3),  # Same priority as 215
    ]
    
    for p in patients:
        room.waitingroom_push(p)
    
    print("Added patients:")
    print("  ID 215, Priority 3")
    print("  ID 212, Priority 1")
    print("  ID 214, Priority 2")
    print("  ID 213, Priority 1")
    print("  ID 216, Priority 3")
    
    # Pop all and check order
    # Expected: P1(212), P1(213), P2(214), P3(215), P3(216)
    results = []
    while not room.is_empty():
        p = room.waitingroom_pop_best()
        results.append((p.priority, p.id))
    
    expected = [
        (1, 28064212),  # Priority 1, lower ID
        (1, 28064213),  # Priority 1, higher ID
        (2, 28064214),  # Priority 2
        (3, 28064215),  # Priority 3, lower ID
        (3, 28064216),  # Priority 3, higher ID
    ]
    
    assert results == expected, f"Expected {expected}, got {results}"
    
    print("Popped in correct order:")
    for p, id in results:
        print(f"  Priority {p}, ID {id}")
    print("TEST PASSED")


def test_rooms_acquire_release():
    """TEST 7: Room acquire/release drives next start"""
    print("\n" + "=" * 70)
    print("TEST 7: Rooms Manager - Acquire/Release")
    print("=" * 70)
    
    rooms = RoomsManager()
    
    # Initial state
    assert rooms.get_available_count() == 3, "Should start with 3 available"
    assert rooms.is_any_available(), "Should have rooms available"
    print("Initial state: 3 rooms available")
    
    # Acquire rooms
    assert rooms.acquire_if_available() == True, "Should acquire room 1"
    assert rooms.get_available_count() == 2, "Should have 2 available"
    print("Acquired room 1, 2 remaining")
    
    assert rooms.acquire_if_available() == True, "Should acquire room 2"
    assert rooms.get_available_count() == 1, "Should have 1 available"
    print("Acquired room 2, 1 remaining")
    
    assert rooms.acquire_if_available() == True, "Should acquire room 3"
    assert rooms.get_available_count() == 0, "Should have 0 available"
    assert rooms.are_all_occupied(), "All rooms should be occupied"
    print("Acquired room 3, 0 remaining")
    
    # Try to acquire when all occupied
    assert rooms.acquire_if_available() == False, "Should not acquire when full"
    print("Cannot acquire when all rooms occupied")
    
    # Release a room
    rooms.release()
    assert rooms.get_available_count() == 1, "Should have 1 available after release"
    assert rooms.is_any_available(), "Should have rooms available"
    print("Released room, 1 now available")
    
    # Can acquire again
    assert rooms.acquire_if_available() == True, "Should acquire after release"
    assert rooms.get_available_count() == 0, "Should have 0 available"
    print("Acquired released room")
    
    print("TEST PASSED")


def test_admission_line_fcfs():
    """TEST 8: Admission line FCFS by treatment finish time"""
    print("\n" + "=" * 70)
    print("TEST 8: Admission Line - FCFS by Treatment Finish Time")
    print("=" * 70)
    
    admission = AdmissionLine()
    
    # Add patients in order they finished treatment
    p1 = MockPatient(28064212, priority=1)
    p2 = MockPatient(28064213, priority=1)
    p3 = MockPatient(28064214, priority=1)
    
    # Patient 2 finishes first, then 1, then 3
    admission.admission_enqueue(p2, wait_start_time=20)
    admission.admission_enqueue(p1, wait_start_time=15)
    admission.admission_enqueue(p3, wait_start_time=25)
    
    print("Enqueued patients:")
    print("  Patient 213, finished at time 20")
    print("  Patient 212, finished at time 15")
    print("  Patient 214, finished at time 25")
    
    # Nurse is free, should get patient who finished earliest (15)
    current_time = 30
    next_patient = admission.admission_peek_pop_if_free(current_time)
    
    assert next_patient is not None, "Should get a patient"
    assert next_patient.id == 28064212, f"Expected ID 212 (earliest finish), got {next_patient.id}"
    assert admission.is_nurse_busy(), "Nurse should be busy now"
    print(f"Nurse assigned patient 212 (finished at 15)")
    
    # Try to get another while nurse busy
    next_patient = admission.admission_peek_pop_if_free(current_time)
    assert next_patient is None, "Should not get patient when nurse busy"
    print("Cannot get patient while nurse busy")
    
    # Nurse finishes
    admission.nurse_free()
    assert not admission.is_nurse_busy(), "Nurse should be free"
    print("✓ Nurse marked as free")
    
    # Get next patient (finished at 20)
    next_patient = admission.admission_peek_pop_if_free(current_time)
    assert next_patient.id == 28064213, f"Expected ID 213, got {next_patient.id}"
    print("Nurse assigned patient 213 (finished at 20)")
    
    print("TEST PASSED")


def test_integration_scenario():
    """TEST 9: Integration scenario with multiple components"""
    print("\n" + "=" * 70)
    print("TEST 9: Integration - Multiple Components Working Together")
    print("=" * 70)
    
    # Create all resources
    resources = create_all_resources()
    scheduler = resources['scheduler']
    waiting_room = resources['waiting_room']
    rooms = resources['rooms']
    
    print("Scenario: 4 patients arrive, 3 rooms available")
    
    # 4 patients with different priorities
    patients = [
        MockPatient(28064212, priority=2),
        MockPatient(28064213, priority=1),
        MockPatient(28064214, priority=4),
        MockPatient(28064215, priority=3),
    ]
    
    # All enter waiting room
    for p in patients:
        waiting_room.waitingroom_push(p)
    
    print("4 patients in waiting room (priorities: 2, 1, 4, 3)")
    
    # Simulate trying to start treatment for all
    started = []
    while rooms.is_any_available() and not waiting_room.is_empty():
        if rooms.acquire_if_available():
            patient = waiting_room.waitingroom_pop_best()
            if patient:
                started.append(patient)
                # Schedule completion event
                scheduler.schedule(MockEvent(time=10 + patient.id % 10, patient=patient))
    
    assert len(started) == 3, f"Should start 3 patients, started {len(started)}"
    assert started[0].priority == 1, "First should be priority 1"
    assert started[1].priority == 2, "Second should be priority 2"
    assert started[2].priority == 3, "Third should be priority 3"
    
    print(f"Started 3 patients in priority order: P1, P2, P3")
    
    # Check waiting room
    remaining = waiting_room.waitingroom_pop_best()
    assert remaining.priority == 4, "Priority 4 should still be waiting"
    print("Priority 4 patient still waiting")
    
    # Check scheduler
    assert scheduler.size() == 3, "Should have 3 events scheduled"
    print("3 completion events scheduled")
    
    print("TEST PASSED")


def test_edge_cases():
    """TEST 10: Edge cases and boundary conditions"""
    print("\n" + "=" * 70)
    print("TEST 10: Edge Cases and Boundary Conditions")
    print("=" * 70)
    
    # Test empty queue operations
    scheduler = EventScheduler()
    assert scheduler.is_empty(), "New scheduler should be empty"
    assert scheduler.pop_next() is None, "Pop from empty should return None"
    print("Empty scheduler handled correctly")
    
    waiting_room = WaitingRoom()
    assert waiting_room.is_empty(), "New waiting room should be empty"
    assert waiting_room.waitingroom_pop_best() is None, "Pop from empty should return None"
    print("Empty waiting room handled correctly")
    
    # Test single patient priority 1
    p1 = MockPatient(28064212, priority=1)
    waiting_room.waitingroom_push(p1)
    popped = waiting_room.waitingroom_pop_best()
    assert popped.id == 28064212, "Should get the only patient"
    print("Single patient handled correctly")
    
    # Test rooms at capacity
    rooms = RoomsManager()
    for _ in range(3):
        rooms.acquire_if_available()
    assert rooms.acquire_if_available() == False, "Should not acquire 4th room"
    
    # Release too many times (should not go negative)
    rooms.release()
    rooms.release()
    rooms.release()
    rooms.release()  # Extra release
    assert rooms.get_available_count() == 3, "Should not exceed total rooms"
    print("Room limits enforced correctly")
    
    print("TEST PASSED")


def run_all_tests():
    """Run all test cases"""
    print("\n" + "🏥" * 35)
    print(" " * 15 + "SCHEDULER + QUEUES + ROOMS TEST SUITE")
    print(" " * 25 + "Member B")
    print("🏥" * 35)
    
    tests = [
        ("Event Scheduler - Basic Time Ordering", test_event_scheduler_basic),
        ("Event Scheduler - Priority Tie-Break", test_event_scheduler_priority_tiebreak),
        ("Event Scheduler - Patient ID Tie-Break", test_event_scheduler_patient_id_tiebreak),
        ("Event Scheduler - Complex Ordering", test_event_scheduler_complex_ordering),
        ("Assessment Line - FIFO", test_assessment_line_fifo),
        ("Waiting Room - Priority Ordering", test_waiting_room_priority_ordering),
        ("Rooms Manager - Acquire/Release", test_rooms_acquire_release),
        ("Admission Line - FCFS", test_admission_line_fcfs),
        ("Integration Scenario", test_integration_scenario),
        ("Edge Cases", test_edge_cases),
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
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {passed} ")
    print(f"Failed: {failed} ")
    print("=" * 70)
    
    if failed == 0:
        print("\n ALL TESTS PASSED! ")
        print("\nMember B deliverables are ready:")
        print(" Event scheduler with correct tie-breaks")
        print(" Assessment line (FIFO)")
        print(" Waiting room (priority queue)")
        print(" Admission line (FCFS)")
        print(" Rooms manager (3 rooms)")
        print("\nReady for integration with other members!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review and fix.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
