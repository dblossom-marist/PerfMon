"""
Class to load the main screen of Perfmon
"""
from PyQt5.QtWidgets import QApplication, QTreeWidgetItem
from PyQt5 import QtCore
from PyQt5.uic import loadUi
import sys
import SystemInformation
from Processes import Processes

app = QApplication(sys.argv)
allUsers = 2
timer = QtCore.QTimer()


class Perfmon:
    def __init__(self):
        self.mainScreen = loadUi('gui/mainwindow.ui')
        # Column names in TreeWidget
        self.treeWidgetColumnsInMainScreen = ["Process", "User", "% CPU", "PID", "Memory", "DiskRead", "DiskWrite", "State"]

    def load_ui(self):
        self.mainScreen.treeWidget.setColumnCount(len(self.treeWidgetColumnsInMainScreen))
        self.mainScreen.treeWidget.setHeaderLabels(self.treeWidgetColumnsInMainScreen)

        # File->exit menu
        self.mainScreen.actionExit.triggered.connect(sys.exit)
        # View->system information
        self.mainScreen.actionSystem_Information.triggered.connect(SystemInformation.show)
        self.mainScreen.show()

    def load_data(self):
        self.mainScreen.treeWidget.clear()
        # Collect process based on the status of the checkbox
        if self.mainScreen.checkBox.checkState() == allUsers:
            list_of_processes = Processes().collectProcesses(True)
        else:
            list_of_processes = Processes().collectProcesses(False)

        # Iterate through the process and add them to the tree widget.
        for process in list_of_processes:
            add_row = []
            for col in range(self.mainScreen.treeWidget.columnCount()):
                add_row.append(str(process[col]))
            self.mainScreen.treeWidget.addTopLevelItem(QTreeWidgetItem(add_row))


if __name__ == '__main__':
    p = Perfmon()
    p.load_ui()
    p.load_data()

    # Refresh screen every 3 seconds
    timer.timeout.connect(p.load_data)
    timer.start(3000)

    app.exec_()
    sys.exit()
