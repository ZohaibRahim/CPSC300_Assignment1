from typing import Optional, List, Any
import heapq


# EVENT SCHEDULER

class EventScheduler:
    """
    Global event queue ordered by:
    1. Time (ascending)
    2. Patient priority (ascending, lower = higher priority)
    3. Patient number (ascending)
    """
    
    def __init__(self):
        self._heap = []
        self._counter = 0  # Tie-breaker for insertion order
    
    def schedule(self, event):
        """
        Schedule an event to be processed.
        
        Events are ordered by:
        - time (primary)
        - patient.priority (secondary, if exists)
        - patient.id (tertiary)
        
        :param event: Event object with .time and .patient attributes
        """
        # Create sort key: (time, priority, patient_id, counter)
        # Priority: Use 999 if None (for events without assessed patients)
        priority = event.patient.priority if event.patient.priority is not None else 999
        patient_id = event.patient.id
        
        # Use counter to maintain stable sort for truly identical events
        sort_key = (event.time, priority, patient_id, self._counter)
        self._counter += 1
        
        heapq.heappush(self._heap, (sort_key, event))
    
    def pop_next(self) -> Optional[Any]:
        """
        Remove and return the next event to process.
        
        :return: Next Event object, or None if queue is empty
        """
        if self._heap:
            _, event = heapq.heappop(self._heap)
            return event
        return None
    
    def is_empty(self) -> bool:
        """Check if the event queue is empty"""
        return len(self._heap) == 0
    
    def peek(self) -> Optional[Any]:
        """Look at the next event without removing it"""
        if self._heap:
            return self._heap[0][1]
        return None
    
    def size(self) -> int:
        """Get number of events in queue"""
        return len(self._heap)


# ASSESSMENT LINE (FIFO)
# ============================================================================

class AssessmentLine:
    """
    FIFO queue for walk-in patients waiting for triage assessment.
    First in, first out.
    """
    
    def __init__(self):
        self._queue = []
    
    def enqueue_assessment(self, patient):
        """
        Add a patient to the assessment line.
        
        :param patient: Patient object
        """
        self._queue.append(patient)
    
    def dequeue_assessment(self) -> Optional[Any]:
        """
        Remove and return the next patient in line for assessment.
        
        :return: Patient object, or None if line is empty
        """
        if self._queue:
            return self._queue.pop(0)
        return None
    
    def is_empty(self) -> bool:
        """Check if assessment line is empty"""
        return len(self._queue) == 0
    
    def size(self) -> int:
        """Get number of patients in assessment line"""
        return len(self._queue)
    
    def peek(self) -> Optional[Any]:
        """Look at next patient without removing"""
        if self._queue:
            return self._queue[0]
        return None


# WAITING ROOM (PRIORITY QUEUE)
# ============================================================================

class WaitingRoom:
    """
    Priority queue for patients waiting for treatment.
    
    Ordering:
    1. Priority (ascending: 1 is highest, 5 is lowest)
    2. Patient ID (ascending: lower patient number first for ties)
    """
    
    def __init__(self):
        self._heap = []
    
    def waitingroom_push(self, patient):
        """
        Add a patient to the waiting room.
        Automatically maintains priority order.
        
        :param patient: Patient object with .priority and .id attributes
        """
        # Sort key: (priority, patient_id)
        sort_key = (patient.priority, patient.id)
        heapq.heappush(self._heap, (sort_key, patient))
    
    def waitingroom_pop_best(self) -> Optional[Any]:
        """
        Remove and return the highest priority patient.
        Priority 1 is highest. Ties broken by patient ID.
        
        :return: Patient object, or None if waiting room is empty
        """
        if self._heap:
            _, patient = heapq.heappop(self._heap)
            return patient
        return None
    
    def is_empty(self) -> bool:
        """Check if waiting room is empty"""
        return len(self._heap) == 0
    
    def size(self) -> int:
        """Get number of patients in waiting room"""
        return len(self._heap)
    
    def peek(self) -> Optional[Any]:
        """Look at next patient without removing"""
        if self._heap:
            return self._heap[0][1]
        return None


# ADMISSION LINE (FCFS by treatment finish time)
# ============================================================================

