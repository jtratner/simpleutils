"""
simpletime - simple utilities to handle common tasks with time
"""

import datetime

def pretty_time(delimiter = '_',colon_sub = '-'):
    """Returns a str of the local time, nicely formatted, with the specific time in nice str
    delimiter replaces spaces, colon_sub replaces ':' in time
    """
    return time.asctime(time.localtime()).replace(':',colon_sub).replace(' ',delimiter)
