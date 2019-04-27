"""
A utility class for common methods required in multiple locations.
@author: D. Blossom but credit to B. Murali for the convert_bytes method
"""
# Needed imports
import datetime


class Pmutils:
    
    def __init__(self):
        pass
    
    '''
    A static method that will convert a number to a human readable string
    IE: 2GB or 1MB for display in the GUI
    @param number: the number to format.
    '''
    @staticmethod
    def convert_bytes(number):
        if isinstance(number, float) or isinstance(number, int):
            symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
            prefix = {}
            for i, s in enumerate(symbols):
                prefix[s] = 1 << (i + 1) * 10
            for s in reversed(symbols):
                if number >= prefix[s]:
                    value = float(number) / prefix[s]
                    return '%.1f%s' % (value, s)
            return "%sB" % number
    
    '''
    A simple method that returns date/time mainly used for DB stuff.
    '''
    @staticmethod
    def create_time_stamp():
        return datetime.datetime.now()
