'''
Created on Apr 11, 2019

@author: blossom
'''
# test

import sqlite3

class Database():
    '''
    classdocs
    '''
    dbName = "MetricCollector.db"
    #dbLocation = "/usr/share/perfmon/"
    dbLocation = "/usr/bin/perfmon/"
    
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
                                                
    sqlCreateOverallCPUavgTbl = """CREATE TABLE if not exists all_cpus_avg
                                   (all_cpu numeric, date numeric)"""
                                   
    sqlInsertCPUOverallAvg = """INSERT INTO all_cpus_avg (all_cpu, date) VALUES(?,?)"""
    
    sqlCreatePerCpuPercentTbl = """CREATE TABLE if not exists per_cpu_percent
                                (cpu integer, cpu_percent numeric, date numeric)"""
                                
    sqlInsertPerCpuPercent = """INSERT INTO per_cpu_percent(cpu,cpu_percent,date) VALUES(?,?,?)"""
    
    sqlCreateMemoryTbl = """CREATE TABLE if not exists memory_percent
                                (percent numeric, date numeric)"""
                                
    sqlInsertMemoryPercent = """INSERT INTO memory_percent(percent,date) VALUES(?,?)"""

    sqlQueryProcessTbl = """SELECT * FROM processes WHERE pid=?"""


    def __init__(self):
        self.connect()
        self.setCursor()
        self.createProcessTable()
        self.createCPUTimesAllTable()
        self.createOverallCPUUsageTable()
        self.createPerCPUPercentTable()
        self.createAverageMemoryTable()
        
    def setCursor(self):
        self.cursor = self.conn.cursor()
        
    def connect(self):
        self.conn = sqlite3.connect(self.dbLocation + self.dbName)
        
    def createAverageMemoryTable(self):
        self.cursor.execute(self.sqlCreateMemoryTbl)
        self.conn.commit()
        
    def updateAverageMemoryTable(self, memoryPercent, dateInfo):
        self.cursor.execute(self.sqlInsertMemoryPercent,(memoryPercent,dateInfo))
        self.conn.commit()
        
    def createCPUTimesAllTable(self):
        self.cursor.execute(self.sqlCreateCPUsTbl)
        self.conn.commit()
        
    def createOverallCPUUsageTable(self):
        self.cursor.execute(self.sqlCreateOverallCPUavgTbl)
        self.conn.commit()
        
    def createPerCPUPercentTable(self):
        self.cursor.execute(self.sqlCreatePerCpuPercentTbl)
        self.conn.commit()
        
    def updateOverAllCPUUsageTable(self, cpuInfo, dateInfo):
        #TODO: Database cleanup - 24 hours, 48 hours? 
        self.cursor.execute(self.sqlInsertCPUOverallAvg,(cpuInfo,dateInfo))
        self.conn.commit()
        
    def updatePerCPUPercentTable(self,cpuPercentTuple, dateInfo):
        for cpu in range(0, len(cpuPercentTuple)):
            self.cursor.execute(self.sqlInsertPerCpuPercent, (cpu, cpuPercentTuple[cpu],dateInfo))      
        
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
            
            self.conn.commit()
            cpuNumber = cpuNumber + 1
            
    def createProcessTable(self):
        self.cursor.execute(self.sqlCreateProcTbl)
        self.conn.commit()
        
    def updateProcessTable(self, processTupleList):
        # pid, name, username, memory, disk_read, disk_write, cpu, running, priority
        
        #name[0],username[1],cpuPercent[2],pid[3],memPercent.uss[4] 
        #diskRead[5],diskWrite[6],isRunning[7],priority[8]
        
        for processTuple in processTupleList:
            
            self.cursor.execute("SELECT * FROM processes WHERE pid=? AND name=? AND username=?", 
                (processTuple[3],processTuple[0],processTuple[1],))
            
            if len(self.cursor.fetchall()) == 1:
                self.cursor.execute("UPDATE processes SET memory=?,disk_read=?,disk_write=?,cpu=?,running=?,priority=? WHERE pid=? AND name=? AND username=?",
                            (processTuple[4],processTuple[5],processTuple[6],processTuple[2],processTuple[7],processTuple[8],
                             processTuple[3],processTuple[0],processTuple[1]))
            else:
                self.cursor.execute("INSERT INTO processes (pid,name,username,memory,disk_read,disk_write,cpu,running,priority) VALUES (?,?,?,?,?,?,?,?,?)",
                            (processTuple[3],processTuple[0],processTuple[1],processTuple[4],processTuple[5],processTuple[6],processTuple[2],processTuple[7],processTuple[8]))
                
                self.conn.commit()   
                
    def queryProcessTable(self, pid=-1):
        
        if pid != -1:
            # Expecting a tuple.
            return self.cursor.execute(self.sqlQueryProcessTbl,(pid,))
        else:
            return self.cursor.execute("SELECT * FROM processes")
        
    def queryCPUTables(self):
        return self.cursor.execute("SELECT * FROM all_cpus_avg")
    
    def queryMemTable(self):
        return self.cursor.execute("SELECT * FROM memory_percent")
        
            
    def close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
                
##########################################
# UNCOMMENT BELOW TO SEE A FEW EXAMPLES  #
##########################################

#d = Database()
# A process that probably doesn't exist
#print(d.queryProcessTable(123456789).fetchall())

# Process 1 ... it might exist
#print(d.queryProcessTable(1).fetchall())

# All processes
#print(d.queryProcessTable().fetchall())

# Overall CPU %
#print(d.queryCPUTables().fetchall())

# Overall mem %
#print(d.queryMemTable().fetchall())




