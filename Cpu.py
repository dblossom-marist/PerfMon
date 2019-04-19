
import psutil
import datetime
from Database import Database

class Cpu:
    
    def __init__(self):
        logicalCPUs = psutil.cpu_count(logical = True)
        physicalCPUSs = psutil.cpu_count(logical = False)
        print("Logical CPUS: " + str(logicalCPUs))
        print("Physical CPUS: " + str(physicalCPUSs))
        
    def createTimeStamp(self):
        return datetime.datetime.now()

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
        db.updateCPUTimesAllTable(self.allCPUTimes(), self.createTimeStamp())
        db.updateOverAllCPUUsageTable(self.getOverallCPUPercent(), self.createTimeStamp())
        db.updatePerCPUPercentTable(self.getPerCPUPercent(), self.createTimeStamp())
        db.close()
        
c = Cpu()
c.updateDatabase()

        