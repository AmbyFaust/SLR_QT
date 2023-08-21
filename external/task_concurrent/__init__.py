from .task_concurrent import concurrent_manager
from . import waiter


def dicted(key, func=None):
    if func is None:
        def wrapper(f):
            def wrapped(*args, **kwargs):
                res = f(*args, **kwargs)
                return key, res
            return wrapped
        return wrapper

    def wrapped(*args, **kwargs):
        res = func(*args, **kwargs)
        return key, res
    return wrapped


def passed(value):
    return lambda val=value: val
