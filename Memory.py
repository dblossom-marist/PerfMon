
import datetime
import psutil
from Database import Database
import time

class Memory:
    
    #psutil.virtual_memory()
    #svmem(total=10367352832, available=6472179712, percent=37.6, used=8186245120, free=2181107712, active=4748992512, inactive=2758115328, buffers=790724608, cached=3500347392, shared=787554304)
    #psutil.swap_memory()
    #sswap(total=2097147904, used=296128512, free=1801019392, percent=14.1, sin=304193536, sout=677842944)

    
    def __init__(self):
        pass
    
    def createTimeStamp(self):
        return datetime.datetime.now()
    
    def getAverageSystemMemory(self):
        mem = psutil.virtual_memory()
        return mem[2]
    
    def updateDatabase(self):
        db = Database()
        db.updateAverageMemoryTable(self.getAverageSystemMemory(), self.createTimeStamp())