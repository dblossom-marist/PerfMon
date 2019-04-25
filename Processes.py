'''
Created on Mar 23, 2019

@author: blossom
'''

import psutil
from Database import Database
import getpass
from Pmutils import Pmutils

class Processes():
    '''
    classdocs
    '''

    def __init__(self):
        pass
            
    def collectProcesses(self, allUsers=False):
            
        returnTupleList = []
        for proc in psutil.process_iter():
            try:
                process = proc.as_dict(attrs=['pid', 'username'])
                p_id = process['pid']
                user = process['username']                
                #uname = os.getlogin()
                uname = getpass.getuser()
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
        #memPercent = process.memory_percent()
        memPercent = process.memory_full_info()
        ioCounters = process.io_counters()
        diskRead = ioCounters[2]
        diskWrite = ioCounters[3]
        cpuPercent = process.cpu_percent(interval=.00001) # TODO: get CPU percent to work better 
        isRunning = process.status() # process.is_running()  #process.status() will do text version
        priority = process.nice()
        
        return (name,username,cpuPercent,pid,Pmutils.convertBytes(memPercent.uss), Pmutils.convertBytes(diskRead), Pmutils.convertBytes(diskWrite),isRunning,priority)
        
    def updateDatabase(self):
        db = Database()
        db.updateProcessTable(self.collectProcesses(True))
        db.close()
