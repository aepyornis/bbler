"""
Various helper functions shared amongst the BBL python scripts
"""
import sys
import requests
from time import sleep

PAUSE_BEFORE_RETRY = 15


class BisWebUnavailableException(requests.exceptions.RequestException):
    pass


def bis_retry(func):
    """
    A decorator for requests to BIS.
    It retries the requests at most 3 times (waiting 15 seconds b/w each one).
    """
    def wrapper(*args, attempt=1):
        if attempt > 3:
            print("tried 3 times but failed to complete the requests", file=sys.stderr)
            return None
        try:
            return func(*args)
        except requests.exceptions.RequestException:
            print("BIS request failed, on attempt {}. Pausing...".format(attempt), file=sys.stderr)
            sleep(PAUSE_BEFORE_RETRY)
            return wrapper(*args, attempt=(attempt+1))
        except:
            print("Unexpected error:", sys.exc_info()[0], file=sys.stderr)
            print("Requested failed", file=sys.stderr)
            raise
    return wrapper
