# SRAD Avionics Ground Software for AIAA UH
#
# Copyright (c) 2024 Nathan Samuell (www.github.com/nathansamuell)
# Licensed under the MIT License
#
# More information on the MIT license as well as a complete copy
# of the license can be found here: https://choosealicense.com/licenses/mit/
# All above text must be included in any restribution.

# imports
import importlib.resources as resources  # used for image handling

# app class/qt imports
from flightctl.Numpad import Numpad

# qt imports
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QTableWidget,
    QTableWidgetItem,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)


# aiaa image path finder
def getLogoPath():
    with resources.path(__package__, "cropped-aiaaweblogo-2.png") as path:
        return str(path)


# The Login Window with the password etc
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        aiaaLogo = QLabel()
        aiaaLogo.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding))
        self.enterPinText = QLabel("       Enter PIN:")
        self.enterPinText.setFixedHeight(150)
        font = QFont()
        font.setPointSize(16)
        self.enterPinText.setFont(font)

        spacerL = QSpacerItem(240, QSizePolicy.Ignored)
        spacerR = QSpacerItem(240, QSizePolicy.Ignored)

        aiaaLogo.setPixmap(QPixmap(getLogoPath()))
        self.numpad = Numpad()

        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QHBoxLayout()

        layout3.addItem(spacerL)
        layout3.addWidget(self.enterPinText)
        layout3.addItem(spacerR)

        layout2.addLayout(layout3)
        layout2.addWidget(self.numpad)
        layout1.addWidget(aiaaLogo)
        layout1.addLayout(layout2)

        # set the layout to the window
        self.setLayout(layout1)


# the barebones view
#
# currently the default until I finish the new default view.
# a list of those components will be left below later on
#
#
#
# other view ideas:
#   --gps info/location info
#   --flight stage/status
#   --data transmission indicator?
#   --send message to the rocket in the future maybe?
class RawText(QTextBrowser):
    def __init__(self):
        super().__init__()

        # setup for before run
        self.setPlainText("FLIGHTCTL 1.0.0post2 -- AIAA UH\n")

    def appendText(self, message):
        for i in range(len(message)):
            self.append(message[i])


class ParsedText(QTableWidget):
    def __init__(self):
        super().__init__()

        # add test data
        self.dataCols = 43
        self.setColumnCount(self.dataCols)
        self.setHorizontalHeaderLabels(
            [
                "time",
                "lat",
                "lon",
                "sat",
                "spd",
                "cou",
                "g_alt",
                "state",
                "eul_x",
                "eul_y",
                "eul_z",
                "q_w",
                "q_x",
                "q_y",
                "q_z",
                "q_wn",
                "q_xn",
                "q_yn",
                "q_zn",
                "acc_i_x,acc_i_y",
                "acc_i_z",
                "rate_x",
                "rate_y",
                "rate_z",
                "acc_b_x",
                "acc_b_y",
                "acc_b_z",
                "rate_xn",
                "rate_yn",
                "rate_zn",
                "acc_b_xn",
                "acc_b_yn",
                "acc_b_zn",
                "acc_b_xh",
                "acc_b_yh",
                "acc_b_zh",
                "press",
                "alt",
                "vel_z",
                "t_lsm",
                "t_axl",
                "t_bno",
                "t_bmp",
            ]
        )
        self.rowCount = 0
        self.scrollable = True
        self.verticalScrollBar().sliderPressed.connect(self.scrollStop)
        self.verticalScrollBar().sliderReleased.connect(self.scrollStart)

    # deletes old entries
    def scrollStop(self):
        self.scrollable = False

    def scrollStart(self):
        self.scrollable = True

    # used to add data to view
    def appendText(self, message):
        for i in range(len(message)):
            self.insertRow(self.rowCount)
            currCol = 0
            for data in message[i].split(","):
                self.setItem(self.rowCount, currCol, QTableWidgetItem(data))
                if self.scrollable:
                    self.scrollToBottom()
                currCol += 1

            self.rowCount += 1
