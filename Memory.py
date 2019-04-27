"""
A class that collects needed memory information about the system.
Mainly overall memory usage.
@author: D. Blossom
"""
# Python imports
import datetime
import psutil
# Import classes created from this project
from Database import Database
from Pmutils import Pmutils


class Memory:
    
    def __init__(self):
        pass
    
    '''
    A method that returns a timestamp that can be deprecated due to Pmutils
    @deprecated: use Pmutils.createTimeStamp() instead.
    @return: date/time
    ''' 
    def createTimeStamp(self):
        return datetime.datetime.now()
    
    '''
    A method that returns overall system memory percent
    @return: overall system memory percent
    '''
    def getAverageSystemMemory(self):
        mem = psutil.virtual_memory()
        return mem[2]
    
    '''
    A method that updates the database with average system memory.
    '''
    def updateDatabase(self):
        db = Database()
        db.updateAverageMemoryTable(self.getAverageSystemMemory(), Pmutils.createTimeStamp())
