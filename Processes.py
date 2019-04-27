"""
This class is used to collect Linux system processes.
Created on Mar 23, 2019
@author: Dan Blossom
"""

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
    def collect_processes(self, all_users=False):
        # Tuple to return
        return_tuple_list = []
        # Loop through all processes.
        for proc in psutil.process_iter():
            # Does process exist?
            try:
                process = proc.as_dict(attrs=['pid', 'username'])
                p_id = process['pid']
                user = process['username']                
                # uname = os.getlogin()
                uname = getpass.getuser()
                # Do we collect all users or not? Then call getProcess.
                if not all_users and (user == uname):
                    return_tuple_list.append(self.get_process_info(p_id))
                elif all_users:
                    return_tuple_list.append(self.get_process_info(p_id))
            # Do nothing if it doesn't exist
            except psutil.NoSuchProcess:
                pass
        return return_tuple_list

    '''
    Method that collects information on a processes given a PID
    @param pid: the pid of the process to gather
    @return a tuple of process information
    '''
    def get_process_info(self, pid):
        
        process = psutil.Process(pid)
        
        name = process.name()
        username = process.username()
        #memPercent = process.memory_percent()
        # Returns all info about the memory.
        mem_percent = process.memory_full_info()
        io_counters = process.io_counters()
        disk_read = io_counters[2]
        disk_write = io_counters[3]
        cpu_percent = process.cpu_percent(interval=.00001)  # TODO: get CPU percent to work better
        is_running = process.status()  # process.is_running()  #process.status() will do text version
        priority = process.nice()
        
        return (name, username, cpu_percent, pid, Pmutils.convert_bytes(mem_percent.uss), Pmutils.convert_bytes(disk_read), Pmutils.convert_bytes(disk_write), is_running, priority)

    '''    
    A method that will update the database with all running system processes.
    '''
    def update_database(self):
        db = Database()
        db.update_process_table(self.collect_processes(True))
        db.close()
