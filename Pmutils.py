
import datetime

class Pmutils:
    
    def __init__(self):
        pass
    
    @staticmethod
    def convertBytes(number):
        if isinstance(number, float):
            symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
            prefix = {}
            for i, s in enumerate(symbols):
                prefix[s] = 1 << (i + 1) * 10
            for s in reversed(symbols):
                if number >= prefix[s]:
                    value = float(number) / prefix[s]
                    return '%.1f%s' % (value, s)
            return "%sB" % number
    
    @staticmethod
    def createTimeStamp():
        return datetime.datetime.now()
