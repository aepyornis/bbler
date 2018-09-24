"""
Various helper functions shared amongst the BBL python scripts
"""
import sys
import requests
from time import sleep

PAUSE_BEFORE_RETRY = 15
UNAVAILABLE = 'Due to the high demand it may take a little longer'

class BisWebUnavailableException(requests.exceptions.RequestException):
    pass


def bis_retry(func):
    """
    A decorator for requests to BIS.

    If the request returns a string, it will check the text to see if
    it contains the 'unavailable' message. If it does it triggers a retry.

    It retries the requests at most 3 times, waiting pausing between each one.
    """
    def wrapper(*args, attempt=1):
        if attempt > 3:
            print("tried 3 times but failed to complete the requests", file=sys.stderr)
            return None
        try:
            text = func(*args)
            if type(text) == str:
                if UNAVAILABLE in text:
                    raise BisWebUnavailableException
                else:
                    return text
        except requests.exceptions.RequestException:
            print("BIS request failed, on attempt {}. Pausing...".format(attempt), file=sys.stderr)
            sleep(PAUSE_BEFORE_RETRY)
            return wrapper(*args, attempt=(attempt+1))
        except:
            print("Unexpected error:", sys.exc_info()[0], file=sys.stderr)
            print("Requested failed", file=sys.stderr)
            raise
    return wrapper
