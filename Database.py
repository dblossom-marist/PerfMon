'''
Created on Apr 11, 2019

@author: blossom
'''

import sqlite3

class Database():
    '''
    classdocs
    '''
    sqlCreateProcTbl = """CREATE TABLE if not exists processes
                         (pid integer, name text, username text, memory numeric, 
                         disk_read numeric, disk_write numeric, cpu numeric, 
                         running integer, priority integer)"""

    def __init__(self):
        self.connect()
        self.setCursor()
        self.createProcessTable()
        
    def setCursor(self):
        self.cursor = self.conn.cursor()
        
    def connect(self):
        self.conn = sqlite3.connect('MetricCollector.db')

    def processTableExist(self):
        self.cursor.execute("""SELECT COUNT(*) 
                                      FROM sqlite_master 
                                      WHERE name = 'processes'""")
        if len(self.cursor.fetchall()) == 1:
            return True
        else:
            return False
        
    def createProcessTable(self):
        self.cursor.execute(self.sqlCreateProcTbl)
        self.conn.commit()
        #self.cursor.close()
        #self.conn.close()
        #self.connect()
        #self.setCursor()
                
    def close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        
    def updateProcessTable(self, processTupleList):
        # pid, name, username, memory, disk_read, disk_write, cpu, running, priority
        
        for processTuple in processTupleList:
            
            self.cursor.execute("SELECT * FROM processes WHERE pid=? AND name=? AND username=?", 
                (processTuple[0],processTuple[1],processTuple[2],))
            
            if len(self.cursor.fetchall()) == 1:
                self.cursor.execute("UPDATE processes SET memory=?,disk_read=?,disk_write=?,cpu=?,running=?,priority=? WHERE pid=? AND name=? AND username=?",
                            (processTuple[3],processTuple[4],processTuple[5],processTuple[6],processTuple[7],processTuple[8],
                             processTuple[0],processTuple[1],processTuple[2],))
            else:
                self.cursor.execute("INSERT INTO processes (pid,name,username,memory,disk_read,disk_write,cpu,running,priority) VALUES (?,?,?,?,?,?,?,?,?)",
                            (processTuple[0],processTuple[1],processTuple[2],processTuple[3],processTuple[4],processTuple[5],processTuple[6],processTuple[7],processTuple[8]))
                
                self.conn.commit()   
                
d = Database()
d.close()
                