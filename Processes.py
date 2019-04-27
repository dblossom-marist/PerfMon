'''
This class is used to collect Linux system processes.
Created on Mar 23, 2019
@author: Dan Blossom
'''

# Python Libs needed
import psutil
import getpass
# Python files from this project
from Database import Database
from Pmutils import Pmutils

class Processes():
 
    # No init needed,
    def __init__(self):
        pass
    '''        
    Method that collects all system processes
    @param allUsers a default (to false) parameter if
           all users should be collected or current.
    @return a tuple of processes
    '''
    def collectProcesses(self, allUsers=False):
        # Tuple to return
        returnTupleList = []
        # Loop through all processes.
        for proc in psutil.process_iter():
            # Does process exist?
            try:
                process = proc.as_dict(attrs=['pid', 'username'])
                p_id = process['pid']
                user = process['username']                
                #uname = os.getlogin()
                uname = getpass.getuser()
                # Do we collect all users or not? Then call getProcess.
                if not allUsers and (user == uname):
                    returnTupleList.append(self.getProcessInfo(p_id))
                elif allUsers:
                    returnTupleList.append(self.getProcessInfo(p_id))
            # Do nothing if it doesn't exist
            except psutil.NoSuchProcess:
                pass
        return returnTupleList
    '''
    Method that collects information on a processes given a PID
    @param pid: the pid of the process to gather
    @return a tuple of process information
    '''
    def getProcessInfo(self, pid):
        
        process = psutil.Process(pid)
        
        name = process.name()
        username = process.username()
        #memPercent = process.memory_percent()
        # Returns all info about the memory.
        memPercent = process.memory_full_info()
        ioCounters = process.io_counters()
        diskRead = ioCounters[2]
        diskWrite = ioCounters[3]
        cpuPercent = process.cpu_percent(interval=.00001) # TODO: get CPU percent to work better 
        isRunning = process.status() # process.is_running()  #process.status() will do text version
        priority = process.nice()
        
        return (name,username,cpuPercent,pid,Pmutils.convertBytes(memPercent.uss), Pmutils.convertBytes(diskRead), Pmutils.convertBytes(diskWrite),isRunning,priority)
    '''    
    A method that will update the database with all running system processes.
    '''
    def updateDatabase(self):
        db = Database()
        db.updateProcessTable(self.collectProcesses(True))
        db.close()
