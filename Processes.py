'''
Created on Mar 23, 2019
@author: blossom
'''

import psutil
import os
import time
from Database import Database
from psutil import cpu_percent
from Database import Database
import time
import getpass
import os


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
            # Added if loop to send process that belongs only to the user.
            # TODO : add option to show all users using menu or checkbox
            # Issue : This loop will update database with only one user
            # instead of all system process
            if proc.username() == os.getlogin():
                try:
                    # self.pids = proc.as_dict(attrs=['name', 'pid', 'username', 'memory_percent', 'cpu_percent'])

                    process = proc.as_dict(attrs=['pid'])

                    p_id = process['pid']

                    pid = psutil.Process(p_id)
                    name = pid.name()
                    username = pid.username()
                    #memPercent = pid.memory_percent()
                    mem = pid.memory_full_info()
                    ioCounters = pid.io_counters()
                    diskRead = ioCounters[2]
                    diskWrite = ioCounters[3]
                    cpuPercent = pid.cpu_percent(interval=.00001)
                    #cpuPercent = 1
                    isRunning = pid.status()  # pid.is_running()  #pid.status() will do text version
                    priority = pid.nice()

                    #returnTupleList.append(
                        #(p_id, name, username, memPercent, diskRead, diskWrite, cpuPercent, isRunning, priority))
                    returnTupleList.append(
                        (name, username, cpuPercent,p_id,self.convert_bytes(mem.uss),self.convert_bytes(diskRead), self.convert_bytes(diskWrite), isRunning))

                except psutil.NoSuchProcess:
                    pass

        print(time.time() - start)
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

p = Processes()

#p.updateDatabase()