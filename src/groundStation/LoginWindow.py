# SRAD Avionics Ground Software for AIAA UH
#
# Copyright (c) 2024 Nathan Samuell (www.github.com/nathansamuell)
# Licensed under the MIT License
#
# More information on the MIT license as well as a complete copy
# of the license can be found here: https://choosealicense.com/licenses/mit/
# All above text must be included in any restribution.


# app class imports
from groundStation.Numpad import Numpad

# qt imports
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


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

        aiaaLogo.setPixmap(QPixmap("/src/groundStation/cropped-aiaaweblogo-2.png"))
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
