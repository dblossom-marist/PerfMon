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
    @deprecated: use Pmutils.create_time_stamp() instead.
    @return: date/time
    ''' 
    def create_time_stamp(self):
        return datetime.datetime.now()
    
    '''
    A method that returns overall system memory percent
    @return: overall system memory percent
    '''
    def get_average_system_memory(self):
        mem = psutil.virtual_memory()
        return mem[2]
    
    '''
    A method that updates the database with average system memory.
    '''
    def update_database(self):
        db = Database()
        db.update_average_memory_table(self.get_average_system_memory(), Pmutils.create_time_stamp())
