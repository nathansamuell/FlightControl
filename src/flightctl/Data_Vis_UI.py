# SRAD Avionics Ground Software for AIAA UH
#
# Copyright (c) 2024 Nathan Samuell (www.github.com/nathansamuell)
# Omkar Borikar (www.github.com/oborikar)
# Licensed under the MIT License
#
# More information on the MIT license as well as a complete copy
# of the license can be found here: https://choosealicense.com/licenses/mit/
# All above text must be included in any restribution.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

flight_data = pd.read_csv("FL42.csv")