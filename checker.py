from flask import session
from functools import wraps


def check_logged_in(func) -> 'func':
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('logged_in'):
            return func(*args, **kwargs)
        return 'You ara not logged in'

    return wrapper
