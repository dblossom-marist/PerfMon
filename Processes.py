'''
Created on Mar 23, 2019

@author: blossom
'''

import psutil
from Database import Database

class Processes():
    '''
    classdocs
    '''

    def __init__(self):
        pass
        
    def collectProcesses(self):
        
        returnTupleList = []
        
        for proc in psutil.process_iter():
            try:
                #self.pids = proc.as_dict(attrs=['name', 'pid', 'username', 'memory_percent', 'cpu_percent'])
                process = proc.as_dict(attrs=['pid'])
                p_id = process['pid']
                returnTupleList.append(self.getProcessInfo(p_id))
            except psutil.NoSuchProcess:
                pass
            
        return returnTupleList
    
    def getProcessInfo(self, pid):
             
        process = psutil.Process(pid)
        name = process.name()
        username = process.username()
        memPercent = process.memory_percent()
        ioCounters = process.io_counters()
        diskRead = ioCounters[2];
        diskWrite = ioCounters[3];
        cpuPercent = process.cpu_percent(interval=0.1)
        #cpuPercent = process.cpu_percent(interval=None)
        isRunning = process.status() # process.is_running()  #process.status() will do text version
        priority = process.nice()
        
        return (pid, name, username, memPercent, diskRead, diskWrite, cpuPercent, isRunning, priority)
        
    def updateDatabase(self):
        db = Database()
        db.updateProcessTable(self.collectProcesses())
        db.close()
        
p = Processes()

p.updateDatabase()


