'''
A class that collects CPU system information
'''
# Python lib import
import psutil
# Imports from this porject
from Database import Database
from Pmutils import Pmutils

class Cpu:
    
    def __init__(self):
        pass
    
    '''
    Returns a tuple of CPU usage times
    @return: a tuple of CPU usage times
    '''
    def allCPUTimes(self):
        return psutil.cpu_times(True)
    
    '''
    Returns the average CPU times
    @return: the aveage CPU times
    '''
    def avgCPUTimes(self):
        return psutil.cpu_times(False)
        
    ''' 
    A method to collect the average percent of CPU usage over
    all CPUS in the system
    @return: average cpu usage. 
    '''    
    def getOverallCPUPercent(self):
        # Setting percpu=false will average, true is all
        return psutil.cpu_percent(interval=0.5)
    
    '''
    A method that returns average of cpu usgae
    @return: average cpu usage
    '''
    def getPerCPUPercent(self):
        return psutil.cpu_percent(interval=0.5, percpu=True)
    
    '''
    A method that returns the number of CPUs in system.
    @param logicalCpuCount: False (default) return logical or physical CPUs.
    @return: CPU count requested
    '''
    def getCpuCount(self, logicalCpuCount = False):
        if isinstance(logicalCpuCount, bool):
            return psutil.cpu_count(logical = logicalCpuCount)

    '''
    A method that updates the databases.
    TODO: maybe make a different method for each table?
    '''
    def updateDatabase(self):
        db = Database()
        db.updateCPUTimesAllTable(self.allCPUTimes(), Pmutils.createTimeStamp())
        db.updateOverAllCPUUsageTable(self.getOverallCPUPercent(), Pmutils.createTimeStamp())
        db.updatePerCPUPercentTable(self.getPerCPUPercent(), Pmutils.createTimeStamp())
        db.close()
        
