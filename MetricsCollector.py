'''
A classes used as a driver to run the needed classes/methods
in the backend writing system information to a SQLite database
@author: blossom
'''

# Import from Python lib
import time
# Import from classes created for this project.
from Processes import Processes
from Cpu import Cpu
from Memory import Memory

class MetricsCollector:
    
    def __init__(self):
        pass
    
    '''
    A static method that does everything, the 'driver'
    '''
    @staticmethod
    def run():
        cpu = Cpu()
        cpu.updateDatabase()
        mem = Memory()
        mem.updateDatabase()
        proc = Processes()
        proc.updateDatabase()

# Run in a loop every minute.
while True:
    MetricsCollector.run()
    time.sleep(60)