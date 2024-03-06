from PySide2 import QtWidgets


def main():
    app = QtWidgets.QApplication()

    window = QtWidgets.QMainWindow()
    window.setWindowTitle('My window')
    window.show()

    app.exec_()


if __name__ == '__main__':
    main()
