from Cpu import Cpu
from Pmutils import Pmutils
from Processes import Processes

# CPU Tests
cpu = Cpu()
print(cpu.get_cpu_count("bad info"))
print(cpu.get_cpu_count(True))
print(cpu.get_cpu_count(False))
print(cpu.get_cpu_count())

# Pmtutils Tests
pmu = Pmutils()
print(pmu.convert_bytes(4444.23432))
print(pmu.convert_bytes("not a number"))
print(pmu.convert_bytes(1))

# Process Test
proc = Processes()
