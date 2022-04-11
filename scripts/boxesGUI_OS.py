"""
Flame Tracker. This program is designed to track flames or bright objects in videos or images.
Copyright (C) 2020-2022  Luca Carmignani; 2021, 2022 Charles Scudiere

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

Original Author: Luca Carmignani, PhD
Collaborator/Contributor: Charles Scudiere, PhD
Contact: flameTrackerContact@gmail.com
"""

import flameTracker as ft
import colorTracking as ct

def previewBox(self):
    self.setWindowTitle(f'Flame Tracker ({self.FTversion})')
    self.setGeometry(10, 10, 1000, 600)
    # self.resize(1000, 800)
    box = ft.QWidget(self)
    self.setCentralWidget(box)
    layout = ft.QVBoxLayout()

    parametersBox = ft.QGroupBox('Preview box')
    parametersBox_layout = ft.QGridLayout() #QVBoxLayout()
    parametersBox_layout.setSpacing(10)

    # first column
    self.msgLabel = ft.QLabel('Welcome to the Flame Tracker! \n\n Click on the Help button to get started.')
    self.msgLabel.setStyleSheet('background-color: white')
    self.msgLabel.setWordWrap(True)
    self.fNameLbl = ft.QLabel('(file name)')
    self.fNameLbl.setStyleSheet('background-color: white')
    widthTxt = ft.QLabel('Width (px):')
    self.vWidthLbl = ft.QLabel()
    self.vWidthLbl.setStyleSheet('background-color: white')
    vHeightTxt = ft.QLabel('Height (px):')
    self.vHeightLbl = ft.QLabel()
    self.vHeightLbl.setStyleSheet('background-color: white')
    vFpsTxt = ft.QLabel('Frame rate (fps):')
    self.vFpsLbl = ft.QLabel()
    self.vFpsLbl.setStyleSheet('background-color: white')
    vFramesTxt = ft.QLabel('Frames #:')
    self.vFramesLbl = ft.QLabel()
    self.vFramesLbl.setStyleSheet('background-color: white')
    vDurationTxt = ft.QLabel('Duration (s):')
    self.vDurationLbl = ft.QLabel()
    self.vDurationLbl.setStyleSheet('background-color: white')

    parametersBox_layout.addWidget(self.msgLabel, 0, 0, 5, 2)
    parametersBox_layout.addWidget(self.fNameLbl, 5, 0, 1, 2)
    parametersBox_layout.addWidget(widthTxt, 6, 0, 1, 1)
    parametersBox_layout.addWidget(self.vWidthLbl, 6, 1, 1, 1)
    parametersBox_layout.addWidget(vHeightTxt, 7, 0, 1, 1)
    parametersBox_layout.addWidget(self.vHeightLbl, 7, 1, 1, 1)
    parametersBox_layout.addWidget(vFpsTxt, 8, 0, 1, 1)
    parametersBox_layout.addWidget(self.vFpsLbl, 8, 1, 1, 1)
    parametersBox_layout.addWidget(vFramesTxt, 9, 0, 1, 1)
    parametersBox_layout.addWidget(self.vFramesLbl, 9, 1, 1, 1)
    parametersBox_layout.addWidget(vDurationTxt, 10, 0, 1, 1)
    parametersBox_layout.addWidget(self.vDurationLbl, 10, 1, 1, 1)

    # second column
    clmn2_Txt = ft.QLabel('Video parameters:')
    self.firstFrameTxt = ft.QLabel('First frame:')
    self.firstFrameIn = ft.QLineEdit()
    self.lastFrameTxt = ft.QLabel('Last frame:')
    self.lastFrameIn = ft.QLineEdit()
    self.skipFrameTxt = ft.QLabel('Skip frames:')
    self.skipFrameIn = ft.QLineEdit()
    self.measureScaleTxt = ft.QLabel('Scale px/mm')
    self.scaleIn = ft.QLineEdit()
    self.refPointTxt = ft.QLabel('Ref. point')
    self.refPointIn = ft.QLineEdit()
    self.roiBtn = ft.QPushButton('Select ROI')
    self.roiBtn.clicked.connect(self.roiBtn_clicked)
    self.roiOneTxt = ft.QLabel('ROI, x:')
    self.roiOneIn = ft.QLineEdit()
    self.roiTwoTxt = ft.QLabel('ROI, y:')
    self.roiTwoIn = ft.QLineEdit()
    self.roiThreeTxt = ft.QLabel('ROI, w:')
    self.roiThreeIn = ft.QLineEdit()
    self.roiFourTxt = ft.QLabel('ROI, h:')
    self.roiFourIn = ft.QLineEdit()

    parametersBox_layout.addWidget(clmn2_Txt, 0, 3, 1, 1)
    parametersBox_layout.addWidget(self.firstFrameTxt, 1, 3, 1, 2)
    parametersBox_layout.addWidget(self.firstFrameIn, 1, 4, 1, 1)
    parametersBox_layout.addWidget(self.lastFrameTxt, 2, 3, 1, 1)
    parametersBox_layout.addWidget(self.lastFrameIn, 2, 4, 1, 1)
    parametersBox_layout.addWidget(self.skipFrameTxt, 3, 3, 1, 1)
    parametersBox_layout.addWidget(self.skipFrameIn, 3, 4, 1, 1)
    parametersBox_layout.addWidget(self.measureScaleTxt, 4, 3, 1, 1)
    parametersBox_layout.addWidget(self.scaleIn, 4, 4, 1, 1)
    parametersBox_layout.addWidget(self.refPointTxt, 5, 3, 1, 1)
    parametersBox_layout.addWidget(self.refPointIn, 5, 4, 1, 1)
    parametersBox_layout.addWidget(self.roiBtn, 6, 3, 1, 2)
    parametersBox_layout.addWidget(self.roiOneTxt, 7, 3, 1, 1)
    parametersBox_layout.addWidget(self.roiOneIn, 7, 4, 1, 1)
    parametersBox_layout.addWidget(self.roiTwoTxt, 8, 3, 1, 1)
    parametersBox_layout.addWidget(self.roiTwoIn, 8, 4, 1, 1)
    parametersBox_layout.addWidget(self.roiThreeTxt, 9, 3, 1, 1)
    parametersBox_layout.addWidget(self.roiThreeIn, 9, 4, 1, 1)
    parametersBox_layout.addWidget(self.roiFourTxt, 10, 3, 1, 1)
    parametersBox_layout.addWidget(self.roiFourIn, 10, 4, 1, 1)

    #third column
    self.rotationAngleInTxt = ft.QLabel('Rotation (deg):')
    self.rotationAngleIn = ft.QLineEdit()
    self.brightnessTxt = ft.QLabel('Brightness:')
    self.brightnessLbl = ft.QLabel('0')
    self.brightnessLbl.setStyleSheet('background-color: white')
    self.brightnessSlider = ft.QSlider(ft.Qt.Orientation.Horizontal)
    # self.brightnessSlider.setGeometry(x3[5], y3[5], w3[5], h_slider)
    self.brightnessSlider.setMinimum(-50)
    self.brightnessSlider.setMaximum(50)
    self.brightnessSlider.setValue(0)
    self.brightnessSlider.sliderReleased.connect(self.editFramesSlider_released)
    self.contrastTxt = ft.QLabel('Contrast:')
    self.contrastLbl = ft.QLabel('0')
    self.contrastLbl.setStyleSheet('background-color: white')
    self.contrastSlider = ft.QSlider(ft.Qt.Orientation.Horizontal)
    # self.contrastSlider.setGeometry(x3[8], y3[8], w3[8], h_slider)
    self.contrastSlider.setMinimum(-100)
    self.contrastSlider.setMaximum(+100)
    self.contrastSlider.setValue(0)
    self.contrastSlider.sliderReleased.connect(self.editFramesSlider_released)
    self.grayscale = ft.QCheckBox('Grayscale')
    correctionTxt = ft.QLabel('Correction lengths (mm):')
    self.sLengthTxt = ft.QLabel('Horizontal:')
    self.sLengthIn = ft.QLineEdit('-')
    self.sWidthTxt = ft.QLabel('Vertical:')
    self.sWidthIn = ft.QLineEdit('-')
    self.perspectiveBtn = ft.QPushButton('Correct perspective')
    self.perspectiveBtn.clicked.connect(self.perspectiveBtn_clicked)
    self.originalBtn = ft.QPushButton('Restore original')
    self.originalBtn.clicked.connect(self.originalBtn_clicked)

    parametersBox_layout.addWidget(self.rotationAngleInTxt, 0, 6, 1, 1)
    parametersBox_layout.addWidget(self.rotationAngleIn, 0, 7, 1, 1)
    parametersBox_layout.addWidget(self.brightnessTxt, 1, 6, 1, 1)
    parametersBox_layout.addWidget(self.brightnessLbl, 1, 7, 1, 1)
    parametersBox_layout.addWidget(self.brightnessSlider, 2, 6, 1, 2)
    parametersBox_layout.addWidget(self.contrastTxt, 3, 6, 1, 1)
    parametersBox_layout.addWidget(self.contrastLbl, 3, 7, 1, 1)
    parametersBox_layout.addWidget(self.contrastSlider, 4, 6, 1, 2)
    parametersBox_layout.addWidget(self.grayscale, 5, 6, 1, 1)
    parametersBox_layout.addWidget(correctionTxt, 6, 6, 1, 2)
    parametersBox_layout.addWidget(self.sLengthTxt, 7, 6, 1, 2)
    parametersBox_layout.addWidget(self.sLengthIn, 7, 7, 1, 1)
    parametersBox_layout.addWidget(self.sWidthTxt, 8, 6, 1, 1)
    parametersBox_layout.addWidget(self.sWidthIn, 8, 7, 1, 1)
    parametersBox_layout.addWidget(self.perspectiveBtn, 9, 6, 1, 2)
    parametersBox_layout.addWidget(self.originalBtn, 10, 6, 1, 2)

    # other objects
    # preview label
    self.win1 = ft.QLabel()
    # self.win1.setGeometry(win1[0], win1[1], win1[2], win1[3])
    self.win1.setStyleSheet('background-color: white')

    self.frameTxt = ft.QLabel('Current frame:')
    self.frameIn = ft.QLineEdit('0')
    self.goToFrameBtn = ft.QPushButton('Go to frame')
    self.goToFrameBtn.clicked.connect(self.goToFrameBtn_clicked)
    self.previewSlider = ft.QSlider(ft.Qt.Orientation.Horizontal)
    self.previewSlider.sliderReleased.connect(self.sliderValue_released)
    self.previewSlider.valueChanged.connect(self.sliderValue_scrolled)
    # self.showFrameLargeBtn = ft.QPushButton('Show frame')
    # self.showFrameLargeBtn.clicked.connect(self.showFrameLargeBtn_clicked)

    parametersBox_layout.addWidget(self.win1, 0, 9, 9, 4)
    parametersBox_layout.addWidget(self.frameTxt, 9, 10, 1, 1)
    parametersBox_layout.addWidget(self.frameIn, 9, 11, 1, 1)
    parametersBox_layout.addWidget(self.goToFrameBtn, 9, 12, 1, 1)
    parametersBox_layout.addWidget(self.previewSlider, 10, 9, 1, 4)
    # parametersBox_layout.addWidget(self.showFrameLargeBtn, 11, 12, 1, 1)

    parametersBox_layout.setColumnMinimumWidth(0, 100)
    parametersBox_layout.setColumnMinimumWidth(1, 50)
    parametersBox_layout.setColumnMinimumWidth(2, 5)
    parametersBox_layout.setColumnMinimumWidth(3, 100)
    parametersBox_layout.setColumnMinimumWidth(4, 50)
    parametersBox_layout.setColumnMinimumWidth(5, 5)
    parametersBox_layout.setColumnMinimumWidth(6, 100)
    parametersBox_layout.setColumnMinimumWidth(7, 50)
    parametersBox_layout.setColumnMinimumWidth(8, 5)
    parametersBox_layout.setColumnMinimumWidth(9, 100)
    parametersBox_layout.setColumnMinimumWidth(11, 50)
    parametersBox_layout.setColumnStretch(0, 1)
    parametersBox_layout.setColumnStretch(1, 1)
    parametersBox_layout.setColumnStretch(3, 1)
    parametersBox_layout.setColumnStretch(4, 1)
    parametersBox_layout.setColumnStretch(6, 1)
    parametersBox_layout.setColumnStretch(7, 1)
    parametersBox_layout.setColumnStretch(9, 1)
    parametersBox_layout.setColumnStretch(11, 1)

    parametersBox.setLayout(parametersBox_layout)



    self.analysisGroupBox = ft.QGroupBox('Analysis box')
    self.box_layout = ft.QGridLayout()
    # this text box is only shown at the beginning in the analysis box
    # tempBox = ft.QGroupBox(' ', self.analysisGroupBox)
    # tempBox.setGeometry(0, 0, 1050, 390)
    introTxt = ft.QLabel('Select the analysis method from the menu Tracking > ... to activate this panel')
    self.box_layout.addWidget(introTxt)
    self.analysisGroupBox.setLayout(self.box_layout)
    # parametersBox = ft.QVBoxLayout()#('Preview box', self)
    # self.analysisGroupBox = ft.QGroupBox('Analysis box', self)

    layout.addWidget(parametersBox)
    layout.addWidget(self.analysisGroupBox)
    box.setLayout(layout)

    # parametersBox.setLayout(layout)
    # # parametersBox = ft.QVBoxLayout()
    # # self.analysisGroupBox = ft.QVBoxLayout()
    # # outerWindow.addLayout(parametersBox)
    # # outerWindow.addLayout(self.analysisGroupBox)
    #

    # tempBox = ft.QGroupBox(' ', self.analysisGroupBox)
    # tempBox.setGeometry(0, 0, 1050, 390)
    # introTxt = ft.QLabel('Select the analysis method from -Choose analysis- to activate this panel')
    # self.analysisGroupBox.addWidget(introTxt)
    # introTxt.setStyleSheet('font: 16pt Helvetica')



    #

    # self.show()

    # menu = self.menuBar()
    # file_menu = menu.addMenu("&File")
            # file_menu.addAction(button_action)

    # Create an outer layout
#     outerLayout = ft.QHBoxLayout()#QGridLayout()
# #     # Create a form layout for the label and line edit
#     text = ft.QLabel('text:')
#     obj = ft.QLineEdit('test')
#     nextBtn = ft.QPushButton('Next')
#
#     firstCln = ft.QVBoxLayout()
#     firstCln.addWidget(text)
#     firstCln.addWidget(obj)
#
#     secondCln = ft.QVBoxLayout()
#     secondCln.addWidget(nextBtn)
#
#     # Add a label and a line edit to the form layout
#
#     # Nest the inner layouts into the outer layout
#     outerLayout.addLayout(firstCln)
#     outerLayout.addLayout(secondCln)
    # Set the window's main layout
    # self.setLayout(outerLayout)

    # if ft.sys.platform == 'darwin':
    #     self.setStyleSheet('font: 12pt Helvetica')
    #     self.setGeometry(10, 10, 1070, 800)
    # elif ft.sys.platform == 'win32':
    #     self.setStyleSheet('font: 10pt Arial')
    #     self.setGeometry(25, 25, 1070, 770)
    # elif ft.sys.platform == 'linux':
    #     self.setStyleSheet('font: 12pt Helvetica')
    #     self.setGeometry(10, 10, 1070, 780)
    # else:
    #     print('\n!!! Warning: Unable to detect OS!!!')

    # create GUI boxes:
    # parametersBox = ft.QGroupBox('Preview box', self)
    # self.analysisGroupBox = ft.QGroupBox('Analysis box', self)

    # OS-dependent coordinates for GUI objects:
#     if ft.sys.platform == 'darwin':
#         parametersBox.setGeometry(10, 30, 1050, 390)
#         self.analysisGroupBox.setGeometry(10, 400, 1050, 390)
#
#         # size of GUI labels:
#         h_msgLbl = 110
#         h_lbl = 20
#         h_txt = 30
#         h_btn = 30
#         h_slider = 25
#
#         if self.pyqtVer == '5':
#             # first column
#             x1 = [10,    5,   5,  58,  10,  10, 105,  10, 105,  10, 105,  10, 105,  10, 105]
#             y1 = [25,  135, 165, 166, 200, 225, 229, 255, 259, 285, 289, 315, 319, 345, 349]
#             w1 = [140, 150,  60, 100, 140, 140,  45,  70,  45,  90,  45,  70,  45,  70,  45]
#
#             # second column
#             x2 = [180, 180, 265, 180, 265, 180, 265, 170, 265, 170, 265, 180, 265, 180, 265, 180, 265, 180, 265, 170]
#             y2 = [ 20,  45,  49,  75,  79, 105, 109, 135, 140, 165, 170, 225, 229, 255, 259, 285, 289, 315, 319, 345]
#             w2 = [120,  80,  50,  80,  50,  80,  50, 100,  50, 100,  50,  80,  50,  80,  50,  80,  50,  80,  50, 150]
#
#             # third column
#             x3 = [340, 340, 425, 340, 428, 340, 340, 428, 340, 335, 340, 340, 425, 340, 425, 330, 330]
#             y3 = [ 20,  45,  49,  75,  82, 105, 130, 138, 160, 190, 230, 255, 259, 285, 289, 315, 345]
#             w3 = [100, 120,  50, 150,  45, 115, 150,  45, 115, 100, 150, 130,  45, 130,  45, 150, 150]
#
#             # fourth column
#             x4 = [500, 490, 500, 490, 490, 500, 500, 610, 500, 595, 500, 595, 500, 595, 490]
#             y4 = [ 20,  45,  70,  95, 125, 155, 200, 199, 225, 229, 255, 259, 285, 289, 315]
#             w4 = [ 60, 150, 130, 150, 150, 150, 150,  30, 120,  40, 100,  40, 100,  40, 150]
#
#             # other objects
#             x5 = [650, 740, 790, 650, 930]
#             y5 = [310, 314, 310, 340, 310]
#             w5 = [120,  45, 100, 390, 115]
#
#         elif self.pyqtVer == '6':
#             # first column
#             x1 = [10,   10,  10,  58,  10,  10, 105,  10, 105,  10, 105,  10, 105,  10, 105]
#             y1 = [25,  135, 165, 166, 200, 225, 229, 255, 259, 285, 289, 315, 319, 345, 349]
#             w1 = [140, 140,  50, 100, 140, 140,  45,  70,  45,  90,  45,  70,  45,  70,  45]
#
#             # second column
#             # x2 = [180, 180, 265, 180, 265, 180, 265, 180, 265, 180, 265, 180, 265, 180, 265, 180, 265, 180, 265, 180]
#             # y2 = [ 20,  45,  49,  75,  79, 105, 109, 135, 140, 165, 170, 225, 229, 255, 259, 285, 289, 315, 319, 345]
#             # w2 = [120,  80,  50,  80,  50,  80,  50,  80,  50,  80,  50,  80,  50,  80,  50,  80,  50,  80,  50, 135]
# # changed in v1.1.7
#             x2 = [180, 180, 265, 180, 265, 180, 265, 180, 265, 180, 265, 180, 265, 180, 265, 180, 265, 180, 265, 180, 180]
#             y2 = [ 20,  45,  49,  75,  79, 105, 109, 135, 140, 165, 170, 225, 229, 255, 259, 285, 289, 315, 319, 345, 195]
#             w2 = [120,  80,  50,  80,  50,  80,  50,  80,  50,  80,  50,  80,  50,  80,  50,  80,  50,  80,  50, 135, 135]
#
#
#             # third column
#             x3 = [340, 340, 425, 340, 428, 340, 340, 428, 340, 335, 340, 340, 425, 340, 425, 340, 340]
#             y3 = [ 20,  45,  49,  75,  82, 105, 130, 138, 160, 190, 230, 255, 259, 285, 289, 315, 345]
#             w3 = [100, 120,  50, 150,  45, 115, 150,  45, 115, 100, 150, 130,  45, 130,  45, 130, 130]
#
#             # fourth column
#             x4 = [500, 490, 500, 500, 500, 500, 500, 610, 500, 595, 500, 595, 500, 595, 500]
#             y4 = [ 20,  45,  70,  95, 125, 155, 200, 199, 225, 229, 255, 259, 285, 289, 315]
#             w4 = [ 60, 150, 130, 135, 135, 150, 150,  25, 120,  40, 100,  40, 100,  40, 135]
#
#             # other objects
#             x5 = [650, 740, 800, 650, 940]
#             y5 = [310, 314, 310, 340, 310]
#             w5 = [120,  45, 100, 390, 100]
#
#         # preview window
#         win1 = [650, 35, 390, 270]
#
#     elif ft.sys.platform == 'win32':
#         parametersBox.setGeometry(10, 5, 1050, 380)
#         self.analysisGroupBox.setGeometry(10, 390, 1050, 370)
#
#         # size of GUI labels:
#         h_msgLbl = 105
#         h_lbl = 20
#         h_txt = 30
#         h_btn = 25
#         h_slider = 15
#
#         # first column
#         x1 = [10,   10,  10,  65,  10,  10, 105,  10, 105,  10, 105,  10, 105,  10, 105]
#         y1 = [20,  135, 165, 165, 200, 225, 230, 255, 260, 285, 290, 315, 320, 345, 350]
#         w1 = [140, 140,  50,  85, 140,  60,  45,  60,  45,  85,  45,  65,  45,  65,  45]
#
#         # second column
#         # x2 = [170, 170, 260, 170, 260, 170, 260, 170, 260, 170, 170, 170, 260, 170, 260, 170, 260, 170, 260, 170]
#         # y2 = [ 10,  35,  40,  65,  70,  95, 100, 125, 130, 160, 190, 225, 230, 255, 260, 285, 290, 315, 320, 347]
#         # w2 = [120,  80,  50,  80,  50,  80,  50,  80,  50, 140, 140,  50,  50,  50,  50,  50,  50,  50,  50, 140]
#             # x2 = [180, 265, 180, 265, 180, 265, 180, 265, 180, 265, 180]
#             # y2 = [165, 170, 225, 229, 255, 259, 285, 289, 315, 319, 345]
#             # w2 = [80,  50,  80,  50,  80,  50,  80,  50,  80,  50, 135]
#
#         # changed in v1.1.7
#         x2 = [170, 170, 260, 170, 260, 170, 260, 170, 260, 170, 260, 170, 260, 170, 260, 170, 260, 170, 260, 170, 170]
#         y2 = [ 10,  35,  40,  65,  70,  95, 100, 125, 127, 160, 162, 225, 230, 255, 260, 285, 290, 315, 320, 347, 190]
#         w2 = [120,  80,  50,  80,  50,  80,  50,  80,  50,  80,  50,  50,  50,  50,  50,  50,  50,  50,  50, 140, 140]
#
#         # third column
#         x3 = [330, 330, 420, 330, 420, 330, 330, 420, 330, 330, 330, 330, 420, 330, 420, 330, 330]
#         y3 = [ 10,  35,  39,  65,  70,  95, 110, 115, 140, 165, 195, 220, 225, 250, 255, 280, 315]
#         w3 = [100, 120,  50, 150,  50, 137, 150,  50, 137, 100, 140, 130,  50,  60,  50, 140, 140]
#
#         # # fourth column
#         x4 = [490, 490, 490, 490, 490, 500, 490, 610, 490, 590, 490, 590, 490, 590, 490]
#         y4 = [ 10,  35,  60,  85, 115, 155, 195, 195, 220, 225, 250, 255, 280, 285, 315]
#         w4 = [ 60, 140, 100, 140, 140, 140, 140,  20, 120,  40, 100,  40, 100,  40, 140]
#
#         # other objects
#         x5 = [650, 740, 795, 650, 930]
#         y5 = [290, 296, 293, 330, 293]
#         w5 = [120,  50, 100, 390, 90]
#
#         # preview window
#         win1 = [650, 15, 390, 270]
#
#     elif ft.sys.platform == 'linux':
#         parametersBox.setGeometry(10, 5, 1050, 390)
#         self.analysisGroupBox.setGeometry(10, 400, 1050, 390)
#
#         # size of GUI labels:
#         h_msgLbl = 110
#         h_lbl = 20
#         h_txt = 30
#         h_btn = 30
#         h_slider = 25
#
#         # first column
#         x1 = [10,    5,   5,  58,  10,  10, 105,  10, 105,  10, 105,  10, 85,  10,  95]
#         y1 = [25,  135, 165, 166, 200, 225, 229, 255, 259, 285, 289, 315, 319, 345, 349]
#         w1 = [140, 150,  60, 100, 140,  90,  45,  90,  45,  90,  45,  90,  65,  90,  55]
#
#         # second column
#         #x2 = [180, 180, 265, 180, 265, 180, 265, 180, 265, 170, 170, 180, 265, 180, 180, 265, 180, 265, 170]
#         #y2 = [ 20,  45,  49,  75,  79, 105, 109, 135, 139, 165, 195, 225, 229, 255, 285, 289, 315, 319, 345]
#         #w2 = [80,   80,  50,  80,  50,  80,  50,  80,  50, 150, 150,  80,  50,  80,  80,  50,  80,  50, 150]
#
#         # x2 = [180, 180, 265, 180, 265, 180, 275, 180, 265, 180, 262, 180, 265, 180, 265, 180, 265, 180, 265, 170]
#         # y2 = [ 20,  45,  49,  75,  79, 105, 109, 135, 139, 170, 175, 225, 229, 255, 259, 285, 289, 315, 319, 345]
#         # w2 = [120,  80,  50,  80,  50,  90,  40,  80,  50,  80,  60,  80,  50,  80,  50,  80,  50,  80,  50, 150]
# # changed in v1.1.7
#         x2 = [180, 180, 265, 180, 265, 180, 275, 180, 265, 180, 262, 180, 265, 180, 265, 180, 265, 180, 265, 170, 180]
#         y2 = [ 20,  45,  49,  75,  79, 105, 109, 135, 139, 170, 175, 225, 229, 255, 259, 285, 289, 315, 319, 345, 195]
#         w2 = [120,  80,  50,  80,  50,  90,  40,  80,  50,  80,  60,  80,  50,  80,  50,  80,  50,  80,  50, 140, 140]
#
#         # third column
#         x3 = [340, 340, 425, 340, 428, 340, 340, 428, 340, 325, 335, 340, 425, 340, 425, 330, 330]
#         y3 = [ 20,  45,  49,  75,  80, 105, 125, 130, 155, 175, 200, 225, 229, 255, 259, 285, 315]
#         w3 = [100, 120,  50, 150,  45, 137, 150,  45, 115, 100, 150, 130,  50,  60,  60, 150, 150]
#
#         # fourth column
#         x4 = [500, 490, 500, 490, 490, 500, 500, 610, 500, 595, 500, 575, 500, 575, 490]
#         y4 = [ 20,  45,  70,  95, 125, 155, 200, 199, 225, 229, 255, 259, 285, 289, 315]
#         w4 = [ 60, 150, 130, 150, 150, 150, 150,  30, 120,  40, 100,  60, 100,  60, 150]
#
#         # other objects
#         x5 = [650, 750, 820, 650, 930]
#         y5 = [310, 314, 310, 340, 310]
#         w5 = [120,  65, 100, 390, 115]
#
#         # preview window
#         win1 = [650, 25, 390, 270]

    # this text box is only shown at the beginning in the analysis box
    # tempBox = ft.QGroupBox(' ', self.analysisGroupBox)
    # tempBox.setGeometry(0, 0, 1050, 390)
    # introTxt = ft.QLabel('Select the analysis method from -Choose analysis- to activate this panel', tempBox)
    # introTxt.setGeometry(100, 100, 700, 100)
    # introTxt.setStyleSheet('font: 16pt Helvetica')

    # first column
    # self.msgLabel = ft.QLabel('Welcome to the Flame Tracker! \n\n Click on the Help button to get started.', parametersBox)
    # self.msgLabel.setGeometry(x1[0], y1[0], w1[0], h_msgLbl)
    # self.msgLabel.setStyleSheet('background-color: white')
    # self.msgLabel.setWordWrap(True)
    # self.helpBtn = ft.QPushButton('Help', parametersBox)
    # self.helpBtn.setGeometry(x1[1], y1[1], w1[1], h_btn)
    # self.helpBtn.clicked.connect(self.helpBtn_clicked)
    # self.openBtn = ft.QPushButton('Open', parametersBox)
    # self.openBtn.setGeometry(x1[2], y1[2], w1[2], h_btn)
    # self.openBtn.clicked.connect(self.openBtn_clicked)
    # self.openSelectionBox = ft.QComboBox(parametersBox)
    # self.openSelectionBox.setGeometry(x1[3], y1[3], w1[3], h_btn)
    # self.openSelectionBox.addItem('Video')
    # self.openSelectionBox.addItem('Image(s)')
    # if self.pyqtVer == '5':
    #     self.openSelectionBox.activated[str].connect(self.openSelection_click)
    # elif self.pyqtVer == '6':
    #     self.openSelectionBox.activated.connect(self.openSelection_click)
    # self.fNameLbl = ft.QLabel('(file name)', parametersBox)
    # self.fNameLbl.setGeometry(x1[4], y1[4], w1[4], h_lbl)
    # self.fNameLbl.setStyleSheet('background-color: white')
    # vWidthTxt = ft.QLabel('Width (px):', parametersBox)
    # vWidthTxt.setGeometry(x1[5], y1[5], w1[5], h_txt)
    # self.vWidthLbl = ft.QLabel(parametersBox)
    # self.vWidthLbl.setGeometry(x1[6], y1[6], w1[6], h_lbl)
    # self.vWidthLbl.setStyleSheet('background-color: white')
    # vHeightTxt = ft.QLabel('Height (px):', parametersBox)
    # vHeightTxt.setGeometry(x1[7], y1[7], w1[7], h_txt)
    # self.vHeightLbl = ft.QLabel(parametersBox)
    # self.vHeightLbl.setGeometry(x1[8], y1[8], w1[8], h_lbl)
    # self.vHeightLbl.setStyleSheet('background-color: white')
    # vFpsTxt = ft.QLabel('Frame rate (fps):', parametersBox)
    # vFpsTxt.setGeometry(x1[9], y1[9], w1[9], h_txt)
    # self.vFpsLbl = ft.QLabel(parametersBox)
    # self.vFpsLbl.setGeometry(x1[10], y1[10], w1[10], h_lbl)
    # self.vFpsLbl.setStyleSheet('background-color: white')
    # vFramesTxt = ft.QLabel('Frames #:', parametersBox)
    # vFramesTxt.setGeometry(x1[11], y1[11], w1[11], h_txt)
    # self.vFramesLbl = ft.QLabel(parametersBox)
    # self.vFramesLbl.setGeometry(x1[12], y1[12], w1[12], h_lbl)
    # self.vFramesLbl.setStyleSheet('background-color: white')
    # vDurationTxt = ft.QLabel('Duration (s):', parametersBox)
    # vDurationTxt.setGeometry(x1[13], y1[13], w1[13], h_txt)
    # self.vDurationLbl = ft.QLabel(parametersBox)
    # self.vDurationLbl.setGeometry(x1[14], y1[14], w1[14], h_lbl)
    # self.vDurationLbl.setStyleSheet('background-color: white')

    #second column
    # clmn2_Txt = ft.QLabel('Video parameters:', parametersBox)
    # clmn2_Txt.setGeometry(x2[0], y2[0], w2[0], h_txt)
