"""
A class that does all database interactions
@author: blossom
"""
# Python SQLite library.
import sqlite3


class Database:
    
    # Name & Location of the database file
    dbName = "MetricCollector.db"
    dbLocation = "/usr/share/perfmon/"
    
    # The SQL command to create a process table
    sql_create_proc_tbl = """CREATE TABLE if not exists processes
                          (pid integer, name text, username text, memory numeric, 
                          disk_read numeric, disk_write numeric, cpu numeric, 
                          running integer, priority integer)"""
    
    # The SQL command to create the table for all CPUs running in system
    sql_create_cpus_tbl = """CREATE TABLE if not exists all_cpus
                          (cpuN integer, user numeric, nice numeric, system numeric,
                          idle numeric, iowait numeric, irq numeric, softirq numeric,
                          steal numeric, guest numeric, guest_nice numeric, date numeric)"""
                          
    # The SQL statement to update all rows in the all CPU table 
    sql_update_all_cpu_row = """UPDATE all_cpus SET user=?, nice=?, system=?, idle=?,
                            iowait=?, irq=?, softirq=?, steal=?, guest=?, guest_nice=?,
                            date=? WHERE cpuN=?"""
    
    # The SQL statement to insert a new row into all CPU table
    sql_insert_all_cpu_row = """INSERT INTO all_cpus (cpuN,user,nice,system,idle,iowait,
                                                  irq,softirq,steal,guest,guest_nice,date) 
                                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
                                                
    # The SQL statement to create the CPU avg useage table
    sql_create_overall_cpu_avg_tbl = """CREATE TABLE if not exists all_cpus_avg
                                   (all_cpu numeric, date numeric)"""
                                   
    # The SQL statement to insert a row in the average CPU table
    sql_insert_cpu_overall_avg = """INSERT INTO all_cpus_avg (all_cpu, date) VALUES(?,?)"""
    
    # The SQL statement to create the CPU percent per CPU table
    sql_create_per_cpu_percent_tbl = """CREATE TABLE if not exists per_cpu_percent
                                (cpu integer, cpu_percent numeric, date numeric)"""
    
    # The SQL statement to insert into per cpu percent table
    sql_insert_per_cpu_percent = """INSERT INTO per_cpu_percent(cpu,cpu_percent,date) VALUES(?,?,?)"""
    
    # The SQL statement to create the memory percent table
    sql_create_memory_tbl = """CREATE TABLE if not exists memory_percent
                                (percent numeric, date numeric)"""
    
    # The SQL statement to insert a row into memory table
    sql_insert_memory_percent = """INSERT INTO memory_percent(percent,date) VALUES(?,?)"""

    # The SQL statement to query the database
    sql_query_process_tbl = """SELECT * FROM processes WHERE pid=?"""

    '''
    Connect to DB, set the cursor and create all tables.
    '''
    def __init__(self):
        self.cursor = None
        self.conn = None

        self.connect()
        self.set_cursor()
        self.create_process_table()
        self.create_cpu_times_all_table()
        self.create_overall_cpu_usage_table()
        self.create_per_cpu_percent_table()
        self.create_average_memory_table()
        
    '''
    A method to set the cursor
    '''
    def set_cursor(self):
        self.cursor = self.conn.cursor()
        
    '''
    A method to connect to the DB
    '''
    def connect(self):
        self.conn = sqlite3.connect(self.db_location + self.db_name)
        
    '''
    Create the memory table
    '''
    def create_average_memory_table(self):
        self.cursor.execute(self.sql_create_memory_tbl)
        self.conn.commit()
        
    '''
    Update the avg memory percent table
    '''
    def update_average_memory_table(self, memory_percent, date_info):
        self.cursor.execute(self.sql_insert_memory_percent, (memory_percent, date_info))
        self.conn.commit()
       
    '''
    Create the all CPU times usage table
    ''' 
    def create_cpu_times_all_table(self):
        self.cursor.execute(self.sql_create_cpus_tbl)
        self.conn.commit()
    
    '''
    Create overall CPU usage table
    ''' 
    def create_overall_cpu_usage_table(self):
        self.cursor.execute(self.sql_create_overall_cpu_avg_tbl)
        self.conn.commit()
        
    '''
    Create per CPU usage table
    '''
    def create_per_cpu_percent_table(self):
        self.cursor.execute(self.sql_create_per_cpu_percent_tbl)
        self.conn.commit()
        
    '''
    Update overall CPU usage able
    '''
    def update_over_all_cpu_usage_table(self, cpu_info, date_info):
        # TODO: Database cleanup - 24 hours, 48 hours?
        self.cursor.execute(self.sql_insert_cpu_overall_avg, (cpu_info, date_info))
        self.conn.commit()
        
    '''
    Update per CPU percent table
    '''
    def update_per_cpu_percent_table(self, cpu_percent_tuple, date_info):
        for cpu in range(0, len(cpu_percent_tuple)):
            self.cursor.execute(self.sql_insert_per_cpu_percent, (cpu, cpu_percent_tuple[cpu], date_info))
        
    '''
    Update CPU usage times table
    '''
    def update_cpu_times_all_table(self, cpu_tuple, date_time):
        cpu_number = 0  # this will line up with cpu_tuple
        for cpu in cpu_tuple:
            
            self.cursor.execute("SELECT * FROM all_cpus WHERE cpuN=?", (cpu_number,))
            
            if len(self.cursor.fetchall()) == 1:
                # Just update row
                self.cursor.execute(self.sql_update_all_cpu_row,
                                    (cpu[0], cpu[1], cpu[2], cpu[3], cpu[4], cpu[5],
                                     cpu[6], cpu[7], cpu[8], cpu[9], date_time, cpu_number))
            else:
                self.cursor.execute(self.sql_insert_all_cpu_row,
                                    (cpu_number, cpu[0], cpu[1], cpu[2], cpu[3], cpu[4],
                                     cpu[5], cpu[6], cpu[7], cpu[8], cpu[9], date_time))
            
            self.conn.commit()
            cpu_number = cpu_number + 1
            
    '''
    Create the process table
    '''
    def create_process_table(self):
        self.cursor.execute(self.sql_create_proc_tbl)
        self.conn.commit()
        
    '''
    Update process table ... the SQL statements are baked in here for no reason other than
                             once it worked, I left it in fear of breaking it.
    @param processTupleList: The list of processes to put in DB 
    '''
    def update_process_table(self, process_tuple_list):
        
        for processTuple in process_tuple_list:
            
            self.cursor.execute("SELECT * FROM processes WHERE pid=? AND name=? AND username=?", 
                                (processTuple[3], processTuple[0], processTuple[1],))
            
            if len(self.cursor.fetchall()) == 1:
                self.cursor.execute("UPDATE processes SET memory=?,disk_read=?,disk_write=?,cpu=?,running=?,priority=? WHERE pid=? AND name=? AND username=?",
                                    (processTuple[4], processTuple[5], processTuple[6], processTuple[2], processTuple[7], processTuple[8],
                                     processTuple[3], processTuple[0], processTuple[1]))
            else:
                self.cursor.execute("INSERT INTO processes (pid,name,username,memory,disk_read,disk_write,cpu,running,priority) VALUES (?,?,?,?,?,?,?,?,?)",
                                    (processTuple[3], processTuple[0], processTuple[1], processTuple[4], processTuple[5], processTuple[6], processTuple[2], processTuple[7], processTuple[8]))
                
                self.conn.commit()   
    
    '''
    Query process table
    @param pid: optional param that will return that process or all nothing passed.
    '''            
    def query_process_table(self, pid=-1):
        
        if pid != -1:
            # Expecting a tuple.
            return self.cursor.execute(self.sql_query_process_tbl, (pid,))
        else:
            return self.cursor.execute("SELECT * FROM processes")
   
    '''
    Query the CPU table
    '''    
    def query_cpu_tables(self):
        return self.cursor.execute("SELECT * FROM all_cpus_avg")
    
    '''
    Query the memory table
    '''
    def query_mem_table(self):
        return self.cursor.execute("SELECT * FROM memory_percent")
        
    '''
    Some closing clean up ..
    '''
    def close(self):
        # Anything not committed?
        self.conn.commit()
        # Close cursor
        self.cursor.close()
        # Officially closed for business.
        self.conn.close()
