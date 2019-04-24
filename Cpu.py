
import psutil
from Database import Database
from Pmutils import Pmutils

class Cpu:
    
    def __init__(self):
        pass

    def allCPUTimes(self):
        return psutil.cpu_times(True)
    
    def avgCPUTimes(self):
        return psutil.cpu_times(False)
        
    ''' A method to collect the average percent of CPU usage over
        all CPUS in the system '''    
    def getOverallCPUPercent(self):
        # Setting percpu=false will average, true is all
        return psutil.cpu_percent(interval=0.5)
        
    def getPerCPUPercent(self):
        return psutil.cpu_percent(interval=0.5, percpu=True)
    
    def updateDatabase(self):
        db = Database()
        db.updateCPUTimesAllTable(self.allCPUTimes(), Pmutils.createTimeStamp())
        db.updateOverAllCPUUsageTable(self.getOverallCPUPercent(), Pmutils.createTimeStamp())
        db.updatePerCPUPercentTable(self.getPerCPUPercent(), Pmutils.createTimeStamp())
        db.close()
