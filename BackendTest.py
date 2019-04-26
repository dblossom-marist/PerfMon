from Cpu import Cpu
from Pmutils import Pmutils
from Processes import Processes

# CPU Tests
cpu = Cpu()
print(cpu.getCpuCount("bad info"))
print(cpu.getCpuCount(True))
print(cpu.getCpuCount(False))
print(cpu.getCpuCount())

#Pmtutils Tests
pmu = Pmutils()
print(pmu.convertBytes(4444.23432))
print(pmu.convertBytes("not a number"))
print(pmu.convertBytes(1))

#Process Test
proc = Processes()