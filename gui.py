'''
Created on Mar 27, 2019

@author: blossom
'''

from Processes import Processes
import sys
import time
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
from PyQt5.uic.Compiler.qtproxies import QtWidgets, QtGui
from PyQt5.Qt import QTableWidget, QTableWidgetItem

class gui(QDialog):
    def __init__(self):
        super(gui,self).__init__()
        loadUi('gui/main.ui',self)
        self.setWindowTitle('PerfMon')
        self.setFixedSize(self.size())
        
    def updateGui(self):
        proc = Processes()

        #while True:
        processesTuple = proc.collectProcesses()
        #time.sleep(10)      
        row = 0
        for process in processesTuple:
            for col in range(0,self.tableWidget.columnCount()):
                self.tableWidget.insertRow(self.tableWidget.rowCount())
                self.tableWidget.setItem(row,col,QTableWidgetItem(str(process[col])))
            row = row + 1
             
app = QApplication(sys.argv)
widget = gui()
widget.updateGui()
widget.show()
widget.updateGui()
sys.exit(app.exec_())
