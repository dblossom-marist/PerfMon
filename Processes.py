'''
Created on Mar 23, 2019

@author: blossom
'''

import psutil
import os
from Database import Database

class Processes():
    '''
    classdocs
    '''

    def __init__(self):
        pass
        
    def collectProcesses(self, allUsers):
            
        returnTupleList = []
        for proc in psutil.process_iter():
            try:
                process = proc.as_dict(attrs=['pid', 'username'])
                p_id = process['pid']
                user = process['username']                
                uname = os.getlogin()
                if not allUsers and (user == uname):
                    returnTupleList.append(self.getProcessInfo(p_id))
                elif allUsers:
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
        db.updateProcessTable(self.collectProcesses(False))
        db.close()
        
p = Processes()

p.updateDatabase()