#     self.firstFrameTxt = ft.QLabel('First frame:', parametersBox)
#     self.firstFrameTxt.setGeometry(x2[1], y2[1], w2[1], h_txt)
#     self.firstFrameIn = ft.QLineEdit(parametersBox)
#     self.firstFrameIn.setGeometry(x2[2], y2[2], w2[2], h_lbl)
#     self.lastFrameTxt = ft.QLabel('Last frame:', parametersBox)
#     self.lastFrameTxt.setGeometry(x2[3], y2[3], w2[3], h_txt)
#     self.lastFrameIn = ft.QLineEdit(parametersBox)
#     self.lastFrameIn.setGeometry(x2[4], y2[4], w2[4], h_lbl)
#     self.skipFrameTxt = ft.QLabel('Skip frames:', parametersBox)
#     self.skipFrameTxt.setGeometry(x2[5], y2[5], w2[5], h_txt)
#     self.skipFrameIn = ft.QLineEdit(parametersBox)
#     self.skipFrameIn.setGeometry(x2[6], y2[6], w2[6], h_lbl)
#     # self.measureScaleBtn = ft.QPushButton('Scale px/mm', parametersBox)
#     # self.measureScaleBtn.setGeometry(x2[7], y2[7], w2[7], h_btn)
#     # self.measureScaleBtn.clicked.connect(self.measureScaleBtn_clicked)
#     self.measureScaleTxt = ft.QLabel('Scale px/mm', parametersBox)
#     self.measureScaleTxt.setGeometry(x2[7], y2[7], w2[7], h_txt)
#     self.scaleIn = ft.QLineEdit(parametersBox)
#     self.scaleIn.setGeometry(x2[8], y2[8], w2[8], h_lbl)
#     #self.measureScaleBtn = QPushButton('Measure scale', parametersBox)
#
#     #self.measureScaleBtn.setGeometry(x2[9], y2[9], w2[9], h_btn)
#
#
#     # CAS Move reference point to display
#     #self.refPointBtn = QPushButton('Reference point', parametersBox)
#     # self.refPointBtn = ft.QPushButton('Ref. point', parametersBox)
#     #self.refPointBtn.setGeometry(x2[10], y2[10], w2[10], h_btn)
#     # self.refPointBtn.setGeometry(x2[9], y2[9], w2[9], h_btn)
#     # self.refPointBtn.clicked.connect(self.refPointBtn_clicked)
#     self.refPointTxt = ft.QLabel('Ref. point', parametersBox)
#     self.refPointTxt.setGeometry(x2[9], y2[9], w2[9], h_txt)
#     self.refPointIn = ft.QLineEdit(parametersBox)
#     self.refPointIn.setGeometry(x2[10], y2[10], w2[10], h_lbl)
#
# # measureLenBtn added in v1.1.7
#     # self.measureLenBtn = ft.QPushButton('Measure length', parametersBox)
#     # self.measureLenBtn.setGeometry(x2[20], y2[20], w2[20], h_btn)
#     # self.measureLenBtn.clicked.connect(self.measureLenBtn_clicked)
#     self.roiOneTxt = ft.QLabel('ROI, x:', parametersBox)
#     self.roiOneTxt.setGeometry(x2[11], y2[11], w2[11], h_txt)
#     self.roiOneIn = ft.QLineEdit(parametersBox)
#     self.roiOneIn.setGeometry(x2[12], y2[12], w2[12], h_lbl)
#     self.roiTwoTxt = ft.QLabel('ROI, y:', parametersBox)
#     self.roiTwoTxt.setGeometry(x2[13], y2[13], w2[13], h_txt)
#     self.roiTwoIn = ft.QLineEdit(parametersBox)
#     self.roiTwoIn.setGeometry(x2[14], y2[14], w2[14], h_lbl)
#     self.roiThreeTxt = ft.QLabel('ROI, w:', parametersBox)
#     self.roiThreeTxt.setGeometry(x2[15], y2[15], w2[15], h_txt)
#     self.roiThreeIn = ft.QLineEdit(parametersBox)
#     self.roiThreeIn.setGeometry(x2[16], y2[16], w2[16], h_lbl)
#     self.roiFourTxt = ft.QLabel('ROI, h:', parametersBox)
#     self.roiFourTxt.setGeometry(x2[17], y2[17], w2[17], h_txt)
#     self.roiFourIn = ft.QLineEdit(parametersBox)
#     self.roiFourIn.setGeometry(x2[18], y2[18], w2[18], h_lbl)
#     self.roiBtn = ft.QPushButton('Select ROI', parametersBox)
#     self.roiBtn.setGeometry(x2[19], y2[19], w2[19], h_btn)
#     self.roiBtn.clicked.connect(self.roiBtn_clicked)
#
#     #third column
#     adjustFramesTxt = ft.QLabel('Edit frames:', parametersBox)
#     adjustFramesTxt.setGeometry(x3[0], y3[0], w3[0], h_txt)
#     self.rotationAngleInTxt = ft.QLabel('Rotation (deg):', parametersBox)
#     self.rotationAngleInTxt.setGeometry(x3[1], y3[1], w3[1], h_txt)
#     self.rotationAngleIn = ft.QLineEdit(parametersBox)
#     self.rotationAngleIn.setGeometry(x3[2], y3[2], w3[2], h_lbl)
#     self.brightnessTxt = ft.QLabel('Brightness:', parametersBox)
#     self.brightnessTxt.setGeometry(x3[3], y3[3], w3[3], h_txt)
#     self.brightnessLbl = ft.QLabel('0', parametersBox)
#     self.brightnessLbl.setGeometry(x3[4], y3[4], w3[4], h_lbl)
#     self.brightnessLbl.setStyleSheet('background-color: white')
#     if self.pyqtVer == '5':
#         self.brightnessSlider = ft.QSlider(ft.Qt.Horizontal, parametersBox)
#     elif self.pyqtVer == '6':
#         self.brightnessSlider = ft.QSlider(ft.Qt.Orientation.Horizontal, parametersBox)
#     self.brightnessSlider.setGeometry(x3[5], y3[5], w3[5], h_slider)
#     self.brightnessSlider.setMinimum(-50)
#     self.brightnessSlider.setMaximum(50)
#     self.brightnessSlider.setValue(0)
#     self.brightnessSlider.sliderReleased.connect(self.editFramesSlider_released)
#     self.contrastTxt = ft.QLabel('Contrast:', parametersBox)
#     self.contrastTxt.setGeometry(x3[6], y3[6], w3[6], h_txt)
#     self.contrastLbl = ft.QLabel('0', parametersBox)
#     self.contrastLbl.setGeometry(x3[7], y3[7], w3[7], h_lbl)
#     self.contrastLbl.setStyleSheet('background-color: white')
#     if self.pyqtVer == '5':
#         self.contrastSlider = ft.QSlider(ft.Qt.Horizontal, parametersBox)
#     elif self.pyqtVer == '6':
#         self.contrastSlider = ft.QSlider(ft.Qt.Orientation.Horizontal, parametersBox)
#     self.contrastSlider.setGeometry(x3[8], y3[8], w3[8], h_slider)
#     self.contrastSlider.setMinimum(-100)
#     self.contrastSlider.setMaximum(+100)
#     self.contrastSlider.setValue(0)
#     self.contrastSlider.sliderReleased.connect(self.editFramesSlider_released)
#     self.grayscale = ft.QCheckBox('Grayscale', parametersBox)
#     self.grayscale.setGeometry(x3[9], y3[9], w3[9], h_btn)
#     correctionTxt = ft.QLabel('Correction lengths (mm):', parametersBox)
#     correctionTxt.setGeometry(x3[10], y3[10], w3[10], h_txt)
#     self.sLengthTxt = ft.QLabel('Horizontal:', parametersBox)
#     self.sLengthTxt.setGeometry(x3[11], y3[11], w3[11], h_txt)
#     self.sLengthIn = ft.QLineEdit('-', parametersBox)
#     self.sLengthIn.setGeometry(x3[12], y3[12], w3[12], h_lbl)
#     self.sWidthTxt = ft.QLabel('Vertical:', parametersBox)
#     self.sWidthTxt.setGeometry(x3[13], y3[13], w3[13], h_txt)
#     self.sWidthIn = ft.QLineEdit('-', parametersBox)
#     self.sWidthIn.setGeometry(x3[14], y3[14], w3[14], h_lbl)
#     self.perspectiveBtn = ft.QPushButton('Correct perspective', parametersBox)
#     self.perspectiveBtn.setGeometry(x3[15], y3[15], w3[15], h_btn)
#     self.perspectiveBtn.clicked.connect(self.perspectiveBtn_clicked)
#     self.originalBtn = ft.QPushButton('Restore original', parametersBox)
#     self.originalBtn.setGeometry(x3[16], y3[16], w3[16], h_btn)
#     self.originalBtn.clicked.connect(self.originalBtn_clicked)
#
    # fourth column
    # analysisTxt = ft.QLabel('Analysis:', parametersBox)
    # analysisTxt.setGeometry(x4[0], y4[0], w4[0], h_txt)
    # self.analysisSelectionBox = ft.QComboBox(parametersBox)
    # self.analysisSelectionBox.setGeometry(x4[1], y4[1], w4[1], h_btn)
    # self.analysisSelectionBox.addItem('Choose analysis')
    # self.analysisSelectionBox.addItem('Manual tracking')
    # self.analysisSelectionBox.addItem('Luma tracking')
    # self.analysisSelectionBox.addItem('Color tracking')
    # self.analysisSelectionBox.addItem('HSV tracking')
    # if self.pyqtVer == '5':
    #     self.analysisSelectionBox.activated[str].connect(self.analysis_click)
    # elif self.pyqtVer == '6':
    #     self.analysisSelectionBox.activated.connect(self.analysis_click)
    # saveLoadTxt = ft.QLabel('Save/Load:', parametersBox)
    # saveLoadTxt.setGeometry(x4[2], y4[2], w4[2], h_txt)
    # self.saveParBtn = ft.QPushButton('Save parameters', parametersBox)
    # self.saveParBtn.setGeometry(x4[3], y4[3], w4[3], h_btn)
    # self.saveParBtn.clicked.connect(self.saveParBtn_clicked)
    # self.loadParBtn = ft.QPushButton('Load parameters', parametersBox)
    # self.loadParBtn.setGeometry(x4[4], y4[4], w4[4], h_btn)
    # self.loadParBtn.clicked.connect(self.loadParBtn_clicked)
    # self.figSize = ft.QCheckBox('Half-size figures', parametersBox)
    # self.figSize.setGeometry(x4[5], y4[5], w4[5], h_btn)
    # exportTxt = ft.QLabel('Save edited video:', parametersBox)
    # exportTxt.setGeometry(x4[6], y4[6], w4[6], h_txt)
    # self.newVideoHelpBtn = ft.QPushButton('?', parametersBox)
    # self.newVideoHelpBtn.setGeometry(x4[7], y4[7], w4[7], h_btn)
    # self.newVideoHelpBtn.clicked.connect(self.newVideoHelpBtn_clicked)
    # fpsTxt = ft.QLabel('Frame rate (fps):', parametersBox)
    # fpsTxt.setGeometry(x4[8], y4[8], w4[8], h_txt)
    # self.fpsIn = ft.QLineEdit('30', parametersBox)
    # self.fpsIn.setGeometry(x4[9], y4[9], w4[9], h_lbl)
    # codecTxt = ft.QLabel('Codec:', parametersBox)
    # codecTxt.setGeometry(x4[10], y4[10], w4[10], h_txt)
    # self.codecIn = ft.QLineEdit('mp4v', parametersBox)
    # self.codecIn.setGeometry(x4[11], y4[11], w4[11], h_lbl)
    # formatTxt = ft.QLabel('Format:', parametersBox)
    # formatTxt.setGeometry(x4[12], y4[12], w4[12], h_txt)
    # self.formatIn = ft.QLineEdit('mp4', parametersBox)
    # self.formatIn.setGeometry(x4[13], y4[13], w4[13], h_lbl)
    # self.exportVideoBtn = ft.QPushButton('Export video', parametersBox)
    # self.exportVideoBtn.setGeometry(x4[14], y4[14], w4[14], h_btn)
    # self.exportVideoBtn.clicked.connect(self.exportVideoBtn_clicked)

    # # other objects
    # self.frameTxt = ft.QLabel('Current frame:', parametersBox)
    # self.frameTxt.setGeometry(x5[0], y5[0], w5[0], h_txt)
    # self.frameIn = ft.QLineEdit('0', parametersBox)
    # self.frameIn.setGeometry(x5[1], y5[1], w5[1], h_lbl)
    # self.goToFrameBtn = ft.QPushButton('Go to frame', parametersBox)
    # self.goToFrameBtn.setGeometry(x5[2], y5[2], w5[2], h_btn)
    # self.goToFrameBtn.clicked.connect(self.goToFrameBtn_clicked)
    # if self.pyqtVer == '5':
    #     self.previewSlider = ft.QSlider(ft.Qt.Horizontal, parametersBox)
    # elif self.pyqtVer == '6':
    #     self.previewSlider = ft.QSlider(ft.Qt.Orientation.Horizontal, parametersBox)
    # self.previewSlider.setGeometry(x5[3], y5[3], w5[3], h_slider)
    # self.previewSlider.sliderReleased.connect(self.sliderValue_released)
    # self.previewSlider.valueChanged.connect(self.sliderValue_scrolled)
    # self.showFrameLargeBtn = ft.QPushButton('Show frame', parametersBox)
    # self.showFrameLargeBtn.setGeometry(x5[4], y5[4], w5[4], h_btn)
    # self.showFrameLargeBtn.clicked.connect(self.showFrameLargeBtn_clicked)
    #
    # # preview label
    # self.win1 = ft.QLabel(parametersBox)
    # self.win1.setGeometry(win1[0], win1[1], win1[2], win1[3])
    # self.win1.setStyleSheet('background-color: white')

