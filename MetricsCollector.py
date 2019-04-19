'''
Created on Mar 8, 2019

@author: blossom
'''

from Processes import Processes
from Cpu import Cpu
from Memory import Memory
import time
import datetime

class MetricsCollector:
    
    def __init__(self):
        pass
    
    def run(self):
        cpu = Cpu()
        cpu.updateDatabase()
        mem = Memory()
        mem.updateDatabase()
        proc = Processes()
        proc.updateDatabase()
        
go = MetricsCollector()

while True:
    print(datetime.datetime.now()) # for debug
    go.run()
    time.sleep(60)
        
    ##########################################################################
    #                                                                        #
    #                 THE BELOW IS FOR REMEMBERING ONLY                      #
    #                                                                        #
    ########################################################################## 
    #def stats(self):
    #    stats = psutil.cpu_stats()
    #    print(stats)
        
    #def diskinfo(self):
    #    print(psutil.disk_partitions())
    #    for mount in psutil.disk_partitions():
    #        print(mount[1],mount[2]) # prints the mount point
    #        print(psutil.disk_usage(mount[1])[2]) # prints disk free space
