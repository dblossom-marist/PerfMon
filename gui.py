'''
Created on Mar 27, 2019

@author: blossom
'''

from Processes import Processes
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
from PyQt5.uic.Compiler.qtproxies import QtWidgets
from PyQt5.Qt import QTableWidget, QVBoxLayout

class gui(QDialog):
    def __init__(self):
        super(gui,self).__init__()
        loadUi('gui/main.ui',self)
        self.setWindowTitle('PerfMon')
        self.setFixedSize(self.size())
        
        
        
        
app = QApplication(sys.argv)
widget = gui()
widget.show()
sys.exit(app.exec_())
