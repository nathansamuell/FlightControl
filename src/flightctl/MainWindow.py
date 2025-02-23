# SRAD Avionics Ground Software for AIAA UH
#
# Copyright (c) 2024 Nathan Samuell (www.github.com/nathansamuell)
# Licensed under the MIT License
#
# More information on the MIT license as well as a complete copy
# of the license can be found here: https://choosealicense.com/licenses/mit/
# All above text must be included in any restribution.


# imports
import os
from enum import Enum

from dotenv import load_dotenv
from flightctl.FileWriter import FileWriter
from flightctl.SerialCommunicator import SerialCommunicator
from flightctl.Views import LoginWindow, ParsedText, RawText
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QStackedLayout, QWidget


class WindowStatus(Enum):
    INIT = 0
    LOGIN = 1
    DEFAULT = 2
    RAW_TEXT = 3
    PARSED_TEXT = 4  # parsed text in the form of a table
    FC_STATUS = 5  # this view shows us status updates from rocket components


class MainWindow(QMainWindow):
    # view status signal
    statusSignal = pyqtSignal(WindowStatus)

    # overrode initial constructor
    def __init__(self):
        super().__init__()

        # window level setup
        self.isDisplayOn = False
        self.windowStack = QStackedLayout()
        self.statusSignal.connect(self.updateStatus)
        self.updateStatus(WindowStatus.INIT)
        mainWidget = QWidget()
        mainWidget.setLayout(self.windowStack)
        self.setCentralWidget(mainWidget)
        self.setFixedSize(800, 480)
        # self.showFullScreen()

        # initialize modules
        self.initGUI()
        self.initNP()
        self.initFW()
        self.initSC()

    # init methods below
    def initGUI(self):
        self.loginWindow = LoginWindow()
        self.windowStack.addWidget(self.loginWindow)
        self.statusSignal.emit(WindowStatus.LOGIN)

        # add other views
        self.rawText = RawText()
        self.windowStack.addWidget(self.rawText)

        self.parsedText = ParsedText()
        self.windowStack.addWidget(self.parsedText)

    def initNP(self):
        self.loginWindow.numpad.loginSuccess.connect(self.loginSuccess)
        self.loginWindow.numpad.loginFailure.connect(self.loginFailure)

    def initFW(self):  # sets up FileWriter!
        # TODO: add file output name/path capabilities in .env file
        # TODO: check issue #37 for more info

        self.fw = FileWriter()

    def initSC(self):  # sets up SerialCommunicator!
        # set up port
        load_dotenv()
        mock = os.getenv("MOCK_SERIAL")
        if mock == "TRUE":
            port = "test"
            self.sc = SerialCommunicator(port, 9600)
        else:
            port = os.getenv("SERIAL_PORT")
            self.sc = SerialCommunicator(port, 9600)

        # set up data signal/start the communicator
        self.sc.dataSignal.connect(self.dataHandler)
        self.sc.start()

    # signal update handlers below
    def dataHandler(self, data):
        # send data to each view
        match self.status:
            case WindowStatus.INIT:  # no data on this view
                pass

            case WindowStatus.LOGIN:  # or this view
                pass

            case WindowStatus.RAW_TEXT:
                self.rawText.appendText(data)

            case WindowStatus.PARSED_TEXT:
                self.parsedText.appendText(data)

        # write out our data regardless of view to file
        for element in data:
            self.fw.addToFile(element + "\n")

    def updateStatus(self, status):
        if status == WindowStatus.RAW_TEXT:
            # print("update status method called")
            self.status = WindowStatus.RAW_TEXT
            self.windowStack.setCurrentIndex(1)
        elif status == WindowStatus.LOGIN:
            # print("login window status called")
            self.status = WindowStatus.LOGIN
            self.windowStack.setCurrentIndex(0)

        elif status == WindowStatus.PARSED_TEXT:
            self.status = WindowStatus.PARSED_TEXT
            self.windowStack.setCurrentIndex(2)

    def loginSuccess(self):
        self.isDisplayOn = True
        self.statusSignal.emit(WindowStatus.RAW_TEXT)
        # self.sc.start()

    def loginFailure(self):
        self.loginWindow.enterPinText.setText("Incorrect Pin--Try Again: ")

    # ui update handler
    def keyPressEvent(
        self, event
    ):  # built in to pyqt5, allows us to bind keys to operations.
        if event.key() == Qt.Key_1:
            self.statusSignal.emit(WindowStatus.DEFAULT)

        elif event.key() == Qt.Key_2:
            self.statusSignal.emit(WindowStatus.LOGIN)

        elif event.key() == Qt.Key_3:
            self.statusSignal.emit(WindowStatus.RAW_TEXT)

        elif event.key() == Qt.Key_4:
            self.statusSignal.emit(WindowStatus.PARSED_TEXT)

        elif event.key() == Qt.Key_Escape:
            # stops the listening thread and closes the app
            self.fw.writeEOF(
                "outputName"
            )  # TODO: check initFW() method or issue #37 for more info
            self.sc.stop()
            self.close()
