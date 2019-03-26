'''
Created on Mar 23, 2019

@author: blossom
'''

import psutil
import sqlite3

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
        
        # pid, name, username, memory, disk_read, disk_write, cpu, running, priority
        
        processTupleList = self.collectProcesses()
        
        conn = sqlite3.connect('MetricCollector')
                
        cur = conn.cursor()
        
        for processTuple in processTupleList:
            
            cur.execute("SELECT * FROM processes WHERE pid=? AND name=? AND username=?", 
                (processTuple[0],processTuple[1],processTuple[2],))
            
            if len(cur.fetchall()) == 1:
                cur.execute("UPDATE processes SET memory=?,disk_read=?,disk_write=?,cpu=?,running=?,priority=? WHERE pid=? AND name=? AND username=?",
                            (processTuple[3],processTuple[4],processTuple[5],processTuple[6],processTuple[7],processTuple[8],
                             processTuple[0],processTuple[1],processTuple[2],))
            else:
                cur.execute("INSERT INTO processes (pid,name,username,memory,disk_read,disk_write,cpu,running,priority) VALUES (?,?,?,?,?,?,?,?,?)",
                            (processTuple[0],processTuple[1],processTuple[2],processTuple[3],processTuple[4],processTuple[5],processTuple[6],processTuple[7],processTuple[8]))
                
                conn.commit()
                
        conn.close()


