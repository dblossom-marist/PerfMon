'''
Created on Mar 23, 2019

@author: blossom
'''

import psutil
import os
import time
from Database import Database
from psutil import cpu_percent


class Processes():
    '''
    classdocs
    '''

    def __init__(self):
        pass
    
    def convertBytes(self,number):
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10
        for s in reversed(symbols):
            if number >= prefix[s]:
                value = float(number) / prefix[s]
                return '%.1f%s' % (value, s)
        return "%sB" % number
        
    def collectProcesses(self, allUsers=False):
            
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
        #memPercent = process.memory_percent()
        memPercent = process.memory_full_info()
        ioCounters = process.io_counters()
        diskRead = ioCounters[2]
        diskWrite = ioCounters[3]
        cpuPercent = process.cpu_percent(interval=.00001) # TODO: get CPU percent to work better 
        isRunning = process.status() # process.is_running()  #process.status() will do text version
        priority = process.nice()
        
        return (name,username,cpuPercent,pid,self.convertBytes(memPercent.uss), diskRead, diskWrite,isRunning,priority)
        
    def updateDatabase(self):
        db = Database()
        # Pass True for only logged in user, False (or nothing) for all user processes
        # TODO: Do we want to get more granular? 
        db.updateProcessTable(self.collectProcesses(True))
        db.close()

#===============================================================================
# p = Processes()
# while True:
#     for proc in psutil.process_iter():
#         p_id = proc.as_dict(attrs=['pid'])
#         pp = p.getProcessInfo(p_id['pid'])
#         if pp[6] > 0:
#             print(str(pp[0]) + " - " + str(pp[6]))
#===============================================================================