def manualTrackingBox(self):
    # self.manualTrackingBox = ft.QGroupBox(' ', self.analysisGroupBox)
    # self.manualTrackingBox.setStyleSheet('background-color: None')
    # self.analysisGroupBox.setCentralWidget(self.manualTrackingBox)

    self.box_layout = ft.QGridLayout() #QVBoxLayout()

    # first column
    directionBoxTxt = ft.QLabel('Flame spread:')#, self.manualTrackingBox)
    self.directionBox = ft.QComboBox()#self.manualTrackingBox)
    self.directionBox.addItem('Left to right')
    self.directionBox.addItem('Right to left')
    lightTxt = ft.QLabel('Flashing light (optional):')#, self.manualTrackingBox)
    self.lightROIBtn_MT = ft.QPushButton('Pick bright region')#, self.manualTrackingBox)
    self.lightROIBtn_MT.clicked.connect(self.lightROIBtn_MT_clicked)
    self.filterLight_MT = ft.QComboBox()#self.manualTrackingBox)
    self.filterLight_MT.addItem('Track every frame')
    self.filterLight_MT.addItem('Frames light on')
    self.filterLight_MT.addItem('Frames light off')
    nClicksTxt = ft.QLabel('Tracking pts #:')#, self.manualTrackingBox)
    self.nClicksLbl = ft.QLineEdit('1')#, self.manualTrackingBox)
    self.showEdges_MT = ft.QCheckBox('Show tracking lines')#, self.manualTrackingBox)
    self.showEdges_MT.setChecked(True)
    self.manualTrackingBtn = ft.QPushButton('Start tracking')#, self.manualTrackingBox)
    self.manualTrackingBtn.clicked.connect(self.manualTrackingBtn_clicked)
    self.absValBtn = ft.QPushButton('Absolute values')#, self.manualTrackingBox)
    self.absValBtn.clicked.connect(self.absValBtn_MT_clicked)
    self.saveBtn_MT = ft.QPushButton('Save data')#, self.manualTrackingBox)
    self.saveBtn_MT.clicked.connect(self.saveBtn_MT_clicked)
    self.updateGraphsBtn_MT = ft.QPushButton('Update graphs')#, self.manualTrackingBox)
    self.updateGraphsBtn_MT.clicked.connect(self.updateGraphsBtn_MT_clicked)

    self.box_layout.addWidget(directionBoxTxt, 0, 0, 1, 1)
    self.box_layout.addWidget(self.directionBox, 0, 1, 1, 1)
    self.box_layout.addWidget(lightTxt, 1, 0, 1, 2)
    self.box_layout.addWidget(self.lightROIBtn_MT, 2, 0, 1, 2)
    self.box_layout.addWidget(self.filterLight_MT, 3, 0, 1, 2)
    self.box_layout.addWidget(nClicksTxt, 4, 0, 1, 1)
    self.box_layout.addWidget(self.nClicksLbl, 4, 1, 1, 1)
    self.box_layout.addWidget(self.showEdges_MT, 5, 0, 1, 2)
    self.box_layout.addWidget(self.manualTrackingBtn, 6, 0, 1, 2)
    self.box_layout.addWidget(self.absValBtn, 7, 0, 1, 2)
    self.box_layout.addWidget(self.saveBtn_MT, 8, 0, 1, 2)
    self.box_layout.addWidget(self.updateGraphsBtn_MT, 9, 0, 1, 2)

    # first label
    self.lbl1_MT = ft.QLabel()#self.manualTrackingBox)
    self.lbl1_MT.setStyleSheet('background-color: white')

    # second label
    self.lbl2_MT = ft.pg.PlotWidget()#self.manualTrackingBox)
    self.lbl2_MT.setBackground('w')
    self.lbl2_MT.setLabel('left', 'Spread Rate [mm/s]', color='black', size=14)
    self.lbl2_MT.setLabel('bottom', 'Time [s]', color='black', size=14)
    self.lbl2_MT.getAxis('bottom').setPen(color=(0, 0, 0))
    self.lbl2_MT.getAxis('left').setPen(color=(0, 0, 0))

    #other objects
    xAxisTxt_lbl1 = ft.QLabel('x axis:')#, self.manualTrackingBox)
    self.xAxis_lbl1 = ft.QComboBox()#self.manualTrackingBox)
    self.xAxis_lbl1.addItem('Time [s]')
    self.xAxis_lbl1.addItem('Frame #')
    yAxisTxt_lbl1 = ft.QLabel('y axis:')#, self.manualTrackingBox)
    self.yAxis_lbl1 = ft.QComboBox()#self.manualTrackingBox)
    self.yAxis_lbl1.addItem('Position [mm]')
    self.yAxis_lbl1.addItem('Position [px]')
    self.yAxis_lbl1.addItem('Spread rate [mm/s]')
    xAxisTxt_lbl2 = ft.QLabel('x axis:')#, self.manualTrackingBox)
    self.xAxis_lbl2 = ft.QComboBox()#self.manualTrackingBox)
    self.xAxis_lbl2.addItem('Time [s]')
    self.xAxis_lbl2.addItem('Frame #')
    yAxisTxt_lbl2 = ft.QLabel('y axis:')#, self.manualTrackingBox)
    self.yAxis_lbl2 = ft.QComboBox()#self.manualTrackingBox)
    self.yAxis_lbl2.addItem('Spread rate [mm/s]')
    self.yAxis_lbl2.addItem('Position [mm]')
    self.yAxis_lbl2.addItem('Position [px]')




    self.box_layout.addWidget(self.lbl1_MT, 0, 3, 8, 4)
    self.box_layout.addWidget(self.lbl2_MT, 0, 8, 8, 4)
    self.box_layout.addWidget(xAxisTxt_lbl1, 8, 5, 1, 1)
    self.box_layout.addWidget(self.xAxis_lbl1, 8, 6, 1, 1)
    self.box_layout.addWidget(yAxisTxt_lbl1, 9, 5, 1, 1)
    self.box_layout.addWidget(self.yAxis_lbl1, 9, 6, 1, 1)
    self.box_layout.addWidget(xAxisTxt_lbl2, 8, 10, 1, 1)
    self.box_layout.addWidget(self.xAxis_lbl2, 8, 11, 1, 1)
    self.box_layout.addWidget(yAxisTxt_lbl2, 9, 10, 1, 1)
    self.box_layout.addWidget(self.yAxis_lbl2, 9, 11, 1, 1)

    # box_layout.setColumnMinimumWidth(0, 80)
    # box_layout.setColumnMinimumWidth(1, 50)
    # box_layout.setColumnMinimumWidth(2, 10)
    self.box_layout.setColumnMinimumWidth(3, 80)
    self.box_layout.setColumnMinimumWidth(4, 40)
    # box_layout.setColumnMinimumWidth(5, 50)
    # box_layout.setColumnMinimumWidth(6, 100)
    # box_layout.setColumnMinimumWidth(7, 10)
    # self.box_layout.setColumnMinimumWidth(8, 40)
    # box_layout.setColumnMinimumWidth(9, 50)
    # box_layout.setColumnMinimumWidth(10, 50)
    # box_layout.setColumnMinimumWidth(11, 100)
    # box_layout.setColumnMinimumWidth(12, 50)

    # self.box_layout.setColumnStretch(0, 1)
    # self.box_layout.setColumnStretch(1, 1)
    self.box_layout.setColumnStretch(3, 1)
    # self.box_layout.setColumnStretch(4, 1)
    # self.box_layout.setColumnStretch(6, 1)
    self.box_layout.setColumnStretch(8, 1)
    # self.box_layout.setColumnStretch(9, 1)
    # self.box_layout.setColumnStretch(11, 1)


    self.analysisGroupBox.setLayout(self.box_layout)
    # self.manualTrackingBox.setLayout(box_layout)
    # self.manualTrackingBox.show()

    print('when built', self.lbl1_MT.size())

    testFun = ft.QAction('test', self)
    self.MTmenu = self.menu.addMenu("&Test")
    self.MTmenu.addAction(testFun)


        # if ft.sys.platform == 'darwin':
    #     self.manualTrackingBox = ft.QGroupBox(' ', self.analysisGroupBox)
    #     self.manualTrackingBox.setGeometry(0,0, 1050, 390)
    #
    #     # size of GUI labels:
    #     h_lbl = 22
    #     h_txt = 30
    #     h_btn = 30
    #
    #     if self.pyqtVer == '5': #PyQt5 GUI will be removed after FlameTrackerv1.1.8
    #         # first column
    #         # x1 = [ 10,   5,  10,   5,   5,  10, 120,  10,   5,   5,   5,   5]
    #         # y1 = [ 20,  45,  70,  95, 120, 150, 154, 180, 210, 240, 270, 300]
    #         # w1 = [100, 150, 150, 150, 150, 100,  30, 140, 150, 150, 150, 150]
    #         x1 = [ 10,   5,  10,  10,   5,  10, 120,  10,  10,  10,  10,  10,  10]
    #         y1 = [ 20,  45,  70,  95, 125, 150, 154, 180, 210, 240, 270, 300, 330]
    #         w1 = [100, 150, 150, 140, 150, 100,  30, 140, 140, 140, 140, 140, 140]
    #     elif self.pyqtVer == '6':
    #         # first column
    #         x1 = [10,  85,  10,  10,   5,  10, 120,  10,  10,  10,  10,  10,  10]
    #         y1 = [20,  20,  50,  80, 110, 140, 144, 170, 200, 230, 260, 290, 320]
    #         w1 = [80, 110, 150, 140, 150, 100,  30, 140, 140, 140, 140, 140, 140]
    #
    #     #other objects
    #     x2 = [450, 490, 450, 490, 850, 890, 850, 890]
    #     y2 = [300, 305, 330, 335, 300, 305, 330, 335]
    #     w2 = [ 80, 150,  80, 150,  80, 150,  80, 150]
    #
    #     # labels (since there's only two, in this case I wrote the entire set of coord.)
    #     # lbl1 = [190, 25, 420, 300]
    #     # lbl2 = [620, 25, 420, 300]
    #     lbl1 = [250, 25, 390, 270]
    #     lbl2 = [650, 25, 390, 270]
    #
    # elif ft.sys.platform == 'win32':
    #     self.manualTrackingBox = ft.QGroupBox('Analysis box', self.analysisGroupBox)
    #     self.manualTrackingBox.setGeometry(0, 0, 1050, 370)
    #
    #     # size of GUI labels:
    #     h_lbl = 22
    #     h_txt = 30
    #     h_btn = 25
    #
    #     # first column
    #     # x1 = [ 10,  10,  10,  10,  10,  10, 120,  10,  10,  10,  10,  10]
    #     # y1 = [ 15,  40,  70,  95, 125, 155, 160, 185, 215, 245, 275, 305]
    #     # w1 = [120, 140, 140, 140, 140, 140,  30, 140, 140, 140, 140, 140]
    #     x1 = [10, 100,  10,  10,  10,  10, 120,  10,  10,  10,  10,  10,  10]
    #     y1 = [15,  17,  45,  75, 105, 135, 139, 165, 195, 225, 255, 285, 315]
    #     w1 = [90, 100, 140, 140, 140, 100,  30, 140, 140, 140, 140, 140, 140]
    #
    #     #other objects
    #     x2 = [450, 490, 450, 490, 850, 890, 850, 890]
    #     y2 = [300, 302, 330, 332, 300, 302, 330, 332]
    #     w2 = [ 80, 150,  80, 150,  80, 150,  80, 150]
    #
    #     # labels (since there's only two, in this case I wrote the entire set of coord.)
    #     # lbl1 = [190, 25, 420, 300]
    #     # lbl2 = [620, 25, 420, 300]
    #     lbl1 = [250, 25, 390, 270]
    #     lbl2 = [650, 25, 390, 270]
    #
    # elif ft.sys.platform == 'linux':
    #     self.manualTrackingBox = ft.QGroupBox(' ', self.analysisGroupBox)
    #     self.manualTrackingBox.setGeometry(0,0, 1050, 390)
    #
    #     # size of GUI labels:
    #     h_lbl = 22
    #     h_txt = 30
    #     h_btn = 30
    #
    #     # first column
    #     # x1 = [ 10,   5,  10,   5,   5,  10, 120,  10,   5,   5,   5,   5]
    #     # y1 = [ 20,  45,  70,  95, 120, 150, 154, 180, 210, 240, 270, 300]
    #     # w1 = [100, 150, 150, 150, 150, 100,  30, 140, 150, 150, 150, 150]
    #     x1 = [ 10,   5,  10,  10,   5,  10, 120,  10,  10,  10,  10,  10,  10]
    #     y1 = [ 20,  45,  70,  95, 125, 150, 154, 180, 210, 240, 270, 300, 330]
    #     w1 = [100, 150, 150, 140, 150, 100,  30, 140, 140, 140, 140, 140, 140]
    #
    #     #other objects
    #     x2 = [450, 490, 450, 490, 850, 890, 850, 890]
    #     y2 = [300, 305, 330, 335, 300, 305, 330, 335]
    #     w2 = [ 80, 150,  80, 150,  80, 150,  80, 150]
    #
    #     # labels (since there's only two, in this case I wrote the entire set of coord.)
    #     # lbl1 = [190, 25, 420, 300]
    #     # lbl2 = [620, 25, 420, 300]
    #     lbl1 = [250, 25, 390, 270]
    #     lbl2 = [650, 25, 390, 270]

    # self.manualTrackingBox.setStyleSheet('background-color: None')
    #
    # # #first column
    # directionBoxTxt = ft.QLabel('Flame spread:', self.manualTrackingBox)
    # directionBoxTxt.setGeometry(x1[0], y1[0], w1[0], h_txt)
    # self.directionBox = ft.QComboBox(self.manualTrackingBox)
    # self.directionBox.setGeometry(x1[1], y1[1], w1[1], h_btn)
    # self.directionBox.addItem('Left to right')
    # self.directionBox.addItem('Right to left')
    # # if self.pyqtVer == '5':
    # #     self.directionBox.activated[str].connect(self.directionMT_clicked)
    # # elif self.pyqtVer == '6':
    # #     self.directionBox.activated.connect(self.directionMT_clicked)
    # lightTxt = ft.QLabel('Flashing light (optional):', self.manualTrackingBox)
    # lightTxt.setGeometry(x1[2], y1[2], w1[2], h_txt)
    # self.lightROIBtn_MT = ft.QPushButton('Pick bright region', self.manualTrackingBox)
    # self.lightROIBtn_MT.setGeometry(x1[3], y1[3], w1[3], h_btn)
    # self.lightROIBtn_MT.clicked.connect(self.lightROIBtn_MT_clicked)
    # self.filterLight_MT = ft.QComboBox(self.manualTrackingBox)
    # self.filterLight_MT.setGeometry(x1[4], y1[4], w1[4], h_btn)
    # self.filterLight_MT.addItem('Track every frame')
    # self.filterLight_MT.addItem('Frames light on')
    # self.filterLight_MT.addItem('Frames light off')
    # # if self.pyqtVer == '5':
    # #     self.filterLight_MT.activated[str].connect(self.filterLight_MT_clicked)
    # # elif self.pyqtVer == '6':
    # #     self.filterLight_MT.activated.connect(self.filterLight_MT_clicked)
    # nClicksTxt = ft.QLabel('Tracking points #:', self.manualTrackingBox)
    # nClicksTxt.setGeometry(x1[5], y1[5], w1[5], h_txt)
    # self.nClicksLbl = ft.QLineEdit('1', self.manualTrackingBox)
    # self.nClicksLbl.setGeometry(x1[6], y1[6], w1[6], h_lbl)
    # self.showEdges_MT = ft.QCheckBox('Show tracking lines', self.manualTrackingBox)
    # self.showEdges_MT.setGeometry(x1[7], y1[7], w1[7], h_btn)
    # self.showEdges_MT.setChecked(True)
    # self.manualTrackingBtn = ft.QPushButton('Start tracking', self.manualTrackingBox)
    # self.manualTrackingBtn.setGeometry(x1[8], y1[8], w1[8], h_btn)
    # self.manualTrackingBtn.clicked.connect(self.manualTrackingBtn_clicked)
    # self.absValBtn = ft.QPushButton('Absolute values', self.manualTrackingBox)
    # self.absValBtn.setGeometry(x1[9], y1[9], w1[9], h_btn)
    # self.absValBtn.clicked.connect(self.absValBtn_MT_clicked)
    # self.saveBtn_MT = ft.QPushButton('Save data', self.manualTrackingBox)
    # self.saveBtn_MT.setGeometry(x1[10], y1[10], w1[10], h_btn)
    # self.saveBtn_MT.clicked.connect(self.saveBtn_MT_clicked)
    # self.updateGraphsBtn_MT = ft.QPushButton('Update graphs', self.manualTrackingBox)
    # self.updateGraphsBtn_MT.setGeometry(x1[11], y1[11], w1[11], h_btn)
    # self.updateGraphsBtn_MT.clicked.connect(self.updateGraphsBtn_MT_clicked)
    # self.helpBtn_MT = ft.QPushButton('Help', self.manualTrackingBox)
    # self.helpBtn_MT.setGeometry(x1[12], y1[12], w1[12], h_btn)
    # self.helpBtn_MT.clicked.connect(self.helpBtn_MT_clicked)
    #
    # #other objects
    # xAxisTxt_lbl1 = ft.QLabel('x axis:', self.manualTrackingBox)
    # xAxisTxt_lbl1.setGeometry(x2[0], y2[0], w2[0], h_txt)
    # self.xAxis_lbl1 = ft.QComboBox(self.manualTrackingBox)
    # self.xAxis_lbl1.setGeometry(x2[1], y2[1], w2[1], h_lbl)
    # self.xAxis_lbl1.addItem('Time [s]')
    # self.xAxis_lbl1.addItem('Frame #')
    # yAxisTxt_lbl1 = ft.QLabel('y axis:', self.manualTrackingBox)
    # yAxisTxt_lbl1.setGeometry(x2[2], y2[2], w2[2], h_txt)
    # self.yAxis_lbl1 = ft.QComboBox(self.manualTrackingBox)
    # self.yAxis_lbl1.setGeometry(x2[3], y2[3], w2[3], h_lbl)
    # self.yAxis_lbl1.addItem('Position [mm]')
    # self.yAxis_lbl1.addItem('Position [px]')
    # self.yAxis_lbl1.addItem('Spread rate [mm/s]')
    # xAxisTxt_lbl2 = ft.QLabel('x axis:', self.manualTrackingBox)
    # xAxisTxt_lbl2.setGeometry(x2[4], y2[4], w2[4], h_txt)
    # self.xAxis_lbl2 = ft.QComboBox(self.manualTrackingBox)
    # self.xAxis_lbl2.setGeometry(x2[5], y2[5], w2[5], h_lbl)
    # self.xAxis_lbl2.addItem('Time [s]')
    # self.xAxis_lbl2.addItem('Frame #')
    # yAxisTxt_lbl2 = ft.QLabel('y axis:', self.manualTrackingBox)
    # yAxisTxt_lbl2.setGeometry(x2[6], y2[6], w2[6], h_txt)
    # self.yAxis_lbl2 = ft.QComboBox(self.manualTrackingBox)
    # self.yAxis_lbl2.setGeometry(x2[7], y2[7], w2[7], h_lbl)
    # self.yAxis_lbl2.addItem('Spread rate [mm/s]')
    # self.yAxis_lbl2.addItem('Position [mm]')
    # self.yAxis_lbl2.addItem('Position [px]')
    #
    # # first label
    # self.lbl1_MT = ft.QLabel(self.manualTrackingBox)
    # self.lbl1_MT.setGeometry(lbl1[0], lbl1[1], lbl1[2], lbl1[3])
    # self.lbl1_MT.setStyleSheet('background-color: white')
    #
    # # second label
    # self.lbl2_MT = ft.pg.PlotWidget(self.manualTrackingBox)
    # self.lbl2_MT.setGeometry(lbl2[0], lbl2[1], lbl2[2], lbl2[3])
    # self.lbl2_MT.setBackground('w')
    # self.lbl2_MT.setLabel('left', 'Spread Rate [mm/s]', color='black', size=14)
    # self.lbl2_MT.setLabel('bottom', 'Time [s]', color='black', size=14)
    # self.lbl2_MT.getAxis('bottom').setPen(color=(0, 0, 0))
    # self.lbl2_MT.getAxis('left').setPen(color=(0, 0, 0))

