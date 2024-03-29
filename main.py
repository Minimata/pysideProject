import requests

from PySide2 import QtWidgets, QtCore


class MessageTrigger(QtWidgets.QMessageBox):
    @QtCore.Slot(str)
    def button_clicked(self, text: str) -> None:
        self.setText(text)
        self.exec_()


class DeletableButton(QtWidgets.QPushButton):
    triggered = QtCore.Signal(QtWidgets.QWidget)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clicked.connect(self._clicked)

    @QtCore.Slot()
    def _clicked(self):
        self.triggered.emit(self)


class ChangeLayout(QtCore.QObject):
    def __init__(self, layout: QtWidgets.QLayout):
        super().__init__()
        self.layout = layout

    @QtCore.Slot(str)
    def button_clicked(self, text: str) -> None:
        widget = DeletableButton(text)
        widget.triggered.connect(self.remove_widget)
        self.layout.addWidget(widget)

    @QtCore.Slot(QtWidgets.QWidget)
    def remove_widget(self, widget: QtWidgets.QWidget) -> None:
        self.layout.removeWidget(widget)
        widget.setParent(None)
        widget.deleteLater()


class MyButton(QtWidgets.QPushButton):
    triggered = QtCore.Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clicked.connect(self._clicked)

    @QtCore.Slot()
    def _clicked(self):
        text = self.text()
        self.triggered.emit(text)


class RequestManager(QtCore.QObject):
    def __init__(self, url="https://echo.free.beeceptor.com"):
        super().__init__()
        self.url = url

    @QtCore.Slot()
    def get_request(self):
        result: requests.Response = requests.get(self.url)
        print(result.json())

    @QtCore.Slot()
    def post_request(self):
        result: requests.Response = requests.post(self.url, {"Hello": "World!"})
        print(result.json())


def main():
    app = QtWidgets.QApplication()
    window = QtWidgets.QMainWindow()
    window.setWindowTitle('My window')
    window.setGeometry(200, 200, 600, 600)

    button1 = MyButton("Push me!")
    button2 = MyButton("No, push me!")
    msg_trigger = MessageTrigger()
    request_manager = RequestManager()

    button_layout = QtWidgets.QHBoxLayout()
    button_layout.addWidget(button1)
    button_layout.addWidget(button2)

    change_layout = ChangeLayout(button_layout)
    button1.triggered.connect(change_layout.button_clicked)
    button2.triggered.connect(change_layout.button_clicked)

    label = QtWidgets.QLabel("Choose your fighter!")
    label_layout = QtWidgets.QHBoxLayout()
    label_layout.addStretch()
    label_layout.addWidget(label)
    label_layout.addStretch()

    button_get = QtWidgets.QPushButton("Get request")
    button_post = QtWidgets.QPushButton("Post request")
    request_layout = QtWidgets.QHBoxLayout()
    request_layout.addWidget(button_get)
    request_layout.addWidget(button_post)

    button_get.clicked.connect(request_manager.get_request)
    button_post.clicked.connect(request_manager.post_request)

    main_layout = QtWidgets.QVBoxLayout()
    main_layout.addStretch()
    main_layout.addLayout(label_layout)
    main_layout.addLayout(button_layout)
    main_layout.addStretch()
    main_layout.addLayout(request_layout)
    main_layout.addStretch()

    main_widget = QtWidgets.QWidget()
    main_widget.setLayout(main_layout)
    window.setCentralWidget(main_widget)
    window.show()

    app.exec_()


if __name__ == '__main__':
    main()
