'''
Created on Mar 8, 2019

@author: blossom
'''

import psutil
#from Processes import Processes
from Cpu import Cpu

class MetricsCollector:
    
    def __init__(self):
        cpuPercent = Cpu.getOverallCPUPercent(self)
            
    def stats(self):
        stats = psutil.cpu_stats()
        print(stats)
        
    def diskinfo(self):
        print(psutil.disk_partitions())
        for mount in psutil.disk_partitions():
            print(mount[1],mount[2]) # prints the mount point
            print(psutil.disk_usage(mount[1])[2]) # prints disk free space
        
#proc = Processes()

metric = MetricsCollector()

#while True:
#    proc.updateDatabase()
#    time.sleep(10)