class AdmissionLine:
    """
    Queue for Priority 1 patients waiting for the single admission nurse.
    First-come-first-served based on when treatment finished.
    """
    
    def __init__(self):
        self._queue = []  # List of (wait_start_time, patient) tuples
        self._nurse_busy = False
        self._current_patient = None
    
    def admission_enqueue(self, patient, wait_start_time):
        """
        Add a Priority 1 patient to admission queue.
        
        :param patient: Patient object
        :param wait_start_time: Time when patient's treatment finished
        """
        self._queue.append((wait_start_time, patient))
        # Sort by wait_start_time to maintain FCFS
        self._queue.sort(key=lambda x: x[0])
    
    def admission_peek_pop_if_free(self, now) -> Optional[Any]:
        """
        If nurse is free, pop next patient and mark nurse as busy.
        
        :param now: Current simulation time
        :return: Patient object if nurse was free, None if nurse busy or no patients
        """
        if self._nurse_busy:
            return None
        
        if not self._queue:
            return None
        
        wait_start_time, patient = self._queue.pop(0)
        self._nurse_busy = True
        self._current_patient = patient
        
        # Calculate admission wait time
        if hasattr(patient, 'admission_wait'):
            patient.admission_wait = now - wait_start_time
        
        return patient
    
    def nurse_free(self):
        """
        Mark the admission nurse as free (called after admission completes).
        """
        self._nurse_busy = False
        self._current_patient = None
    
    def is_nurse_busy(self) -> bool:
        """Check if admission nurse is currently busy"""
        return self._nurse_busy
    
    def is_empty(self) -> bool:
        """Check if admission queue is empty"""
        return len(self._queue) == 0
    
    def size(self) -> int:
        """Get number of patients waiting for admission"""
        return len(self._queue)
    
    def peek(self) -> Optional[Any]:
        """Look at next patient without removing"""
        if self._queue:
            return self._queue[0][1]
        return None


# TREATMENT ROOMS MANAGER
# ============================================================================

class RoomsManager:
    """
    Manages 3 treatment rooms.
    Tracks availability and publishes count changes.
    """
    
    TOTAL_ROOMS = 3
    
    def __init__(self):
        self._total = self.TOTAL_ROOMS
        self._occupied = 0
    
    def acquire_if_available(self) -> bool:
        """
        Try to acquire a treatment room.
        
        :return: True if room was acquired, False if all rooms occupied
        """
        if self._occupied < self._total:
            self._occupied += 1
            return True
        return False
    
    def release(self):
        """
        Release a treatment room (patient departed).
        """
        if self._occupied > 0:
            self._occupied -= 1
    
    def get_available_count(self) -> int:
        """
        Get number of currently available rooms.
        
        :return: Number of free rooms (0-3)
        """
        return self._total - self._occupied
    
    def get_occupied_count(self) -> int:
        """Get number of occupied rooms"""
        return self._occupied
    
    def is_any_available(self) -> bool:
        """Check if any room is available"""
        return self._occupied < self._total
    
    def are_all_occupied(self) -> bool:
        """Check if all rooms are occupied"""
        return self._occupied >= self._total


# FACTORY FUNCTIONS
# ============================================================================

def create_scheduler():
    """Create and return an EventScheduler instance"""
    return EventScheduler()


def create_assessment_line():
    """Create and return an AssessmentLine instance"""
    return AssessmentLine()


def create_waiting_room():
    """Create and return a WaitingRoom instance"""
    return WaitingRoom()


def create_admission_line():
    """Create and return an AdmissionLine instance"""
    return AdmissionLine()


def create_rooms_manager():
    """Create and return a RoomsManager instance"""
    return RoomsManager()


def create_all_resources():
    """
    Convenience function to create all shared resources at once.
    
    :return: Dictionary with all resources
    """
    return {
        'scheduler': create_scheduler(),
        'assessment_line': create_assessment_line(),
        'waiting_room': create_waiting_room(),
        'admission_line': create_admission_line(),
        'rooms': create_rooms_manager()
    }


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("SCHEDULER + QUEUES + ROOMS MODULE - MEMBER B")
    print("=" * 70)
    print("\nThis module provides:")
    print("\n1. EventScheduler")
    print("   - schedule(event): Add event to queue")
    print("   - pop_next(): Get next event by time/priority/patient#")
    print("\n2. AssessmentLine (FIFO)")
    print("   - enqueue_assessment(patient): Add to line")
    print("   - dequeue_assessment(): Get next patient")
    print("\n3. WaitingRoom (Priority Queue)")
    print("   - waitingroom_push(patient): Add patient")
    print("   - waitingroom_pop_best(): Get highest priority patient")
    print("\n4. AdmissionLine (FCFS by treatment finish time)")
    print("   - admission_enqueue(patient, wait_start_time): Add patient")
    print("   - admission_peek_pop_if_free(now): Get next if nurse free")
    print("   - nurse_free(): Mark nurse as available")
    print("\n5. RoomsManager (3 treatment rooms)")
    print("   - acquire_if_available(): Try to get a room")
    print("   - release(): Free up a room")
    print("   - get_available_count(): Check how many rooms free")
    print("\n" + "=" * 70)
    print("\nTo use in simulation:")
    print("  resources = create_all_resources()")
    print("  scheduler = resources['scheduler']")
    print("  rooms = resources['rooms']")
    print("  # etc...")
    print("=" * 70)
