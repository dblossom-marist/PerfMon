'''
This class plots the db CPU percentage and memory percentage using pyqtgrapgh.
'''
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog
import numpy as np
from Cpu import Cpu
from Memory import Memory
from Database import Database


class SystemInformationArchive():
    def __init__(self):
        self.dialog = QDialog()
        self.sysinfo = loadUi('gui/systeminformationarchive.ui', baseinstance=self.dialog)
        self.buffer_size = 60 # number of seconds
        self.cpu = Cpu()
        self.memory = Memory()
        self.cpu_count = self.cpu.getCpuCount()
        self.memory_data = np.zeros(self.buffer_size)
        self.cpu_data = np.zeros(self.buffer_size)
        self.seconds_elapsed = 0
        self.number_of_iterations = 1
        self.memory_line = None
        self.cpu_line = None
        self.cpu_plot = None
        self.memory_plot = self.sysinfo.memoryView.plot(pen=(255,0,0))
        self.cpu_plot = self.sysinfo.cpuView.plot(pen=(255,0,0))
        self.db = Database()

    def load_ui(self):
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
        self.memory_plot.setData(self.memory_data)
        self.cpu_data = self.db.queryhourCPUAvgTable(self.sysinfo.timeEdit.time().hour(),self.sysinfo.timeEdit.time().minute())
        self.memory_data = self.db.queryhourMEMAvgTable(self.sysinfo.timeEdit.time().hour(),self.sysinfo.timeEdit.time().minute())
        self.memory_plot.setData(self.memory_data)
        self.cpu_plot.setData(self.cpu_data)


def show():
    si = SystemInformationArchive()
    si.load_ui()
    si.load_data()
    # refresh screen every 1 second
    timer = QtCore.QTimer()
    timer.timeout.connect(si.load_data)
    timer.start(1000)
    si.dialog.exec_()

