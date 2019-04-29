from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QApplication
import sys
import pyqtgraph as pg
import numpy as np
from Cpu import Cpu
from Memory import Memory

global_bufferSize = 60 #seconds for x-axis
global_numberOfIterations = 1  # update 1 samples per iteration
global_data_cpu1 = None
global_data_cpu2 = None
global_data_cpu3 = None
global_data_cpu4 = None
global_curve_cpu1 = None
global_curve_cpu2 = None
global_curve_cpu3 = None
global_curve_cpu4 = None
global_line = None
global_line_memory = None
global_secondsElapsed = 0
global_memory = None
global_memory_curve = None

def update():
    global global_data_cpu1,global_data_cpu2,global_data_cpu3,global_data_cpu4, global_line, global_secondsElapsed
    global curve_cpu1,curve_cpu2,curve_cpu3,curve_cpu4,global_memory,global_memory_curve,global_line_memory

    c = Cpu()
    cpuPercent = c.getPerCPUPercent()
    m = Memory()
    memoryPercent = m.getAverageSystemMemory()

    #cpu1
    global_data_cpu1[global_secondsElapsed:global_secondsElapsed + global_numberOfIterations] = cpuPercent[0]
    global_curve_cpu1.setData(global_data_cpu1)
    #cpu2
    global_data_cpu2[global_secondsElapsed:global_secondsElapsed + global_numberOfIterations] = cpuPercent[1]
    global_curve_cpu2.setData(global_data_cpu2)
    #cpu3
    global_data_cpu3[global_secondsElapsed:global_secondsElapsed + global_numberOfIterations] = cpuPercent[2]
    global_curve_cpu3.setData(global_data_cpu3)
    #cpu4
    global_data_cpu4[global_secondsElapsed:global_secondsElapsed + global_numberOfIterations] = cpuPercent[3]
    global_curve_cpu4.setData(global_data_cpu4)

    global_memory[global_secondsElapsed:global_secondsElapsed + global_numberOfIterations] = memoryPercent
    global_memory_curve.setData(global_memory)

    global_secondsElapsed = (global_secondsElapsed + global_numberOfIterations) % global_bufferSize
    global_line.setValue(global_secondsElapsed)
    global_line_memory.setValue(global_secondsElapsed)


def prepareUI():
    global global_data_cpu1,global_data_cpu2,global_data_cpu3,global_data_cpu4
    global global_curve_cpu1, global_curve_cpu2, global_curve_cpu3, global_curve_cpu4
    global global_line, global_memory,global_memory_curve,global_line_memory
    app = QApplication(sys.argv)
    __dialog__ = QtGui.QDialog()
    __ui__ = uic.loadUi('gui/systeminformation.ui')

    pWidget = __ui__.cpuView
    pMemoryWidget = __ui__.memoryView

    #cpu1
    global_data_cpu1 = np.zeros(global_bufferSize)
    global_curve_cpu1 = pWidget.plot(pen=(255, 0, 0))
    #cpu2
    global_data_cpu2 = np.zeros(global_bufferSize)
    global_curve_cpu2 = pWidget.plot(pen=(0, 255, 0))
    #cpu3
    global_data_cpu3 = np.zeros(global_bufferSize)
    global_curve_cpu3 = pWidget.plot(pen=(0, 0, 255))
    #cpu4
    global_data_cpu4 = np.zeros(global_bufferSize)
    global_curve_cpu4 = pWidget.plot(pen=(255, 140, 0))

    #memory view
    global_memory = np.zeros(global_bufferSize)
    global_memory_curve = pMemoryWidget.plot(pen=(255,0,0))

    global_line = pWidget.addLine(x=0)
    pWidget.setLabel('left','Percentage',units = '%')
    pWidget.setLabel('bottom','Time',units = 's')

    pWidget.setRange(xRange=[0, global_bufferSize], yRange=[0, 100])
    pWidget.showGrid(x=True,y=True)
    #pWidget.addLegend()

    global_line_memory = pMemoryWidget.addLine(x=0)
    pMemoryWidget.setLabel('left','Percentage',units = '%')
    pMemoryWidget.setLabel('bottom','Time',units = 's')
    pMemoryWidget.setRange(xRange=[0, global_bufferSize], yRange=[0, 100])
    pMemoryWidget.showGrid(x=True,y=True)
    #pMemoryWidget.addLegend()

    __ui__.show()
    # refresh screen every 1000ms
    timer = pg.QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(1000)

    # todo: Syntax error on purpose, have to fix this code otherwise dialog
    #  box would not showup. _exec cannot execute here and widget cannot
    # todo: be constructed before the main window
    pg.QtGui.QApplication.instan().exec_()
    sys.exit()




