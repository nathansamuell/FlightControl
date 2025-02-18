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
