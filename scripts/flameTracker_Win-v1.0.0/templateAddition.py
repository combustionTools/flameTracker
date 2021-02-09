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

### This connects this specific file to the main one (flameTracker.py)
from flameTracker import *

### This is the box that will show in the "analysis box" of the GUI. There are a few examples of widgets you can use
def createYourNameBox(self):
    self.youFileNameValue = True #this tells the main code that this analysis is selected. Include a default false value in the main file flameTracker.py
    self.yourNameBox = QGroupBox(' ', self.analysisGroupBox)
    self.yourNameBox.setGeometry(0,0, 850, 350)
    self.yourNameBox.setStyleSheet('background-color: None')

### This are examples of objects available. In the other files I used x_cln1 and h_txt to modify the location and height of the objects all at once for convenience.

#    h_txt = 30
#    h_btn = 25
# first column
#    x_cln1 = 10
#    staticTxt = QLabel(self.yourNameBox)
#    staticTxt.setText('Your text')
#    staticTxt.setGeometry(x_cln1, 20, 100, h_txt)

#    self.comboBox = QComboBox(self.yourNameBox)
#    self.comboBox.setGeometry(x_cln1, 40, 120, h_btn)
#    self.comboBox.addItem('item 1')
#    self.comboBox.addItem('item 2')
#    self.comboBox.activated.connect(self.comboBox_clicked) #this function will be defined in main file

#    self.slider = QSlider(Qt.Horizontal, self.yourNameBox)
#    self.slider.setGeometry(x_cln1 + 90, 50, 80, 25)

#    self.yourLabel = QLabel(self.yourNameBox)
#    self.yourLabel.setGeometry(450, 50, 360, 240)
#    self.yourLabel.setStyleSheet('background-color: white')

    self.yourNameBox.show()

### here you can write the text for the help button
def helpBtn_FileInitials(self):
    msg = QMessageBox(self)
    msg.setText(""" Your help text """)
    msg.exec_()
