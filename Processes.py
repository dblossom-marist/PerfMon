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
                
                pid = psutil.Process(p_id)
                name = pid.name()
                username = pid.username()
                memPercent = pid.memory_percent()
                ioCounters = pid.io_counters()
                diskRead = ioCounters[2];
                diskWrite = ioCounters[3];
                cpuPercent = pid.cpu_percent(interval=0.1)
                isRunning = pid.status() # pid.is_running()  #pid.status() will do text version
                priority = pid.nice() 
                
                returnTupleList.append((p_id,name,username,memPercent,diskRead,diskWrite,cpuPercent,isRunning,priority))
                                                    
            except psutil.NoSuchProcess:
                pass
            
        return returnTupleList
            
    def updateDatabase(self):
        db = Database()
        db.updateProcessTable(self.collectProcesses())
        db.close()
        
p = Processes()

p.updateDatabase()


