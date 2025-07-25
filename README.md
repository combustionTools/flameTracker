# Flame Tracker
Flame Tracker is a Python-based video processing application designed for the fire research community. With its Graphical User Interface (GUI), it is possible to edit images and videos to track a flame or a bright object on a frame by frame basis. Flame characteristics such as position, spread rate, length and area can be obtained by isolating a flame from its background with different methods.

Flame Tracker is open source and cross platform, and information about how to use it is available on the Wiki page (https://github.com/combustionTools/flameTracker/wiki).

Original Author: Luca Carmignani, PhD

Collaborator/Contributor/Co-Author: Charles Scudiere, PhD

Contact: flameTrackerContact@gmail.com

Copyright (C) 2020-2025  Luca Carmignani, Charles Scudiere

## Subscribe to the Flame Tracker newsletter!
Stay up to date with new versions and other information! Subscribe here: https://docs.google.com/forms/d/e/1FAIpQLSc73pIB-tiwwX9s0nAkJ12WQ9dFSfLL3er3lLuyeshLAXtvhA/viewform?usp=sf_link

## To cite this work:
L. Carmignani, Flame Tracker: An image analysis program to measure flame characteristics, SoftwareX, Vol. 15, 2021, https://www.sciencedirect.com/science/article/pii/S2352711021000984?via%3Dihub

# Before you start
Note: Windows users have the option to donwload the latest release of the executable file of the Flame Tracker (https://github.com/combustionTools/flameTracker/releases), avoiding the need to download the scripts.

## 1. Python installation (if needed)

Python is required; if you don't have it, you can download it from: https://www.python.org

## 2. Required packages

The packages required to run the code are (they can be installed with pip or anaconda):
- Pyqt6 (https://pypi.org/project/PyQt6/)
- opencv-python (https://pypi.org/project/opencv-python/)
- numPy (https://numpy.org)
- PyQtgraph (http://www.pyqtgraph.org)

**Note:** Creating a virtual environment is recommended to make sure you are using the right packages.

# Additional information
For more information about installing and running Flame Tracker (with the script and the Windows release), as well as the use of the software, refer to the Wiki page: https://github.com/combustionTools/flameTracker/wiki.

For issues with the code and/or the analysis, please attach screenshots or other useful information related to you problem with your question at: flameTrackerContact@gmail.com.

# Code overview
As mentioned before, the Flame Tracker folder contains a number of Python files: flameTracker.py, manualTracking.py, lumaTracking.py, RGBTracking.py, HSVTracking.py, boxesGUI_OS.py, and templateAddition.py. Flame Tracker is conceptually divided in two categories, video editing and video analysis. Both the scripts and the GUI follow this conceptual scheme.
The objects and their locations in the GUI are listed in boxesGUI_OS.py, with specific values depending on the operating system of the user. The file flameTracker.py (the only one launched by the user) controls the video editing, while the analysis methods, ie. manualTracking.py, lumaTracking.py, colorTracking.py, HSVTracking.py, represent methods to be used for the video analysis.

- flameTracker.py: this is the main code to run Flame Tracker. Only the functions related to the "Preview Box" in the GUI are written in this file.

- boxesGUI_OS.py: controls the location and initialization of every object (buttons, labels, etc.) in the GUI.

- manualTracking.py: this script is used to track an object "manually" based on point-and-click method.

- lumaTracking.py: this script is used to track a flame automatically based on the luma intensity value of each pixel.

- RGBTracking.py: this script is used to automatically track a flame based on the color intensity of each pixel (RGB channels).

- HSVTracking.py: this script is used to track a flame based on Hue-Saturation-Value color space thresholding. Similar to color tracking and luma tracking, it is an automatic method requriing limited user input.

- templateAddition.py: this script is a template file to add new analysis methods to the Flame Tracker.

# Add methods to the Flame Tracker:
To add an analysis (starting from templateAddition.py is recommended):
1) create a new 'Analysis box' in boxesGUI_OS.py (check size with other recent files such as colorTracking.py), and a new file with your new functions 
2) in the self.analysisSelectionBox function in flameTracker.py, add the connection to your new file
3) the buttons in the new file will need their methods declared in flameTracker.py. There is an assigned method block for each analysis at the end of the class 'Window'.

# License
Flame Tracker is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Flame Tracker is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
