'''
Created on Mar 23, 2019
@author: blossom
'''

import psutil
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

    def convert_bytes(self,n):
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10
        for s in reversed(symbols):
            if n >= prefix[s]:
                value = float(n) / prefix[s]
                return '%.1f%s' % (value, s)
        return "%sB" % n

    def collectProcesses(self):
        print("Entering collectProcess")
        start = time.time()

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

    def updateDatabase(self):
        db = Database()
        db.updateProcessTable(self.collectProcesses())
        db.close()




p = Processes()

#p.updateDatabase()