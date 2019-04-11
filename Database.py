'''
Created on Apr 11, 2019

@author: blossom
'''

import sqlite3

class Database():
    '''
    classdocs
    '''

    def __init__(self):
        self.connect()
    
    def connect(self):
        self.conn = sqlite3.connect('MetricCollector.db')
        
    def close(self):
        self.conn.close()
        
    def updateProcessTable(self, processTupleList):
        # pid, name, username, memory, disk_read, disk_write, cpu, running, priority
        
        #processTupleList = Processes.collectProcesses()
                
        self.cur = self.conn.cursor()
        
        for processTuple in processTupleList:
            
            self.cur.execute("SELECT * FROM processes WHERE pid=? AND name=? AND username=?", 
                (processTuple[0],processTuple[1],processTuple[2],))
            
            if len(self.cur.fetchall()) == 1:
                self.cur.execute("UPDATE processes SET memory=?,disk_read=?,disk_write=?,cpu=?,running=?,priority=? WHERE pid=? AND name=? AND username=?",
                            (processTuple[3],processTuple[4],processTuple[5],processTuple[6],processTuple[7],processTuple[8],
                             processTuple[0],processTuple[1],processTuple[2],))
            else:
                self.cur.execute("INSERT INTO processes (pid,name,username,memory,disk_read,disk_write,cpu,running,priority) VALUES (?,?,?,?,?,?,?,?,?)",
                            (processTuple[0],processTuple[1],processTuple[2],processTuple[3],processTuple[4],processTuple[5],processTuple[6],processTuple[7],processTuple[8]))
                
                self.conn.commit()   
                