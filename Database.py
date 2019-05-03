'''
A class that does all database interactions
@author: blossom
'''
# Python SQLite library.
import sqlite3
import datetime

class Database():
    
    # Name & Location of the database file
    dbName = "MetricCollector.db"
    dbLocation = "/usr/share/perfmon/" #TODO: put in /var
    
    # The SQL command to create a process table
    sqlCreateProcTbl = """CREATE TABLE if not exists processes
                         (pid integer, name text, username text, memory numeric, 
                         disk_read numeric, disk_write numeric, cpu numeric, 
                         running integer, priority integer)"""
    
    # The SQL command to create the table for all CPUs running in system
    sqlCreateCPUsTbl = """CREATE TABLE if not exists all_cpus
                          (cpuN integer, user numeric, nice numeric, system numeric,
                          idle numeric, iowait numeric, irq numeric, softirq numeric,
                          steal numeric, guest numeric, guest_nice numeric, date numeric)"""
                          
    # The SQL statement to update all rows in the all CPU table 
    sqlUpdateAllCPUrow = """UPDATE all_cpus SET user=?, nice=?, system=?, idle=?,
                            iowait=?, irq=?, softirq=?, steal=?, guest=?, guest_nice=?,
                            date=? WHERE cpuN=?"""
    
    # The SQL statement to insert a new row into all CPU table
    sqlInsertAllCPUrow = """INSERT INTO all_cpus (cpuN,user,nice,system,idle,iowait,
                                                  irq,softirq,steal,guest,guest_nice,date) 
                                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
                                                
    # The SQL statement to create the CPU avg useage table
    sqlCreateOverallCPUavgTbl = """CREATE TABLE if not exists all_cpus_avg
                                   (all_cpu numeric, date numeric)"""
                                   
    # The SQL statement to insert a row in the average CPU table
    sqlInsertCPUOverallAvg = """INSERT INTO all_cpus_avg (all_cpu, date) VALUES(?,?)"""
    
    # The SQL statement to create the CPU percent per CPU table
    sqlCreatePerCpuPercentTbl = """CREATE TABLE if not exists per_cpu_percent
                                (cpu integer, cpu_percent numeric, date numeric)"""
    
    # The SQL statement to insert into per cpu percent table
    sqlInsertPerCpuPercent = """INSERT INTO per_cpu_percent(cpu,cpu_percent,date) VALUES(?,?,?)"""
    
    # The SQL statement to create the memory percent table
    sqlCreateMemoryTbl = """CREATE TABLE if not exists memory_percent
                                (percent numeric, date numeric)"""
    
    # The SQL statement to insert a row into memory table
    sqlInsertMemoryPercent = """INSERT INTO memory_percent(percent,date) VALUES(?,?)"""

    # The SQL statement to query the database
    sqlQueryProcessTbl = """SELECT * FROM processes WHERE pid=?"""
    
    # The SQL statement to return overall CPU avgs between two datea
    sqlQueryDateRangeCPUAvgTbl = """SELECT all_cpu FROM all_cpus_avg WHERE date >? AND date <?"""
    
    sqlQueryDateRangeMEMAvgTbl = """SELECT percent FROM memory_percent WHERE date >? AND date <?"""

    '''
    Connect to DB, set the cursor and create all tables.
    '''
    def __init__(self):
        self.connect()
        self.setCursor()
        self.createProcessTable()
        self.createCPUTimesAllTable()
        self.createOverallCPUUsageTable()
        self.createPerCPUPercentTable()
        self.createAverageMemoryTable()
        
    '''
    A method to set the cursor
    '''
    def setCursor(self):
        self.cursor = self.conn.cursor()
        
    '''
    A method to connect to the DB
    '''
    def connect(self):
        self.conn = sqlite3.connect(self.dbLocation + self.dbName)
        
    '''
    Create the memory table
    '''
    def createAverageMemoryTable(self):
        self.cursor.execute(self.sqlCreateMemoryTbl)
        self.conn.commit()
        
    '''
    Update the avg memory percent table
    '''
    def updateAverageMemoryTable(self, memoryPercent, dateInfo):
        self.cursor.execute(self.sqlInsertMemoryPercent,(memoryPercent,dateInfo))
        self.conn.commit()
       
    '''
    Create the all CPU times usage table
    ''' 
    def createCPUTimesAllTable(self):
        self.cursor.execute(self.sqlCreateCPUsTbl)
        self.conn.commit()
    
    '''
    Create overall CPU usage table
    ''' 
    def createOverallCPUUsageTable(self):
        self.cursor.execute(self.sqlCreateOverallCPUavgTbl)
        self.conn.commit()
        
    '''
    Create per CPU usage table
    '''
    def createPerCPUPercentTable(self):
        self.cursor.execute(self.sqlCreatePerCpuPercentTbl)
        self.conn.commit()
        
    '''
    Update overall CPU usage able
    '''
    def updateOverAllCPUUsageTable(self, cpuInfo, dateInfo):
        #TODO: Database cleanup - 24 hours, 48 hours? 
        self.cursor.execute(self.sqlInsertCPUOverallAvg,(cpuInfo,dateInfo))
        self.conn.commit()
        
    '''
    Update per CPU percent table
    '''
    def updatePerCPUPercentTable(self,cpuPercentTuple, dateInfo):
        for cpu in range(0, len(cpuPercentTuple)):
            self.cursor.execute(self.sqlInsertPerCpuPercent, (cpu, cpuPercentTuple[cpu],dateInfo))      
        
    '''
    Update CPU usage times table
    '''
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
            
    '''
    Create the process table
    '''
    def createProcessTable(self):
        self.cursor.execute(self.sqlCreateProcTbl)
        self.conn.commit()
        
    '''
    Update process table ... the SQL statements are baked in here for no reason other than
                             once it worked, I left it in fear of breaking it.
    @param processTupleList: The list of processes to put in DB 
    '''
    def updateProcessTable(self, processTupleList):
        
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
    
    '''
    Query process table
    @param pid: optional param that will return that process or all nothing passed.
    '''            
    def queryProcessTable(self, pid=-1):
        
        if pid != -1:
            # Expecting a tuple.
            return self.cursor.execute(self.sqlQueryProcessTbl,(pid,))
        else:
            return self.cursor.execute("SELECT * FROM processes")
   
    '''
    Query the CPU table
    '''    
    def queryCPUTables(self):
        return self.cursor.execute("SELECT * FROM all_cpus_avg")
    
    '''
    Query the memory table
    '''
    def queryMemTable(self):
        return self.cursor.execute("SELECT * FROM memory_percent")
    
    '''
    Query the CPU table for overall averages given a date range
    Note: '>' and '<' is used so results might not be as expected
    @param date1: The first date in the range
    @param date2: The second date in the range
    @return a tuple with a range of averages given the time frame
    '''
    def queryDateRangeCPUAvgTable(self, date1, date2):
        #TODO: add checks for parms or bad things will happen.        
        self.conn.row_factory = lambda cursor, row: row[0]
        self.setCursor()
        results = self.cursor.execute(self.sqlQueryDateRangeCPUAvgTbl, (date1, date2))
        # so, a bit of a hack here... Since I changed the connection row factory I am
        # not sure what it will do to me later - so - the sake of not to break anything
        # I am saving the list, closing the connection, re-establishing a connection
        # setting the cursor again and finally returning the list ... yep.
        return_array = results.fetchall()
        self.close()
        self.connect()
        self.setCursor()
        return return_array
    '''
    Query CPU Table for an hour
    '''    
    def queryhourCPUAvgTable(self, hour, minute=0):
        # quick and dirty minute string .... 
        minute_string = ""
        if minute < 0 or minute > 59:
            minute_string = ":00" # just make it top of hour
        if minute < 10:
            minute_string = ":0" + str(minute)
        else:
            minute_string = ":" + str(minute)
        
        if hour < 10:
            date1 = str(datetime.date.today()) + " 0" + str(hour) + minute_string
        else:
            date1 = str(datetime.date.today()) + " " + str(hour) + minute_string

        next_hour = hour + 1
        if next_hour == 24: # it's midnight
            next_hour = 0
            # break this up into multiple steps for readablility
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            date2 = str(tomorrow) +  " 0" + str(next_hour) + minute_string
        else:
            if next_hour < 10:
                date2 = str(datetime.date.today()) + " 0" + str(next_hour) + minute_string
            else:
                date2 = str(datetime.date.today()) + " " + str(next_hour) + minute_string
                        
        #TODO: add checks for parms or bad things will happen.        
        self.conn.row_factory = lambda cursor, row: row[0]
        self.setCursor()
        results = self.cursor.execute(self.sqlQueryDateRangeCPUAvgTbl, (date1, date2))
        # so, a bit of a hack here... Since I changed the connection row factory I am
        # not sure what it will do to me later - so - the sake of not to break anything
        # I am saving the list, closing the connection, re-establishing a connection
        # setting the cursor again and finally returning the list ... yep.
        return_array = results.fetchall()
        self.close()
        self.connect()
        self.setCursor()
        return return_array
    
    '''
    Query memory table for hour
    '''
    def queryhourMEMAvgTable(self, hour, minute=0):
        minute_string = ""
        if minute < 0 or minute > 59:
            minute_string = ":00" # just make it top of hour
        if minute < 10:
            minute_string = ":0" + str(minute)
        else:
            minute_string = ":" + str(minute)
        
        if hour < 10:
            date1 = str(datetime.date.today()) + " 0" + str(hour) + minute_string
        else:
            date1 = str(datetime.date.today()) + " " + str(hour) + minute_string

        next_hour = hour + 1
        if next_hour == 24: # it's midnight
            next_hour = 0
            # break this up into multiple steps for readablility
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            date2 = str(tomorrow) +  " 0" + str(next_hour) + minute_string
        else:
            if next_hour < 10:
                date2 = str(datetime.date.today()) + " 0" + str(next_hour) + minute_string
            else:
                date2 = str(datetime.date.today()) + " " + str(next_hour) + minute_string
                        
        #TODO: add checks for parms or bad things will happen.        
        self.conn.row_factory = lambda cursor, row: row[0]
        self.setCursor()
        results = self.cursor.execute(self.sqlQueryDateRangeMEMAvgTbl, (date1, date2))
        # so, a bit of a hack here... Since I changed the connection row factory I am
        # not sure what it will do to me later - so - the sake of not to break anything
        # I am saving the list, closing the connection, re-establishing a connection
        # setting the cursor again and finally returning the list ... yep.
        return_array = results.fetchall()
        self.close()
        self.connect()
        self.setCursor()
        return return_array
    
    '''
    
    '''
    def queryDateRangeMEMAvgTable(self, date1, date2):
        #TODO: add checks for parms or bad things will happen.
        self.conn.row_factory = lambda cursor, row: row[0]
        self.setCursor()
        results = self.cursor.execute(self.sqlQueryDateRangeMEMAvgTbl, (date1, date2))
        # so, a bit of a hack here... Since I changed the connection row factory I am
        # not sure what it will do to me later - so - the sake of not to break anything
        # I am saving the list, closing the connection, re-establishing a connection
        # setting the cursor again and finally returning the list ... yep.
        return_array = results.fetchall()
        self.close()
        self.connect()
        self.setCursor()
        return return_array

        
    '''
    Some closing clean up ..
    '''
    def close(self):
        # Anything not commited?
        self.conn.commit()
        # Close cursor
        self.cursor.close()
        # Offically closed for business. 
        self.conn.close()
        