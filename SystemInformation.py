'''
This class plots the live CPU percentage and memory percentage using pyqtgrapgh.
'''
from PyQt5.uic import loadUi
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QDialog
import numpy as np
from Cpu import Cpu
from Memory import Memory
from random import randint


class SystemInformation():
    def __init__(self):
        self.dialog = QDialog()
        self.sysinfo = loadUi('gui/systeminformation.ui', baseinstance=self.dialog)
        self.buffer_size = 60 # number of seconds
        self.cpu = Cpu()
        self.memory = Memory()
        self.cpu_count = self.cpu.getCpuCount()
        self.memory_data = np.zeros(self.buffer_size)
        self.cpu_data = np.zeros((self.cpu_count,self.buffer_size))
        self.seconds_elapsed = 0
        self.number_of_iterations = 1
        self.memory_line = None
        self.cpu_line = None
        self.cpu_plot = []
        self.memory_plot = self.sysinfo.memoryView.plot(pen=(255,0,0))

    def load_ui(self):
        # Depending on the number of CPUs this loop will create the plots
        for count in range(0,self.cpu_count):
            self.cpu_plot.append(self.sysinfo.cpuView.plot(pen=(randint(0,255),randint(0,255),randint(0,255))))

        # Memory and CPU line shows the current x-axis on the widget
        self.memory_line = self.sysinfo.memoryView.addLine(x=0)
        self.cpu_line = self.sysinfo.cpuView.addLine(x=0)

        self.sysinfo.memoryView.setLabel('left','Percentage',units = '%')
        self.sysinfo.memoryView.setLabel('bottom','Time',units = 's')
        self.sysinfo.memoryView.setRange(xRange=[0, self.buffer_size], yRange=[0, 100])
        self.sysinfo.memoryView.showGrid(x=True,y=True)

        self.sysinfo.cpuView.setLabel('left','Percentage',units = '%')
        self.sysinfo.cpuView.setLabel('bottom','Time',units = 's')
        self.sysinfo.cpuView.setRange(xRange=[0, self.buffer_size], yRange=[0, 100])
        self.sysinfo.cpuView.showGrid(x=True,y=True)

    def load_data(self):
        # Plot the memory line based on the memory reported.
        self.memory_data[self.seconds_elapsed:self.seconds_elapsed + self.number_of_iterations] = \
            self.memory.getAverageSystemMemory()
        self.memory_plot.setData(self.memory_data)

        per_cpu_percent = self.cpu.getPerCPUPercent()
        # Loop  to iterate through the number of CPUs in the machine and plot them on the widget
        for cpu in range(0,self.cpu_count):
            self.cpu_data[cpu][self.seconds_elapsed:self.seconds_elapsed + self.number_of_iterations] = \
                per_cpu_percent[cpu]
            self.cpu_plot[cpu].setData(self.cpu_data[cpu])

        # Increase the seconds based on the number of times update is requested
        self.seconds_elapsed = (self.seconds_elapsed + self.number_of_iterations) % self.buffer_size
        # Move the memory and cpu line on x-axis
        self.memory_line.setValue(self.seconds_elapsed)
        self.cpu_line.setValue(self.seconds_elapsed)


def show():
    si = SystemInformation()
    si.load_ui()
    si.load_data()
    # refresh screen every 1 second
    timer = QtCore.QTimer()
    timer.timeout.connect(si.load_data)
    timer.start(1000)
    si.dialog.exec_()

