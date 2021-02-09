# Flame Tracker
The Flame Tracker is a video processing application designed for the combustion research community.

The code is open source and cross platform; however, the MacOS and Windows versions are different. In the 'script' folder there are both versions. Windows user have the additional option to donwload the latest release of the Flame Tracker without the need to download the scripts (see...).

# Before you start:
Inside the script folder there are five python files, with flameTracker.py being the main file.
The Flame Tracker was written in Python 3.6+, and the packages required to run the code are:
- Pyqt5
- cv2 
- numpy
- pyqtgraph

In the last package (pyqtgraph), one of the source codes related to the legend visualization in graphs has been modified. The version used by the Flame Tracker is in combustionTools/flameTracker/scripts/other; this file should replace the original one in the package folder pyqtgraph/graphicsItems/legendItems.py.

# Run the code:
At this point, you should be able to run flameTracker.py using python3 on terminal (Mac users) or console (Windows users).

# Add methods to the Flame Tracker:


