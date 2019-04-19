'''
Created on Mar 27, 2019

@author: blossom
'''

from Processes import Processes
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi
from PyQt5.Qt import QTreeWidgetItem
from PyQt5 import QtCore

g_timer = None
mainUI = None

treeWidgetColumns = ["Process","User","% CPU","PID","Memory","DiskRead","DiskWrite","State"]

def paintUI(mainWindow):
    global g_timer
    mainWindow.treeWidget.setColumnCount(len(treeWidgetColumns))
    mainWindow.treeWidget.setHeaderLabels(treeWidgetColumns)

def loadData():
    mainUI.treeWidget.clear()
    if mainUI.checkBox.checkState() == 2:
        listOfProcesses = Processes().collectProcesses(True)
    else:
        listOfProcesses = Processes().collectProcesses(False)

    for process in listOfProcesses:
        addRow = []
        for col in range(mainUI.treeWidget.columnCount()):
            addRow.append(str(process[col]))
        mainUI.treeWidget.addTopLevelItem(QTreeWidgetItem(addRow))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainUI = loadUi('gui/mainwindow.ui')
    paintUI(mainUI)
    loadData()

    mainUI.show()

    g_timer = QtCore.QTimer()

    g_timer.timeout.connect(loadData)

    g_timer.start(3000)

    sys.exit(app.exec_())

