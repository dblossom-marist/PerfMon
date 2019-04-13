'''
Created on Apr 11, 2019

@author: blossom
'''

import sqlite3

class Database():
    '''
    classdocs
    '''
    dbName = "MetricCollector.db"
    dbLocation = ""
    
    sqlCreateProcTbl = """CREATE TABLE if not exists processes
                         (pid integer, name text, username text, memory numeric, 
                         disk_read numeric, disk_write numeric, cpu numeric, 
                         running integer, priority integer)"""
                         
    sqlCreateCPUsTbl = """CREATE TABLE if not exists all_cpus
                          (cpuN integer, user numeric, nice numeric, system numeric,
                          idle numeric, iowait numeric, irq numeric, softirq numeric,
                          steal numeric, guest numeric, guest_nice numeric, date numeric)"""
                          
    sqlUpdateAllCPUrow = """UPDATE all_cpus SET user=?, nice=?, system=?, idle=?,
                            iowait=?, irq=?, softirq=?, steal=?, guest=?, guest_nice=?,
                            date=? WHERE cpuN=?"""
                            
    sqlInsertAllCPUrow = """INSERT INTO all_cpus (cpuN,user,nice,system,idle,iowait,
                                                  irq,softirq,steal,guest,guest_nice,date) 
                                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""

    def __init__(self):
        self.connect()
        self.setCursor()
        self.createProcessTable()
        self.createCPUTimesAllTable()
        
    def setCursor(self):
        self.cursor = self.conn.cursor()
        
    def connect(self):
        self.conn = sqlite3.connect(self.dbLocation + self.dbName)
        
    def createProcessTable(self):
        self.cursor.execute(self.sqlCreateProcTbl)
        self.conn.commit()
        
    def createCPUTimesAllTable(self):
        self.cursor.execute(self.sqlCreateCPUsTbl)
        self.conn.commit()
                
    def close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        
    def updateCPUTimesAllTable(self, cpuTuple, date_time):
        cpuNumber = 0; #this will line up with cpuTuble
        for cpu in cpuTuple:
            
            self.cursor.execute("SELECT * FROM all_cpus WHERE cpuN=?",(cpuNumber,))
            
            if len(self.cursor.fetchall()) == 1:
                # Just update row
                self.cursor.execute(self.sqlUpdateAllCPUrow,
                                    (cpu[0],cpu[1],cpu[2],cpu[3],cpu[4],cpu[5],
                                     cpu[6],cpu[7],cpu[8],cpu[9],date_time,cpuNumber))
            else:
                self.cursor.execute(self.sqlInsertAllCPUrow,
                                    (cpuNumber,cpu[0],cpu[1],cpu[2],cpu[3],cpu[4],
                                        cpu[5],cpu[6],cpu[7],cpu[8],cpu[9],date_time))
            
            cpuNumber = cpuNumber + 1
        
    def updateProcessTable(self, processTupleList):
        # pid, name, username, memory, disk_read, disk_write, cpu, running, priority
        
        for processTuple in processTupleList:
            
            self.cursor.execute("SELECT * FROM processes WHERE pid=? AND name=? AND username=?", 
                (processTuple[0],processTuple[1],processTuple[2],))
            
            if len(self.cursor.fetchall()) == 1:
                self.cursor.execute("UPDATE processes SET memory=?,disk_read=?,disk_write=?,cpu=?,running=?,priority=? WHERE pid=? AND name=? AND username=?",
                            (processTuple[3],processTuple[4],processTuple[5],processTuple[6],processTuple[7],processTuple[8],
                             processTuple[0],processTuple[1],processTuple[2]))
            else:
                self.cursor.execute("INSERT INTO processes (pid,name,username,memory,disk_read,disk_write,cpu,running,priority) VALUES (?,?,?,?,?,?,?,?,?)",
                            (processTuple[0],processTuple[1],processTuple[2],processTuple[3],processTuple[4],processTuple[5],processTuple[6],processTuple[7],processTuple[8]))
                
                self.conn.commit()   

                