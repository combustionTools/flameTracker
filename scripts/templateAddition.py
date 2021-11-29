"""
Flame Tracker. This program is designed to track flames or bright objects in videos or images.
Copyright (C) 2020,2021  Luca Carmignani

This file is part of Flame Tracker.

Flame Tracker is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Flame Tracker is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Author: Luca Carmignani, PhD
Contact: flameTrackerContact@gmail.com
"""

### This connects this specific file to the main code (flameTracker.py)
import flameTracker as ft
import boxesGUI_OS as gui # for the objects in the user interface

def initVars(self): # define initial variables
    global a, b
    var = 0

def yourFunction(self, par):
    # The video editing is covered by the Flame Tracker code, here only the independent analysis should be included

""" The following part is for creating the user interface objects in 'boxexGUI_OS'. """

### This is the box that will show in the "analysis box" of the GUI. There are a few examples of widgets you can use
def yourGUIBox(self):
    # Differentiate the locations of the objects based on the Operating System.
    if sys.platform == 'darwin': #Mac
        self.yourTrackingBox = QGroupBox(' ', self.analysisGroupBox)
        self.yourTrackingBox.setGeometry(0, 0, 1050, 390)

        # size of GUI labels (in px):
        h_lbl = 22 # height of labels
        h_txt = 30 # height of text boxes
        h_btn = 30 # height of buttons

        # first column coordinates
        x1 = [ 10,   5]
        y1 = [ 20,  45]
        w1 = [100, 150]

        # second column coordinates
        x2 = [ 10,   5]
        y2 = [ 20,  45]
        w2 = [100, 150]

        # labels (since there's only one or two usually, it's easier to write the entire set of coord.)
        lbl1 = [190, 25, 420, 300]
        lbl2 = [620, 25, 420, 300]
    elif sys.platform == 'win32': #Windows
        self.yourTrackingBox = QGroupBox(' ', self.analysisGroupBox)
        self.yourTrackingBox.setGeometry(0, 0, 1050, 390)

        # size of GUI labels (in px):
        h_lbl = 22 # height of labels
        h_txt = 30 # height of text boxes
        h_btn = 30 # height of buttons

        # first column coordinates
        x1 = [ 10,   5]
        y1 = [ 20,  45]
        w1 = [100, 150]

        # second column coordinates
        x2 = [ 10,   5]
        y2 = [ 20,  45]
        w2 = [100, 150]

        # labels (since there's only one or two usually, it's easier to write the entire set of coord.)
        lbl1 = [190, 25, 420, 300]
        lbl2 = [620, 25, 420, 300]
    elif sys.platform == 'linux':
        self.yourTrackingBox = QGroupBox(' ', self.analysisGroupBox)
        self.yourTrackingBox.setGeometry(0, 0, 1050, 390)

        # size of GUI labels (in px):
        h_lbl = 22 # height of labels
        h_txt = 30 # height of text boxes
        h_btn = 30 # height of buttons

        # first column coordinates
        x1 = [ 10,   5]
        y1 = [ 20,  45]
        w1 = [100, 150]

        # second column coordinates
        x2 = [ 10,   5]
        y2 = [ 20,  45]
        w2 = [100, 150]

        # labels (since there's only one or two usually, it's easier to write the entire set of coord.)
        lbl1 = [190, 25, 420, 300]
        lbl2 = [620, 25, 420, 300]

    self.yourTrackingBox.setStyleSheet('background-color: None')

    # first column
    txtBox = QLabel('Your text', self.yourTrackingBox) # static text
    txtBox.setGeometry(x1[0], y1[0], w1[0], h_txt)
    self.label = QLineEdit('Your label', self.yourTrackingBox) # the user can type in the box
    self.label.setGeometry(x1[1], y1[1], w1[1], h_lbl)

    # second column
    self.button = QPushButton('Your button', self.yourTrackingBox)
    self.button.setGeometry(x2[0], y2[0], w2[0], h_btn)
    self.button.clicked.connect(self.button_clicked) # this line connects the button object to the function in flameTracker.py
    self.checkBox = QCheckBox('Your checkbox', self.yourTrackingBox)
    self.checkBox.setGeometry(x2[1], y2[1], w2[1], h_btn)
    self.checkBox.setChecked(True)

    # Make sure to include a button to explain the functionalities of your code
    helpBtn = QPushButton('How to use your method', self.yourTrackingBox)
    helpBtn.setGeometry(x3[0], y3[0], w3[0], h_btn)
    helpBtn.clicked.connect(self.helpBtn_clicked)

    # first label
    self.lbl1 = QLabel(self.yourTrackingBox)
    self.lbl1.setGeometry(lbl1[0], lbl1[1], lbl1[2], lbl1[3])
    self.lbl1.setStyleSheet('background-color: white')

### here you can write the text for the help button
def helpBtn_clicked(self):
    msg = QMessageBox(self)
    msg.setText(""" Your help text """)
    msg.exec_()