def lumaTrackingBox(self):
    self.box_layout = ft.QGridLayout()

    # first column

    # self.lumaTrackingBox.setStyleSheet('background-color: None')

    #first column
    directionBoxTxt = ft.QLabel('Flame spread:')
    self.directionBox = ft.QComboBox()
    self.directionBox.addItem('Left to right')
    self.directionBox.addItem('Right to left')
    thresholdTxt = ft.QLabel('Luma threshold:')#, self.lumaTrackingBox)
    self.thresholdIn = ft.QLineEdit('30')#, self.lumaTrackingBox)
    filterParticleTxt = ft.QLabel('Filter particles:')#, self.lumaTrackingBox)
    self.particleSldrMax = ft.QLineEdit('1000')#, self.lumaTrackingBox)
    self.filterParticleSldr_LT = ft.QSlider(ft.Qt.Orientation.Horizontal)#, self.lumaTrackingBox)
    self.filterParticleSldr_LT.setMinimum(1)
    self.filterParticleSldr_LT.setMaximum(1000)
    self.filterParticleSldr_LT.setValue(10)
    self.filterParticleSldr_LT.sliderReleased.connect(self.filterParticleSldr_LT_released)
    avgLE_txt = ft.QLabel('#px to locate edges:')#, self.lumaTrackingBox)
    self.avgLEIn_LT = ft.QLineEdit('5')#, self.lumaTrackingBox)
    trackingTxt = ft.QLabel('Flame tracking:')#, self.lumaTrackingBox)
    self.lightROIBtn_LT = ft.QPushButton('Pick bright region')#, self.lumaTrackingBox)
    self.lightROIBtn_LT.clicked.connect(self.lightROIBtn_LT_clicked)
    self.filterLight = ft.QCheckBox('Ignore flashing light')#, self.lumaTrackingBox)
    movAvgTxt = ft.QLabel('Moving avg pts:')#, self.lumaTrackingBox)
    self.movAvgIn_LT = ft.QLineEdit('2')#, self.lumaTrackingBox)
    self.lumaTrackingBtn = ft.QPushButton('Start tracking')#, self.lumaTrackingBox)
    self.lumaTrackingBtn.clicked.connect(self.lumaTrackingBtn_clicked)
    self.absValBtn = ft.QPushButton('Absolute values')#, self.lumaTrackingBox)
    self.absValBtn.clicked.connect(self.absValBtn_LT_clicked)
    self.saveBtn_LT = ft.QPushButton('Save data')#, self.lumaTrackingBox)
    self.saveBtn_LT.clicked.connect(self.saveDataBtn_LT_clicked)
    self.showFrameLargeBtn_LT = ft.QPushButton('Show frames')#, self.lumaTrackingBox)
    self.showFrameLargeBtn_LT.clicked.connect(self.showFrameLargeBtn_LT_clicked)
    self.updateGraphsBtn_LT = ft.QPushButton('Update graphs')#, self.lumaTrackingBox)
    self.updateGraphsBtn_LT.clicked.connect(self.updateGraphsBtn_LT_clicked)

    self.box_layout.addWidget(directionBoxTxt, 0, 0, 1, 1)
    self.box_layout.addWidget(self.directionBox, 0, 1, 1, 1)
    self.box_layout.addWidget(thresholdTxt, 1, 0, 1, 1)
    self.box_layout.addWidget(self.thresholdIn, 1, 1, 1, 1)
    self.box_layout.addWidget(filterParticleTxt, 2, 0, 1, 1)
    self.box_layout.addWidget(self.particleSldrMax, 2, 1, 1, 1)
    self.box_layout.addWidget(self.filterParticleSldr_LT, 3, 0, 1, 2)
    self.box_layout.addWidget(avgLE_txt, 4, 0, 1, 1)
    self.box_layout.addWidget(self.avgLEIn_LT, 4, 1, 1, 1)
    self.box_layout.addWidget(self.lumaTrackingBtn, 5, 0, 1, 2)
    self.box_layout.addWidget(self.absValBtn, 6, 0, 1, 2)
    self.box_layout.addWidget(self.saveBtn_LT, 7, 0, 1, 2)
    self.box_layout.addWidget(self.showFrameLargeBtn_LT, 8, 0, 1, 2)
    self.box_layout.addWidget(self.updateGraphsBtn_LT, 9, 0, 1, 2)

    # below is defined in flameTracker.py already in an OS specific way (line 973 in "lumaTrackingValue" condition)
    # first label
    self.lbl1_LT = ft.QLabel()
    self.lbl1_LT.setStyleSheet('background-color: white')

    # second label
    self.lbl2_LT = ft.QLabel()
    self.lbl2_LT.setStyleSheet('background-color: white')

    # #other objects
    xAxisTxt_lbl1 = ft.QLabel('x axis:')
    self.xAxis_lbl1 = ft.QComboBox()
    self.xAxis_lbl1.addItem('Time [s]')
    self.xAxis_lbl1.addItem('Frame #')
    yAxisTxt_lbl1 = ft.QLabel('y axis:')
    self.yAxis_lbl1 = ft.QComboBox()
    self.yAxis_lbl1.addItem('Position [mm]')
    self.yAxis_lbl1.addItem('Position [px]')
    self.yAxis_lbl1.addItem('Flame length [mm]')
    self.yAxis_lbl1.addItem('Spread rate [mm/s]')
    xAxisTxt_lbl2 = ft.QLabel('x axis:')
    self.xAxis_lbl2 = ft.QComboBox()
    self.xAxis_lbl2.addItem('Time [s]')
    self.xAxis_lbl2.addItem('Frame #')
    yAxisTxt_lbl2 = ft.QLabel('y axis:')
    self.yAxis_lbl2 = ft.QComboBox()
    self.yAxis_lbl2.addItem('Spread rate [mm/s]')
    self.yAxis_lbl2.addItem('Flame length [mm]')
    self.yAxis_lbl2.addItem('Position [mm]')
    self.yAxis_lbl2.addItem('Position [px]')

    self.box_layout.addWidget(self.lbl1_LT, 0, 3, 8, 4)
    self.box_layout.addWidget(self.lbl2_LT, 0, 8, 8, 4)
    self.box_layout.addWidget(xAxisTxt_lbl1, 8, 5, 1, 1)
    self.box_layout.addWidget(self.xAxis_lbl1, 8, 6, 1, 1)
    self.box_layout.addWidget(yAxisTxt_lbl1, 9, 5, 1, 1)
    self.box_layout.addWidget(self.yAxis_lbl1, 9, 6, 1, 1)
    self.box_layout.addWidget(xAxisTxt_lbl2, 8, 10, 1, 1)
    self.box_layout.addWidget(self.xAxis_lbl2, 8, 11, 1, 1)
    self.box_layout.addWidget(yAxisTxt_lbl2, 9, 10, 1, 1)
    self.box_layout.addWidget(self.yAxis_lbl2, 9, 11, 1, 1)

    self.showEdges_LT = ft.QAction('Show edge lines', self)
    self.showEdges_LT.setCheckable(True)
    self.showEdges_LT.setChecked(True)
    self.exportEdges_LT = ft.QAction('Output video analysis', self)
    self.exportEdges_LT.setCheckable(True)


    self.LTmenu = self.menu.addMenu("&LumaTracking settings")
    self.LTmenu.addAction(self.showEdges_LT)
    self.LTmenu.addAction(self.exportEdges_LT)

    # self.box_layout.setColumnMinimumWidth(0, 80)
    self.box_layout.setColumnMinimumWidth(1, 40)
    # box_layout.setColumnMinimumWidth(2, 10)
    self.box_layout.setColumnMinimumWidth(3, 50)
    self.box_layout.setColumnMinimumWidth(4, 40)
    # box_layout.setColumnMinimumWidth(5, 50)
    # box_layout.setColumnMinimumWidth(6, 100)
    # box_layout.setColumnMinimumWidth(7, 10)
    self.box_layout.setColumnMinimumWidth(8, 80)
    # box_layout.setColumnMinimumWidth(9, 50)
    # box_layout.setColumnMinimumWidth(10, 50)
    # box_layout.setColumnMinimumWidth(11, 100)
    # box_layout.setColumnMinimumWidth(12, 50)



    #
    self.analysisGroupBox.setLayout(self.box_layout)

    # if ft.sys.platform == 'darwin':
    #     self.lumaTrackingBox = ft.QGroupBox(' ', self.analysisGroupBox)
    #     self.lumaTrackingBox.setGeometry(0, 0, 1050, 390)
    #
    #     # size of GUI labels:
    #     h_lbl = 22
    #     h_txt = 30
    #     h_btn = 30
    #     h_slider = 25
    #
    #     if self.pyqtVer == '5': #PyQt5 GUI will be removed after FlameTrackerv1.1.8
    #          # first column
    #         # x1 = [ 10,   5,  10, 120,  10, 105,   5,  10, 120,  10,   5,  10,  10, 120,   5,   5,   5,   5]
    #         # y1 = [ 20,  45,  75,  79, 100, 103, 128, 150, 154, 175, 195, 220, 245, 249, 270, 300, 330, 360]
    #         # w1 = [100, 150, 100,  30, 150,  45, 140, 140,  30, 120, 150, 140, 100,  30, 150, 150, 150, 150]
    #         x1 = [10,  85,  10, 120,  10, 110,   5,  10, 120,  10,  10,  10,  10, 120,  10,  10,  10,  10,  10]
    #         y1 = [20,  25,  45,  49,  70,  74, 100, 125, 129, 150, 175, 200, 225, 229, 250, 275, 300, 325, 350]
    #         w1 = [80, 105, 100,  40, 150,  50, 155, 140,  40, 120, 150, 140, 100,  40, 150, 150, 150, 150, 150]
    #     elif self.pyqtVer == '6':
    #         # first column
    #         # x1 = [ 10,   5,  10, 120,  10, 105,   5,  10, 120,  10,  10,  10,  10, 120,  10,  10,  10,  10]
    #         # y1 = [ 20,  45,  75,  79, 100, 103, 128, 150, 154, 175, 195, 220, 245, 249, 270, 295, 320, 345]
    #         # w1 = [100, 150, 100,  30, 150,  45, 140, 140,  30, 120, 140, 140, 100,  30, 140, 140, 140, 140]
    #         x1 = [10,  85,  10, 130,  10, 130,   5,  10, 130,  10,  20,  10,  10, 130,  20,  20,  20,  20,  20]
    #         y1 = [20,  25,  45,  49,  70,  74, 100, 125, 129, 150, 175, 200, 225, 229, 250, 275, 300, 325, 350]
    #         w1 = [80, 105, 100,  50, 150,  50, 155, 140,  50, 120, 150, 140, 100,  50, 150, 150, 150, 150, 150]
    #
    #     # other objects
    #     # x2 = [780, 780, 930]
    #     # y2 = [325, 350, 325]
    #     # w2 = [135, 135, 115]
    #     x2 = [250, 250, 250, 460, 500, 460, 500, 850, 890, 850, 890]
    #     y2 = [300, 325, 350, 300, 302, 330, 332, 300, 302, 330, 332]
    #     w2 = [135, 135, 115,  80, 150,  80, 150,  80, 150,  80, 150]
    #     # labels (since there's only two, in this case I wrote the entire set of coord.)
    #     # lbl1 = [190, 25, 420, 300]
    #     lbl1 = [250, 25, 390, 270]
    #     # lbl2 = [620, 25, 420, 300]
    #     lbl2 = [650, 25, 390, 270]
    #
    # elif ft.sys.platform == 'win32':
    #     self.lumaTrackingBox = ft.QGroupBox('Analysis box', self.analysisGroupBox)
    #     self.lumaTrackingBox.setGeometry(0,0, 1050, 370)
    #
    #     # size of GUI labels:
    #     h_lbl = 20
    #     h_txt = 25
    #     h_btn = 20
    #     h_slider = 15
    #
    #     # first column
    #     # x1 = [ 10,  10,  10, 115,  10, 105,  10,  10, 115,  10,  10,  10,  10, 115,  10,  10,  10, 190]
    #     # y1 = [ 15,  40,  70,  75,  95, 103, 125, 140, 145, 165, 190, 215, 240, 245, 275, 305, 335, 335]
    #     # w1 = [140, 140,  80,  35, 150,  45, 135, 140,  35, 120, 140, 140, 100,  35, 140, 140, 140, 140]
    #     x1 = [10, 100,  10, 130,  10, 130,  10,  10, 130,  10,  20,  10,  10, 130,  20,  20,  20,  20,  20]
    #     y1 = [15,  17,  45,  47,  70,  72, 100, 120, 122, 145, 170, 195, 220, 222, 245, 270, 295, 320, 345]
    #     w1 = [90, 100, 100,  50, 150,  50, 170, 140,  50, 120, 150, 140, 100,  50, 150, 150, 150, 150, 150]
    #
    #
    #     # other objects
    #     # x2 = [750, 750, 920]
    #     # y2 = [320, 340, 325]
    #     # w2 = [140, 140, 120]
    #     x2 = [250, 250, 250, 460, 500, 460, 500, 850, 890, 850, 890]
    #     y2 = [290, 315, 340, 290, 292, 320, 322, 290, 292, 320, 322]
    #     w2 = [150, 150, 115,  80, 150,  80, 150,  80, 150,  80, 150]
    #     # labels (since there's only two, in this case I wrote the entire set of coord.)
    #     # lbl1 = [190, 15, 420, 300]
    #     # lbl2 = [620, 15, 420, 300]
    #     lbl1 = [250, 15, 390, 270]
    #     lbl2 = [650, 15, 390, 270]
    #
    # elif ft.sys.platform == 'linux':
    #     self.lumaTrackingBox = ft.QGroupBox(' ', self.analysisGroupBox)
    #     self.lumaTrackingBox.setGeometry(0, 0, 1050, 390)
    #
    #     # size of GUI labels:
    #     h_lbl = 22
    #     h_txt = 30
    #     h_btn = 30
    #     h_slider = 25
    #
    #     # first column
    #     # x1 = [ 10,   5,  10, 120,  10, 105,   5,  10, 120,  10,   5,  10,  10, 120,   5,   5,   5,   5]
    #     # y1 = [ 20,  45,  75,  79, 100, 103, 128, 150, 154, 175, 195, 220, 245, 249, 270, 300, 330, 360]
    #     # w1 = [100, 150, 100,  30, 150,  45, 140, 140,  30, 120, 150, 140, 100,  30, 150, 150, 150, 150]
    #     x1 = [10,  55,  10, 120,  10, 110,   5,  10, 120,  10,  10,  10,  10, 120,  10,  10,  10,  10,  10]
    #     y1 = [20,  20,  45,  49,  70,  74, 100, 125, 129, 150, 175, 200, 225, 229, 250, 275, 300, 325, 350]
    #     w1 = [80, 110, 100,  40, 150,  50, 155, 140,  40, 120, 150, 140, 100,  40, 150, 150, 150, 150, 150]
    #
    #     # other objects
    #     # x2 = [780, 780, 930]
    #     # y2 = [325, 350, 325]
    #     # w2 = [135, 135, 115]
    #     x2 = [250, 250, 250, 460, 500, 460, 500, 850, 890, 850, 890]
    #     y2 = [300, 325, 350, 300, 302, 330, 332, 300, 302, 330, 332]
    #     w2 = [135, 135, 115,  80, 150,  80, 150,  80, 150,  80, 150]
    #     # labels (since there's only two, in this case I wrote the entire set of coord.)
    #     # lbl1 = [190, 25, 420, 300]
    #     # lbl2 = [620, 25, 420, 300]
    #     lbl1 = [250, 25, 390, 270]
    #     lbl2 = [650, 25, 390, 270]

    # self.lumaTrackingBox.setStyleSheet('background-color: None')
    #
    # #first column
    # directionBoxTxt = ft.QLabel('Flame spread:', self.lumaTrackingBox)
    # directionBoxTxt.setGeometry(x1[0], y1[0], w1[0], h_txt)
    # self.directionBox = ft.QComboBox(self.lumaTrackingBox)
    # self.directionBox.setGeometry(x1[1], y1[1], w1[1], h_lbl)
    # self.directionBox.addItem('Left to right')
    # self.directionBox.addItem('Right to left')
    # # if self.pyqtVer == '5':
    # #     self.directionBox.activated[str].connect(self.directionLT_clicked)
    # # elif self.pyqtVer == '6':
    # #     self.directionBox.activated.connect(self.directionLT_clicked)
    # thresholdTxt = ft.QLabel('Luma threshold:', self.lumaTrackingBox)
    # thresholdTxt.setGeometry(x1[2], y1[2], w1[2], h_txt)
    # self.thresholdIn = ft.QLineEdit('30', self.lumaTrackingBox)
    # self.thresholdIn.setGeometry(x1[3], y1[3], w1[3], h_lbl)
    # filterParticleTxt = ft.QLabel('Filter particles:', self.lumaTrackingBox)
    # filterParticleTxt.setGeometry(x1[4], y1[4], w1[4], h_txt)
    # self.particleSldrMax = ft.QLineEdit('1000', self.lumaTrackingBox)
    # self.particleSldrMax.setGeometry(x1[5], y1[5], w1[5], h_lbl)
    # if self.pyqtVer == '5':
    #     self.filterParticleSldr_LT = ft.QSlider(ft.Qt.Horizontal, self.lumaTrackingBox)
    # elif self.pyqtVer == '6':
    #     self.filterParticleSldr_LT = ft.QSlider(ft.Qt.Orientation.Horizontal, self.lumaTrackingBox)
    # self.filterParticleSldr_LT.setGeometry(x1[6], y1[6], w1[6], h_slider)
    # self.filterParticleSldr_LT.setMinimum(1)
    # self.filterParticleSldr_LT.setMaximum(1000)
    # self.filterParticleSldr_LT.setValue(10)
    # self.filterParticleSldr_LT.sliderReleased.connect(self.filterParticleSldr_LT_released)
    # avgLE_txt = ft.QLabel('#px to locate edges:', self.lumaTrackingBox)
    # avgLE_txt.setGeometry(x1[7], y1[7], w1[7], h_txt)
    # self.avgLEIn_LT = ft.QLineEdit('5', self.lumaTrackingBox)
    # self.avgLEIn_LT.setGeometry(x1[8], y1[8], w1[8], h_lbl)
    # trackingTxt = ft.QLabel('Flame tracking:', self.lumaTrackingBox)
    # trackingTxt.setGeometry(x1[9], y1[9], w1[9], h_txt)
    # self.lightROIBtn_LT = ft.QPushButton('Pick bright region', self.lumaTrackingBox)
    # self.lightROIBtn_LT.setGeometry(x1[10], y1[10], w1[10], h_btn)
    # self.lightROIBtn_LT.clicked.connect(self.lightROIBtn_LT_clicked)
    # self.filterLight = ft.QCheckBox('Ignore flashing light', self.lumaTrackingBox)
    # self.filterLight.setGeometry(x1[11], y1[11], w1[11], h_btn)
    # movAvgTxt = ft.QLabel('Moving avg points:', self.lumaTrackingBox)
    # movAvgTxt.setGeometry(x1[12], y1[12], w1[12], h_txt)
    # self.movAvgIn_LT = ft.QLineEdit('2', self.lumaTrackingBox)
    # self.movAvgIn_LT.setGeometry(x1[13], y1[13], w1[13], h_lbl)
    # self.lumaTrackingBtn = ft.QPushButton('Start tracking', self.lumaTrackingBox)
    # self.lumaTrackingBtn.setGeometry(x1[14], y1[14], w1[14], h_btn)
    # self.lumaTrackingBtn.clicked.connect(self.lumaTrackingBtn_clicked)
    # self.absValBtn = ft.QPushButton('Absolute values', self.lumaTrackingBox)
    # self.absValBtn.setGeometry(x1[15], y1[15], w1[15], h_btn)
    # self.absValBtn.clicked.connect(self.absValBtn_LT_clicked)
    # self.saveBtn_LT = ft.QPushButton('Save data', self.lumaTrackingBox)
    # self.saveBtn_LT.setGeometry(x1[16], y1[16], w1[16], h_btn)
    # self.saveBtn_LT.clicked.connect(self.saveDataBtn_LT_clicked)
    # self.showFrameLargeBtn_LT = ft.QPushButton('Show frames', self.lumaTrackingBox)
    # self.showFrameLargeBtn_LT.setGeometry(x1[17], y1[17], w1[17], h_btn)
    # self.showFrameLargeBtn_LT.clicked.connect(self.showFrameLargeBtn_LT_clicked)
    # self.updateGraphsBtn_LT = ft.QPushButton('Update graphs', self.lumaTrackingBox)
    # self.updateGraphsBtn_LT.setGeometry(x1[18], y1[18], w1[18], h_btn)
    # self.updateGraphsBtn_LT.clicked.connect(self.updateGraphsBtn_LT_clicked)
    #
    # #other objects
    # self.showEdges = ft.QCheckBox('Show edges location', self.lumaTrackingBox)
    # self.showEdges.setGeometry(x2[0], y2[0], w2[0], h_btn)
    # self.showEdges.setChecked(True)
    # self.exportEdges_LT = ft.QCheckBox('Output video analysis', self.lumaTrackingBox)
    # self.exportEdges_LT.setGeometry(x2[1], y2[1], w2[1], h_btn)
    # self.helpBtn_LT = ft.QPushButton('Help', self.lumaTrackingBox)
    # self.helpBtn_LT.setGeometry(x2[2], y2[2], w2[2], h_btn)
    # self.helpBtn_LT.clicked.connect(self.helpBtn_LT_clicked)
    # xAxisTxt_lbl1 = ft.QLabel('x axis:', self.lumaTrackingBox)
    # xAxisTxt_lbl1.setGeometry(x2[3], y2[3], w2[3], h_txt)
    # self.xAxis_lbl1 = ft.QComboBox(self.lumaTrackingBox)
    # self.xAxis_lbl1.setGeometry(x2[4], y2[4], w2[4], h_lbl)
    # self.xAxis_lbl1.addItem('Time [s]')
    # self.xAxis_lbl1.addItem('Frame #')
    # yAxisTxt_lbl1 = ft.QLabel('y axis:', self.lumaTrackingBox)
    # yAxisTxt_lbl1.setGeometry(x2[5], y2[5], w2[5], h_txt)
    # self.yAxis_lbl1 = ft.QComboBox(self.lumaTrackingBox)
    # self.yAxis_lbl1.setGeometry(x2[6], y2[6], w2[6], h_lbl)
    # self.yAxis_lbl1.addItem('Position [mm]')
    # self.yAxis_lbl1.addItem('Position [px]')
    # self.yAxis_lbl1.addItem('Flame length [mm]')
    # self.yAxis_lbl1.addItem('Spread rate [mm/s]')
    # xAxisTxt_lbl2 = ft.QLabel('x axis:', self.lumaTrackingBox)
    # xAxisTxt_lbl2.setGeometry(x2[7], y2[7], w2[7], h_txt)
    # self.xAxis_lbl2 = ft.QComboBox(self.lumaTrackingBox)
    # self.xAxis_lbl2.setGeometry(x2[8], y2[8], w2[8], h_lbl)
    # self.xAxis_lbl2.addItem('Time [s]')
    # self.xAxis_lbl2.addItem('Frame #')
    # yAxisTxt_lbl2 = ft.QLabel('y axis:', self.lumaTrackingBox)
    # yAxisTxt_lbl2.setGeometry(x2[9], y2[9], w2[9], h_txt)
    # self.yAxis_lbl2 = ft.QComboBox(self.lumaTrackingBox)
    # self.yAxis_lbl2.setGeometry(x2[10], y2[10], w2[10], h_lbl)
    # self.yAxis_lbl2.addItem('Spread rate [mm/s]')
    # self.yAxis_lbl2.addItem('Flame length [mm]')
    # self.yAxis_lbl2.addItem('Position [mm]')
    # self.yAxis_lbl2.addItem('Position [px]')
    #
    # # below is defined in flameTracker.py already in an OS specific way (line 973 in "lumaTrackingValue" condition)
    # # first label
    # self.lbl1_LT = ft.QLabel(self.lumaTrackingBox)
    # self.lbl1_LT.setGeometry(lbl1[0], lbl1[1], lbl1[2], lbl1[3])
    # self.lbl1_LT.setStyleSheet('background-color: white')
    #
    # # second label
    # self.lbl2_LT = ft.QLabel(self.lumaTrackingBox)
    # self.lbl2_LT.setGeometry(lbl2[0], lbl2[1], lbl2[2], lbl2[3])
    # self.lbl2_LT.setStyleSheet('background-color: white')

