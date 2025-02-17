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


# instantiation
class FileWriter:
    def __init__(self):
        self.tempFile = "dataOut.tmp"
        self.devFile = "FL42.csv"
        with open(self.tempFile, "w") as file:
            file.write("File Initialized\n")

    def addToFile(self, dataOut):
        with open(self.tempFile, "a") as file:
            file.write(dataOut)

    def writeEOF(self, fileName):
        outputFileName = fileName + ".csv"
        with open(self.tempFile, "r") as file:
            flightData = file.read()

        with open(outputFileName, "w") as file:
            file.write(flightData)

        os.remove(self.tempFile)
