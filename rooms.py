from scheduler_queues_rooms import create_all_resources
_resources = create_all_resources()
_rooms = _resources["rooms"]

def acquire_if_available(): return _rooms.acquire_if_available()
def release():              _rooms.release()
def available_count():      return _rooms.get_available_count()

def reset(n=3):
    # soft reset for tests/demos
    _rooms._total = n
    _rooms._occupied = 0