def colorTrackingBox(self):
    self.box_layout = ft.QGridLayout()
    self.box_layout.setSpacing(10)

    # #first column
    directionBoxTxt = ft.QLabel('Flame spread:')
    self.directionBox = ft.QComboBox()
    self.directionBox.addItem('Left to right')
    self.directionBox.addItem('Right to left')

    redChannelTxt = ft.QLabel('Red channel:')
    redMinTxt = ft.QLabel('Min:')
    self.redMinLeftBtn_RT = ft.QPushButton('<')
    self.redMinLeftBtn_RT.clicked.connect(self.redMinLeftBtn_RT_clicked)
    self.redMinRightBtn_RT = ft.QPushButton('>')
    self.redMinRightBtn_RT.clicked.connect(self.redMinRightBtn_RT_clicked)
    self.redMinSlider = ft.QSlider(ft.Qt.Orientation.Horizontal)
    self.redMinSlider.setMinimum(0)
    self.redMinSlider.setMaximum(255)
    self.redMinSlider.setValue(10)
    self.redMinSlider.sliderReleased.connect(self.singleColorSlider_released)
    redMaxTxt = ft.QLabel('Max:')
    self.redMaxLeftBtn_RT = ft.QPushButton('<')
    self.redMaxLeftBtn_RT.clicked.connect(self.redMaxLeftBtn_RT_clicked)
    self.redMaxRightBtn_RT = ft.QPushButton('>')
    self.redMaxRightBtn_RT.clicked.connect(self.redMaxRightBtn_RT_clicked)
    self.redMaxSlider = ft.QSlider(ft.Qt.Orientation.Horizontal)
    self.redMaxSlider.setMinimum(0)
    self.redMaxSlider.setMaximum(255)
    self.redMaxSlider.setValue(255)
    self.redMaxSlider.sliderReleased.connect(self.singleColorSlider_released)
    greenChannelTxt = ft.QLabel('Green channel:')
    greenMinTxt = ft.QLabel('Min:')
    self.greenMinLeftBtn_RT = ft.QPushButton('<')
    self.greenMinLeftBtn_RT.clicked.connect(self.greenMinLeftBtn_RT_clicked)
    self.greenMinRightBtn_RT = ft.QPushButton('>')
    self.greenMinRightBtn_RT.clicked.connect(self.greenMinRightBtn_RT_clicked)
    self.greenMinSlider = ft.QSlider(ft.Qt.Orientation.Horizontal)
    self.greenMinSlider.setMinimum(0)
    self.greenMinSlider.setMaximum(255)
    self.greenMinSlider.setValue(10)
    self.greenMinSlider.sliderReleased.connect(self.singleColorSlider_released)
    greenMaxTxt = ft.QLabel('Max:')
    self.greenMaxLeftBtn_RT = ft.QPushButton('<')
    self.greenMaxLeftBtn_RT.clicked.connect(self.greenMaxLeftBtn_RT_clicked)
    self.greenMaxRightBtn_RT = ft.QPushButton('>')
    self.greenMaxRightBtn_RT.clicked.connect(self.greenMaxRightBtn_RT_clicked)
    self.greenMaxSlider = ft.QSlider(ft.Qt.Orientation.Horizontal)
    self.greenMaxSlider.setMinimum(0)
    self.greenMaxSlider.setMaximum(255)
    self.greenMaxSlider.setValue(255)
    self.greenMaxSlider.sliderReleased.connect(self.singleColorSlider_released)
    blueChannelTxt = ft.QLabel('Blue channel:')
    blueMinTxt = ft.QLabel('Min:')
    self.blueMinLeftBtn_RT = ft.QPushButton('<')
    self.blueMinLeftBtn_RT.clicked.connect(self.blueMinLeftBtn_RT_clicked)
    self.blueMinRightBtn_RT = ft.QPushButton('>')
    self.blueMinRightBtn_RT.clicked.connect(self.blueMinRightBtn_RT_clicked)
    self.blueMinSlider = ft.QSlider(ft.Qt.Orientation.Horizontal)
    self.blueMinSlider.setMinimum(0)
    self.blueMinSlider.setMaximum(255)
    self.blueMinSlider.sliderReleased.connect(self.singleColorSlider_released)
    blueMaxTxt = ft.QLabel('Max:')
    self.blueMaxLeftBtn_RT = ft.QPushButton('<')
    self.blueMaxLeftBtn_RT.clicked.connect(self.blueMaxLeftBtn_RT_clicked)
    self.blueMaxRightBtn_RT = ft.QPushButton('>')
    self.blueMaxRightBtn_RT.clicked.connect(self.blueMaxRightBtn_RT_clicked)
    self.blueMaxSlider = ft.QSlider(ft.Qt.Orientation.Horizontal)
    self.blueMaxSlider.setMinimum(0)
    self.blueMaxSlider.setMaximum(255)
    self.blueMaxSlider.setValue(255)
    self.blueMaxSlider.sliderReleased.connect(self.singleColorSlider_released)

    filterParticleTxt = ft.QLabel('Filter particles (px):')
    self.particleSldrMax = ft.QLineEdit('1000')
    self.filterParticleSldr_RT = ft.QSlider(ft.Qt.Orientation.Horizontal)
    self.filterParticleSldr_RT.setMinimum(1)
    self.filterParticleSldr_RT.setMaximum(1000)
    self.filterParticleSldr_RT.setValue(10)
    self.filterParticleSldr_RT.sliderReleased.connect(self.filterParticleSldr_RT_released)

    self.box_layout.addWidget(directionBoxTxt, 0, 0, 1, 3)
    self.box_layout.addWidget(self.directionBox, 0, 3, 1, 1)
    self.box_layout.addWidget(redChannelTxt, 1, 0, 1, 3)
    self.box_layout.addWidget(redMinTxt, 2, 0, 1, 1)
    self.box_layout.addWidget(self.redMinLeftBtn_RT, 2, 1, 1, 1)
    self.box_layout.addWidget(self.redMinRightBtn_RT, 2, 4, 1, 1)
    self.box_layout.addWidget(self.redMinSlider, 2, 2, 1, 2)
    self.box_layout.addWidget(redMaxTxt, 3, 0, 1, 1)
    self.box_layout.addWidget(self.redMaxLeftBtn_RT, 3, 1, 1, 1)
    self.box_layout.addWidget(self.redMaxRightBtn_RT, 3, 4, 1, 1)
    self.box_layout.addWidget(self.redMaxSlider, 3, 2, 1, 2)
    self.box_layout.addWidget(greenChannelTxt, 4, 0, 1, 3)
    self.box_layout.addWidget(greenMinTxt, 5, 0, 1, 1)
    self.box_layout.addWidget(self.greenMinLeftBtn_RT, 5, 1, 1, 1)
    self.box_layout.addWidget(self.greenMinRightBtn_RT, 5, 4, 1, 1)
    self.box_layout.addWidget(self.greenMinSlider, 5, 2, 1, 2)
    self.box_layout.addWidget(greenMaxTxt, 6, 0, 1, 1)
    self.box_layout.addWidget(self.greenMaxLeftBtn_RT, 6, 1, 1, 1)
    self.box_layout.addWidget(self.greenMaxRightBtn_RT, 6, 4, 1, 1)
    self.box_layout.addWidget(self.greenMaxSlider, 6, 2, 1, 2)
    self.box_layout.addWidget(blueChannelTxt, 7, 0, 1, 3)
    self.box_layout.addWidget(blueMinTxt, 8, 0, 1, 1)
    self.box_layout.addWidget(self.blueMinLeftBtn_RT, 8, 1, 1, 1)
    self.box_layout.addWidget(self.blueMinRightBtn_RT, 8, 4, 1, 1)
    self.box_layout.addWidget(self.blueMinSlider, 8, 2, 1, 2)
    self.box_layout.addWidget(blueMaxTxt, 9, 0, 1, 1)
    self.box_layout.addWidget(self.blueMaxLeftBtn_RT, 9, 1, 1, 1)
    self.box_layout.addWidget(self.blueMaxRightBtn_RT, 9, 4, 1, 1)
    self.box_layout.addWidget(self.blueMaxSlider, 9, 2, 1, 2)
    self.box_layout.addWidget(filterParticleTxt, 10, 0, 1, 3)
    self.box_layout.addWidget(self.particleSldrMax, 10, 3, 1, 1)
    self.box_layout.addWidget(self.filterParticleSldr_RT, 11, 2, 1, 2)



    #second column
    trackingTxt = ft.QLabel('Flame tracking:')
    avgLE_txt = ft.QLabel('Pts to locate edges:')
    self.avgLEIn_RT = ft.QLineEdit('1')
    movAvgTxt = ft.QLabel('Moving avg pts:')
    self.movAvgIn_RT = ft.QLineEdit('2')
    self.colorTrackingBtn = ft.QPushButton('Start tracking')
    self.colorTrackingBtn.clicked.connect(self.colorTrackingBtn_clicked)
    self.saveBtn_RT = ft.QPushButton('Save data')
    self.saveBtn_RT.clicked.connect(self.saveBtn_RT_clicked)
    self.saveChannelsBtn_RT = ft.QPushButton('Save RGB values')
    self.saveChannelsBtn_RT.clicked.connect(self.saveChannelsBtn_RT_clicked)
    self.loadChannelsBtn_RT = ft.QPushButton('Load RGB values')
    self.loadChannelsBtn_RT.clicked.connect(self.loadChannelsBtn_RT_clicked)
    self.updateGraphsBtn_RT = ft.QPushButton('Update graphs')
    self.updateGraphsBtn_RT.clicked.connect(self.updateGraphsBtn_RT_clicked)

    self.box_layout.addWidget(trackingTxt, 0, 5, 1, 1)
    self.box_layout.addWidget(avgLE_txt, 1, 5, 1, 1)
    self.box_layout.addWidget(self.avgLEIn_RT, 1, 6, 1, 1)
    self.box_layout.addWidget(movAvgTxt, 2, 5, 1, 2)
    self.box_layout.addWidget(self.movAvgIn_RT, 2, 6, 1, 1)
    self.box_layout.addWidget(self.colorTrackingBtn, 3, 5, 1, 2)
    self.box_layout.addWidget(self.saveBtn_RT, 4, 5, 1, 2)
    self.box_layout.addWidget(self.saveChannelsBtn_RT, 5, 5, 1, 2)
    self.box_layout.addWidget(self.loadChannelsBtn_RT, 6, 5, 1, 2)
    self.box_layout.addWidget(self.updateGraphsBtn_RT, 7, 5, 1, 2)

    # first label
    self.lbl1_RT = ft.QLabel()
    self.lbl1_RT.setStyleSheet('background-color: white')

    # second label
    self.lbl2_RT = ft.QLabel()
    self.lbl2_RT.setStyleSheet('background-color: white')

    # other objects
    txt_lbl1 = ft.QLabel('Graph #1:')
    xAxisTxt_lbl1 = ft.QLabel('x axis:')
    self.xAxis_lbl1 = ft.QComboBox()
    self.xAxis_lbl1.addItem('Time [s]')
    self.xAxis_lbl1.addItem('Frame #')
    yAxisTxt_lbl1 = ft.QLabel('y axis:')
    self.yAxis_lbl1 = ft.QComboBox()
    self.yAxis_lbl1.addItem('Position [mm]')
    self.yAxis_lbl1.addItem('Position [px]')
    self.yAxis_lbl1.addItem('Flame length [mm]')
    self.yAxis_lbl1.addItem('Spread rate [mm/s]')
    txt_lbl2 = ft.QLabel('Graph #2:')
    xAxisTxt_lbl2 = ft.QLabel('x axis:')
    self.xAxis_lbl2 = ft.QComboBox()
    self.xAxis_lbl2.addItem('Time [s]')
    self.xAxis_lbl2.addItem('Frame #')
    yAxisTxt_lbl2 = ft.QLabel('y axis:')
    self.yAxis_lbl2 = ft.QComboBox()
    self.yAxis_lbl2.addItem('Spread rate [mm/s]')
    self.yAxis_lbl2.addItem('Flame length [mm]')
    self.yAxis_lbl2.addItem('Position [mm]')
    self.yAxis_lbl2.addItem('Position [px]')

    self.box_layout.addWidget(self.lbl1_RT, 0, 9, 8, 3)
    self.box_layout.addWidget(self.lbl2_RT, 0, 12, 8, 3)
    self.box_layout.addWidget(xAxisTxt_lbl1, 8, 10, 1, 1)
    self.box_layout.addWidget(self.xAxis_lbl1, 8, 11, 1, 1)
    self.box_layout.addWidget(yAxisTxt_lbl1, 9, 10, 1, 1)
    self.box_layout.addWidget(self.yAxis_lbl1, 9, 11, 1, 1)
    self.box_layout.addWidget(xAxisTxt_lbl2, 8, 13, 1, 1)
    self.box_layout.addWidget(self.xAxis_lbl2, 8, 14, 1, 1)
    self.box_layout.addWidget(yAxisTxt_lbl2, 9, 13, 1, 1)
    self.box_layout.addWidget(self.yAxis_lbl2, 9, 14, 1, 1)

    # self.box_layout.setColumnMinimumWidth(0, 10)
    self.box_layout.setColumnMinimumWidth(1, 10)
    # self.box_layout.setColumnMinimumWidth(2, 60)
    # self.box_layout.setColumnMinimumWidth(3, 10)
    self.box_layout.setColumnMinimumWidth(4, 10)
    # box_layout.setColumnMinimumWidth(5, 50)
    self.box_layout.setColumnMinimumWidth(6, 40)
    # box_layout.setColumnMinimumWidth(7, 10)
    # box_layout.setColumnMinimumWidth(8, 50)
    self.box_layout.setColumnMinimumWidth(9, 50)
    # box_layout.setColumnMinimumWidth(10, 50)
    # box_layout.setColumnMinimumWidth(11, 100)
    self.box_layout.setColumnMinimumWidth(12, 50)
    self.analysisGroupBox.setLayout(self.box_layout)

    # create menu on the menubar
    connectivity0 = ft.QAction('4', self, checkable=True, checked=True)
    connectivity1 = ft.QAction('8', self, checkable=True, checked=False)
    showFrameLargeBtn_RT = ft.QAction('Show filtered frame', self)
    showFrameLargeBtn_RT.triggered.connect(self.showFrameLargeBtn_RT_clicked)
    self.filterLight_RT = ft.QAction('Ignore flashing light', self)
    self.filterLight_RT.setCheckable(True)
    self.lightROIBtn_RT = ft.QAction('Pick bright region', self)
    self.lightROIBtn_RT.triggered.connect(self.lightROIBtn_RT_clicked)
    self.absValBtn_RT = ft.QAction('Absolute values', self)
    self.absValBtn_RT.triggered.connect(self.absValBtn_RT_clicked)
    self.showEdges_RT = ft.QAction('Show edge lines', self)
    self.showEdges_RT.setCheckable(True)
    self.showEdges_RT.setChecked(True)
    self.exportEdges_RT = ft.QAction('Output video analysis', self)
    self.exportEdges_RT.setCheckable(True)

    self.RTmenu = self.menu.addMenu('&RGB Tracking')

    connectivitySub = self.RTmenu.addMenu('Connectivity (px)')
    connectivitySub.addAction(connectivity0)
    connectivitySub.addAction(connectivity1)
    self.connectivityGroup = ft.QActionGroup(self)
    self.connectivityGroup.addAction(connectivity0)
    self.connectivityGroup.addAction(connectivity1)
    self.connectivityGroup.setExclusive(True)

    self.RTmenu.addAction(showFrameLargeBtn_RT)
    self.RTmenu.addAction(self.filterLight_RT)
    self.RTmenu.addAction(self.lightROIBtn_RT)
    self.RTmenu.addAction(self.absValBtn_RT)
    self.RTmenu.addAction(self.showEdges_RT)
    self.RTmenu.addAction(self.exportEdges_RT)


    # self.colorTrackingBox.setStyleSheet('background-color: None')

    # if ft.sys.platform == 'darwin':
    #     self.colorTrackingBox = ft.QGroupBox(' ', self.analysisGroupBox)
    #     self.colorTrackingBox.setGeometry(0, 0, 1050, 390)
    #
    #     # size of GUI labels:
    #     h_lbl = 22
    #     h_txt = 30
    #     h_btn = 30
    #     h_btn_arrows = 30
    #     h_slider = 25
    #
    #     if self.pyqtVer == '5': #PyQt5 GUI will be removed after FlameTrackerv1.1.8
    #         # first column without color channels objects
    #         # x1 = [ 10,   5,  10, 135,  10,  10, 145,  10, 120]
    #         # y1 = [ 20,  45, 280, 283, 305, 330, 334, 360, 360]
    #         # w1 = [100, 150, 150,  40, 170, 140,  30, 100,  60]
    #         x1 = [10,  90,  10, 135,  10,  10, 135,  10, 130,  10]
    #         y1 = [20,  20, 255, 258, 285, 310, 314, 335, 335, 360]
    #         w1 = [80, 110, 150,  40, 170, 140,  40, 100,  50, 150]
    #
    #         # first column - 'colors' objects
    #         # x_rgb = [ 10,  10, 35, 175,  60,  10,  35, 175,  60]
    #         # w_rgb = [100, 100, 30,  30, 120, 100,  30,  30, 120]
    #         x_rgb = [ 10,  10, 40, 180,  60,  10,  40, 180,  60]
    #         w_rgb = [100, 100, 20,  20, 120, 100,  20,  20, 120]
    #
    #
    #         # y_r = [ 70,  92,  90,  90,  95, 114, 112, 112, 117]
    #         # y_g = [140, 162, 160, 160, 165, 184, 182, 182, 187]
    #         # y_b = [210, 232, 230, 230, 235, 254, 252, 252, 257]
    #         y_r = [ 45,  67,  65,  65,  70,  89,  87,  87,  92]
    #         y_g = [115, 137, 135, 135, 140, 159, 157, 157, 162]
    #         y_b = [185, 208, 205, 205, 210, 229, 227, 227, 232]
    #
    #         # second column
    #         # x2 = [210, 210, 210, 220, 210, 220, 220, 325, 210, 210, 210]
    #         # y2 = [ 30,  60,  90, 120, 145, 170, 200, 204, 230, 260, 290]
    #         # w2 = [150, 150, 150, 120, 150, 135, 130,  30, 150, 150, 150]
    #         x2 = [220, 220, 220, 220, 315, 220, 220, 220, 220, 220, 220, 220, 220]
    #         y2 = [ 20,  50,  80, 110, 114, 140, 170, 200, 230, 260, 290, 320, 350]
    #         w2 = [135, 135, 135, 120,  40, 135, 135, 135, 135, 135, 135, 135, 135]
    #     elif self.pyqtVer == '6':
    #         # first column without color channels objects
    #         # x1 = [ 10,   5,  10, 135,  10,  10, 145,  10, 120]
    #         # y1 = [ 20,  45, 280, 283, 305, 330, 334, 360, 360]
    #         # w1 = [100, 150, 150,  40, 170, 140,  30, 100,  60]
    #         x1 = [10,  90,  10, 135,  10,  10, 135,  10, 130,  10]
    #         y1 = [20,  20, 255, 258, 285, 310, 314, 335, 335, 360]
    #         w1 = [85, 110, 150,  40, 170, 140,  40, 100,  50, 150]
    #
    #         # first column - 'colors' objects
    #         # x_rgb = [ 10,  10, 40, 180,  60,  10,  40, 180,  60]
    #         # w_rgb = [100, 100, 20,  20, 120, 100,  20,  20, 120]
    #         x_rgb = [ 10,  10, 40, 180,  60,  10,  40, 180,  60]
    #         w_rgb = [100, 100, 20,  20, 120, 100,  20,  20, 120]
    #
    #         # y_r = [ 70,  92,  90,  90,  95, 114, 112, 112, 117]
    #         # y_g = [140, 162, 160, 160, 165, 184, 182, 182, 187]
    #         # y_b = [210, 232, 230, 230, 235, 254, 252, 252, 257]
    #         y_r = [ 45,  67,  65,  65,  70,  89,  87,  87,  92]
    #         y_g = [115, 137, 135, 135, 140, 159, 157, 157, 162]
    #         y_b = [185, 208, 205, 205, 210, 229, 227, 227, 232]
    #
    #         # second column (added checkboxes in v1.1.8)
    #         # x2 = [220, 220, 220, 220, 220, 220, 220, 325, 220, 220, 220]
    #         # y2 = [ 30,  60,  90, 120, 145, 170, 200, 204, 230, 260, 290]
    #         # w2 = [135, 135, 135, 120, 135, 135, 130,  30, 135, 135, 135]
    #         x2 = [220, 220, 220, 220, 315, 220, 220, 220, 220, 220, 220, 220, 220]
    #         y2 = [ 20,  50,  80, 110, 114, 140, 170, 200, 230, 260, 290, 320, 350]
    #         w2 = [135, 135, 135, 120,  40, 135, 135, 135, 135, 135, 135, 135, 135]
    #
    #     # other objects
    #     # x3 = [780, 780, 930]
    #     # y3 = [275, 300, 275]
    #     # w3 = [135, 135, 115]
    #     x3 = [370, 370, 620, 620, 660, 620, 660, 860, 860, 900, 860, 900]
    #     y3 = [280, 305, 280, 305, 310, 330, 335, 280, 305, 310, 330, 335]
    #     w3 = [135, 135, 135,  80, 150,  80, 150, 135,  80, 150,  80, 150]
    #     # labels (since there's only two, in this case I wrote the entire set of coord.)
    #     lbl1 = [370, 25, 330, 250]
    #     lbl2 = [710, 25, 330, 250]
    #
    # elif ft.sys.platform == 'win32':
    #     self.colorTrackingBox = ft.QGroupBox('Analysis box', self.analysisGroupBox)
    #     self.colorTrackingBox.setGeometry(0, 0, 1050, 370)
    #
    #     # size of GUI labels:
    #     h_lbl = 20
    #     h_txt = 25
    #     h_btn = 20
    #     h_btn_arrows = 20
    #     h_slider = 15
    #
    #     # first column without color channels objects
    #     # x1 = [ 10,  10,  10, 140,  10,  10, 120,  10, 120]
    #     # y1 = [ 10,  35, 255, 260, 280, 295, 300, 325, 330]
    #     # w1 = [100, 140, 150,  35, 170, 100,  30, 100,  35]
    #     x1 = [10, 100,  10, 135,  10,  10, 135,  10, 130,  25]
    #     y1 = [15,  17, 245, 248, 275, 295, 298, 320, 322, 345]
    #     w1 = [85, 100, 150,  50, 170, 140,  50, 100,  50, 150]
    #
    #     # first column - 'colors' objects
    #     # x_rgb = [ 10,  10, 40, 185,  60,  10,  40, 185,  60]
    #     # w_rgb = [100, 100, 15,  15, 120, 100,  15,  15, 120]
    #     x_rgb = [ 10,  10, 40, 180,  60,  10,  40, 180,  60]
    #     w_rgb = [100, 100, 20,  20, 120, 100,  20,  20, 120]
    #
    #     # y_r   = [ 60,  80,  85,  85,  88, 100, 105, 105, 108]
    #     # y_g   = [125, 145, 150, 150, 153, 165, 170, 170, 173]
    #     # y_b   = [190, 210, 215, 215, 218, 230, 235, 235, 238]
    #     y_r = [ 35,  55,  57,  57,  60,  80,  82,  82,  85]
    #     y_g = [105, 125, 127, 127, 130, 150, 152, 152, 155]
    #     y_b = [175, 195, 197, 197, 200, 220, 222, 222, 225]
    #
    #     # second column
    #     # x2 = [220, 220, 220, 220, 220, 220, 220, 330, 220, 220, 220]
    #     # y2 = [ 15,  45,  75, 100, 130, 155, 185, 190, 220, 250, 280]
    #     # w2 = [140, 140, 140, 120, 140, 140, 100,  30, 140, 140, 140]
    #     x2 = [220, 220, 220, 220, 315, 220, 220, 220, 220, 220, 220, 220, 220]
    #     y2 = [ 15,  40,  65,  90,  92, 120, 150, 180, 210, 240, 270, 300, 330]
    #     w2 = [135, 135, 135, 120,  40, 135, 135, 135, 135, 135, 135, 135, 135]
    #
    #     # other objects
    #     # x3 = [780, 780, 920]
    #     # y3 = [270, 290, 270]
    #     # w3 = [120, 120, 120]
    #     x3 = [370, 370, 580, 580, 620, 580, 620, 820, 820, 860, 820, 860]
    #     y3 = [270, 295, 270, 295, 297, 320, 322, 270, 295, 297, 320, 322]
    #     w3 = [150, 150, 135,  80, 150,  80, 150, 135,  80, 150,  80, 150]
    #
    #
    #     # labels (since there's only two, in this case I wrote the entire set of coord.)
    #     lbl1 = [370, 15, 330, 250]
    #     lbl2 = [710, 15, 330, 250]
    #
    # elif ft.sys.platform == 'linux':
    #     self.colorTrackingBox = ft.QGroupBox(' ', self.analysisGroupBox)
    #     self.colorTrackingBox.setGeometry(0, 0, 1050, 390)
    #
    #     # size of GUI labels:
    #     h_lbl = 22
    #     h_txt = 30
    #     h_btn = 30
    #     h_btn_arrows = 30
    #     h_slider = 25
    #
    #     # first column without color channels objects
    #     # x1 = [ 10,   5,  10, 135,  10,  10, 145,  10, 120]
    #     # y1 = [ 20,  45, 280, 283, 305, 330, 334, 360, 360]
    #     # w1 = [100, 150, 150,  40, 170, 140,  30, 100,  60]
    #     x1 = [10,  90,  10, 140,  10,  10, 140,  10, 140,  10]
    #     y1 = [20,  20, 245, 248, 275, 295, 298, 320, 322, 345]
    #     w1 = [80, 110, 150,  50, 170, 140,  50, 100,  50, 180]
    #
    #     # first column - 'colors' objects
    #     # x_rgb = [ 10,  10, 35, 175,  60,  10,  35, 175,  60]
    #     # w_rgb = [100, 100, 30,  30, 120, 100,  30,  30, 120]
    #     x_rgb = [ 10,  10, 40, 180,  60,  10,  40, 180,  60]
    #     w_rgb = [100, 100, 20,  20, 120, 100,  20,  20, 120]
    #
    #     # y_r = [ 70,  92, 90,  90,  95, 114, 112, 112, 117]
    #     # y_g = [140, 162, 160, 160, 165, 184, 182, 182, 187]
    #     # y_b = [210, 232, 230, 230, 235, 254, 252, 252, 257]
    #     y_r = [ 35,  55,  57,  57,  60,  80,  82,  82,  85]
    #     y_g = [105, 125, 127, 127, 130, 150, 152, 152, 155]
    #     y_b = [175, 195, 197, 197, 200, 220, 222, 222, 225]
    #
    #     # second column
    #     # x2 = [210, 210, 210, 220, 210, 220, 220, 325, 210, 210, 210]
    #     # y2 = [ 30,  60,  90, 120, 145, 170, 200, 204, 230, 260, 290]
    #     # w2 = [150, 150, 150, 120, 150, 135, 130,  30, 150, 150, 150]
    #     x2 = [220, 220, 220, 220, 315, 220, 220, 220, 220, 220, 220, 220, 220]
    #     y2 = [ 15,  40,  65,  90,  92, 120, 150, 180, 210, 240, 270, 300, 330]
    #     w2 = [135, 135, 135, 120,  40, 135, 135, 135, 135, 135, 135, 135, 135]
    #
    #     # other objects
    #     # x3 = [780, 780, 930]
    #     # y3 = [275, 300, 275]
    #     # w3 = [135, 135, 115]
    #     x3 = [370, 370, 580, 580, 620, 580, 620, 820, 820, 860, 820, 860]
    #     y3 = [270, 295, 270, 295, 300, 320, 325, 270, 295, 300, 320, 325]
    #     w3 = [150, 150, 135,  80, 150,  80, 150, 135,  80, 150,  80, 150]
    #
    #     # labels (since there's only two, in this case I wrote the entire set of coord.)
    #     lbl1 = [370, 25, 330, 250]
    #     lbl2 = [710, 25, 330, 250]

    # self.colorTrackingBox.setStyleSheet('background-color: None')
    #
    # # #first column
    # directionBoxTxt = ft.QLabel('Flame spread:', self.colorTrackingBox)
    # directionBoxTxt.setGeometry(x1[0], y1[0], w1[0], h_txt)
    # self.directionBox = ft.QComboBox(self.colorTrackingBox)
    # self.directionBox.setGeometry(x1[1], y1[1], w1[1], h_btn)
    # self.directionBox.addItem('Left to right')
    # self.directionBox.addItem('Right to left')
    # # if self.pyqtVer == '5':
    # #     self.directionBox.activated[str].connect(self.directionCT_clicked)
    # # elif self.pyqtVer == '6':
    # #     self.directionBox.activated.connect(self.directionCT_clicked)
    #
    # filterParticleTxt = ft.QLabel('Filter particles:', self.colorTrackingBox)
    # filterParticleTxt.setGeometry(x1[2], y1[2], w1[2], h_txt)
    # self.particleSldrMax = ft.QLineEdit('1000', self.colorTrackingBox)
    # self.particleSldrMax.setGeometry(x1[3], y1[3], w1[3], h_lbl)
    # if self.pyqtVer == '5':
    #     self.filterParticleSldr_CT = ft.QSlider(ft.Qt.Horizontal, self.colorTrackingBox)
    # elif self.pyqtVer == '6':
    #     self.filterParticleSldr_CT = ft.QSlider(ft.Qt.Orientation.Horizontal, self.colorTrackingBox)
    # self.filterParticleSldr_CT.setGeometry(x1[4], y1[4], w1[4], h_slider)
    # self.filterParticleSldr_CT.setMinimum(1)
    # self.filterParticleSldr_CT.setMaximum(1000)
    # self.filterParticleSldr_CT.setValue(10)
    # self.filterParticleSldr_CT.sliderReleased.connect(self.filterParticleSldr_CT_released)
    # avgLE_txt = ft.QLabel('#px to locate edges:', self.colorTrackingBox)
    # avgLE_txt.setGeometry(x1[5], y1[5], w1[5], h_txt)
    # self.avgLEIn_CT = ft.QLineEdit('1', self.colorTrackingBox)
    # self.avgLEIn_CT.setGeometry(x1[6], y1[6], w1[6], h_lbl)
    # connectivityTxt = ft.QLabel('Connectivity (px):', self.colorTrackingBox)
    # connectivityTxt.setGeometry(x1[7], y1[7], w1[7], h_txt)
    # self.connectivityBox = ft.QComboBox(self.colorTrackingBox)
    # self.connectivityBox.setGeometry(x1[8], y1[8], w1[8], h_btn)
    # self.connectivityBox.addItem('4')
    # self.connectivityBox.addItem('8')
    # # if self.pyqtVer == '5':
    # #     self.connectivityBox.activated[str].connect(self.connectivityBoxCT_clicked)
    # # elif self.pyqtVer == '6':
    # #     self.connectivityBox.activated.connect(self.connectivityBoxCT_clicked)
    # self.showFrameLargeBtn_CT = ft.QPushButton('Show frames', self.colorTrackingBox)
    # self.showFrameLargeBtn_CT.setGeometry(x1[9], y1[9], w1[9], h_btn)
    # self.showFrameLargeBtn_CT.clicked.connect(self.showFrameLargeBtn_CT_clicked)
    #
    # redChannelTxt = ft.QLabel('Red channel:', self.colorTrackingBox)
    # redChannelTxt.setGeometry(x_rgb[0], y_r[0], w_rgb[0], h_txt)
    # redMinTxt = ft.QLabel('Min:', self.colorTrackingBox)
    # redMinTxt.setGeometry(x_rgb[1], y_r[1], w_rgb[1], h_txt)
    # self.redMinLeftBtn_CT = ft.QPushButton('<', self.colorTrackingBox)
    # self.redMinLeftBtn_CT.setGeometry(x_rgb[2], y_r[2], w_rgb[2], h_btn_arrows)
    # self.redMinLeftBtn_CT.clicked.connect(self.redMinLeftBtn_CT_clicked)
    # self.redMinRightBtn_CT = ft.QPushButton('>', self.colorTrackingBox)
    # self.redMinRightBtn_CT.setGeometry(x_rgb[3], y_r[3], w_rgb[3], h_btn_arrows)
    # self.redMinRightBtn_CT.clicked.connect(self.redMinRightBtn_CT_clicked)
    # if self.pyqtVer == '5':
    #     self.redMinSlider = ft.QSlider(ft.Qt.Horizontal, self.colorTrackingBox)
    # elif self.pyqtVer == '6':
    #     self.redMinSlider = ft.QSlider(ft.Qt.Orientation.Horizontal, self.colorTrackingBox)
    # self.redMinSlider.setGeometry(x_rgb[4], y_r[4], w_rgb[4], h_slider)
    # self.redMinSlider.setMinimum(0)
    # self.redMinSlider.setMaximum(255)
    # self.redMinSlider.setValue(10)
    # self.redMinSlider.sliderReleased.connect(self.singleColorSlider_released)
    # redMaxTxt = ft.QLabel('Max:', self.colorTrackingBox)
    # redMaxTxt.setGeometry(x_rgb[5], y_r[5], w_rgb[5], h_txt)
    # self.redMaxLeftBtn_CT = ft.QPushButton('<', self.colorTrackingBox)
    # self.redMaxLeftBtn_CT.setGeometry(x_rgb[6], y_r[6], w_rgb[6], h_btn_arrows)
    # self.redMaxLeftBtn_CT.clicked.connect(self.redMaxLeftBtn_CT_clicked)
    # self.redMaxRightBtn_CT = ft.QPushButton('>', self.colorTrackingBox)
    # self.redMaxRightBtn_CT.setGeometry(x_rgb[7], y_r[7], w_rgb[7], h_btn_arrows)
    # self.redMaxRightBtn_CT.clicked.connect(self.redMaxRightBtn_CT_clicked)
    # if self.pyqtVer == '5':
    #     self.redMaxSlider = ft.QSlider(ft.Qt.Horizontal, self.colorTrackingBox)
    # elif self.pyqtVer == '6':
    #     self.redMaxSlider = ft.QSlider(ft.Qt.Orientation.Horizontal, self.colorTrackingBox)
    # self.redMaxSlider.setGeometry(x_rgb[8], y_r[8], w_rgb[8], h_slider)
    # self.redMaxSlider.setMinimum(0)
    # self.redMaxSlider.setMaximum(255)
    # self.redMaxSlider.setValue(255)
    # self.redMaxSlider.sliderReleased.connect(self.singleColorSlider_released)
    # greenChannelTxt = ft.QLabel('Green channel:', self.colorTrackingBox)
    # greenChannelTxt.setGeometry(x_rgb[0], y_g[0], w_rgb[0], h_txt)
    # greenMinTxt = ft.QLabel('Min:', self.colorTrackingBox)
    # greenMinTxt.setGeometry(x_rgb[1], y_g[1], w_rgb[1], h_txt)
    # self.greenMinLeftBtn_CT = ft.QPushButton('<', self.colorTrackingBox)
    # self.greenMinLeftBtn_CT.setGeometry(x_rgb[2], y_g[2], w_rgb[2], h_btn_arrows)
    # self.greenMinLeftBtn_CT.clicked.connect(self.greenMinLeftBtn_CT_clicked)
    # self.greenMinRightBtn_CT = ft.QPushButton('>', self.colorTrackingBox)
    # self.greenMinRightBtn_CT.setGeometry(x_rgb[3], y_g[3], w_rgb[3], h_btn_arrows)
    # self.greenMinRightBtn_CT.clicked.connect(self.greenMinRightBtn_CT_clicked)
    # if self.pyqtVer == '5':
    #     self.greenMinSlider = ft.QSlider(ft.Qt.Horizontal, self.colorTrackingBox)
    # elif self.pyqtVer == '6':
    #     self.greenMinSlider = ft.QSlider(ft.Qt.Orientation.Horizontal, self.colorTrackingBox)
    # self.greenMinSlider.setGeometry(x_rgb[4], y_g[4], w_rgb[4], h_slider)
    # self.greenMinSlider.setMinimum(0)
    # self.greenMinSlider.setMaximum(255)
    # self.greenMinSlider.setValue(10)
    # self.greenMinSlider.sliderReleased.connect(self.singleColorSlider_released)
    # greenMaxTxt = ft.QLabel('Max:', self.colorTrackingBox)
    # greenMaxTxt.setGeometry(x_rgb[5], y_g[5], w_rgb[5], h_txt)
    # self.greenMaxLeftBtn_CT = ft.QPushButton('<', self.colorTrackingBox)
    # self.greenMaxLeftBtn_CT.setGeometry(x_rgb[6], y_g[6], w_rgb[6], h_btn_arrows)
    # self.greenMaxLeftBtn_CT.clicked.connect(self.greenMaxLeftBtn_CT_clicked)
    # self.greenMaxRightBtn_CT = ft.QPushButton('>', self.colorTrackingBox)
    # self.greenMaxRightBtn_CT.setGeometry(x_rgb[7], y_g[7], w_rgb[7], h_btn_arrows)
    # self.greenMaxRightBtn_CT.clicked.connect(self.greenMaxRightBtn_CT_clicked)
    # if self.pyqtVer == '5':
    #     self.greenMaxSlider = ft.QSlider(ft.Qt.Horizontal, self.colorTrackingBox)
    # elif self.pyqtVer == '6':
    #     self.greenMaxSlider = ft.QSlider(ft.Qt.Orientation.Horizontal, self.colorTrackingBox)
    # self.greenMaxSlider.setGeometry(x_rgb[8], y_g[8], w_rgb[8], h_slider)
    # self.greenMaxSlider.setMinimum(0)
    # self.greenMaxSlider.setMaximum(255)
    # self.greenMaxSlider.setValue(255)
    # self.greenMaxSlider.sliderReleased.connect(self.singleColorSlider_released)
    # blueChannelTxt = ft.QLabel('Blue channel:', self.colorTrackingBox)
    # blueChannelTxt.setGeometry(x_rgb[0], y_b[0], w_rgb[0], h_txt)
    # blueMinTxt = ft.QLabel('Min:', self.colorTrackingBox)
    # blueMinTxt.setGeometry(x_rgb[1], y_b[1], w_rgb[1], h_txt)
    # self.blueMinLeftBtn_CT = ft.QPushButton('<', self.colorTrackingBox)
    # self.blueMinLeftBtn_CT.setGeometry(x_rgb[2], y_b[2], w_rgb[2], h_btn_arrows)
    # self.blueMinLeftBtn_CT.clicked.connect(self.blueMinLeftBtn_CT_clicked)
    # self.blueMinRightBtn_CT = ft.QPushButton('>', self.colorTrackingBox)
    # self.blueMinRightBtn_CT.setGeometry(x_rgb[3], y_b[3], w_rgb[3], h_btn_arrows)
    # self.blueMinRightBtn_CT.clicked.connect(self.blueMinRightBtn_CT_clicked)
    # if self.pyqtVer == '5':
    #     self.blueMinSlider = ft.QSlider(ft.Qt.Horizontal, self.colorTrackingBox)
    # elif self.pyqtVer == '6':
    #     self.blueMinSlider = ft.QSlider(ft.Qt.Orientation.Horizontal, self.colorTrackingBox)
    # self.blueMinSlider.setGeometry(x_rgb[4], y_b[4], w_rgb[4], h_slider)
    # self.blueMinSlider.setMinimum(0)
    # self.blueMinSlider.setMaximum(255)
    # self.blueMinSlider.sliderReleased.connect(self.singleColorSlider_released)
    # blueMaxTxt = ft.QLabel('Max:', self.colorTrackingBox)
    # blueMaxTxt.setGeometry(x_rgb[5], y_b[5], w_rgb[5], h_txt)
    # self.blueMaxLeftBtn_CT = ft.QPushButton('<', self.colorTrackingBox)
    # self.blueMaxLeftBtn_CT.setGeometry(x_rgb[6], y_b[6], w_rgb[6], h_btn_arrows)
    # self.blueMaxLeftBtn_CT.clicked.connect(self.blueMaxLeftBtn_CT_clicked)
    # self.blueMaxRightBtn_CT = ft.QPushButton('>', self.colorTrackingBox)
    # self.blueMaxRightBtn_CT.setGeometry(x_rgb[7], y_b[7], w_rgb[7], h_btn_arrows)
    # self.blueMaxRightBtn_CT.clicked.connect(self.blueMaxRightBtn_CT_clicked)
    # if self.pyqtVer == '5':
    #     self.blueMaxSlider = ft.QSlider(ft.Qt.Horizontal, self.colorTrackingBox)
    # elif self.pyqtVer == '6':
    #     self.blueMaxSlider = ft.QSlider(ft.Qt.Orientation.Horizontal, self.colorTrackingBox)
    # self.blueMaxSlider.setGeometry(x_rgb[8], y_b[8], w_rgb[8], h_slider)
    # self.blueMaxSlider.setMinimum(0)
    # self.blueMaxSlider.setMaximum(255)
    # self.blueMaxSlider.setValue(255)
    # self.blueMaxSlider.sliderReleased.connect(self.singleColorSlider_released)
    #
    # #second column
    # trackingTxt = ft.QLabel('Flame tracking:', self.colorTrackingBox)
    # trackingTxt.setGeometry(x2[0], y2[0], w2[0], h_txt)
    # self.lightROIBtn_CT = ft.QPushButton('Pick bright region', self.colorTrackingBox)
    # self.lightROIBtn_CT.setGeometry(x2[1], y2[1], w2[1], h_btn)
    # self.lightROIBtn_CT.clicked.connect(self.lightROIBtn_CT_clicked)
    # self.filterLight_CT = ft.QCheckBox('Ignore flashing light', self.colorTrackingBox)
    # self.filterLight_CT.setGeometry(x2[2], y2[2], w2[2], h_btn)
    # movAvgTxt = ft.QLabel('Moving avg pts:', self.colorTrackingBox)
    # movAvgTxt.setGeometry(x2[3], y2[3], w2[3], h_txt)
    # self.movAvgIn_CT = ft.QLineEdit('2', self.colorTrackingBox)
    # self.movAvgIn_CT.setGeometry(x2[4], y2[4], w2[4], h_lbl)
    # self.colorTrackingBtn = ft.QPushButton('Start tracking', self.colorTrackingBox)
    # self.colorTrackingBtn.setGeometry(x2[5], y2[5], w2[5], h_btn)
    # self.colorTrackingBtn.clicked.connect(self.colorTrackingBtn_clicked)
    # self.saveBtn_CT = ft.QPushButton('Save data', self.colorTrackingBox)
    # self.saveBtn_CT.setGeometry(x2[6], y2[6], w2[6], h_btn)
    # self.saveBtn_CT.clicked.connect(self.saveBtn_CT_clicked)
    # self.absValBtn_CT = ft.QPushButton('Absolute values', self.colorTrackingBox)
    # self.absValBtn_CT.setGeometry(x2[7], y2[7], w2[7], h_btn)
    # self.absValBtn_CT.clicked.connect(self.absValBtn_CT_clicked)
    # self.saveChannelsBtn_CT = ft.QPushButton('Save RGB values', self.colorTrackingBox)
    # self.saveChannelsBtn_CT.setGeometry(x2[8], y2[8], w2[8], h_btn) #x2[0], y2[0], w2[0], h_btn
    # self.saveChannelsBtn_CT.clicked.connect(self.saveChannelsBtn_CT_clicked)
    # self.loadChannelsBtn_CT = ft.QPushButton('Load RGB values', self.colorTrackingBox)
    # self.loadChannelsBtn_CT.setGeometry(x2[9], y2[9], w2[9], h_btn) #x2[1], y2[1], w2[1],
    # self.loadChannelsBtn_CT.clicked.connect(self.loadChannelsBtn_CT_clicked)
    # self.updateGraphsBtn_CT = ft.QPushButton('Update graphs', self.colorTrackingBox)
    # self.updateGraphsBtn_CT.setGeometry(x2[10], y2[10], w2[10], h_btn)
    # self.updateGraphsBtn_CT.clicked.connect(self.updateGraphsBtn_CT_clicked)
    # self.helpBtn_CT = ft.QPushButton('Help', self.colorTrackingBox)
    # self.helpBtn_CT.setGeometry(x2[11], y2[11], w2[11], h_btn) #x2[2], y2[2], w2[2],
    # self.helpBtn_CT.clicked.connect(self.helpBtn_CT_clicked)
    # # trackingTxt = ft.QLabel('Flame tracking:', self.colorTrackingBox)
    # # trackingTxt.setGeometry(x2[3], y2[3], w2[3], h_txt)
    # # self.lightROIBtn_CT = ft.QPushButton('Pick bright region', self.colorTrackingBox)
    # # self.lightROIBtn_CT.setGeometry(x2[4], y2[4], w2[4], h_btn)
    # # self.lightROIBtn_CT.clicked.connect(self.lightROIBtn_CT_clicked)
    # # self.filterLight_CT = ft.QCheckBox('Ignore flashing light', self.colorTrackingBox)
    # # self.filterLight_CT.setGeometry(x2[5], y2[5], w2[5], h_btn)
    # # movAvgTxt = ft.QLabel('Moving avg points:', self.colorTrackingBox)
    # # movAvgTxt.setGeometry(x2[6], y2[6], w2[6], h_txt)
    # # self.movAvgIn_CT = ft.QLineEdit('2', self.colorTrackingBox)
    # # self.movAvgIn_CT.setGeometry(x2[7], y2[7], w2[7], h_lbl)
    #
    # # self.colorTrackingBtn = ft.QPushButton('Start tracking', self.colorTrackingBox)
    # # self.colorTrackingBtn.setGeometry(x2[8], y2[8], w2[8], h_btn)
    # # self.colorTrackingBtn.clicked.connect(self.colorTrackingBtn_clicked)
    # # self.absValBtn_CT = ft.QPushButton('Absolute values', self.colorTrackingBox)
    # # self.absValBtn_CT.setGeometry(x2[9], y2[9], w2[9], h_btn)
    # # self.absValBtn_CT.clicked.connect(self.absValBtn_CT_clicked)
    # # self.saveBtn_CT = ft.QPushButton('Save data', self.colorTrackingBox)
    # # self.saveBtn_CT.setGeometry(x2[10], y2[10], w2[10], h_btn)
    # # self.saveBtn_CT.clicked.connect(self.saveBtn_CT_clicked)
    #
    #
    # # other objects
    # self.showEdges = ft.QCheckBox('Show edges location', self.colorTrackingBox)
    # self.showEdges.setGeometry(x3[0], y3[0], w3[0], h_btn)
    # self.showEdges.setChecked(True)
    # self.exportEdges_CT = ft.QCheckBox('Output video analysis', self.colorTrackingBox)
    # self.exportEdges_CT.setGeometry(x3[1], y3[1], w3[1], h_btn) #x2[12], y2[12], w2[12], h_btn
    # txt_lbl1 = ft.QLabel('Graph #1:', self.colorTrackingBox)
    # txt_lbl1.setGeometry(x3[2], y3[2], w3[2], h_txt)
    # xAxisTxt_lbl1 = ft.QLabel('x axis:', self.colorTrackingBox)
    # xAxisTxt_lbl1.setGeometry(x3[3], y3[3], w3[3], h_txt)
    # self.xAxis_lbl1 = ft.QComboBox(self.colorTrackingBox)
    # self.xAxis_lbl1.setGeometry(x3[4], y3[4], w3[4], h_lbl)
    # self.xAxis_lbl1.addItem('Time [s]')
    # self.xAxis_lbl1.addItem('Frame #')
    # yAxisTxt_lbl1 = ft.QLabel('y axis:', self.colorTrackingBox)
    # yAxisTxt_lbl1.setGeometry(x3[5], y3[5], w3[5], h_txt)
    # self.yAxis_lbl1 = ft.QComboBox(self.colorTrackingBox)
    # self.yAxis_lbl1.setGeometry(x3[6], y3[6], w3[6], h_lbl)
    # self.yAxis_lbl1.addItem('Position [mm]')
    # self.yAxis_lbl1.addItem('Position [px]')
    # self.yAxis_lbl1.addItem('Flame length [mm]')
    # self.yAxis_lbl1.addItem('Spread rate [mm/s]')
    # txt_lbl2 = ft.QLabel('Graph #2:', self.colorTrackingBox)
    # txt_lbl2.setGeometry(x3[7], y3[7], w3[7], h_txt)
    # xAxisTxt_lbl2 = ft.QLabel('x axis:', self.colorTrackingBox)
    # xAxisTxt_lbl2.setGeometry(x3[8], y3[8], w3[8], h_txt)
    # self.xAxis_lbl2 = ft.QComboBox(self.colorTrackingBox)
    # self.xAxis_lbl2.setGeometry(x3[9], y3[9], w3[9], h_lbl)
    # self.xAxis_lbl2.addItem('Time [s]')
    # self.xAxis_lbl2.addItem('Frame #')
    # yAxisTxt_lbl2 = ft.QLabel('y axis:', self.colorTrackingBox)
    # yAxisTxt_lbl2.setGeometry(x3[10], y3[10], w3[10], h_txt)
    # self.yAxis_lbl2 = ft.QComboBox(self.colorTrackingBox)
    # self.yAxis_lbl2.setGeometry(x3[11], y3[11], w3[11], h_lbl)
    # self.yAxis_lbl2.addItem('Spread rate [mm/s]')
    # self.yAxis_lbl2.addItem('Flame length [mm]')
    # self.yAxis_lbl2.addItem('Position [mm]')
    # self.yAxis_lbl2.addItem('Position [px]')
    #
    # # first label
    # self.lbl1_CT = ft.QLabel(self.colorTrackingBox)
    # self.lbl1_CT.setGeometry(lbl1[0], lbl1[1], lbl1[2], lbl1[3])
    # self.lbl1_CT.setStyleSheet('background-color: white')
    #
    # # second label
    # self.lbl2_CT = ft.QLabel(self.colorTrackingBox)
    # self.lbl2_CT.setGeometry(lbl2[0], lbl2[1], lbl2[2], lbl2[3])
    # self.lbl2_CT.setStyleSheet('background-color: white')

