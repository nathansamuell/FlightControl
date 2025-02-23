# SRAD Avionics Ground Software for AIAA UH
#
# Copyright (c) 2024 Nathan Samuell (www.github.com/nathansamuell)
# Licensed under the MIT License
#
# More information on the MIT license as well as a complete copy
# of the license can be found here: https://choosealicense.com/licenses/mit/
# All above text must be included in any restribution.

# imports
import importlib.resources as resources
import threading
import time

import serial  # noqa: F401
from PyQt5.QtCore import QObject, pyqtSignal


class SerialCommunicator(QObject):
    dataSignal = pyqtSignal(list)

    def __init__(self, sp, br):
        super().__init__()  # needed to inherit from any Q class
        serialPort = sp  # noqa: F841
        baudRate = br  # noqa: F841

        if sp == "test":
            # set up reading from file
            # run devRead method on FL42.csv
            self.readThread = threading.Thread(target=self.devRead)
            rocketPacket = "FLIGHTCTL: DEV MODE USING FL42.CSV"
            self.dataSignal.emit([rocketPacket])

        else:
            try:
                self.ser = serial.Serial(serialPort, baudRate, timeout=1)

            except serial.serialutil.SerialException:
                rocketPacket = "FLIGHTCTL: ERROR: Serial Port Not Open!"
                self.dataSignal.emit([rocketPacket])

            self.readThread = threading.Thread(target=self.read)

        self.stopEvent = threading.Event()

    def devRead(self):
        while not self.stopEvent.is_set():
            rocketData = []
            with resources.path(__package__, "FL42.csv") as path:
                with open(path, "r") as file:
                    i = 0
                    for line in file:
                        if self.stopEvent.is_set():
                            return

                        rocketPacket = line
                        rocketData.append(rocketPacket)
                        i += 1
                        if i == 5:
                            self.dataSignal.emit(rocketData)
                            i = 0
                            rocketData = []
                            time.sleep(0.1)

    def read(self):
        # while the thread is running,
        while not self.stopEvent.is_set():

            rocketData = []  # holds our list of five correctly picked data

            # attempt to collect five data collections (keeps our number of pyqt5 signals down)
            for i in range(5):
                try:
                    rocketPacket = (
                        self.ser.readline().decode("utf-8").rstrip()
                    )  # read from rocket
                    if (
                        rocketPacket == b""
                    ):  # empty string byte means no data was received before timeout
                        rocketPacket = (
                            "no data"  # FIXME: we need a standardized signal for this
                        )

                    rocketData.append(rocketPacket)  # add to list to send to app!

                except serial.serialutil.PortNotOpenError:
                    rocketPacket = "FLIGHTCTL: ERROR: Serial Port Not Open!"
                    self.stopEvent.set()
                    self.dataSignal.emit([rocketPacket])

                except AttributeError as e:
                    rocketPacket = "FLIGHTCTL: ERROR: " + str(e)
                    self.stopEvent.set()
                    self.dataSignal.emit([rocketPacket])

            self.dataSignal.emit(rocketData)  # if no errors occur then send the list!

        if self.stopEvent.is_set():
            self.dataSignal.emit(rocketData)
            self.dataSignal.emit(["FLIGHTCTL: Restart app to try again"])

    def transmit(self, message):
        self.ser.write(message.encode("utf-8"))  # noqa: E1101

    def write(self, message):
        return message

    def start(self):
        self.stopEvent.clear()
        self.readThread.start()

    def stop(self):
        self.stopEvent.set()
