"""
A class that collects CPU system information
"""
# Python lib import
import psutil
# Imports from this project
from Database import Database
from Pmutils import Pmutils


class Cpu:
    
    def __init__(self):
        pass
    
    '''
    Returns a tuple of CPU usage times
    @return: a tuple of CPU usage times
    '''
    def all_cpu_times(self):
        return psutil.cpu_times(True)
    
    '''
    Returns the average CPU times
    @return: the average CPU times
    '''
    def avg_cpu_times(self):
        return psutil.cpu_times(False)
        
    ''' 
    A method to collect the average percent of CPU usage over
    all CPUS in the system
    @return: average cpu usage. 
    '''    
    def get_overall_cpu_percent(self):
        # Setting percpu=false will average, true is all
        return psutil.cpu_percent(interval=0.5)
    
    '''
    A method that returns average of cpu usgae
    @return: average cpu usage
    '''
    def get_per_cpu_percent(self):
        return psutil.cpu_percent(interval=0.5, percpu=True)
    
    '''
    A method that returns the number of CPUs in system.
    @param logicalCpuCount: False (default) return logical or physical CPUs.
    @return: CPU count requested
    '''
    def get_cpu_count(self, logical_cpu_count = False):
        if isinstance(logical_cpu_count, bool):
            return psutil.cpu_count(logical = logical_cpu_count)

    '''
    A method that updates the databases.
    TODO: maybe make a different method for each table?
    '''
    def update_database(self):
        db = Database()
        db.update_cpu_times_all_table(self.all_cpu_times(), Pmutils.create_time_stamp())
        db.update_over_all_cpu_usage_table(self.get_overall_cpu_percent(), Pmutils.create_time_stamp())
        db.update_per_cpu_percent_table(self.get_per_cpu_percent(), Pmutils.create_time_stamp())
        db.close()