def HSVTrackingBox(self):
    # self.HSVTrackingBox.setStyleSheet('background-color: None')
    self.box_layout = ft.QGridLayout()
    self.box_layout.setSpacing(10)

    # first column
    directionBoxTxt = ft.QLabel('Flame spread:')
    self.directionBox = ft.QComboBox()
    self.directionBox.addItem('Left to right')
    self.directionBox.addItem('Right to left')
    hueChannelTxt = ft.QLabel('Hue:')
    hueMinTxt = ft.QLabel('Min:')
    self.hueMinLeftBtn_HT = ft.QPushButton('<')
    self.hueMinLeftBtn_HT.clicked.connect(self.hueMinLeftBtn_HT_clicked)
    self.hueMinRightBtn_HT = ft.QPushButton('>')
    self.hueMinRightBtn_HT.clicked.connect(self.hueMinRightBtn_HT_clicked)
    self.hueMinSlider = ft.QSlider(ft.Qt.Orientation.Horizontal)
    self.hueMinSlider.setMinimum(0)
    self.hueMinSlider.setMaximum(180) # since stored as H/2 for 8-bit (normally 0-360)
    self.hueMinSlider.setValue(80) # Default to include blue values - 92=~185 deg Min Hue
    self.hueMinSlider.sliderReleased.connect(self.singleHSVSlider_released)
    self.hueMinSlider.valueChanged.connect(self.singleHSVSlider_released) #LC We need to check this line. I had to remove one from the other files (changed or released) because on Mac it counts twice
    hueMaxTxt = ft.QLabel('Max:')
    self.hueMaxLeftBtn_HT = ft.QPushButton('<')
    self.hueMaxLeftBtn_HT.clicked.connect(self.hueMaxLeftBtn_HT_clicked)
    self.hueMaxRightBtn_HT = ft.QPushButton('>')
    self.hueMaxRightBtn_HT.clicked.connect(self.hueMaxRightBtn_HT_clicked)
    self.hueMaxSlider = ft.QSlider(ft.Qt.Orientation.Horizontal)
    self.hueMaxSlider.setMinimum(0)
    self.hueMaxSlider.setMaximum(180) # since stored as H/2 for 8-bit (normally 0-360)
    self.hueMaxSlider.setValue(163) # Default to include blue values - 130=~260 deg Max Hue
    self.hueMaxSlider.sliderReleased.connect(self.singleHSVSlider_released)
    self.hueMaxSlider.valueChanged.connect(self.singleHSVSlider_released)
    satChannelTxt = ft.QLabel('Saturation:')
    satMinTxt = ft.QLabel('Min:')
    self.satMinLeftBtn_HT = ft.QPushButton('<')
    self.satMinLeftBtn_HT.clicked.connect(self.satMinLeftBtn_HT_clicked)
    self.satMinRightBtn_HT = ft.QPushButton('>')
    self.satMinRightBtn_HT.clicked.connect(self.satMinRightBtn_HT_clicked)
    self.satMinSlider = ft.QSlider(ft.Qt.Orientation.Horizontal)
    self.satMinSlider.setMinimum(0)
    self.satMinSlider.setMaximum(255)
    self.satMinSlider.setValue(30) # Default to include blue values - 100=~40% min Saturation
    self.satMinSlider.sliderReleased.connect(self.singleHSVSlider_released)
    self.satMinSlider.valueChanged.connect(self.singleHSVSlider_released)
    satMaxTxt = ft.QLabel('Max:')
    self.satMaxLeftBtn_HT = ft.QPushButton('<')
    self.satMaxLeftBtn_HT.clicked.connect(self.satMaxLeftBtn_HT_clicked)
    self.satMaxRightBtn_HT = ft.QPushButton('>')
    self.satMaxRightBtn_HT.clicked.connect(self.satMaxRightBtn_HT_clicked)
    self.satMaxSlider = ft.QSlider(ft.Qt.Orientation.Horizontal)
    self.satMaxSlider.setMinimum(0)
    self.satMaxSlider.setMaximum(255)
    self.satMaxSlider.setValue(255) # Default to some blue value - 255=~100% max Saturation
    self.satMaxSlider.sliderReleased.connect(self.singleHSVSlider_released)
    self.satMaxSlider.valueChanged.connect(self.singleHSVSlider_released)
    valChannelTxt = ft.QLabel('Value:')
    valMinTxt = ft.QLabel('Min:')
    self.valMinLeftBtn_HT = ft.QPushButton('<')
    self.valMinLeftBtn_HT.clicked.connect(self.valMinLeftBtn_HT_clicked)
    self.valMinRightBtn_HT = ft.QPushButton('>')
    self.valMinRightBtn_HT.clicked.connect(self.valMinRightBtn_HT_clicked)
    self.valMinSlider = ft.QSlider(ft.Qt.Orientation.Horizontal)
    self.valMinSlider.setMinimum(0)
    self.valMinSlider.setMaximum(255)
    self.valMinSlider.setValue(20) # Default to some blue value - 63=~25% min Value
    self.valMinSlider.sliderReleased.connect(self.singleHSVSlider_released)
    self.valMinSlider.valueChanged.connect(self.singleHSVSlider_released)
    valMaxTxt = ft.QLabel('Max:')
    self.valMaxLeftBtn_HT = ft.QPushButton('<')
    self.valMaxLeftBtn_HT.clicked.connect(self.valMaxLeftBtn_HT_clicked)
    self.valMaxRightBtn_HT = ft.QPushButton('>')
    self.valMaxRightBtn_HT.clicked.connect(self.valMaxRightBtn_HT_clicked)
    self.valMaxSlider = ft.QSlider(ft.Qt.Orientation.Horizontal)
    self.valMaxSlider.setMinimum(0)
    self.valMaxSlider.setMaximum(255)
    self.valMaxSlider.setValue(255) # Default to some blue value - 255=~100% max Value
    self.valMaxSlider.sliderReleased.connect(self.singleHSVSlider_released)
    self.valMaxSlider.valueChanged.connect(self.singleHSVSlider_released)
    filterParticleTxt = ft.QLabel('Filter particles:')
    self.particleSldrMax = ft.QLineEdit('1000')
    self.filterParticleSldr_HT = ft.QSlider(ft.Qt.Orientation.Horizontal)
    self.filterParticleSldr_HT.setMinimum(1)
    self.filterParticleSldr_HT.setMaximum(1000)
    self.filterParticleSldr_HT.setValue(20) #	was defulted to 10, but experience says around ~1228 or ~350 to not filter too much
    self.filterParticleSldr_HT.sliderReleased.connect(self.filterParticleSldr_HT_released)

    self.box_layout.addWidget(directionBoxTxt, 0, 0, 1, 3)
    self.box_layout.addWidget(self.directionBox, 0, 3, 1, 1)
    self.box_layout.addWidget(hueChannelTxt, 1, 0, 1, 3)
    self.box_layout.addWidget(hueMinTxt, 2, 0, 1, 1)
    self.box_layout.addWidget(self.hueMinLeftBtn_HT, 2, 1, 1, 1)
    self.box_layout.addWidget(self.hueMinRightBtn_HT, 2, 4, 1, 1)
    self.box_layout.addWidget(self.hueMinSlider, 2, 2, 1, 2)
    self.box_layout.addWidget(hueMaxTxt, 3, 0, 1, 1)
    self.box_layout.addWidget(self.hueMaxLeftBtn_HT, 3, 1, 1, 1)
    self.box_layout.addWidget(self.hueMaxRightBtn_HT, 3, 4, 1, 1)
    self.box_layout.addWidget(self.hueMaxSlider, 3, 2, 1, 2)
    self.box_layout.addWidget(satChannelTxt, 4, 0, 1, 3)
    self.box_layout.addWidget(satMinTxt, 5, 0, 1, 1)
    self.box_layout.addWidget(self.satMinLeftBtn_HT, 5, 1, 1, 1)
    self.box_layout.addWidget(self.satMinRightBtn_HT, 5, 4, 1, 1)
    self.box_layout.addWidget(self.satMinSlider, 5, 2, 1, 2)
    self.box_layout.addWidget(satMaxTxt, 6, 0, 1, 1)
    self.box_layout.addWidget(self.satMaxLeftBtn_HT, 6, 1, 1, 1)
    self.box_layout.addWidget(self.satMaxRightBtn_HT, 6, 4, 1, 1)
    self.box_layout.addWidget(self.satMaxSlider, 6, 2, 1, 2)
    self.box_layout.addWidget(valChannelTxt, 7, 0, 1, 3)
    self.box_layout.addWidget(valMinTxt, 8, 0, 1, 1)
    self.box_layout.addWidget(self.valMinLeftBtn_HT, 8, 1, 1, 1)
    self.box_layout.addWidget(self.valMinRightBtn_HT, 8, 4, 1, 1)
    self.box_layout.addWidget(self.valMinSlider, 8, 2, 1, 2)
    self.box_layout.addWidget(valMaxTxt, 9, 0, 1, 1)
    self.box_layout.addWidget(self.valMaxLeftBtn_HT, 9, 1, 1, 1)
    self.box_layout.addWidget(self.valMaxRightBtn_HT, 9, 4, 1, 1)
    self.box_layout.addWidget(self.valMaxSlider, 9, 2, 1, 2)
    self.box_layout.addWidget(filterParticleTxt, 10, 0, 1, 3)
    self.box_layout.addWidget(self.particleSldrMax, 10, 3, 1, 1)
    self.box_layout.addWidget(self.filterParticleSldr_HT, 11, 2, 1, 2)

    #second column
    trackingTxt = ft.QLabel('Flame tracking:')
    avgLE_txt = ft.QLabel('Pts to locate edges:')
    self.avgLEIn_HT = ft.QLineEdit('10')
    movAvgTxt = ft.QLabel('Moving avg pts:')
    self.movAvgIn_HT = ft.QLineEdit('5')
    self.HSVTrackingBtn = ft.QPushButton('Start tracking')
    self.HSVTrackingBtn.clicked.connect(self.HSVTrackingBtn_clicked)
    self.saveBtn_HT = ft.QPushButton('Save data')
    self.saveBtn_HT.clicked.connect(self.saveBtn_HT_clicked)
    self.saveChannelsBtn_HT = ft.QPushButton('Save HSV values')
    self.saveChannelsBtn_HT.clicked.connect(self.saveChannelsBtn_HT_clicked)
    self.loadChannelsBtn_HT = ft.QPushButton('Load HSV values')
    self.loadChannelsBtn_HT.clicked.connect(self.loadChannelsBtn_HT_clicked)
    self.updateGraphsBtn_HT = ft.QPushButton('Update graphs')
    self.updateGraphsBtn_HT.clicked.connect(self.updateGraphsBtn_HT_clicked)

    self.box_layout.addWidget(trackingTxt, 0, 5, 1, 1)
    self.box_layout.addWidget(avgLE_txt, 1, 5, 1, 1)
    self.box_layout.addWidget(self.avgLEIn_HT, 1, 6, 1, 1)
    self.box_layout.addWidget(movAvgTxt, 2, 5, 1, 2)
    self.box_layout.addWidget(self.movAvgIn_HT, 2, 6, 1, 1)
    self.box_layout.addWidget(self.HSVTrackingBtn, 3, 5, 1, 2)
    self.box_layout.addWidget(self.saveBtn_HT, 4, 5, 1, 2)
    self.box_layout.addWidget(self.saveChannelsBtn_HT, 5, 5, 1, 2)
    self.box_layout.addWidget(self.loadChannelsBtn_HT, 6, 5, 1, 2)
    self.box_layout.addWidget(self.updateGraphsBtn_HT, 7, 5, 1, 2)

    # first label
    self.lbl1_HT = ft.QLabel()
    self.lbl1_HT.setStyleSheet('background-color: white')

    # second label
    self.lbl2_HT = ft.QLabel()
    self.lbl2_HT.setStyleSheet('background-color: white')

    # # other objects
    txt_lbl1 = ft.QLabel('Graph #1:')
    xAxisTxt_lbl1 = ft.QLabel('x axis:')
    self.xAxis_lbl1 = ft.QComboBox()
    self.xAxis_lbl1.addItem('Time [s]')
    self.xAxis_lbl1.addItem('Frame #')
    yAxisTxt_lbl1 = ft.QLabel('y axis:')
    self.yAxis_lbl1 = ft.QComboBox()
    self.yAxis_lbl1.addItem('Position [mm]')
    self.yAxis_lbl1.addItem('Position [px]')
    self.yAxis_lbl1.addItem('Flame length [mm]')
    self.yAxis_lbl1.addItem('Spread rate [mm/s]')
    txt_lbl2 = ft.QLabel('Graph #2:')
    xAxisTxt_lbl2 = ft.QLabel('x axis:')
    self.xAxis_lbl2 = ft.QComboBox()
    self.xAxis_lbl2.addItem('Time [s]')
    self.xAxis_lbl2.addItem('Frame #')
    yAxisTxt_lbl2 = ft.QLabel('y axis:')
    self.yAxis_lbl2 = ft.QComboBox()
    self.yAxis_lbl2.addItem('Spread rate [mm/s]')
    self.yAxis_lbl2.addItem('Flame length [mm]')
    self.yAxis_lbl2.addItem('Position [mm]')
    self.yAxis_lbl2.addItem('Position [px]')

    self.box_layout.addWidget(self.lbl1_HT, 0, 9, 4, 6)
    self.box_layout.addWidget(self.lbl2_HT, 4, 9, 4, 6)
    self.box_layout.addWidget(txt_lbl1, 8, 10, 1, 1)
    self.box_layout.addWidget(xAxisTxt_lbl1, 9, 10, 1, 1)
    self.box_layout.addWidget(self.xAxis_lbl1, 9, 11, 1, 1)
    self.box_layout.addWidget(yAxisTxt_lbl1, 10, 10, 1, 1)
    self.box_layout.addWidget(self.yAxis_lbl1, 10, 11, 1, 1)
    self.box_layout.addWidget(txt_lbl2, 8, 13, 1, 1)
    self.box_layout.addWidget(xAxisTxt_lbl2, 9, 13, 1, 1)
    self.box_layout.addWidget(self.xAxis_lbl2, 9, 14, 1, 1)
    self.box_layout.addWidget(yAxisTxt_lbl2, 10, 13, 1, 1)
    self.box_layout.addWidget(self.yAxis_lbl2, 10, 14, 1, 1)

    # self.box_layout.setColumnMinimumWidth(0, 10)
    self.box_layout.setColumnMinimumWidth(1, 10)
    # self.box_layout.setColumnMinimumWidth(2, 60)
    # self.box_layout.setColumnMinimumWidth(3, 10)
    self.box_layout.setColumnMinimumWidth(4, 10)
    # box_layout.setColumnMinimumWidth(5, 50)
    self.box_layout.setColumnMinimumWidth(6, 40)
    # box_layout.setColumnMinimumWidth(7, 10)
    # box_layout.setColumnMinimumWidth(8, 50)
    self.box_layout.setColumnMinimumWidth(9, 50)
    # box_layout.setColumnMinimumWidth(10, 50)
    # box_layout.setColumnMinimumWidth(11, 100)
    self.box_layout.setColumnMinimumWidth(12, 50)
    self.analysisGroupBox.setLayout(self.box_layout)


    # create menu on the menubar
    connectivity0 = ft.QAction('4', self, checkable=True, checked=True)
    connectivity1 = ft.QAction('8', self, checkable=True, checked=False)
    showFrameLargeBtn_HT = ft.QAction('Show filtered frame', self)
    showFrameLargeBtn_HT.triggered.connect(self.showFrameLargeBtn_HT_clicked)
    self.filterLight_HT = ft.QAction('Ignore flashing light', self)
    self.filterLight_HT.setCheckable(True)
    self.lightROIBtn_HT = ft.QAction('Pick bright region', self)
    self.lightROIBtn_HT.triggered.connect(self.lightROIBtn_HT_clicked)
    self.absValBtn_HT = ft.QAction('Absolute values', self)
    self.absValBtn_HT.triggered.connect(self.absValBtn_HT_clicked)
    self.showEdges_HT = ft.QAction('Show edges location', self)
    self.showEdges_HT.setCheckable(True)
    self.showEdges_HT.setChecked(True)
    self.exportEdges_HT = ft.QAction('Output video analysis', self)
    self.exportEdges_HT.setCheckable(True)
    #CAS Export with tracking line
    self.exportTrackOverlay_HT = ft.QAction('Video tracking overlay')
    self.exportTrackOverlay_HT.setCheckable(True)

    self.HTmenu = self.menu.addMenu('&HSV Tracking')

    connectivitySub = self.HTmenu.addMenu('Connectivity (px)')
    connectivitySub.addAction(connectivity0)
    connectivitySub.addAction(connectivity1)
    self.connectivityGroup = ft.QActionGroup(self)
    self.connectivityGroup.addAction(connectivity0)
    self.connectivityGroup.addAction(connectivity1)
    self.connectivityGroup.setExclusive(True)

    self.HTmenu.addAction(showFrameLargeBtn_HT)
    self.HTmenu.addAction(self.filterLight_HT)
    self.HTmenu.addAction(self.lightROIBtn_HT)
    self.HTmenu.addAction(self.absValBtn_HT)
    self.HTmenu.addAction(self.showEdges_HT)
    self.HTmenu.addAction(self.exportEdges_HT)
    self.HTmenu.addAction(self.exportTrackOverlay_HT)


    # if ft.sys.platform == 'darwin':
    #     self.HSVTrackingBox = ft.QGroupBox(' ', self.analysisGroupBox)
    #     self.HSVTrackingBox.setGeometry(0, 0, 1050, 390)
    #
    #     # size of GUI labels:
    #     h_lbl = 22
    #     h_txt = 30
    #     h_btn = 30
    #     h_btn_arrows = 30
    #     h_slider = 25
    #
    #     if self.pyqtVer == '5': #PyQt5 GUI will be removed after FlameTrackerv1.1.8
    #         # first column without hsv channels objects
    #         # x1 = [ 10,   5,  10, 140,  10,  10, 145,  10, 120]
    #         # y1 = [ 20,  45, 280, 283, 305, 330, 334, 360, 360]
    #         # w1 = [100, 150, 150,  35, 170, 140,  30, 100,  60]
    #         x1 = [10,  90,  10, 135,  10,  10, 135,  10, 130,  10]
    #         y1 = [20,  20, 255, 258, 285, 310, 314, 335, 335, 360]
    #         w1 = [80, 110, 150,  40, 170, 140,  40, 100,  50, 150]
    #
    #         # first column - 'hsv' objects
    #         x_hsv = [ 10,  10,  35, 175,  60,  10,  35, 175,  60]
    #         w_hsv = [100, 100,  30,  30, 120, 100,  30,  30, 120]
    #
    #         # y_h   = [ 70,  92,  90,  90,  95, 114, 112, 112, 117]
    #         # y_s   = [140, 162, 160, 160, 165, 184, 182, 182, 187]
    #         # y_v   = [210, 232, 230, 230, 235, 254, 252, 252, 257]
    #         y_h = [ 45,  67,  65,  65,  70,  89,  87,  87,  92]
    #         y_s = [115, 137, 135, 135, 140, 159, 157, 157, 162]
    #         y_v = [185, 208, 205, 205, 210, 229, 227, 227, 232]
    #
    #         # second column
    #         # x2 = [210, 210, 210, 220, 210, 220, 220, 325, 210, 210, 210]
    #         # y2 = [ 30,  60,  90, 120, 145, 170, 200, 204, 230, 260, 290]
    #         # w2 = [150, 150, 150, 120, 150, 135, 130,  30, 150, 150, 150]
    #         x2 = [220, 220, 220, 220, 315, 220, 220, 220, 220, 220, 220, 220, 220]
    #         y2 = [ 20,  50,  80, 110, 114, 140, 170, 200, 230, 260, 290, 320, 350]
    #         w2 = [135, 135, 135, 120,  40, 135, 135, 135, 135, 135, 135, 135, 135]
    #
    #     elif self.pyqtVer == '6':
    #         # first column without hsv channels objects
    #         # x1 = [ 10,   5,  10, 140,  10,  10, 145,  10, 120]
    #         # y1 = [ 20,  45, 280, 283, 305, 330, 334, 360, 360]
    #         # w1 = [100, 150, 150,  35, 170, 140,  30, 100,  60]
    #         x1 = [10,  90,  10, 135,  10,  10, 135,  10, 130,  10]
    #         y1 = [20,  20, 255, 258, 285, 310, 314, 335, 335, 360]
    #         w1 = [80, 110, 150,  40, 170, 140,  40, 100,  50, 150]
    #
    #         # first column - 'hsv' objects
    #         x_hsv = [ 10,  10,  40, 180,  60,  10,  40, 180,  60]
    #         w_hsv = [100, 100,  20,  20, 120, 100,  20,  20, 120]
    #
    #         # y_h   = [ 70,  92,  90,  90,  95, 114, 112, 112, 117]
    #         # y_s   = [140, 162, 160, 160, 165, 184, 182, 182, 187]
    #         # y_v   = [210, 232, 230, 230, 235, 254, 252, 252, 257]
    #         y_h = [ 45,  67,  65,  65,  70,  89,  87,  87,  92]
    #         y_s = [115, 137, 135, 135, 140, 159, 157, 157, 162]
    #         y_v = [185, 208, 205, 205, 210, 229, 227, 227, 232]
    #
    #         # second column
    #         # x2 = [220, 220, 220, 220, 220, 220, 220, 325, 220, 220, 220, 220, 220, 220]
    #         # y2 = [ 30,  60,  90, 120, 145, 170, 200, 204, 230, 260, 290, 315, 335, 360]
    #         # w2 = [135, 135, 135, 120, 135, 135, 130,  30, 135, 135, 135, 135, 135, 135]
    #         x2 = [220, 220, 220, 220, 315, 220, 220, 220, 220, 220, 220, 220, 220]
    #         y2 = [ 20,  50,  80, 110, 114, 140, 170, 200, 230, 260, 290, 320, 350]
    #         w2 = [135, 135, 135, 120,  40, 135, 135, 135, 135, 135, 135, 135, 135]
    #     # other objects
    #     # x3 = [780, 930, 780, 780]
    #     # y3 = [275, 275, 300, 325]
    #     # w3 = [135, 115, 135, 130]
    #     x3 = [370, 370, 370, 620, 620, 660, 620, 660, 860, 860, 900, 860, 900]
    #     y3 = [280, 305, 330, 280, 305, 310, 330, 335, 280, 305, 310, 330, 335]
    #     w3 = [135, 135, 150, 135,  80, 150,  80, 150, 135,  80, 150,  80, 150]
    #
    #     # labels (since there's only two, in this case I wrote the entire set of coord.)
    #     lbl1 = [370,  25, 670, 125]
    #     lbl2 = [370, 150, 670, 125]
    #
    # elif ft.sys.platform == 'win32':
    #     self.HSVTrackingBox = ft.QGroupBox('Analysis box', self.analysisGroupBox)
    #     self.HSVTrackingBox.setGeometry(0, 0, 1050, 390)
    #
    #     # size of GUI labels:
    #     h_lbl = 20
    #     h_txt = 25
    #     h_btn = 20
    #     h_btn_arrows = 20
    #     h_slider = 15
    #
    #     # first column without hsv channels objects
    #     # x1 = [ 10,  10,  10, 140,  10,  10, 145,  10, 120]
    #     # y1 = [ 10,  35, 255, 260, 280, 295, 300, 325, 330]
    #     # w1 = [100, 150, 150,  35, 170, 140,  30, 100,  60]
    #     x1 = [10, 100,  10, 140,  10,  10, 140,  10, 140,  25]
    #     y1 = [15,  17, 245, 248, 275, 295, 298, 320, 322, 345]
    #     w1 = [85, 100, 150,  50, 170, 140,  50, 100,  50, 150]
    #
    #     # first column - 'hsv' objects
    #     # x_hsv = [ 10,  10,  35, 175,  60,  10,  35, 175,  60]
    #     # w_hsv = [100, 100,  20,  20, 110, 100,  20,  20, 110]
    #     x_hsv = [ 10,  10, 40, 180,  60,  10,  40, 180,  60]
    #     w_hsv = [100, 100, 20,  20, 120, 100,  20,  20, 120]
    #
    #     # y_h   = [ 60,  80,  85,  85,  88, 100, 105, 105, 108]
    #     # y_s   = [125, 145, 150, 150, 153, 165, 170, 170, 173]
    #     # y_v   = [190, 210, 215, 215, 218, 230, 235, 235, 238]
    #     y_h = [ 35,  55,  57,  57,  60,  80,  82,  82,  85]
    #     y_s = [105, 125, 127, 127, 130, 150, 152, 152, 155]
    #     y_v = [175, 195, 197, 197, 200, 220, 222, 222, 225]
    #
    #     # second column
    #     # x2 = [210, 210, 210, 220, 210, 220, 220, 325, 210, 210, 210]
    #     # y2 = [ 30,  60,  90, 120, 145, 170, 200, 204, 230, 260, 290]
    #     # w2 = [140, 140, 140, 120, 140, 135, 130,  30, 140, 140, 140]
    #     x2 = [220, 220, 220, 220, 315, 220, 220, 220, 220, 220, 220, 220, 220]
    #     y2 = [ 15,  40,  65,  90,  92, 120, 150, 180, 210, 240, 270, 300, 330]
    #     w2 = [135, 135, 135, 120,  40, 135, 135, 135, 135, 135, 135, 135, 135]
    #
    #
    #     # other objects
    #     # x3 = [780, 930, 780, 780]
    #     # y3 = [275, 275, 300, 325]
    #     # w3 = [135, 115, 135, 130]
    #     x3 = [370, 370, 370, 580, 580, 620, 580, 620, 820, 820, 860, 820, 860]
    #     y3 = [280, 305, 330, 280, 305, 307, 330, 332, 280, 305, 307, 330, 332]
    #     w3 = [150, 150, 160, 135,  80, 150,  80, 150, 135,  80, 150,  80, 150]
    #
    #
    #     # labels (since there's only two, in this case I wrote the entire set of coord.)
    #     lbl1 = [370,  25, 670, 125]
    #     lbl2 = [370, 150, 670, 125]
    #
    # elif ft.sys.platform == 'linux':
    #     self.HSVTrackingBox = ft.QGroupBox(' ', self.analysisGroupBox)
    #     self.HSVTrackingBox.setGeometry(0, 0, 1050, 390)
    #
    #     # size of GUI labels:
    #     h_lbl = 22
    #     h_txt = 30
    #     h_btn = 30
    #     h_btn_arrows = 30
    #     h_slider = 25
    #
    #     # first column without hsv channels objects
    #     # x1 = [ 10,   5,  10, 140,  10,  10, 145,  10, 120]
    #     # y1 = [ 20,  45, 280, 283, 305, 330, 334, 360, 360]
    #     # w1 = [100, 150, 150,  35, 170, 140,  30, 100,  60]
    #     x1 = [10,  90,  10, 135,  10,  10, 135,  10, 130,  10]
    #     y1 = [20,  20, 255, 258, 285, 310, 314, 335, 335, 360]
    #     w1 = [80, 110, 150,  40, 170, 140,  40, 100,  50, 150]
    #
    #     # first column - 'hsv' objects
    #     x_hsv = [ 10,  10,  35, 175,  60,  10,  35, 175,  60]
    #     w_hsv = [100, 100,  30,  30, 120, 100,  30,  30, 120]
    #
    #     # y_h   = [ 70,  92,  90,  90,  95, 114, 112, 112, 117]
    #     # y_s   = [140, 162, 160, 160, 165, 184, 182, 182, 187]
    #     # y_v   = [210, 232, 230, 230, 235, 254, 252, 252, 257]
    #     y_h = [ 45,  67,  65,  65,  70,  89,  87,  87,  92]
    #     y_s = [115, 137, 135, 135, 140, 159, 157, 157, 162]
    #     y_v = [185, 208, 205, 205, 210, 229, 227, 227, 232]
    #
    #     # second column
    #     # x2 = [210, 210, 210, 220, 210, 220, 220, 325, 210, 210, 210]
    #     # y2 = [ 30,  60,  90, 120, 145, 170, 200, 204, 230, 260, 290]
    #     # w2 = [150, 150, 150, 120, 150, 135, 130,  30, 150, 150, 150]
    #     x2 = [220, 220, 220, 220, 315, 220, 220, 220, 220, 220, 220, 220, 220]
    #     y2 = [ 20,  50,  80, 110, 114, 140, 170, 200, 230, 260, 290, 320, 350]
    #     w2 = [135, 135, 135, 120,  40, 135, 135, 135, 135, 135, 135, 135, 135]
    #
    #     # other objects
    #     # x3 = [780, 930, 780, 780]
    #     # y3 = [275, 275, 300, 325]
    #     # w3 = [135, 115, 135, 130]
    #     x3 = [370, 370, 370, 620, 620, 660, 620, 660, 860, 860, 900, 860, 900]
    #     y3 = [280, 305, 330, 280, 305, 310, 330, 335, 280, 305, 310, 330, 335]
    #     w3 = [135, 135, 150, 135,  80, 150,  80, 150, 135,  80, 150,  80, 150]
    #
    #     # labels (since there's only two, in this case I wrote the entire set of coord.)
    #     lbl1 = [370,  25, 670, 125]
    #     lbl2 = [370, 150, 670, 125]

    # self.HSVTrackingBox.setStyleSheet('background-color: None')
    #
    # # first column
    # directionBoxTxt = ft.QLabel('Flame spread:', self.HSVTrackingBox)
    # directionBoxTxt.setGeometry(x1[0], y1[0], w1[0], h_txt)
    # self.directionBox = ft.QComboBox(self.HSVTrackingBox)
    # self.directionBox.setGeometry(x1[1], y1[1], w1[1], h_btn)
    # self.directionBox.addItem('Left to right')
    # self.directionBox.addItem('Right to left')
    # # if self.pyqtVer == '5':
    # #     self.directionBox.activated[str].connect(self.directionHT_clicked)
    # # elif self.pyqtVer == '6':
    # #     self.directionBox.activated.connect(self.directionHT_clicked)
    #
    # filterParticleTxt = ft.QLabel('Filter particles:', self.HSVTrackingBox)
    # filterParticleTxt.setGeometry(x1[2], y1[2], w1[2], h_txt)
    # self.particleSldrMax = ft.QLineEdit('1000', self.HSVTrackingBox)
    # self.particleSldrMax.setGeometry(x1[3], y1[3], w1[3], h_lbl)
    # if self.pyqtVer == '5':
    #     self.filterParticleSldr_HT = ft.QSlider(ft.Qt.Horizontal, self.HSVTrackingBox)
    # elif self.pyqtVer == '6':
    #     self.filterParticleSldr_HT = ft.QSlider(ft.Qt.Orientation.Horizontal, self.HSVTrackingBox)
    # self.filterParticleSldr_HT.setGeometry(x1[4], y1[4], w1[4], h_slider)
    # self.filterParticleSldr_HT.setMinimum(1)
    # self.filterParticleSldr_HT.setMaximum(1000)
    # self.filterParticleSldr_HT.setValue(20) #	was defulted to 10, but experience says around ~1228 or ~350 to not filter too much
    # self.filterParticleSldr_HT.sliderReleased.connect(self.filterParticleSldr_HT_released)
    # avgLE_txt = ft.QLabel('#px to locate edges:', self.HSVTrackingBox)
    # avgLE_txt.setGeometry(x1[5], y1[5], w1[5], h_txt)
    # self.avgLEIn_HT = ft.QLineEdit('10', self.HSVTrackingBox) #was defaulted to 1, but experience says around 5-10
    # self.avgLEIn_HT.setGeometry(x1[6], y1[6], w1[6], h_lbl)
    # connectivityTxt = ft.QLabel('Connectivity (px):', self.HSVTrackingBox)
    # connectivityTxt.setGeometry(x1[7], y1[7], w1[7], h_txt)
    # self.connectivityBox = ft.QComboBox(self.HSVTrackingBox)
    # self.connectivityBox.setGeometry(x1[8], y1[8], w1[8], h_btn)
    # self.connectivityBox.addItem('4')
    # self.connectivityBox.addItem('8')
    # # if self.pyqtVer == '5':
    # #     self.connectivityBox.activated[str].connect(self.connectivityBoxHT_clicked)
    # # elif self.pyqtVer == '6':
    # #     self.connectivityBox.activated.connect(self.connectivityBoxHT_clicked)
    # self.showFrameLargeBtn_HT = ft.QPushButton('Show frames', self.HSVTrackingBox)
    # # self.showFrameLargeBtn_HT.setGeometry(x3[1], y3[1], w3[1], h_btn)
    # self.showFrameLargeBtn_HT.setGeometry(x1[9], y1[9], w1[9], h_btn)
    # self.showFrameLargeBtn_HT.clicked.connect(self.showFrameLargeBtn_HT_clicked)
    #
    # hueChannelTxt = ft.QLabel('Hue:', self.HSVTrackingBox)
    # hueChannelTxt.setGeometry(x_hsv[0], y_h[0], w_hsv[0], h_txt)
    # hueMinTxt = ft.QLabel('Min:', self.HSVTrackingBox)
    # hueMinTxt.setGeometry(x_hsv[1], y_h[1], w_hsv[1], h_txt)
    # self.hueMinLeftBtn_HT = ft.QPushButton('<', self.HSVTrackingBox)
    # self.hueMinLeftBtn_HT.setGeometry(x_hsv[2], y_h[2], w_hsv[2], h_btn_arrows)
    # self.hueMinLeftBtn_HT.clicked.connect(self.hueMinLeftBtn_HT_clicked)
    # self.hueMinRightBtn_HT = ft.QPushButton('>', self.HSVTrackingBox)
    # self.hueMinRightBtn_HT.setGeometry(x_hsv[3], y_h[3], w_hsv[3], h_btn_arrows)
    # self.hueMinRightBtn_HT.clicked.connect(self.hueMinRightBtn_HT_clicked)
    # # CAS slider setting:
    # if self.pyqtVer == '5':
    #     self.hueMinSlider = ft.QSlider(ft.Qt.Horizontal, self.HSVTrackingBox)
    # elif self.pyqtVer == '6':
    #     self.hueMinSlider = ft.QSlider(ft.Qt.Orientation.Horizontal, self.HSVTrackingBox)
    # self.hueMinSlider.setGeometry(x_hsv[4], y_h[4], w_hsv[4], h_slider)
    # self.hueMinSlider.setMinimum(0)
    # self.hueMinSlider.setMaximum(180) # since stored as H/2 for 8-bit (normally 0-360)
    # self.hueMinSlider.setValue(80) # Default to include blue values - 92=~185 deg Min Hue
    # self.hueMinSlider.sliderReleased.connect(self.singleHSVSlider_released)
    # self.hueMinSlider.valueChanged.connect(self.singleHSVSlider_released) #LC We need to check this line. I had to remove one from the other files (changed or released) because on Mac it counts twice
    # hueMaxTxt = ft.QLabel('Max:', self.HSVTrackingBox)
    # hueMaxTxt.setGeometry(x_hsv[5], y_h[5], w_hsv[5], h_txt)
    # self.hueMaxLeftBtn_HT = ft.QPushButton('<', self.HSVTrackingBox)
    # self.hueMaxLeftBtn_HT.setGeometry(x_hsv[6], y_h[6], w_hsv[6], h_btn_arrows)
    # self.hueMaxLeftBtn_HT.clicked.connect(self.hueMaxLeftBtn_HT_clicked)
    # self.hueMaxRightBtn_HT = ft.QPushButton('>', self.HSVTrackingBox)
    # self.hueMaxRightBtn_HT.setGeometry(x_hsv[7], y_h[7], w_hsv[7], h_btn_arrows)
    # self.hueMaxRightBtn_HT.clicked.connect(self.hueMaxRightBtn_HT_clicked)
    # # CAS slider setting:
    # if self.pyqtVer == '5':
    #     self.hueMaxSlider = ft.QSlider(ft.Qt.Horizontal, self.HSVTrackingBox)
    # elif self.pyqtVer == '6':
    #     self.hueMaxSlider = ft.QSlider(ft.Qt.Orientation.Horizontal, self.HSVTrackingBox)
    # self.hueMaxSlider.setGeometry(x_hsv[8], y_h[8], w_hsv[8], h_slider)
    # self.hueMaxSlider.setMinimum(0)
    # self.hueMaxSlider.setMaximum(180) # since stored as H/2 for 8-bit (normally 0-360)
    # self.hueMaxSlider.setValue(163) # Default to include blue values - 130=~260 deg Max Hue
    # self.hueMaxSlider.sliderReleased.connect(self.singleHSVSlider_released)
    # self.hueMaxSlider.valueChanged.connect(self.singleHSVSlider_released)
    #
    # satChannelTxt = ft.QLabel('Saturation:', self.HSVTrackingBox)
    # satChannelTxt.setGeometry(x_hsv[0], y_s[0], w_hsv[0], h_txt)
    # satMinTxt = ft.QLabel('Min:', self.HSVTrackingBox)
    # satMinTxt.setGeometry(x_hsv[1], y_s[1], w_hsv[1], h_txt)
    # self.satMinLeftBtn_HT = ft.QPushButton('<', self.HSVTrackingBox)
    # self.satMinLeftBtn_HT.setGeometry(x_hsv[2], y_s[2], w_hsv[2], h_btn_arrows)
    # self.satMinLeftBtn_HT.clicked.connect(self.satMinLeftBtn_HT_clicked)
    # self.satMinRightBtn_HT = ft.QPushButton('>', self.HSVTrackingBox)
    # self.satMinRightBtn_HT.setGeometry(x_hsv[3], y_s[3], w_hsv[3], h_btn_arrows)
    # self.satMinRightBtn_HT.clicked.connect(self.satMinRightBtn_HT_clicked)
    # # CAS slider setting:
    # if self.pyqtVer == '5':
    #     self.satMinSlider = ft.QSlider(ft.Qt.Horizontal, self.HSVTrackingBox)
    # elif self.pyqtVer == '6':
    #     self.satMinSlider = ft.QSlider(ft.Qt.Orientation.Horizontal, self.HSVTrackingBox)
    # self.satMinSlider.setGeometry(x_hsv[4], y_s[4], w_hsv[4], h_slider)
    # self.satMinSlider.setMinimum(0)
    # self.satMinSlider.setMaximum(255)
    # self.satMinSlider.setValue(30) # Default to include blue values - 100=~40% min Saturation
    # self.satMinSlider.sliderReleased.connect(self.singleHSVSlider_released)
    # self.satMinSlider.valueChanged.connect(self.singleHSVSlider_released)
    # satMaxTxt = ft.QLabel('Max:', self.HSVTrackingBox)
    # satMaxTxt.setGeometry(x_hsv[5], y_s[5], w_hsv[5], h_txt)
    # self.satMaxLeftBtn_HT = ft.QPushButton('<', self.HSVTrackingBox)
    # self.satMaxLeftBtn_HT.setGeometry(x_hsv[6], y_s[6], w_hsv[6], h_btn_arrows)
    # self.satMaxLeftBtn_HT.clicked.connect(self.satMaxLeftBtn_HT_clicked)
    # self.satMaxRightBtn_HT = ft.QPushButton('>', self.HSVTrackingBox)
    # self.satMaxRightBtn_HT.setGeometry(x_hsv[7], y_s[7], w_hsv[7], h_btn_arrows)
    # self.satMaxRightBtn_HT.clicked.connect(self.satMaxRightBtn_HT_clicked)
    # # CAS slider setting:
    # if self.pyqtVer == '5':
    #     self.satMaxSlider = ft.QSlider(ft.Qt.Horizontal, self.HSVTrackingBox)
    # elif self.pyqtVer == '6':
    #     self.satMaxSlider = ft.QSlider(ft.Qt.Orientation.Horizontal, self.HSVTrackingBox)
    # self.satMaxSlider.setGeometry(x_hsv[8], y_s[8], w_hsv[8], h_slider)
    # self.satMaxSlider.setMinimum(0)
    # self.satMaxSlider.setMaximum(255)
    # self.satMaxSlider.setValue(255) # Default to some blue value - 255=~100% max Saturation
    # self.satMaxSlider.sliderReleased.connect(self.singleHSVSlider_released)
    # self.satMaxSlider.valueChanged.connect(self.singleHSVSlider_released)
    #
    # valChannelTxt = ft.QLabel('Value:', self.HSVTrackingBox)
    # valChannelTxt.setGeometry(x_hsv[0], y_v[0], w_hsv[0], h_txt)
    # valMinTxt = ft.QLabel('Min:', self.HSVTrackingBox)
    # valMinTxt.setGeometry(x_hsv[1], y_v[1], w_hsv[1], h_txt)
    # self.valMinLeftBtn_HT = ft.QPushButton('<', self.HSVTrackingBox)
    # self.valMinLeftBtn_HT.setGeometry(x_hsv[2], y_v[2], w_hsv[2], h_btn_arrows)
    # self.valMinLeftBtn_HT.clicked.connect(self.valMinLeftBtn_HT_clicked)
    # self.valMinRightBtn_HT = ft.QPushButton('>', self.HSVTrackingBox)
    # self.valMinRightBtn_HT.setGeometry(x_hsv[3], y_v[3], w_hsv[3], h_btn_arrows)
    # self.valMinRightBtn_HT.clicked.connect(self.valMinRightBtn_HT_clicked)
    # # CAS slider setting:
    # if self.pyqtVer == '5':
    #     self.valMinSlider = ft.QSlider(ft.Qt.Horizontal, self.HSVTrackingBox)
    # elif self.pyqtVer == '6':
    #     self.valMinSlider = ft.QSlider(ft.Qt.Orientation.Horizontal, self.HSVTrackingBox)
    # self.valMinSlider.setGeometry(x_hsv[4], y_v[4], w_hsv[4], h_slider)
    # self.valMinSlider.setMinimum(0)
    # self.valMinSlider.setMaximum(255)
    # self.valMinSlider.setValue(20) # Default to some blue value - 63=~25% min Value
    # self.valMinSlider.sliderReleased.connect(self.singleHSVSlider_released)
    # self.valMinSlider.valueChanged.connect(self.singleHSVSlider_released)
    # valMaxTxt = ft.QLabel('Max:', self.HSVTrackingBox)
    # valMaxTxt.setGeometry(x_hsv[5], y_v[5], w_hsv[5], h_txt)
    # self.valMaxLeftBtn_HT = ft.QPushButton('<', self.HSVTrackingBox)
    # self.valMaxLeftBtn_HT.setGeometry(x_hsv[6], y_v[6], w_hsv[6], h_btn_arrows)
    # self.valMaxLeftBtn_HT.clicked.connect(self.valMaxLeftBtn_HT_clicked)
    # self.valMaxRightBtn_HT = ft.QPushButton('>', self.HSVTrackingBox)
    # self.valMaxRightBtn_HT.setGeometry(x_hsv[7], y_v[7], w_hsv[7], h_btn_arrows)
    # self.valMaxRightBtn_HT.clicked.connect(self.valMaxRightBtn_HT_clicked)
    # # CAS slider setting:
    # if self.pyqtVer == '5':
    #     self.valMaxSlider = ft.QSlider(ft.Qt.Horizontal, self.HSVTrackingBox)
    # elif self.pyqtVer == '6':
    #     self.valMaxSlider = ft.QSlider(ft.Qt.Orientation.Horizontal, self.HSVTrackingBox)
    # self.valMaxSlider.setGeometry(x_hsv[8], y_v[8], w_hsv[8], h_slider)
    # self.valMaxSlider.setMinimum(0)
    # self.valMaxSlider.setMaximum(255)
    # self.valMaxSlider.setValue(255) # Default to some blue value - 255=~100% max Value
    # self.valMaxSlider.sliderReleased.connect(self.singleHSVSlider_released)
    # self.valMaxSlider.valueChanged.connect(self.singleHSVSlider_released)
    #
    # #second column
    # trackingTxt = ft.QLabel('Flame tracking:', self.HSVTrackingBox)
    # trackingTxt.setGeometry(x2[0], y2[0], w2[0], h_txt)
    # self.lightROIBtn_HT = ft.QPushButton('Pick bright region', self.HSVTrackingBox)
    # self.lightROIBtn_HT.setGeometry(x2[1], y2[1], w2[1], h_btn)
    # self.lightROIBtn_HT.clicked.connect(self.lightROIBtn_HT_clicked)
    # self.filterLight_HT = ft.QCheckBox('Ignore flashing light', self.HSVTrackingBox)
    # self.filterLight_HT.setGeometry(x2[2], y2[2], w2[2], h_btn)
    # movAvgTxt = ft.QLabel('Moving avg pts:', self.HSVTrackingBox)
    # movAvgTxt.setGeometry(x2[3], y2[3], w2[3], h_txt)
    # self.movAvgIn_HT = ft.QLineEdit('5', self.HSVTrackingBox) #was defaulted to 2, experience says around 5 better
    # self.movAvgIn_HT.setGeometry(x2[4], y2[4], w2[4], h_lbl)
    # self.HSVTrackingBtn = ft.QPushButton('Start tracking', self.HSVTrackingBox)
    # self.HSVTrackingBtn.setGeometry(x2[5], y2[5], w2[5], h_btn)
    # self.HSVTrackingBtn.clicked.connect(self.HSVTrackingBtn_clicked)
    # self.saveBtn_HT = ft.QPushButton('Save data', self.HSVTrackingBox)
    # self.saveBtn_HT.setGeometry(x2[6], y2[6], w2[6], h_btn)
    # self.saveBtn_HT.clicked.connect(self.saveBtn_HT_clicked)
    # self.absValBtn_HT = ft.QPushButton('Absolute values', self.HSVTrackingBox)
    # self.absValBtn_HT.setGeometry(x2[7], y2[7], w2[7], h_btn)
    # self.absValBtn_HT.clicked.connect(self.absValBtn_HT_clicked)
    # self.saveChannelsBtn_HT = ft.QPushButton('Save HSV values', self.HSVTrackingBox)
    # self.saveChannelsBtn_HT.setGeometry(x2[8], y2[8], w2[8], h_btn)
    # self.saveChannelsBtn_HT.clicked.connect(self.saveChannelsBtn_HT_clicked)
    # self.loadChannelsBtn_HT = ft.QPushButton('Load HSV values', self.HSVTrackingBox)
    # self.loadChannelsBtn_HT.setGeometry(x2[9], y2[9], w2[9], h_btn)
    # self.loadChannelsBtn_HT.clicked.connect(self.loadChannelsBtn_HT_clicked)
    # self.updateGraphsBtn_HT = ft.QPushButton('Update graphs', self.HSVTrackingBox)
    # self.updateGraphsBtn_HT.setGeometry(x2[10], y2[10], w2[10], h_btn)
    # self.updateGraphsBtn_HT.clicked.connect(self.updateGraphsBtn_HT_clicked)
    # self.helpBtn_HT = ft.QPushButton('Help', self.HSVTrackingBox)
    # self.helpBtn_HT.setGeometry(x2[11], y2[11], w2[11], h_btn)
    # self.helpBtn_HT.clicked.connect(self.helpBtn_HT_clicked)
    # # trackingTxt = ft.QLabel('Flame tracking:', self.HSVTrackingBox)
    # # trackingTxt.setGeometry(x2[3], y2[3], w2[3], h_txt)
    #
    # # self.lightROIBtn_HT = ft.QPushButton('Pick bright region', self.HSVTrackingBox)
    # # self.lightROIBtn_HT.setGeometry(x2[4], y2[4], w2[4], h_btn)
    # # self.lightROIBtn_HT.clicked.connect(self.lightROIBtn_HT_clicked)
    # # self.filterLight_HT = ft.QCheckBox('Ignore flashing light', self.HSVTrackingBox)
    # # self.filterLight_HT.setGeometry(x2[5], y2[5], w2[5], h_btn)
    # # movAvgTxt = ft.QLabel('Moving avg points:', self.HSVTrackingBox)
    # # movAvgTxt.setGeometry(x2[6], y2[6], w2[6], h_txt)
    # # self.movAvgIn_HT = ft.QLineEdit('5', self.HSVTrackingBox) #was defaulted to 2, experience says around 5 better
    # # self.movAvgIn_HT.setGeometry(x2[7], y2[7], w2[7], h_lbl)
    # # self.HSVTrackingBtn = ft.QPushButton('Start tracking', self.HSVTrackingBox)
    # # self.HSVTrackingBtn.setGeometry(x2[8], y2[8], w2[8], h_btn)
    # # self.HSVTrackingBtn.clicked.connect(self.HSVTrackingBtn_clicked)
    # # self.absValBtn_HT = ft.QPushButton('Absolute values', self.HSVTrackingBox)
    # # self.absValBtn_HT.setGeometry(x2[9], y2[9], w2[9], h_btn)
    # # self.absValBtn_HT.clicked.connect(self.absValBtn_HT_clicked)
    # # self.saveBtn_HT = ft.QPushButton('Save data', self.HSVTrackingBox)
    # # self.saveBtn_HT.setGeometry(x2[10], y2[10], w2[10], h_btn)
    # # self.saveBtn_HT.clicked.connect(self.saveBtn_HT_clicked)
    #
    # # other objects
    # self.showEdges = ft.QCheckBox('Show edges location', self.HSVTrackingBox)
    # self.showEdges.setGeometry(x3[0], y3[0], w3[0], h_btn)
    # self.showEdges.setChecked(True)
    # self.exportEdges_HT = ft.QCheckBox('Output video analysis', self.HSVTrackingBox)
    # # self.exportEdges_HT.setGeometry(x3[2], y3[2], w3[2], h_btn)
    # self.exportEdges_HT.setGeometry(x3[1], y3[1], w3[1], h_btn)
    # # self.showFrameLargeBtn_HT = ft.QPushButton('Show frames', self.HSVTrackingBox)
    # # # self.showFrameLargeBtn_HT.setGeometry(x3[1], y3[1], w3[1], h_btn)
    # # self.showFrameLargeBtn_HT.setGeometry(x2[13], y2[13], w2[13], h_btn)
    # # self.showFrameLargeBtn_HT.clicked.connect(self.showFrameLargeBtn_HT_clicked)
    # #CAS Export with tracking line
    # self.exportTrackOverlay_HT = ft.QCheckBox('Video Tracking Overlay', self.HSVTrackingBox)
    # # self.exportTrackOverlay_HT.setGeometry(x3[3], y3[3], w3[3], h_btn)
    # self.exportTrackOverlay_HT.setGeometry(x3[2], y3[2], w3[2], h_btn)
    # txt_lbl1 = ft.QLabel('Graph #1:', self.HSVTrackingBox)
    # txt_lbl1.setGeometry(x3[3], y3[3], w3[3], h_txt)
    # xAxisTxt_lbl1 = ft.QLabel('x axis:', self.HSVTrackingBox)
    # xAxisTxt_lbl1.setGeometry(x3[4], y3[4], w3[4], h_txt)
    # self.xAxis_lbl1 = ft.QComboBox(self.HSVTrackingBox)
    # self.xAxis_lbl1.setGeometry(x3[5], y3[5], w3[5], h_lbl)
    # self.xAxis_lbl1.addItem('Time [s]')
    # self.xAxis_lbl1.addItem('Frame #')
    # yAxisTxt_lbl1 = ft.QLabel('y axis:', self.HSVTrackingBox)
    # yAxisTxt_lbl1.setGeometry(x3[6], y3[6], w3[6], h_txt)
    # self.yAxis_lbl1 = ft.QComboBox(self.HSVTrackingBox)
    # self.yAxis_lbl1.setGeometry(x3[7], y3[7], w3[7], h_lbl)
    # self.yAxis_lbl1.addItem('Position [mm]')
    # self.yAxis_lbl1.addItem('Position [px]')
    # self.yAxis_lbl1.addItem('Flame length [mm]')
    # self.yAxis_lbl1.addItem('Spread rate [mm/s]')
    # txt_lbl2 = ft.QLabel('Graph #2:', self.HSVTrackingBox)
    # txt_lbl2.setGeometry(x3[8], y3[8], w3[8], h_txt)
    # xAxisTxt_lbl2 = ft.QLabel('x axis:', self.HSVTrackingBox)
    # xAxisTxt_lbl2.setGeometry(x3[9], y3[9], w3[9], h_txt)
    # self.xAxis_lbl2 = ft.QComboBox(self.HSVTrackingBox)
    # self.xAxis_lbl2.setGeometry(x3[10], y3[10], w3[10], h_lbl)
    # self.xAxis_lbl2.addItem('Time [s]')
    # self.xAxis_lbl2.addItem('Frame #')
    # yAxisTxt_lbl2 = ft.QLabel('y axis:', self.HSVTrackingBox)
    # yAxisTxt_lbl2.setGeometry(x3[11], y3[11], w3[11], h_txt)
    # self.yAxis_lbl2 = ft.QComboBox(self.HSVTrackingBox)
    # self.yAxis_lbl2.setGeometry(x3[12], y3[12], w3[12], h_lbl)
    # self.yAxis_lbl2.addItem('Spread rate [mm/s]')
    # self.yAxis_lbl2.addItem('Flame length [mm]')
    # self.yAxis_lbl2.addItem('Position [mm]')
    # self.yAxis_lbl2.addItem('Position [px]')
    #
    # # first label
    # self.lbl1_HT = ft.QLabel(self.HSVTrackingBox)
    # self.lbl1_HT.setGeometry(lbl1[0], lbl1[1], lbl1[2], lbl1[3])
    # self.lbl1_HT.setStyleSheet('background-color: white')
    #
    # # second label
    # self.lbl2_HT = ft.QLabel(self.HSVTrackingBox)
    # self.lbl2_HT.setGeometry(lbl2[0], lbl2[1], lbl2[2], lbl2[3])
    # self.lbl2_HT.setStyleSheet('background-color: white')
