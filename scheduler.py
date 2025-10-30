from scheduler_queues_rooms import create_all_resources

# Create shared singletons from your existing factory
_resources = create_all_resources()
_sched = _resources["scheduler"]

def schedule(ev): _sched.schedule(ev)
def pop_next():   return _sched.pop_next()
def peek():       return _sched.peek()
def empty():      return _sched.is_empty()
