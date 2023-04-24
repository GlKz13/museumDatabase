from PyQt5 import QtWidgets as qtw


def error():
    error = qtw.QMessageBox()
    error.setWindowTitle('Ошибка использования заголовка.')
    error.setText('Выберите другой заголовок.')
    error.setInformativeText(
        'Этот заголовок уже используется.'
        ' Пожалуйста, выберите другой.')
    error.exec()

