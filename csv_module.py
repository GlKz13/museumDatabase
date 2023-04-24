from PyQt5 import QtWidgets as qtw

class Table(qtw.QTableWidget):
    def __init__(self):
        super().__init__(3,4)
        self.table = qtw.QTableWidget()
