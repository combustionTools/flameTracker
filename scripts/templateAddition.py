"""
Flame Tracker. This program is designed to track flames or bright objects in videos or images.
Copyright (C) 2020,2025  Luca Carmignani

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

########### The following part is for creating the user interface objects at the end of 'boxexGUI_OS.py'. ####
#######################################################################################################

### This is the box that will show in the "analysis box" of the GUI. There are a few examples of widgets you can use
def yourGUIBox(self):
    self.box_layout = ft.QGridLayout()
    self.box_layout.setSpacing(10)

    # #first column
    txtBox = ft.QLabel('Text:')
    self.editBox = ft.QLineEdit('100')


    # second column
    self.button = ft.QPushButton('Btn')
    self.button.clicked.connect(self.button_clicked) # this line connects the button object to the function in flameTracker.py


    # Make sure to include a button to explain the functionalities of your code
    helpBtn = ft.QPushButton('How to use your method')
    helpBtn.clicked.connect(self.helpBtn_clicked)

    # first label
    self.lbl1 = ft.QLabel()
    self.lbl1.setStyleSheet('background-color: white')
    self.plot1 = ft.pg.PlotWidget()
    self.plot1.setBackground('w')


    # specify the layout of the box
    self.box_layout.addWidget(txtBox, 0, 0, 1, 3)
    self.box_layout.addWidget(self.editBox, 1, 0, 1, 1)
    self.box_layout.addWidget(self.button, 1, 1, 1, 1)

### here you can write the text for the help button
def helpBtn_clicked(self):
    msg = QMessageBox(self)
    msg.setText(""" Your help text """)
    msg.exec_()
