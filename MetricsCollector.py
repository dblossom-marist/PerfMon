'''
Created on Mar 8, 2019

@author: blossom
'''

from Processes import Processes
from Cpu import Cpu
from Memory import Memory
from Pmutils import Pmutils
import time

class MetricsCollector:
    
    def __init__(self):
        pass
    
    @staticmethod
    def run():
        cpu = Cpu()
        cpu.updateDatabase()
        mem = Memory()
        mem.updateDatabase()
        proc = Processes()
        proc.updateDatabase()
        
while True:
    print(Pmutils.createTimeStamp()) # for debug
    MetricsCollector.run()
    time.sleep(60)