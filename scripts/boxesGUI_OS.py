"""
Flame Tracker. This program is designed to track flames or bright objects in videos or images.
Copyright (C) 2020,2021  Luca Carmignani; 2021 Charles Scudiere

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

from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from itertools import zip_longest
from pyqtgraph import PlotWidget, plot

import flameTracker as ft
import pyqtgraph as pg
import sys

def previewBox(self):
#    global OStype

    self.setWindowTitle('Flame Tracker (v1.1.12beta)')

    if sys.platform == 'darwin':
        # OStype = 'mac'
        self.setStyleSheet('font: 12pt Helvetica')
        self.setGeometry(10, 10, 1070, 800)
    elif sys.platform == 'win32':
#        OStype = 'win'
        self.setStyleSheet('font: 12pt Helvetica')
        self.setGeometry(25, 25, 1070, 780)
    elif sys.platform == 'linux':
#        OStype = 'lin'
        self.setStyleSheet('font: 12pt Helvetica')
        self.setGeometry(10, 10, 1070, 780)
    else:
        print('\n!!! Warning: Unable to detect OS!!!')

    # create GUI boxes:
    parametersBox = QGroupBox('Preview box', self)
    self.analysisGroupBox = QGroupBox('Analysis box', self)
    # this text box is only shown at the beginning
    tempBox = QGroupBox(' ', self.analysisGroupBox)
    tempBox.setGeometry(0, 0, 1050, 390)
    introTxt = QLabel('Select the analysis method from -Choose analysis- to activate this panel', tempBox)
    introTxt.setGeometry(100, 100, 600, 100)
    introTxt.setStyleSheet('font: 16pt Helvetica')

    # OS-dependent coordinates for GUI objects:
    if sys.platform == 'darwin':
        parametersBox.setGeometry(10, 5, 1050, 390)
        self.analysisGroupBox.setGeometry(10, 400, 1050, 390)

        # size of GUI labels:
        h_msgLbl = 110
        h_lbl = 20
        h_txt = 30
        h_btn = 30
        h_slider = 25

        # first column
        x1 = [10,    5,   5,  58,  10,  10, 105,  10, 105,  10, 105,  10, 105,  10, 105]
        y1 = [25,  135, 165, 166, 200, 225, 229, 255, 259, 285, 289, 315, 319, 345, 349]
        w1 = [140, 150,  60, 100, 140, 140,  45,  70,  45,  70,  45,  70,  45,  70,  45]

        # second column
        x2 = [180, 180, 265, 180, 265, 180, 265, 180, 265, 170, 170, 180, 265, 180, 265, 180, 265, 180, 265, 170]
        y2 = [ 20,  45,  49,  75,  79, 105, 109, 135, 139, 165, 195, 225, 229, 255, 259, 285, 289, 315, 319, 345]
        w2 = [120,  80,  50,  80,  50,  80,  50,  80,  50, 150, 150,  80,  50,  80,  50,  80,  50,  80,  50, 150]

        # third column
        x3 = [340, 340, 425, 340, 428, 340, 340, 428, 340, 335, 340, 340, 425, 340, 425, 330, 330]
        y3 = [ 20,  45,  49,  75,  82, 105, 130, 138, 160, 190, 230, 255, 259, 285, 289, 315, 345]
        w3 = [100, 120,  50, 150,  45, 115, 150,  45, 115, 100, 150, 130,  45, 130,  45, 150, 150]

        # fourth column
        x4 = [500, 490, 500, 490, 490, 500, 500, 610, 500, 595, 500, 595, 500, 595, 490]
        y4 = [ 20,  45,  70,  95, 125, 155, 200, 199, 225, 229, 255, 259, 285, 289, 315]
        w4 = [ 60, 150, 130, 150, 150, 150, 150,  30, 120,  40, 100,  40, 100,  40, 150]
        # labels
        x5 = [650,   650,  740,   790,       650,   930]
        y5 = [ 35,   310,  314,   310,       340,   310]
        w5 = [390,   120,   45,   100,       390,   115]
        h5 = [270, h_txt, h_lbl, h_btn, h_slider, h_btn]

    elif sys.platform == 'win32':
        parametersBox.setGeometry(10, 5, 1050, 390)
        self.analysisGroupBox.setGeometry(10, 400, 1050, 370)

        # size of GUI labels:
        h_msgLbl = 105
        h_lbl = 20
        h_txt = 30
        h_btn = 25
        h_slider = 15

        # first column
        x1 = [10,   10,  10,  65,  10,  10, 105,  10,  45,  10,  45,  10, 105,  10,  45]
        y1 = [20,  135, 165, 166, 200, 225, 230, 255, 260, 285, 290, 315, 320, 345, 350]
        w1 = [140, 140,  50,  85, 140,  60,  45,  60,  45,  85,  45,  65,  45,  65,  45]

        # second column
        x2 = [170, 170, 260, 170, 260, 170, 260, 170, 260, 170, 170, 170, 260, 170, 260, 170, 260, 170, 260, 170]
        y2 = [ 10,  35,  40,  65,  70,  95, 100, 125, 130, 160, 190, 225, 230, 255, 260, 285, 290, 315, 320, 347]
        w2 = [120,  80,  50,  80,  50,  80,  50,  80,  50, 140,  80,  50,  80,  50,  80,  50,  80,  50,  80, 140]

        # third column
        x3 = [330, 330, 420, 330, 420, 330, 330, 420, 330, 330, 330, 330, 420, 330, 420, 330, 330]
        y3 = [ 10,  35,  39,  65,  70,  95, 110, 115, 140, 165, 195, 220, 225, 250, 255, 280, 315]
        w3 = [100, 120,  50, 150,  50, 137, 150,  50, 137, 100, 140, 130,  50,  60,  60, 140, 140]

        # # fourth column
        x4 = [490, 490, 490, 490, 490, 500, 610, 500, 490, 580, 490, 580, 490, 580, 490]
        y4 = [ 10,  35,  60,  85, 115, 155, 195, 200, 220, 225, 250, 255, 280, 285, 315]
        w4 = [ 60, 140,  60, 140, 140, 140,  20, 150, 120,  50, 100,  50, 100,  50, 140]

        # labels
        x5 = [650,   650,  740,          875,       650,         945]
        y5 = [ 15,   290,  296,          293,       325,         293]
        w5 = [390,   120,   50,          100,       390,          90]
        h5 = [270, h_txt, h_lbl, (h_btn - 2),  h_slider, (h_btn - 2)]

    elif sys.platform == 'linux':
        parametersBox.setGeometry(10, 5, 1050, 390)
        self.analysisGroupBox.setGeometry(10, 400, 1050, 390)

        # size of GUI labels:
        h_msgLbl = 110
        h_lbl = 20
        h_txt = 30
        h_btn = 30
        h_slider = 25

        # first column
        x1 = [10,    5,   5,  58,  10,  10, 105,  10, 105,  10,  45,  10, 105,  10,  45]
        y1 = [25,  135, 165, 166, 200, 225, 229, 255, 259, 285, 289, 315, 319, 345, 349]
        w1 = [140, 150,  60, 100, 140,  70,  45,  70,  45,  90,  45,  70,  45,  70,  45]

        # second column
        x2 = [180, 180, 265, 180, 265, 180, 265, 180, 265, 170, 170, 180, 265, 180, 180, 265, 180, 265, 170]
        y2 = [ 20,  45,  49,  75,  79, 105, 109, 135, 139, 165, 195, 225, 229, 255, 285, 289, 315, 319, 345]
        w2 = [80,   80,  50,  80,  50,  80,  50,  80,  50, 150, 150,  80,  50,  80,  80,  50,  80,  50, 150]

        # third column
        x3 = [340, 340, 425, 340, 428, 340, 340, 428, 340, 325, 335, 340, 425, 340, 425, 330, 330]
        y3 = [ 20,  45,  49,  75,  80, 105, 125, 130, 155, 175, 200, 225, 229, 255, 259, 285, 315]
        w3 = [100, 120,  50, 150,  45, 137, 150,  45, 115, 100, 150, 130,  50,  60,  60, 150, 150]

        # fourth column
        x4 = [500, 490, 500, 490, 490, 500, 500, 610, 500, 595, 500, 595, 500, 595, 490]
        y4 = [ 20,  45,  70,  95, 125, 155, 200, 199, 225, 229, 255, 259, 285, 289, 315]
        w4 = [ 60, 150, 130, 150, 150, 150, 150,  30, 120,  40, 100,  40, 100,  40, 150]

        # labels
        x5 = [650,   650,  740,   790,       650,   930]
        y5 = [ 25,   295,  299,   295,       325,   295]
        w5 = [390,   120,   45,   100,       390,   115]
        h5 = [270, h_txt, h_lbl, h_btn, h_slider, h_btn]

    #self.setStyleSheet('font: 12pt Helvetica')
    #self.setWindowTitle('Flame Tracker (v1.1.2beta)')
    # self.setGeometry(10, 10, 1070, 800)
    #Box to choose video parameters, the widgets are listed below
#    parametersBox = QGroupBox('Preview box', self)
#    parametersBox.setGeometry(10, 5, 1050, 390)
    #This box changes for each analysis;
    #widgets must be declared in the specific py file
#    self.analysisGroupBox = QGroupBox('Analysis box', self)
#    self.analysisGroupBox.setGeometry(10, 400, 1050, 390)


    ### parametersBox
    # first column
    # x_cln1 = 10
    # x_cln2 = 105
    # h_lbl = 20
    # h_txt = 30
    # h_btn = 30
    self.msgLabel = QLabel('Welcome to the Flame Tracker! \n\n Click on the Help button to get started.', parametersBox)
    self.msgLabel.setGeometry(x1[0], y1[0], w1[0], h_msgLbl)
    self.msgLabel.setStyleSheet('background-color: white')
    self.msgLabel.setWordWrap(True)
    self.helpBtn = QPushButton('Help', parametersBox)
    self.helpBtn.setGeometry(x1[1], y1[1], w1[1], h_btn)
    self.helpBtn.clicked.connect(self.helpBtn_clicked)
    self.openBtn = QPushButton('Open', parametersBox)
    self.openBtn.setGeometry(x1[2], y1[2], w1[2], h_btn)
    self.openBtn.clicked.connect(self.openBtn_clicked)
    self.openSelectionBox = QComboBox(parametersBox)
    self.openSelectionBox.setGeometry(x1[3], y1[3], w1[3], h_btn)
    self.openSelectionBox.addItem('Video')
    self.openSelectionBox.addItem('Image(s)')
    self.openSelectionBox.activated[str].connect(self.openSelection_click)
    self.fNameLbl = QLabel('(file name)', parametersBox)
    self.fNameLbl.setGeometry(x1[4], y1[4], w1[4], h_lbl)
    self.fNameLbl.setStyleSheet('background-color: white')
    vWidthTxt = QLabel('Width (px):', parametersBox)
    vWidthTxt.setGeometry(x1[5], y1[5], w1[5], h_txt)
    self.vWidthLbl = QLabel(parametersBox)
    self.vWidthLbl.setGeometry(x1[6], y1[6], w1[6], h_lbl)
    self.vWidthLbl.setStyleSheet('background-color: white')
    vHeightTxt = QLabel('Height (px):', parametersBox)
    vHeightTxt.setGeometry(x1[7], y1[7], w1[7], h_txt)
    self.vHeightLbl = QLabel(parametersBox)
    self.vHeightLbl.setGeometry(x1[8], y1[8], w1[8], h_lbl)
    self.vHeightLbl.setStyleSheet('background-color: white')
    vFpsTxt = QLabel('Frame rate (fps):', parametersBox)
    vFpsTxt.setGeometry(x1[9], y1[9], w1[9], h_txt)
    self.vFpsLbl = QLabel(parametersBox)
    self.vFpsLbl.setGeometry(x1[10], y1[10], w1[10], h_lbl)
    self.vFpsLbl.setStyleSheet('background-color: white')
    vFramesTxt = QLabel('Frames #:', parametersBox)
    vFramesTxt.setGeometry(x1[11], y1[11], w1[11], h_txt)
    self.vFramesLbl = QLabel(parametersBox)
    self.vFramesLbl.setGeometry(x1[12], y1[12], w1[12], h_lbl)
    self.vFramesLbl.setStyleSheet('background-color: white')
    vDurationTxt = QLabel('Duration (s):', parametersBox)
    vDurationTxt.setGeometry(x1[13], y1[13], w1[13], h_txt)
    self.vDurationLbl = QLabel(parametersBox)
    self.vDurationLbl.setGeometry(x1[14], y1[14], w1[14], h_lbl)
    self.vDurationLbl.setStyleSheet('background-color: white')

    #second column
    # x_cln1 = 180
    # x_cln2 = 265
    # w_cln1 = 80
    # w_cln2 = 50
    # h_lbl = 22
    clmn2_Txt = QLabel('Video parameters:', parametersBox)
    clmn2_Txt.setGeometry(x2[0], y2[0], w2[0], h_txt)
    self.firstFrameTxt = QLabel('First frame:', parametersBox)
    self.firstFrameTxt.setGeometry(x2[1], y2[1], w2[1], h_txt)
    self.firstFrameIn = QLineEdit(parametersBox)
    self.firstFrameIn.setGeometry(x2[2], y2[2], w2[2], h_lbl)
    self.lastFrameTxt = QLabel('Last frame:', parametersBox)
    self.lastFrameTxt.setGeometry(x2[3], y2[3], w2[3], h_txt)
    self.lastFrameIn = QLineEdit(parametersBox)
    self.lastFrameIn.setGeometry(x2[4], y2[4], w2[4], h_lbl)
    self.skipFrameTxt = QLabel('Skip frames:', parametersBox)
    self.skipFrameTxt.setGeometry(x2[5], y2[5], w2[5], h_txt)
    self.skipFrameIn = QLineEdit(parametersBox)
    self.skipFrameIn.setGeometry(x2[6], y2[6], w2[6], h_lbl)
    self.scaleTxt = QLabel('Scale (px/mm):', parametersBox)
    self.scaleTxt.setGeometry(x2[7], y2[7], w2[7], h_txt)
    self.scaleIn = QLineEdit(parametersBox)
    self.scaleIn.setGeometry(x2[8], y2[8], w2[8], h_lbl)
    self.measureScaleBtn = QPushButton('Measure scale', parametersBox)
    self.measureScaleBtn.setGeometry(x2[9], y2[9], w2[9], h_btn)
    self.measureScaleBtn.clicked.connect(self.measureScaleBtn_clicked)
    self.refPointBtn = QPushButton('Reference point', parametersBox)
    self.refPointBtn.setGeometry(x2[10], y2[10], w2[10], h_btn)
    self.refPointBtn.clicked.connect(self.refPointBtn_clicked)
    self.roiOneTxt = QLabel('ROI, x:', parametersBox)
    self.roiOneTxt.setGeometry(x2[11], y2[11], w2[11], h_txt)
    self.roiOneIn = QLineEdit(parametersBox)
    self.roiOneIn.setGeometry(x2[12], y2[12], w2[12], h_lbl)
    self.roiTwoTxt = QLabel('ROI, y:', parametersBox)
    self.roiTwoTxt.setGeometry(x2[13], y2[13], w2[13], h_txt)
    self.roiTwoIn = QLineEdit(parametersBox)
    self.roiTwoIn.setGeometry(x2[14], y2[14], w2[14], h_lbl)
    self.roiThreeTxt = QLabel('ROI, w:', parametersBox)
    self.roiThreeTxt.setGeometry(x2[15], y2[15], w2[15], h_txt)
    self.roiThreeIn = QLineEdit(parametersBox)
    self.roiThreeIn.setGeometry(x2[16], y2[16], w2[16], h_lbl)
    self.roiFourTxt = QLabel('ROI, h:', parametersBox)
    self.roiFourTxt.setGeometry(x2[17], y2[17], w2[17], h_txt)
    self.roiFourIn = QLineEdit(parametersBox)
    self.roiFourIn.setGeometry(x2[18], y2[18], w2[18], h_lbl)
    self.roiBtn = QPushButton('Select ROI', parametersBox)
    self.roiBtn.setGeometry(x2[19], y2[19], w2[19], h_btn)
    self.roiBtn.clicked.connect(self.roiBtn_clicked)

    #third column
    # x_cln1 = 340
    # x_cln2 = 425
    # w_cln1 = 60
    # w_cln2 = 50
    adjustFramesTxt = QLabel('Edit frames:', parametersBox)
    adjustFramesTxt.setGeometry(x3[0], y3[0], w3[0], h_txt)
    self.rotationAngleInTxt = QLabel('Rotation (deg):', parametersBox)
    self.rotationAngleInTxt.setGeometry(x3[1], y3[1], w3[1], h_txt)
    self.rotationAngleIn = QLineEdit(parametersBox)
    self.rotationAngleIn.setGeometry(x3[2], y3[2], w3[2], h_lbl)
    self.brightnessTxt = QLabel('Brightness:', parametersBox)
    self.brightnessTxt.setGeometry(x3[3], y3[3], w3[3], h_txt)
    self.brightnessLbl = QLabel('0', parametersBox)
    self.brightnessLbl.setGeometry(x3[4], y3[4], w3[4], h_lbl - 4)
    self.brightnessLbl.setStyleSheet('background-color: white')
    self.brightnessSlider = QSlider(Qt.Horizontal, parametersBox)
    self.brightnessSlider.setGeometry(x3[5], y3[5], w3[5], h_slider)
    self.brightnessSlider.setMinimum(-50)
    self.brightnessSlider.setMaximum(50)
    self.brightnessSlider.setValue(0)
    self.brightnessSlider.sliderReleased.connect(self.editFramesSlider_released)
    self.contrastTxt = QLabel('Contrast:', parametersBox)
    self.contrastTxt.setGeometry(x3[6], y3[6], w3[6], h_txt)
    self.contrastLbl = QLabel('0', parametersBox)
    self.contrastLbl.setGeometry(x3[7], y3[7], w3[7], h_lbl - 4)
    self.contrastLbl.setStyleSheet('background-color: white')
    self.contrastSlider = QSlider(Qt.Horizontal, parametersBox)
    self.contrastSlider.setGeometry(x3[8], y3[8], w3[8], h_slider)
    self.contrastSlider.setMinimum(-100)
    self.contrastSlider.setMaximum(+100)
    self.contrastSlider.setValue(0)
    self.contrastSlider.sliderReleased.connect(self.editFramesSlider_released)
    self.grayscale = QCheckBox('Grayscale', parametersBox)
    self.grayscale.setGeometry(x3[9], y3[9], w3[9], h_btn)
    correctionTxt = QLabel('Correction lengths (mm):', parametersBox)
    correctionTxt.setGeometry(x3[10], y3[10], w3[10], h_txt)
    self.sLengthTxt = QLabel('Horizontal:', parametersBox)
    self.sLengthTxt.setGeometry(x3[11], y3[11], w3[11], h_txt)
    self.sLengthIn = QLineEdit('-', parametersBox)
    self.sLengthIn.setGeometry(x3[12], y3[12], w3[12], h_lbl)
    self.sWidthTxt = QLabel('Vertical:', parametersBox)
    self.sWidthTxt.setGeometry(x3[13], y3[13], w3[13], h_txt)
    self.sWidthIn = QLineEdit('-', parametersBox)
    self.sWidthIn.setGeometry(x3[14], y3[14], w3[14], h_lbl)
    self.perspectiveBtn = QPushButton('Correct perspective', parametersBox)
    self.perspectiveBtn.setGeometry(x3[15], y3[15], w3[15], h_btn)
    self.perspectiveBtn.clicked.connect(self.perspectiveBtn_clicked)
    self.originalBtn = QPushButton('Restore original', parametersBox)
    self.originalBtn.setGeometry(x3[16], y3[16], w3[16], h_btn)
    self.originalBtn.clicked.connect(self.originalBtn_clicked)

    # fourth column
    # x_cln1 = 500
    # x_cln2 = 595
    analysisTxt = QLabel('Analysis:', parametersBox)
    analysisTxt.setGeometry(x4[0], y4[0], w4[0], h_txt)
    self.analysisSelectionBox = QComboBox(parametersBox)
    self.analysisSelectionBox.setGeometry(x4[1], y4[1], w4[1], h_btn)
    self.analysisSelectionBox.addItem('Choose analysis')
    self.analysisSelectionBox.addItem('Manual tracking')
    self.analysisSelectionBox.addItem('Luma tracking')
    self.analysisSelectionBox.addItem('Color tracking')
    self.analysisSelectionBox.addItem('HSV tracking')
    self.analysisSelectionBox.activated[str].connect(self.analysis_click)
    saveLoadTxt = QLabel('Save/Load:', parametersBox)
    saveLoadTxt.setGeometry(x4[2], y4[2], w4[2], h_txt)
    self.saveParBtn = QPushButton('Save parameters', parametersBox)
    self.saveParBtn.setGeometry(x4[3], y4[3], w4[3], h_btn)
    self.saveParBtn.clicked.connect(self.saveParBtn_clicked)
    self.loadParBtn = QPushButton('Load parameters', parametersBox)
    self.loadParBtn.setGeometry(x4[4], y4[4], w4[4], h_btn)
    self.loadParBtn.clicked.connect(self.loadParBtn_clicked)
    self.figSize = QCheckBox('Half-size figures', parametersBox)
    self.figSize.setGeometry(x4[5], y4[5], w4[5], h_btn)
    exportTxt = QLabel('Save edited video:', parametersBox)
    exportTxt.setGeometry(x4[6], y4[6], w4[6], h_txt)
    self.newVideoHelpBtn = QPushButton('?', parametersBox)
    self.newVideoHelpBtn.setGeometry(x4[7], y4[7], w4[7], h_btn)
    self.newVideoHelpBtn.clicked.connect(self.newVideoHelpBtn_clicked)
    fpsTxt = QLabel('Frame rate (fps):', parametersBox)
    fpsTxt.setGeometry(x4[8], y4[8], w4[8], h_txt)
    self.fpsIn = QLineEdit('30', parametersBox)
    self.fpsIn.setGeometry(x4[9], y4[9], w4[9], h_lbl)
    codecTxt = QLabel('Codec:', parametersBox)
    codecTxt.setGeometry(x4[10], y4[10], w4[10], h_txt)
    self.codecIn = QLineEdit('mp4v', parametersBox)
    self.codecIn.setGeometry(x4[11], y4[11], w4[11], h_lbl)
    formatTxt = QLabel('Format:', parametersBox)
    formatTxt.setGeometry(x4[12], y4[12], w4[12], h_txt)
    self.formatIn = QLineEdit('mp4', parametersBox)
    self.formatIn.setGeometry(x4[13], y4[13], w4[13], h_lbl)
    self.exportVideoBtn = QPushButton('Export video', parametersBox)
    self.exportVideoBtn.setGeometry(x4[14], y4[14], w4[14], h_btn)
    self.exportVideoBtn.clicked.connect(self.exportVideoBtn_clicked)

    # preview label
    # x_cln1 = 650
    self.win1 = QLabel(parametersBox)
    self.win1.setGeometry(x5[0], y5[0], w5[0], h5[0])
    self.win1.setStyleSheet('background-color: white')
    self.frameTxt = QLabel('Current frame:', parametersBox)
    self.frameTxt.setGeometry(x5[1], y5[1], w5[1], h5[1])
    self.frameIn = QLineEdit('0', parametersBox)
    self.frameIn.setGeometry(x5[2], y5[2], w5[2], h5[2])
    self.goToFrameBtn = QPushButton('Go to frame', parametersBox)
    self.goToFrameBtn.setGeometry(x5[3], y5[3], w5[3], h5[3])
    self.goToFrameBtn.clicked.connect(self.goToFrameBtn_clicked)
    self.previewSlider = QSlider(Qt.Horizontal, parametersBox)
    self.previewSlider.setGeometry(x5[4], y5[4], w5[4], h5[4])
    self.previewSlider.sliderReleased.connect(self.sliderValue_released)
#    self.previewSlider.valueChanged.connect(self.sliderValue_released)
    self.showFrameLargeBtn = QPushButton('Show frame', parametersBox)
    self.showFrameLargeBtn.setGeometry(x5[5], y5[5], w5[5], h5[5])
    self.showFrameLargeBtn.clicked.connect(self.showFrameLargeBtn_clicked)

# def previewBox_Linux(self):
#    print('Welcome Linux user!')
#    self.setStyleSheet('font: 12pt Helvetica')
#    self.setWindowTitle('Flame Tracker (v1.1.2beta)')
    #self.setGeometry(10, 10, 1070, 780)
    #Box to choose video parameters, the widgets are listed below
#    parametersBox = QGroupBox('Preview box', self)
#    parametersBox.setGeometry(10, 5, 1050, 390)
    #This box changes for each analysis;
    #widgets must be declared in the specific py file
#    self.analysisGroupBox = QGroupBox('Analysis box', self)
#    self.analysisGroupBox.setGeometry(10, 400, 1050, 390)

    # this text box is only shown at the beginning
    # tempBox = QGroupBox(' ', self.analysisGroupBox)
    # tempBox.setGeometry(0, 0, 1050, 390)
    # introTxt = QLabel('Select the analysis method from -Choose analysis- to activate this panel', tempBox)
    # introTxt.setGeometry(100, 100, 600, 100)
    # introTxt.setStyleSheet('font: 16pt Helvetica')
    #
    #
    # ### parametersBox
    # # first column
    # x_cln1 = 10
    # x_cln2 = 105
    # h_lbl = 20
    # h_txt = 30
    # h_btn = 30
    # self.msgLabel = QLabel('Welcome to the Flame Tracker! \n\n Click on the Help button to get started.', parametersBox)
    # self.msgLabel.setGeometry(x_cln1, 25, 140, h_lbl + 85)
    # self.msgLabel.setStyleSheet('background-color: white')
    # self.msgLabel.setWordWrap(True)
    # self.helpBtn = QPushButton('Help', parametersBox)
    # self.helpBtn.setGeometry(x_cln1 - 5, 135, 150, h_btn)
    # self.helpBtn.clicked.connect(self.helpBtn_clicked)
    # self.openBtn = QPushButton('Open', parametersBox)
    # self.openBtn.setGeometry(x_cln1 - 5, 165, 60, h_btn)
    # self.openBtn.clicked.connect(self.openBtn_clicked)
    # self.openSelectionBox = QComboBox(parametersBox)
    # self.openSelectionBox.setGeometry(x_cln1 + 48, 166, 100, h_btn)
    # self.openSelectionBox.addItem('Video')
    # self.openSelectionBox.addItem('Image(s)')
    # self.openSelectionBox.activated[str].connect(self.openSelection_click)
    # self.fNameLbl = QLabel('(file name)', parametersBox)
    # self.fNameLbl.setGeometry(x_cln1, 200, 140, h_lbl)
    # self.fNameLbl.setStyleSheet('background-color: white')
    # vWidthTxt = QLabel('Width (px):', parametersBox)
    # vWidthTxt.setGeometry(x_cln1, 225, 70, h_txt)
    # self.vWidthLbl = QLabel(parametersBox)
    # self.vWidthLbl.setGeometry(x_cln2, 229, 45, h_lbl)
    # self.vWidthLbl.setStyleSheet('background-color: white')
    # vHeightTxt = QLabel('Height (px):', parametersBox)
    # vHeightTxt.setGeometry(x_cln1, 255, 70, h_txt)
    # self.vHeightLbl = QLabel(parametersBox)
    # self.vHeightLbl.setGeometry(x_cln2, 259, 45, h_lbl)
    # self.vHeightLbl.setStyleSheet('background-color: white')
    # vFpsTxt = QLabel('Frame rate (fps):', parametersBox)
    # vFpsTxt.setGeometry(x_cln1, 285, 90, h_txt)
    # self.vFpsLbl = QLabel(parametersBox)
    # self.vFpsLbl.setGeometry(x_cln2, 289, 45, h_lbl)
    # self.vFpsLbl.setStyleSheet('background-color: white')
    # vFramesTxt = QLabel('Frames #:', parametersBox)
    # vFramesTxt.setGeometry(x_cln1, 315, 70, h_txt)
    # self.vFramesLbl = QLabel(parametersBox)
    # self.vFramesLbl.setGeometry(x_cln2, 319, 45, h_lbl)
    # self.vFramesLbl.setStyleSheet('background-color: white')
    # vDurationTxt = QLabel('Duration (s):', parametersBox)
    # vDurationTxt.setGeometry(x_cln1, 345, 70, h_txt)
    # self.vDurationLbl = QLabel(parametersBox)
    # self.vDurationLbl.setGeometry(x_cln2, 349, 45, h_lbl)
    # self.vDurationLbl.setStyleSheet('background-color: white')

    # #second column
    # x_cln1 = 180
    # x_cln2 = 265
    # w_cln1 = 80
    # w_cln2 = 50
    # h_lbl = 22
    # clmn2_Txt = QLabel('Video parameters:', parametersBox)
    # clmn2_Txt.setGeometry(x_cln1, 20, 120, h_txt)
    #
    #CAS Squish to fit xrefpix to display
    # self.firstFrameTxt = QLabel('First frame:', parametersBox)
    # self.firstFrameTxt.setGeometry(x_cln1, 40, w_cln1, h_txt)
    # self.firstFrameIn = QLineEdit(parametersBox)
    # self.firstFrameIn.setGeometry(x_cln2, 44, w_cln2, h_lbl)
    # self.lastFrameTxt = QLabel('Last frame:', parametersBox)
    # self.lastFrameTxt.setGeometry(x_cln1, 65, w_cln1, h_txt)
    # self.lastFrameIn = QLineEdit(parametersBox)
    # self.lastFrameIn.setGeometry(x_cln2, 69, w_cln2, h_lbl)
    # self.skipFrameTxt = QLabel('Skip frames:', parametersBox)
    # self.skipFrameTxt.setGeometry(x_cln1, 90, w_cln1, h_txt)
    # self.skipFrameIn = QLineEdit(parametersBox)
    # self.skipFrameIn.setGeometry(x_cln2, 94, w_cln2, h_lbl)
    # self.scaleTxt = QLabel('Scale (px/mm):', parametersBox)
    # self.scaleTxt.setGeometry(x_cln1, 115, w_cln1, h_txt)
    # self.scaleIn = QLineEdit(parametersBox)
    # self.scaleIn.setGeometry(x_cln2, 119, w_cln2, h_lbl)

    #CAS add xref line
    # self.xrefTxt = QLabel('xref (px):', parametersBox)
    # self.xrefTxt.setGeometry(x_cln1, 140, w_cln1, h_txt)
    # self.xref = QLineEdit(parametersBox)
    # xRefGUI_shiftBackAmnt = 20
    # xRefGUI_extendAmnt = 20
    # self.xref.setGeometry(x_cln2-xRefGUI_shiftBackAmnt, 144, w_cln2+xRefGUI_shiftBackAmnt+xRefGUI_extendAmnt, h_lbl)
    #
    # self.measureScaleBtn = QPushButton('Measure scale', parametersBox)
    # #self.measureScaleBtn.setGeometry(x_cln1 - 10, 165, 150, h_btn)
    # self.measureScaleBtn.setGeometry(x_cln1 - 10, 168, 150, h_btn-2)
    # self.measureScaleBtn.clicked.connect(self.measureScaleBtn_clicked)
    # self.roiOneTxt = QLabel('ROI, x:', parametersBox)
    # self.roiOneTxt.setGeometry(x_cln1, 225, w_cln1, h_txt)
    # self.roiOneIn = QLineEdit(parametersBox)
    # self.roiOneIn.setGeometry(x_cln2, 229, w_cln2, h_lbl)
    # self.roiTwoTxt = QLabel('ROI, y:', parametersBox)
    # self.roiTwoTxt.setGeometry(x_cln1, 255, w_cln1, h_txt)
    # self.roiTwoIn = QLineEdit(parametersBox)
    # self.roiTwoIn.setGeometry(x_cln2, 259, w_cln2, h_lbl)
    # self.roiThreeTxt = QLabel('ROI, w:', parametersBox)
    # self.roiThreeTxt.setGeometry(x_cln1, 285, w_cln1, h_txt)
    # self.roiThreeIn = QLineEdit(parametersBox)
    # self.roiThreeIn.setGeometry(x_cln2, 289, w_cln2, h_lbl)
    # self.roiFourTxt = QLabel('ROI, h:', parametersBox)
    # self.roiFourTxt.setGeometry(x_cln1, 315, w_cln1, h_txt)
    # self.roiFourIn = QLineEdit(parametersBox)
    # self.roiFourIn.setGeometry(x_cln2, 319, w_cln2, h_lbl)
    # self.roiBtn = QPushButton('Select ROI', parametersBox)
    # self.roiBtn.setGeometry(x_cln1 - 10, 345, 150, h_btn)
    # self.roiBtn.clicked.connect(self.roiBtn_clicked)

    #third column
    # x_cln1 = 340
    # x_cln2 = 425
    # w_cln1 = 60
    # w_cln2 = 50
    # adjustFramesTxt = QLabel('Adjust frames:', parametersBox)
    # adjustFramesTxt.setGeometry(x_cln1, 20, 100, h_txt)
    # self.rotationAngleInTxt = QLabel('Rotation (deg):', parametersBox)
    # self.rotationAngleInTxt.setGeometry(x_cln1, 45, 120, h_txt)
    # self.rotationAngleIn = QLineEdit(parametersBox)
    # self.rotationAngleIn.setGeometry(x_cln2, 49, w_cln2, h_lbl)
    # self.brightnessTxt = QLabel('Brightness:', parametersBox)
    # self.brightnessTxt.setGeometry(x_cln1, 75, 150, h_txt)
    # self.brightnessSlider = QSlider(Qt.Horizontal, parametersBox)
    # self.brightnessSlider.setGeometry(x_cln1, 105, 115, 25)
    # self.brightnessSlider.setMinimum(-50)
    # self.brightnessSlider.setMaximum(50)
    # self.brightnessSlider.setValue(0)
    # self.brightnessSlider.sliderReleased.connect(self.editFramesSlider_released)
    # self.brightnessSlider.valueChanged.connect(self.editFramesSlider_released)
    # self.brightnessLbl = QLabel('0', parametersBox)
    # self.brightnessLbl.setGeometry(x_cln2 + 3, 80, w_cln2 - 5, h_lbl - 4)
    # self.brightnessLbl.setStyleSheet('background-color: white')
    # self.contrastTxt = QLabel('Contrast:', parametersBox)
    # self.contrastTxt.setGeometry(x_cln1, 125, 150, h_txt)
    # self.contrastSlider = QSlider(Qt.Horizontal, parametersBox)
    # self.contrastSlider.setGeometry(x_cln1, 155, 115, 25)
    # self.contrastSlider.setMinimum(-100)
    # self.contrastSlider.setMaximum(+100)
    # self.contrastSlider.setValue(0)
    # self.contrastSlider.sliderReleased.connect(self.editFramesSlider_released)
    # self.contrastSlider.valueChanged.connect(self.editFramesSlider_released)
    # self.contrastLbl = QLabel('0', parametersBox)
    # self.contrastLbl.setGeometry(x_cln2 + 3, 130, w_cln2 - 5, h_lbl - 4)
    # self.contrastLbl.setStyleSheet('background-color: white')
    # self.grayscale = QCheckBox('Grayscale', parametersBox)
    # self.grayscale.setGeometry(x_cln1 - 5, 175, 100, h_btn)
    # correctionTxt = QLabel('Correction lengths (mm):', parametersBox)
    # correctionTxt.setGeometry(x_cln1, 200, 150, h_txt)
    # self.sLengthTxt = QLabel('Horizontal:', parametersBox)
    # self.sLengthTxt.setGeometry(x_cln1, 225, 130, h_txt)
    # self.sLengthIn = QLineEdit('-', parametersBox)
    # self.sLengthIn.setGeometry(x_cln2, 229, w_cln2, h_lbl)
    # self.sWidthTxt = QLabel('Vertical:', parametersBox)
    # self.sWidthTxt.setGeometry(x_cln1, 255, 130, h_txt)
    # self.sWidthIn = QLineEdit('-', parametersBox)
    # self.sWidthIn.setGeometry(x_cln2, 259, w_cln2, h_lbl)
    # self.perspectiveBtn = QPushButton('Correct perspective', parametersBox)
    # self.perspectiveBtn.setGeometry(x_cln1 - 10, 285, 150, h_btn)
    # self.perspectiveBtn.clicked.connect(self.perspectiveBtn_clicked)
    # self.originalBtn = QPushButton('Restore original', parametersBox)
    # self.originalBtn.setGeometry(x_cln1 - 10, 315, 150, h_btn)
    # self.originalBtn.clicked.connect(self.originalBtn_clicked)

    # # fourth column
    # x_cln1 = 500
    # x_cln2 = 595
    # analysisTxt = QLabel('Analysis:', parametersBox)
    # analysisTxt.setGeometry(x_cln1, 20, w_cln1, h_txt)
    # self.analysisSelectionBox = QComboBox(parametersBox)
    # self.analysisSelectionBox.setGeometry(x_cln1 - 10, 45, 150, h_btn)
    # self.analysisSelectionBox.addItem('Choose analysis')
    # self.analysisSelectionBox.addItem('Manual tracking')
    # self.analysisSelectionBox.addItem('Luma tracking')
    # self.analysisSelectionBox.addItem('Color tracking')
    # self.analysisSelectionBox.addItem('HSV tracking')
    # self.analysisSelectionBox.activated[str].connect(self.analysis_click)
    # saveLoadTxt = QLabel('Save/Load:', parametersBox)
    # saveLoadTxt.setGeometry(x_cln1, 70, w_cln1, h_txt)
    # self.saveParBtn = QPushButton('Save parameters', parametersBox)
    # self.saveParBtn.setGeometry(x_cln1 - 10, 95, 150, h_btn)
    # self.saveParBtn.clicked.connect(self.saveParBtn_clicked)
    # self.loadParBtn = QPushButton('Load parameters', parametersBox)
    # self.loadParBtn.setGeometry(x_cln1 - 10, 125, 150, h_btn)
    # self.loadParBtn.clicked.connect(self.loadParBtn_clicked)
    # exportTxt = QLabel('Save edited video:', parametersBox)
    # exportTxt.setGeometry(x_cln1, 200, 150, h_txt)
    # self.newVideoHelpBtn = QPushButton('?', parametersBox)
    # self.newVideoHelpBtn.setGeometry(x_cln2 + 15, 199, 30, h_btn)
    # self.newVideoHelpBtn.clicked.connect(self.newVideoHelpBtn_clicked)
    # fpsTxt = QLabel('Frame rate (fps):', parametersBox)
    # fpsTxt.setGeometry(x_cln1, 225, 120, h_txt)
    # self.fpsIn = QLineEdit('30', parametersBox)
    # self.fpsIn.setGeometry(x_cln2, 229, 40, h_lbl)
    # codecTxt = QLabel('Codec:', parametersBox)
    # codecTxt.setGeometry(x_cln1, 255, 100, h_txt)
    # self.codecIn = QLineEdit('mp4v', parametersBox)
    # self.codecIn.setGeometry(x_cln2, 259, 40, h_lbl)
    # formatTxt = QLabel('Format:', parametersBox)
    # formatTxt.setGeometry(x_cln1, 285, 100, h_txt)
    # self.formatIn = QLineEdit('mp4', parametersBox)
    # self.formatIn.setGeometry(x_cln2, 289, 40, h_lbl)
    # self.exportVideoBtn = QPushButton('Export video', parametersBox)
    # self.exportVideoBtn.setGeometry(x_cln1 - 10, 315, 150, h_btn)
    # self.exportVideoBtn.clicked.connect(self.exportVideoBtn_clicked)

    # preview label
    # x_cln1 = 650
    # self.win1 = QLabel(parametersBox)
    # self.win1.setGeometry(x_cln1, 25, 390, 270)
    # self.win1.setStyleSheet('background-color: white')
    # self.frameTxt = QLabel('Current frame:', parametersBox)
    # self.frameTxt.setGeometry(x_cln1, 295, 120, h_txt)
    # self.frameIn = QLineEdit('0', parametersBox)
    # self.frameIn.setGeometry(x_cln1 + 90, 299, w_cln2, h_lbl)
    # self.goToFrameBtn = QPushButton('Go to frame', parametersBox)
    # self.goToFrameBtn.setGeometry(x_cln1 + 140, 295, 100, h_btn)
    # self.goToFrameBtn.clicked.connect(self.goToFrameBtn_clicked)
    # self.previewSlider = QSlider(Qt.Horizontal, parametersBox)
    # self.previewSlider.setGeometry(x_cln1, 325, 390, 25)
    # self.previewSlider.sliderReleased.connect(self.sliderValue_released)
    # self.previewSlider.valueChanged.connect(self.sliderValue_released)
    # self.showFrameLargeBtn = QPushButton('Show frame', parametersBox)
    # self.showFrameLargeBtn.setGeometry(930, 295, 115, h_btn)
    # self.showFrameLargeBtn.clicked.connect(self.showFrameLargeBtn_clicked)

def manualTrackingBox(self):
    if sys.platform == 'darwin':
        self.manualTrackingBox = QGroupBox(' ', self.analysisGroupBox)
        self.manualTrackingBox.setGeometry(0,0, 1050, 390)

        # size of GUI labels:
        h_lbl = 22
        h_txt = 30
        h_btn = 30

        # first column
        x1 = [ 10,   5,  10,   5,   5,  10, 120,  10,   5,   5,   5,   5]
        y1 = [ 20,  45,  70,  95, 120, 150, 154, 180, 210, 240, 270, 300]
        w1 = [100, 150, 150, 150, 150, 100,  30, 140, 150, 150, 150, 150]

        # labels (since there's only two, in this case I wrote the entire set of coord.)
        lbl1 = [190, 25, 420, 300]
        lbl2 = [620, 25, 420, 300]

    elif sys.platform == 'win32':
        self.manualTrackingBox = QGroupBox('Analysis box', self.analysisGroupBox)
        self.manualTrackingBox.setGeometry(0, 0, 1050, 370)

        # size of GUI labels:
        h_lbl = 22
        h_txt = 30
        h_btn = 30

        # first column
        x1 = [ 10,  10,  10,  10,  10,  10, 120,  10,  10,  10,  10,  10]
        y1 = [ 15,  40,  70,  95, 125, 155, 160, 185, 215, 245, 275, 305]
        w1 = [120, 140, 140, 140, 140, 140,  30, 140, 140, 140, 140, 140]

        # labels (since there's only two, in this case I wrote the entire set of coord.)
        lbl1 = [190, 25, 420, 300]
        lbl2 = [620, 25, 420, 300]

    elif sys.platform == 'linux':
        self.manualTrackingBox = QGroupBox(' ', self.analysisGroupBox)
        self.manualTrackingBox.setGeometry(0,0, 1050, 390)

        # size of GUI labels:
        h_lbl = 22
        h_txt = 30
        h_btn = 30

        # first column
        x1 = [ 10,   5,  10,   5,   5,  10, 120,  10,   5,   5,   5,   5]
        y1 = [ 20,  45,  70,  95, 120, 150, 154, 180, 210, 240, 270, 300]
        w1 = [100, 150, 150, 150, 150, 100,  30, 140, 150, 150, 150, 150]

        # labels (since there's only two, in this case I wrote the entire set of coord.)
        lbl1 = [190, 25, 420, 300]
        lbl2 = [620, 25, 420, 300]


#    self.manualTrackingBox = QGroupBox(' ', self.analysisGroupBox)
#    self.manualTrackingBox.setGeometry(0,0, 1050, 390)
    self.manualTrackingBox.setStyleSheet('background-color: None')

    # #first column
    # x_cln1 = 10
    # x_cln2 = 120
    # h_txt = 30
    # h_btn = 30
    # h_lbl = 22
    # w_cln1 = 80
    # w_cln2 = 50
    directionBoxTxt = QLabel('Flame direction:', self.manualTrackingBox)
    directionBoxTxt.setGeometry(x1[0], y1[0], w1[0], h_txt)
    self.directionBox = QComboBox(self.manualTrackingBox)
    self.directionBox.setGeometry(x1[1], y1[1], w1[1], h_btn)
    self.directionBox.addItem('Left to right')
    self.directionBox.addItem('Right to left')
    self.directionBox.activated.connect(self.directionMT_clicked)
    lightTxt = QLabel('Flashing light (optional):', self.manualTrackingBox)
    lightTxt.setGeometry(x1[2], y1[2], w1[2], h_txt)
    self.lightROIBtn_MT = QPushButton('Pick bright region', self.manualTrackingBox)
    self.lightROIBtn_MT.setGeometry(x1[3], y1[3], w1[3], h_btn)
    self.lightROIBtn_MT.clicked.connect(self.lightROIBtn_MT_clicked)
    self.filterLight_MT = QComboBox(self.manualTrackingBox)
    self.filterLight_MT.setGeometry(x1[4], y1[4], w1[4], h_btn)
    self.filterLight_MT.addItem('Track every frame')
    self.filterLight_MT.addItem('Frames light on')
    self.filterLight_MT.addItem('Frames light off')
    self.filterLight_MT.activated.connect(self.filterLight_MT_clicked)
    nClicksTxt = QLabel('Tracking points #:', self.manualTrackingBox)
    nClicksTxt.setGeometry(x1[5], y1[5], w1[5], h_txt)
    self.nClicksLbl = QLineEdit('1', self.manualTrackingBox)
    self.nClicksLbl.setGeometry(x1[6], y1[6], w1[6], h_lbl)
    self.showEdges_MT = QCheckBox('Show tracking lines', self.manualTrackingBox)
    self.showEdges_MT.setGeometry(x1[7], y1[7], w1[7], h_btn)
    self.showEdges_MT.setChecked(True)
    self.manualTrackingBtn = QPushButton('Start Tracking', self.manualTrackingBox)
    self.manualTrackingBtn.setGeometry(x1[8], y1[8], w1[8], h_btn)
    self.manualTrackingBtn.clicked.connect(self.manualTrackingBtn_clicked)
    self.absValBtn = QPushButton('Absolute values', self.manualTrackingBox)
    self.absValBtn.setGeometry(x1[9], y1[9], w1[9], h_btn)
    self.absValBtn.clicked.connect(self.absValBtn_MT_clicked)
    self.saveBtn_MT = QPushButton('Save data', self.manualTrackingBox)
    self.saveBtn_MT.setGeometry(x1[10], y1[10], w1[10], h_btn)
    self.saveBtn_MT.clicked.connect(self.saveBtn_MT_clicked)
    self.helpBtn_MT = QPushButton('Help', self.manualTrackingBox)
    self.helpBtn_MT.setGeometry(x1[11], y1[11], w1[11], h_btn)
    self.helpBtn_MT.clicked.connect(self.helpBtn_MT_clicked)

    # first label
    self.lbl1_MT = QLabel(self.manualTrackingBox)
    self.lbl1_MT.setGeometry(lbl1[0], lbl1[1], lbl1[2], lbl1[3])
    self.lbl1_MT.setStyleSheet('background-color: white')

    # second label
    self.lbl2_MT = pg.PlotWidget(self.manualTrackingBox)
    self.lbl2_MT.setGeometry(lbl2[0], lbl2[1], lbl2[2], lbl2[3])
    self.lbl2_MT.setBackground('w')
    self.lbl2_MT.setLabel('left', 'Spread Rate [mm/s]', color='black', size=14)
    self.lbl2_MT.setLabel('bottom', 'Time [s]', color='black', size=14)
    self.lbl2_MT.getAxis('bottom').setPen(color=(0, 0, 0))
    self.lbl2_MT.getAxis('left').setPen(color=(0, 0, 0))

# def manualTrackingBox_Win(self):
    #self.manualTrackingBox = QGroupBox('Analysis box', self.analysisGroupBox)
#    self.manualTrackingBox.setGeometry(0, 0, 1050, 370)
    #self.manualTrackingBox.setStyleSheet('background-color: None')

    #first column
    # x_cln1 = 10
    # x_cln2 = 120
    # h_txt = 30
    # h_lbl = 22
    # h_btn = 25
    # w_cln1 = 80
    # w_cln2 = 50
    # directionBoxTxt = QLabel('Flame direction:', self.manualTrackingBox)
    # directionBoxTxt.setGeometry(x_cln1, 15, 120, h_txt)
    # self.directionBox = QComboBox(self.manualTrackingBox)
    # self.directionBox.setGeometry(x_cln1, 40, 140, h_btn)
    # self.directionBox.addItem('Left to right')
    # self.directionBox.addItem('Right to left')
    # self.directionBox.activated.connect(self.directionMT_clicked)
    # lightTxt = QLabel('Flashing light (optional):', self.manualTrackingBox)
    # lightTxt.setGeometry(x_cln1, 70, 140, h_txt)
    # self.lightROIBtn_MT = QPushButton('Pick bright region', self.manualTrackingBox)
    # self.lightROIBtn_MT.setGeometry(x_cln1, 95, 140, h_btn)
    # self.lightROIBtn_MT.clicked.connect(self.lightROIBtn_MT_clicked)
    # self.filterLight_MT = QComboBox(self.manualTrackingBox)
    # self.filterLight_MT.setGeometry(x_cln1, 125, 140, h_btn)
    # self.filterLight_MT.addItem('Track every frame')
    # self.filterLight_MT.addItem('Frames light on')
    # self.filterLight_MT.addItem('Frames light off')
    # self.filterLight_MT.activated.connect(self.filterLight_MT_clicked)
    # nClicksTxt = QLabel('Tracking points #:', self.manualTrackingBox)
    # nClicksTxt.setGeometry(x_cln1, 155, 140, h_txt)
    # self.nClicksLbl = QLineEdit('1', self.manualTrackingBox)
    # self.nClicksLbl.setGeometry(x_cln2, 160, 30, h_lbl)
    # self.showEdges_MT = QCheckBox('Show tracking lines', self.manualTrackingBox)
    # self.showEdges_MT.setGeometry(x_cln1, 185, 140, h_btn)
    # self.showEdges_MT.setChecked(True)
    # self.manualTrackingBtn = QPushButton('Start Tracking', self.manualTrackingBox)
    # self.manualTrackingBtn.setGeometry(x_cln1, 215, 140, h_btn)
    # self.manualTrackingBtn.clicked.connect(self.manualTrackingBtn_clicked)
    # self.absValBtn = QPushButton('Absolute values', self.manualTrackingBox)
    # self.absValBtn.setGeometry(x_cln1, 245, 140, h_btn)
    # self.absValBtn.clicked.connect(self.absValBtn_MT_clicked)
    # self.saveBtn_MT = QPushButton('Save data', self.manualTrackingBox)
    # self.saveBtn_MT.setGeometry(x_cln1, 275, 140, h_btn)
    # self.saveBtn_MT.clicked.connect(self.saveBtn_MT_clicked)
    # self.helpBtn_MT = QPushButton('Help', self.manualTrackingBox)
    # self.helpBtn_MT.setGeometry(x_cln1, 305, 140, h_btn)
    # self.helpBtn_MT.clicked.connect(self.helpBtn_MT_clicked)
    #
    # # first label
    # self.lbl1_MT = QLabel(self.manualTrackingBox)
    # self.lbl1_MT.setGeometry(190, 25, 420, 300)
    # self.lbl1_MT.setStyleSheet('background-color: white')
    #
    # # second label
    # self.lbl2_MT = pg.PlotWidget(self.manualTrackingBox)
    # self.lbl2_MT.setGeometry(620, 25, 420, 300)
    # self.lbl2_MT.setBackground('w')
    # self.lbl2_MT.setLabel('left', 'Spread Rate [mm/s]', color='black', size=14)
    # self.lbl2_MT.setLabel('bottom', 'Time [s]', color='black', size=14)
    # self.lbl2_MT.getAxis('bottom').setPen(color=(0, 0, 0))
    # self.lbl2_MT.getAxis('left').setPen(color=(0, 0, 0))

def lumaTrackingBox(self):
    if sys.platform == 'darwin':
        self.lumaTrackingBox = QGroupBox(' ', self.analysisGroupBox)
        self.lumaTrackingBox.setGeometry(0, 0, 1050, 390)

        # size of GUI labels:
        h_lbl = 22
        h_txt = 30
        h_btn = 30
        h_slider = 25

        # first column
        x1 = [ 10,   5,  10, 120,  10, 105,   5,  10, 120,  10,   5,  10,  10, 120,   5,   5,   5,   5]
        y1 = [ 20,  45,  75,  79, 100, 103, 128, 150, 154, 175, 195, 220, 245, 249, 270, 300, 330, 360]
        w1 = [100, 150, 100,  30, 150,  45, 140, 140,  30, 120, 150, 140, 100,  30, 150, 150, 150, 150]

        # other objects
        x2 = [780, 780, 930]
        y2 = [325, 350, 325]
        w2 = [135, 135, 115]
        # labels (since there's only two, in this case I wrote the entire set of coord.)
        lbl1 = [190, 25, 420, 300]
        lbl2 = [620, 25, 420, 300]

    elif sys.platform == 'win32':
        self.lumaTrackingBox = QGroupBox('Analysis box', self.analysisGroupBox)
        self.lumaTrackingBox.setGeometry(0,0, 1050, 370)

        # size of GUI labels:
        h_lbl = 22
        h_txt = 30
        h_btn = 25
        h_slider = 25

        # first column
        x1 = [ 10,  10,  10, 115,  10, 105,  10,  10, 115,  10,  10,  10,  10, 115,  10,  10,  10, 190]
        y1 = [ 15,  40,  70,  75,  95, 103, 125, 140, 145, 165, 190, 215, 240, 245, 275, 305, 335, 335]
        w1 = [140, 140,  80,  35, 150,  45, 135, 140,  35, 120, 140, 140, 100,  35, 140, 140, 140, 140]

        # other objects
        x2 = [750, 750, 920]
        y2 = [320, 340, 325]
        w2 = [140, 140, 120]
        # labels (since there's only two, in this case I wrote the entire set of coord.)
        lbl1 = [190, 15, 420, 300]
        lbl2 = [620, 15, 420, 300]

    elif sys.platform == 'linux':
        self.lumaTrackingBox = QGroupBox(' ', self.analysisGroupBox)
        self.lumaTrackingBox.setGeometry(0, 0, 1050, 390)

        # size of GUI labels:
        h_lbl = 22
        h_txt = 30
        h_btn = 30
        h_slider = 25

        # first column
        x1 = [ 10,   5,  10, 120,  10, 105,   5,  10, 120,  10,   5,  10,  10, 120,   5,   5,   5,   5]
        y1 = [ 20,  45,  75,  79, 100, 103, 128, 150, 154, 175, 195, 220, 245, 249, 270, 300, 330, 360]
        w1 = [100, 150, 100,  30, 150,  45, 140, 140,  30, 120, 150, 140, 100,  30, 150, 150, 150, 150]

        # other objects
        x2 = [780, 780, 930]
        y2 = [325, 350, 325]
        w2 = [135, 135, 115]
        # labels (since there's only two, in this case I wrote the entire set of coord.)
        lbl1 = [190, 25, 420, 300]
        lbl2 = [620, 25, 420, 300]

    #first column
    # x_cln1 = 10
    # x_cln2 = 120
    # w_btn = 150
    # h_btn = 30
    # h_txt = 30
    # h_lbl = 22
    directionBoxTxt = QLabel('Flame direction:', self.lumaTrackingBox)
    directionBoxTxt.setGeometry(x1[0], y1[0], w1[0], h_txt)
    self.directionBox = QComboBox(self.lumaTrackingBox)
    self.directionBox.setGeometry(x1[1], y1[1], w1[1], h_btn)
    self.directionBox.addItem('Left to right')
    self.directionBox.addItem('Right to left')
    self.directionBox.activated.connect(self.directionLT_clicked)
    thresholdTxt = QLabel('Luma threshold:', self.lumaTrackingBox)
    thresholdTxt.setGeometry(x1[2], y1[2], w1[2], h_txt)
    self.thresholdIn = QLineEdit('30', self.lumaTrackingBox)
    self.thresholdIn.setGeometry(x1[3], y1[3], w1[3], h_lbl)
    filterParticleTxt = QLabel('Filter particles:', self.lumaTrackingBox)
    filterParticleTxt.setGeometry(x1[4], y1[4], w1[4], h_txt)
    self.particleSldrMax = QLineEdit('1000', self.lumaTrackingBox)
    self.particleSldrMax.setGeometry(x1[5], y1[5], w1[5], h_lbl)
    self.filterParticleSldr_LT = QSlider(Qt.Horizontal, self.lumaTrackingBox)
    self.filterParticleSldr_LT.setGeometry(x1[6], y1[6], w1[6], h_slider)
    self.filterParticleSldr_LT.setMinimum(1)
    self.filterParticleSldr_LT.setMaximum(1000)
    self.filterParticleSldr_LT.setValue(10)
    self.filterParticleSldr_LT.sliderReleased.connect(self.filterParticleSldr_LT_released)
    avgLE_txt = QLabel('#px to locate edges:', self.lumaTrackingBox)
    avgLE_txt.setGeometry(x1[7], y1[7], w1[7], h_txt)
    self.avgLEIn_LT = QLineEdit('5', self.lumaTrackingBox)
    self.avgLEIn_LT.setGeometry(x1[8], y1[8], w1[8], h_lbl)
    trackingTxt = QLabel('Flame tracking:', self.lumaTrackingBox)
    trackingTxt.setGeometry(x1[9], y1[9], w1[9], h_txt)
    self.lightROIBtn_LT = QPushButton('Pick bright region', self.lumaTrackingBox)
    self.lightROIBtn_LT.setGeometry(x1[10], y1[10], w1[10], h_btn)
    self.lightROIBtn_LT.clicked.connect(self.lightROIBtn_LT_clicked)
    self.filterLight = QCheckBox('Ignore flashing light', self.lumaTrackingBox)
    self.filterLight.setGeometry(x1[11], y1[11], w1[11], h_btn)
    movAvgTxt = QLabel('Moving avg points:', self.lumaTrackingBox)
    movAvgTxt.setGeometry(x1[12], y1[12], w1[12], h_txt)
    self.movAvgIn_LT = QLineEdit('2', self.lumaTrackingBox)
    self.movAvgIn_LT.setGeometry(x1[13], y1[13], w1[13], h_lbl)
    self.lumaTrackingBtn = QPushButton('Start Tracking', self.lumaTrackingBox)
    self.lumaTrackingBtn.setGeometry(x1[14], y1[14], w1[14], h_txt)
    self.lumaTrackingBtn.clicked.connect(self.lumaTrackingBtn_clicked)
    self.absValBtn = QPushButton('Absolute values', self.lumaTrackingBox)
    self.absValBtn.setGeometry(x1[15], y1[15], w1[15], h_btn)
    self.absValBtn.clicked.connect(self.absValBtn_LT_clicked)
    self.saveBtn_LT = QPushButton('Save data', self.lumaTrackingBox)
    self.saveBtn_LT.setGeometry(x1[16], y1[16], w1[16], h_btn)
    self.saveBtn_LT.clicked.connect(self.saveDataBtn_LT_clicked)
    self.helpBtn_LT = QPushButton('Help', self.lumaTrackingBox)
    self.helpBtn_LT.setGeometry(x1[17], y1[17], w1[17], h_btn)
    self.helpBtn_LT.clicked.connect(self.helpBtn_LT_clicked)

    self.showEdges = QCheckBox('Show edges location', self.lumaTrackingBox)
    self.showEdges.setGeometry(x2[0], y2[0], w2[0], h_btn)
    self.showEdges.setChecked(True)
    self.exportEdges_LT = QCheckBox('Output video analysis', self.lumaTrackingBox)
    self.exportEdges_LT.setGeometry(x2[1], y2[1], w2[1], h_btn)
    self.showFrameLargeBtn_LT = QPushButton('Show frames', self.lumaTrackingBox)
    self.showFrameLargeBtn_LT.setGeometry(x2[2], y2[2], w2[2], h_btn)
    self.showFrameLargeBtn_LT.clicked.connect(self.showFrameLargeBtn_LT_clicked)

    # below is defined in flameTracker.py already in an OS specific way
    # first label
    self.lbl1_LT = QLabel(self.lumaTrackingBox)
    self.lbl1_LT.setGeometry(lbl1[0], lbl1[1], lbl1[2], lbl1[3])
    self.lbl1_LT.setStyleSheet('background-color: white')

    # second label
    self.lbl2_LT = QLabel(self.lumaTrackingBox)
    self.lbl2_LT.setGeometry(lbl2[0], lbl2[1], lbl2[2], lbl2[3])
    self.lbl2_LT.setStyleSheet('background-color: white')

# def lumaTrackingBox_Win(self):
    # self.lumaTrackingBox = QGroupBox('Analysis box', self.analysisGroupBox)
    # self.lumaTrackingBox.setGeometry(0,0, 1050, 370)

    # h_btn = 25
    # h_txt = 30
    # h_lbl = 22
    # w_lbl = 35
    #
    # #first column
    # x_cln1 = 10
    # x_cln2 = 115
    # directionBoxTxt = QLabel('Flame direction:', self.lumaTrackingBox)
    # directionBoxTxt.setGeometry(x_cln1, 15, 140, h_txt)
    # self.directionBox = QComboBox(self.lumaTrackingBox)
    # self.directionBox.setGeometry(x_cln1, 40, 140, h_btn)
    # self.directionBox.addItem('Left to right')
    # self.directionBox.addItem('Right to left')
    # self.directionBox.activated.connect(self.directionLT_clicked)
    # thresholdTxt = QLabel('Luma threshold:', self.lumaTrackingBox)
    # thresholdTxt.setGeometry(x_cln1, 70, 80, h_txt)
    # self.thresholdIn = QLineEdit('30', self.lumaTrackingBox)
    # self.thresholdIn.setGeometry(x_cln2, 75, w_lbl, h_lbl)

    # filterParticleTxt = QLabel('Filter particles:', self.lumaTrackingBox)
    # filterParticleTxt.setGeometry(x_cln1, 95, 150, h_txt)
    # self.particleSldrMax = QLineEdit('1000', self.lumaTrackingBox)
    # self.particleSldrMax.setGeometry(x_cln2 - 10, 103, 45, h_lbl) #beta
    # self.filterParticleSldr_LT = QSlider(Qt.Horizontal, self.lumaTrackingBox)
    # self.filterParticleSldr_LT.setGeometry(x_cln1, 125, 135, 15)
    # self.filterParticleSldr_LT.setMinimum(1)
    # self.filterParticleSldr_LT.setMaximum(1000)
    # self.filterParticleSldr_LT.setValue(10)
    # self.filterParticleSldr_LT.sliderReleased.connect(self.filterParticleSldr_LT_released)
    #
    # avgLE_txt = QLabel('#px to locate edges:', self.lumaTrackingBox)
    # avgLE_txt.setGeometry(x_cln1, 140, 140, h_txt)
    # self.avgLEIn_LT = QLineEdit('5', self.lumaTrackingBox)
    # self.avgLEIn_LT.setGeometry(x_cln2, 145, w_lbl, h_lbl)
    # trackingTxt = QLabel('Flame tracking:', self.lumaTrackingBox)
    # trackingTxt.setGeometry(x_cln1, 165, 120, h_txt)
    # self.lightROIBtn_LT = QPushButton('Pick bright region', self.lumaTrackingBox)
    # self.lightROIBtn_LT.setGeometry(x_cln1, 190, 140, h_btn)
    # self.lightROIBtn_LT.clicked.connect(self.lightROIBtn_LT_clicked)
    # self.filterLight = QCheckBox('Ignore flashing light', self.lumaTrackingBox)
    # self.filterLight.setGeometry(x_cln1, 215, 140, h_btn)
    # movAvgTxt = QLabel('Moving avg points:', self.lumaTrackingBox)
    # movAvgTxt.setGeometry(x_cln1, 240, 100, h_txt)
    # self.movAvgIn_LT = QLineEdit('2', self.lumaTrackingBox)
    # self.movAvgIn_LT.setGeometry(x_cln2, 245, w_lbl, h_lbl)
    # self.lumaTrackingBtn = QPushButton('Start Tracking', self.lumaTrackingBox)
    # self.lumaTrackingBtn.setGeometry(x_cln1, 275, 140, h_btn)
    # self.lumaTrackingBtn.clicked.connect(self.lumaTrackingBtn_clicked)
    # self.absValBtn = QPushButton('Absolute values', self.lumaTrackingBox)
    # self.absValBtn.setGeometry(x_cln1, 305, 140, h_btn)
    # self.absValBtn.clicked.connect(self.absValBtn_LT_clicked)
    # self.saveBtn_LT = QPushButton('Save data', self.lumaTrackingBox)
    # self.saveBtn_LT.setGeometry(x_cln1, 335, 140, h_btn)
    # self.saveBtn_LT.clicked.connect(self.saveDataBtn_LT_clicked)
    #
    # self.helpBtn_LT = QPushButton('Help', self.lumaTrackingBox)
    # self.helpBtn_LT.setGeometry(190, 335, 140, h_btn)
    # self.helpBtn_LT.clicked.connect(self.helpBtn_LT_clicked)

    # self.showEdges = QCheckBox('Show edges location', self.lumaTrackingBox)
    # self.showEdges.setGeometry(750, 320, 140, h_btn)
    # self.showEdges.setChecked(True)
    # self.exportEdges_LT = QCheckBox('Output video analysis', self.lumaTrackingBox)
    # self.exportEdges_LT.setGeometry(750, 340, 140, h_btn)
    # self.showFrameLargeBtn_LT = QPushButton('Show frames', self.lumaTrackingBox)
    # self.showFrameLargeBtn_LT.setGeometry(920, 325, 120, h_btn)
    # self.showFrameLargeBtn_LT.clicked.connect(self.showFrameLargeBtn_LT_clicked)
    #
    # # below is defined in flameTracker.py already in an OS specific way
    # # first label
    # self.lbl1_LT = QLabel(self.lumaTrackingBox)
    # self.lbl1_LT.setGeometry(190, 15, 420, 300)
    # self.lbl1_LT.setStyleSheet('background-color: white')
    #
    # # second label
    # self.lbl2_LT = QLabel(self.lumaTrackingBox)
    # self.lbl2_LT.setGeometry(620, 15, 420, 300)
    # self.lbl2_LT.setStyleSheet('background-color: white')

def colorTrackingBox(self):
    if sys.platform == 'darwin':
        self.colorTrackingBox = QGroupBox(' ', self.analysisGroupBox)
        self.colorTrackingBox.setGeometry(0, 0, 1050, 390)

        # size of GUI labels:
        h_lbl = 22
        h_txt = 30
        h_btn = 30
        h_slider = 25

        # first column without color channels objects
        x1 = [ 10,   5,  10, 135,  10,  10, 145,  10, 120]
        y1 = [ 20,  45, 280, 283, 305, 330, 334, 360, 360]
        w1 = [100, 150, 150,  40, 170, 140,  30, 100,  60]

        # first column - 'colors' objects
        x_rgb = [ 10,  10, 35, 175,  60,  10,  35, 175,  60]
        w_rgb = [100, 100, 30,  30, 120, 100,  30,  30, 120]

        y_r = [ 70,  92, 90,  90,  95, 114, 112, 112, 117]
        y_g = [140, 162, 160, 160, 165, 184, 182, 182, 187]
        y_b = [210, 232, 230, 230, 235, 254, 252, 252, 257]

        # second column
        x2 = [210, 210, 210, 220, 210, 220, 220, 325, 210, 210, 210]
        y2 = [ 30,  60,  90, 120, 145, 170, 200, 204, 230, 260, 290]
        w2 = [150, 150, 150, 120, 150, 135, 130,  30, 150, 150, 150]

        # other objects
        x3 = [780, 780, 930]
        y3 = [275, 300, 275]
        w3 = [135, 135, 115]

        # labels (since there's only two, in this case I wrote the entire set of coord.)
        lbl1 = [370, 25, 330, 250]
        lbl2 = [710, 25, 330, 250]

    elif sys.platform == 'win32':
        self.colorTrackingBox = QGroupBox('Analysis box', self.analysisGroupBox)
        self.colorTrackingBox.setGeometry(0, 0, 1050, 370)

        # size of GUI labels:
        h_lbl = 22
        h_txt = 30
        h_btn = 25
        h_slider = 15

        # first column without color channels objects
        x1 = [ 10,  10,  10, 140,  10,  10, 120,  10, 120]
        y1 = [ 15,  40, 250, 253, 275, 295, 300, 325, 330]
        w1 = [100, 140, 150,  35, 170, 100,  30, 100,  35]

        # first column - 'colors' objects
        x_rgb = [ 10,  10, 40, 185,  60,  10,  40, 185,  60]
        w_rgb = [100, 100, 15,  15, 120, 100,  15,  15, 120]

        y_r   = [ 65,  85,  92,  92,  92, 105, 112, 112, 112]
        y_g   = [125, 145, 152, 152, 152, 165, 185, 172, 172]
        y_b   = [185, 205, 212, 212, 212, 225, 232, 232, 232]

        # second column
        x2 = [220, 220, 220, 220, 220, 220, 220, 330, 220, 220, 220]
        y2 = [ 15,  45,  75, 100, 130, 155, 185, 190, 220, 250, 280]
        w2 = [140, 140, 140, 120, 140, 140, 100,  30, 140, 140, 140]

        # other objects
        x3 = [780, 780, 920]
        y3 = [270, 290, 270]
        w3 = [120, 120, 120]

        # labels (since there's only two, in this case I wrote the entire set of coord.)
        lbl1 = [370, 15, 330, 250]
        lbl2 = [710, 15, 330, 250]

    elif sys.platform == 'linux':
        self.colorTrackingBox = QGroupBox(' ', self.analysisGroupBox)
        self.colorTrackingBox.setGeometry(0, 0, 1050, 390)

        # size of GUI labels:
        h_lbl = 22
        h_txt = 30
        h_btn = 30
        h_slider = 25

        # first column without color channels objects
        x1 = [ 10,   5,  10, 135,  10,  10, 145,  10, 120]
        y1 = [ 20,  45, 280, 283, 305, 330, 334, 360, 360]
        w1 = [100, 150, 150,  40, 170, 140,  30, 100,  60]

        # first column - 'colors' objects
        x_rgb = [ 10,  10, 35, 175,  60,  10,  35, 175,  60]
        w_rgb = [100, 100, 30,  30, 120, 100,  30,  30, 120]

        y_r = [ 70,  92, 90,  90,  95, 114, 112, 112, 117]
        y_g = [140, 162, 160, 160, 165, 184, 182, 182, 187]
        y_b = [210, 232, 230, 230, 235, 254, 252, 252, 257]

        # second column
        x2 = [210, 210, 210, 220, 210, 220, 220, 325, 210, 210, 210]
        y2 = [ 30,  60,  90, 120, 145, 170, 200, 204, 230, 260, 290]
        w2 = [150, 150, 150, 120, 150, 135, 130,  30, 150, 150, 150]

        # other objects
        x3 = [780, 780, 930]
        y3 = [275, 300, 275]
        w3 = [135, 135, 115]

        # labels (since there's only two, in this case I wrote the entire set of coord.)
        lbl1 = [370, 25, 330, 250]
        lbl2 = [710, 25, 330, 250]

    # self.colorTrackingBox = QGroupBox(' ', self.analysisGroupBox)
    # self.colorTrackingBox.setGeometry(0, 0, 1050, 390)
    self.colorTrackingBox.setStyleSheet('background-color: None')


    # w_btn2 = 30
    # #first column
    # x_cln1 = 10
    directionBoxTxt = QLabel('Flame direction:', self.colorTrackingBox)
    directionBoxTxt.setGeometry(x1[0], y1[0], w1[0], h_txt)
    self.directionBox = QComboBox(self.colorTrackingBox)
    self.directionBox.setGeometry(x1[1], y1[1], w1[1], h_btn)
    self.directionBox.addItem('Left to right')
    self.directionBox.addItem('Right to left')
    self.directionBox.activated.connect(self.directionCT_clicked)

    filterParticleTxt = QLabel('Filter particles:', self.colorTrackingBox)
    filterParticleTxt.setGeometry(x1[2], y1[2], w1[2], h_txt)
    self.particleSldrMax = QLineEdit('1000', self.colorTrackingBox)
    self.particleSldrMax.setGeometry(x1[3], y1[3], w1[3], h_lbl)
    self.filterParticleSldr_CT = QSlider(Qt.Horizontal, self.colorTrackingBox)
    self.filterParticleSldr_CT.setGeometry(x1[4], y1[4], w1[4], h_slider)
    self.filterParticleSldr_CT.setMinimum(1)
    self.filterParticleSldr_CT.setMaximum(1000)
    self.filterParticleSldr_CT.setValue(10)
    self.filterParticleSldr_CT.sliderReleased.connect(self.filterParticleSldr_CT_released)
    avgLE_txt = QLabel('#px to locate edges:', self.colorTrackingBox)
    avgLE_txt.setGeometry(x1[5], y1[5], w1[5], h_txt)
    self.avgLEIn_CT = QLineEdit('1', self.colorTrackingBox)
    self.avgLEIn_CT.setGeometry(x1[6], y1[6], w1[6], h_lbl)
    connectivityTxt = QLabel('Connectivity (px):', self.colorTrackingBox)
    connectivityTxt.setGeometry(x1[7], y1[7], w1[7], h_txt)
    self.connectivityBox = QComboBox(self.colorTrackingBox)
    self.connectivityBox.setGeometry(x1[8], y1[8], w1[8], h_btn)
    self.connectivityBox.addItem('4')
    self.connectivityBox.addItem('8')
    self.connectivityBox.activated.connect(self.connectivityBoxCT_clicked)

    redChannelTxt = QLabel('Red channel:', self.colorTrackingBox)
    redChannelTxt.setGeometry(x_rgb[0], y_r[0], w_rgb[0], h_txt)
    redMinTxt = QLabel('Min:', self.colorTrackingBox)
    redMinTxt.setGeometry(x_rgb[1], y_r[1], w_rgb[1], h_txt)
    self.redMinLeftBtn_CT = QPushButton('<', self.colorTrackingBox)
    self.redMinLeftBtn_CT.setGeometry(x_rgb[2], y_r[2], w_rgb[2], h_btn)
    self.redMinLeftBtn_CT.clicked.connect(self.redMinLeftBtn_CT_clicked)
    self.redMinRightBtn_CT = QPushButton('>', self.colorTrackingBox)
    self.redMinRightBtn_CT.setGeometry(x_rgb[3], y_r[3], w_rgb[3], h_btn)
    self.redMinRightBtn_CT.clicked.connect(self.redMinRightBtn_CT_clicked)
    self.redMinSlider = QSlider(Qt.Horizontal, self.colorTrackingBox)
    self.redMinSlider.setGeometry(x_rgb[4], y_r[4], w_rgb[4], h_slider)
    self.redMinSlider.setMinimum(0)
    self.redMinSlider.setMaximum(255)
    self.redMinSlider.setValue(10)
    self.redMinSlider.sliderReleased.connect(self.singleColorSlider_released)
    redMaxTxt = QLabel('Max:', self.colorTrackingBox)
    redMaxTxt.setGeometry(x_rgb[5], y_r[5], w_rgb[5], h_txt)
    self.redMaxLeftBtn_CT = QPushButton('<', self.colorTrackingBox)
    self.redMaxLeftBtn_CT.setGeometry(x_rgb[6], y_r[6], w_rgb[6], h_btn)
    self.redMaxLeftBtn_CT.clicked.connect(self.redMaxLeftBtn_CT_clicked)
    self.redMaxRightBtn_CT = QPushButton('>', self.colorTrackingBox)
    self.redMaxRightBtn_CT.setGeometry(x_rgb[7], y_r[7], w_rgb[7], h_btn)
    self.redMaxRightBtn_CT.clicked.connect(self.redMaxRightBtn_CT_clicked)
    self.redMaxSlider = QSlider(Qt.Horizontal, self.colorTrackingBox)
    self.redMaxSlider.setGeometry(x_rgb[8], y_r[8], w_rgb[8], 25)
    self.redMaxSlider.setMinimum(0)
    self.redMaxSlider.setMaximum(255)
    self.redMaxSlider.setValue(255)
    self.redMaxSlider.sliderReleased.connect(self.singleColorSlider_released)
    greenChannelTxt = QLabel('Green channel:', self.colorTrackingBox)
    greenChannelTxt.setGeometry(x_rgb[0], y_g[0], w_rgb[0], h_txt)
    greenMinTxt = QLabel('Min:', self.colorTrackingBox)
    greenMinTxt.setGeometry(x_rgb[1], y_g[1], w_rgb[1], h_txt)
    self.greenMinLeftBtn_CT = QPushButton('<', self.colorTrackingBox)
    self.greenMinLeftBtn_CT.setGeometry(x_rgb[2], y_g[2], w_rgb[2], h_btn)
    self.greenMinLeftBtn_CT.clicked.connect(self.greenMinLeftBtn_CT_clicked)
    self.greenMinRightBtn_CT = QPushButton('>', self.colorTrackingBox)
    self.greenMinRightBtn_CT.setGeometry(x_rgb[3], y_g[3], w_rgb[3], h_btn)
    self.greenMinRightBtn_CT.clicked.connect(self.greenMinRightBtn_CT_clicked)
    self.greenMinSlider = QSlider(Qt.Horizontal, self.colorTrackingBox)
    self.greenMinSlider.setGeometry(x_rgb[4], y_g[4], w_rgb[4], h_slider)
    self.greenMinSlider.setMinimum(0)
    self.greenMinSlider.setMaximum(255)
    self.greenMinSlider.setValue(10)
    self.greenMinSlider.sliderReleased.connect(self.singleColorSlider_released)
    greenMaxTxt = QLabel('Max:', self.colorTrackingBox)
    greenMaxTxt.setGeometry(x_rgb[5], y_g[5], w_rgb[5], h_txt)
    self.greenMaxLeftBtn_CT = QPushButton('<', self.colorTrackingBox)
    self.greenMaxLeftBtn_CT.setGeometry(x_rgb[6], y_g[6], w_rgb[6], h_btn)
    self.greenMaxLeftBtn_CT.clicked.connect(self.greenMaxLeftBtn_CT_clicked)
    self.greenMaxRightBtn_CT = QPushButton('>', self.colorTrackingBox)
    self.greenMaxRightBtn_CT.setGeometry(x_rgb[7], y_g[7], w_rgb[7], h_btn)
    self.greenMaxRightBtn_CT.clicked.connect(self.greenMaxRightBtn_CT_clicked)
    self.greenMaxSlider = QSlider(Qt.Horizontal, self.colorTrackingBox)
    self.greenMaxSlider.setGeometry(x_rgb[8], y_g[8], w_rgb[8], h_slider)
    self.greenMaxSlider.setMinimum(0)
    self.greenMaxSlider.setMaximum(255)
    self.greenMaxSlider.setValue(255)
    self.greenMaxSlider.sliderReleased.connect(self.singleColorSlider_released)
    blueChannelTxt = QLabel('Blue channel:', self.colorTrackingBox)
    blueChannelTxt.setGeometry(x_rgb[0], y_b[0], w_rgb[0], h_txt)
    blueMinTxt = QLabel('Min:', self.colorTrackingBox)
    blueMinTxt.setGeometry(x_rgb[1], y_b[1], w_rgb[1], h_txt)
    self.blueMinLeftBtn_CT = QPushButton('<', self.colorTrackingBox)
    self.blueMinLeftBtn_CT.setGeometry(x_rgb[2], y_b[2], w_rgb[2], h_btn)
    self.blueMinLeftBtn_CT.clicked.connect(self.blueMinLeftBtn_CT_clicked)
    self.blueMinRightBtn_CT = QPushButton('>', self.colorTrackingBox)
    self.blueMinRightBtn_CT.setGeometry(x_rgb[3], y_b[3], w_rgb[3], h_btn)
    self.blueMinRightBtn_CT.clicked.connect(self.blueMinRightBtn_CT_clicked)
    self.blueMinSlider = QSlider(Qt.Horizontal, self.colorTrackingBox)
    self.blueMinSlider.setGeometry(x_rgb[4], y_b[4], w_rgb[4], h_slider)
    self.blueMinSlider.setMinimum(0)
    self.blueMinSlider.setMaximum(255)
    self.blueMinSlider.sliderReleased.connect(self.singleColorSlider_released)
    blueMaxTxt = QLabel('Max:', self.colorTrackingBox)
    blueMaxTxt.setGeometry(x_rgb[5], y_b[5], w_rgb[5], h_txt)
    self.blueMaxLeftBtn_CT = QPushButton('<', self.colorTrackingBox)
    self.blueMaxLeftBtn_CT.setGeometry(x_rgb[6], y_b[6], w_rgb[6], h_btn)
    self.blueMaxLeftBtn_CT.clicked.connect(self.blueMaxLeftBtn_CT_clicked)
    self.blueMaxRightBtn_CT = QPushButton('>', self.colorTrackingBox)
    self.blueMaxRightBtn_CT.setGeometry(x_rgb[7], y_b[7], w_rgb[7], h_btn)
    self.blueMaxRightBtn_CT.clicked.connect(self.blueMaxRightBtn_CT_clicked)
    self.blueMaxSlider = QSlider(Qt.Horizontal, self.colorTrackingBox)
    self.blueMaxSlider.setGeometry(x_rgb[8], y_b[8], w_rgb[8], h_slider)
    self.blueMaxSlider.setMinimum(0)
    self.blueMaxSlider.setMaximum(255)
    self.blueMaxSlider.setValue(255)
    self.blueMaxSlider.sliderReleased.connect(self.singleColorSlider_released)

    #second column
    # x_cln1 = 220
    self.saveChannelsBtn_CT = QPushButton('Save filter values', self.colorTrackingBox)
    self.saveChannelsBtn_CT.setGeometry(x2[0], y2[0], w2[0], h_btn)
    self.saveChannelsBtn_CT.clicked.connect(self.saveChannelsBtn_CT_clicked)
    self.loadChannelsBtn_CT = QPushButton('Load filter values', self.colorTrackingBox)
    self.loadChannelsBtn_CT.setGeometry(x2[1], y2[1], w2[1], h_btn)
    self.loadChannelsBtn_CT.clicked.connect(self.loadChannelsBtn_CT_clicked)
    self.helpBtn_CT = QPushButton('Help', self.colorTrackingBox)
    self.helpBtn_CT.setGeometry(x2[2], y2[2], w2[2], h_btn)
    self.helpBtn_CT.clicked.connect(self.helpBtn_CT_clicked)
    trackingTxt = QLabel('Flame tracking:', self.colorTrackingBox)
    trackingTxt.setGeometry(x2[3], y2[3], w2[3], h_txt)

    self.lightROIBtn_CT = QPushButton('Pick bright region', self.colorTrackingBox)
    self.lightROIBtn_CT.setGeometry(x2[4], y2[4], w2[4], h_btn)
    self.lightROIBtn_CT.clicked.connect(self.lightROIBtn_CT_clicked)
    self.filterLight_CT = QCheckBox('Ignore flashing light', self.colorTrackingBox)
    self.filterLight_CT.setGeometry(x2[5], y2[5], w2[5], h_btn)
    movAvgTxt = QLabel('Moving avg points:', self.colorTrackingBox)
    movAvgTxt.setGeometry(x2[6], y2[6], w2[6], h_txt)
    self.movAvgIn_CT = QLineEdit('2', self.colorTrackingBox)
    self.movAvgIn_CT.setGeometry(x2[7], y2[7], w2[7], h_lbl)

    self.colorTrackingBtn = QPushButton('Start tracking', self.colorTrackingBox)
    self.colorTrackingBtn.setGeometry(x2[8], y2[8], w2[8], h_btn)
    self.colorTrackingBtn.clicked.connect(self.colorTrackingBtn_clicked)
    self.absValBtn_CT = QPushButton('Absolute values', self.colorTrackingBox)
    self.absValBtn_CT.setGeometry(x2[9], y2[9], w2[9], h_btn)
    self.absValBtn_CT.clicked.connect(self.absValBtn_CT_clicked)
    self.saveBtn_CT = QPushButton('Save data', self.colorTrackingBox)
    self.saveBtn_CT.setGeometry(x2[10], y2[10], w2[10], h_btn)
    self.saveBtn_CT.clicked.connect(self.saveBtn_CT_clicked)

    # other objects
    self.showEdges = QCheckBox('Show edges location', self.colorTrackingBox)
    self.showEdges.setGeometry(x3[0], y3[0], w3[0], h_btn)
    self.showEdges.setChecked(True)
    self.exportEdges_CT = QCheckBox('Output video analysis', self.colorTrackingBox)
    self.exportEdges_CT.setGeometry(x3[1], y3[1], w3[1], h_btn)
    self.showFrameLargeBtn_CT = QPushButton('Show frames', self.colorTrackingBox)
    self.showFrameLargeBtn_CT.setGeometry(x3[2], y3[2], w3[2], h_btn)
    self.showFrameLargeBtn_CT.clicked.connect(self.showFrameLargeBtn_CT_clicked)

    # first label
    self.lbl1_CT = QLabel(self.colorTrackingBox)
    self.lbl1_CT.setGeometry(lbl1[0], lbl1[1], lbl1[2], lbl1[3])
    self.lbl1_CT.setStyleSheet('background-color: white')

    # second label
    self.lbl2_CT = QLabel(self.colorTrackingBox)
    self.lbl2_CT.setGeometry(lbl2[0], lbl2[1], lbl2[2], lbl2[3])
    self.lbl2_CT.setStyleSheet('background-color: white')


# def colorTrackingBox_Win(self):
    # self.colorTrackingBox = QGroupBox('Analysis box', self.analysisGroupBox)
    # self.colorTrackingBox.setGeometry(0, 0, 1050, 370)
    # self.colorTrackingBox.setStyleSheet('background-color: None')

    # h_btn = 25
    # h_btn2 = 15
    # h_txt = 30
    # h_lbl = 22
    # w_btn2 = 15
    # #first column
    # x_cln1 = 10
    # x_cln2 = 120
    # directionBoxTxt = QLabel('Flame direction:', self.colorTrackingBox)
    # directionBoxTxt.setGeometry(x_cln1, 15, 100, h_txt)
    # self.directionBox = QComboBox(self.colorTrackingBox)
    # self.directionBox.setGeometry(x_cln1, 40, 140, h_btn)
    # self.directionBox.addItem('Left to right')
    # self.directionBox.addItem('Right to left')
    # self.directionBox.activated.connect(self.directionCT_clicked)
    # redChannelTxt = QLabel('Red channel:', self.colorTrackingBox)
    # redChannelTxt.setGeometry(x_cln1, 65, 100, h_txt)
    # redMinTxt = QLabel('Min:', self.colorTrackingBox)
    # redMinTxt.setGeometry(x_cln1, 85, 80, h_txt)
    # self.redMinLeftBtn_CT = QPushButton('<', self.colorTrackingBox)
    # self.redMinLeftBtn_CT.setGeometry(40, 92, w_btn2, h_btn2)
    # self.redMinLeftBtn_CT.clicked.connect(self.redMinLeftBtn_CT_clicked)
    # self.redMinRightBtn_CT = QPushButton('>', self.colorTrackingBox)
    # self.redMinRightBtn_CT.setGeometry(185, 92, w_btn2, h_btn2)
    # self.redMinRightBtn_CT.clicked.connect(self.redMinRightBtn_CT_clicked)
    # self.redMinSlider = QSlider(Qt.Horizontal, self.colorTrackingBox)
    # self.redMinSlider.setGeometry(60, 92, 120, h_btn2)
    # self.redMinSlider.setMinimum(0)
    # self.redMinSlider.setMaximum(255)
    # self.redMinSlider.setValue(10)
    # self.redMinSlider.sliderReleased.connect(self.singleColorSlider_released)
    # self.redMinSlider.valueChanged.connect(self.singleColorSlider_released)
    # redMaxTxt = QLabel('Max:', self.colorTrackingBox)
    # redMaxTxt.setGeometry(x_cln1, 105, 100, h_txt)
    # self.redMaxLeftBtn_CT = QPushButton('<', self.colorTrackingBox)
    # self.redMaxLeftBtn_CT.setGeometry(40, 112, w_btn2, h_btn2)
    # self.redMaxLeftBtn_CT.clicked.connect(self.redMaxLeftBtn_CT_clicked)
    # self.redMaxRightBtn_CT = QPushButton('>', self.colorTrackingBox)
    # self.redMaxRightBtn_CT.setGeometry(185, 112, w_btn2, h_btn2)
    # self.redMaxRightBtn_CT.clicked.connect(self.redMaxRightBtn_CT_clicked)
    # self.redMaxSlider = QSlider(Qt.Horizontal, self.colorTrackingBox)
    # self.redMaxSlider.setGeometry(60, 112, 120, h_btn2)
    # self.redMaxSlider.setMinimum(0)
    # self.redMaxSlider.setMaximum(255)
    # self.redMaxSlider.setValue(255)
    # self.redMaxSlider.sliderReleased.connect(self.singleColorSlider_released)
    # self.redMaxSlider.valueChanged.connect(self.singleColorSlider_released)
    # greenChannelTxt = QLabel('Green channel:', self.colorTrackingBox)
    # greenChannelTxt.setGeometry(x_cln1, 125, 100, h_txt)
    # greenMinTxt = QLabel('Min:', self.colorTrackingBox)
    # greenMinTxt.setGeometry(x_cln1, 145, 100, h_txt)
    # self.greenMinLeftBtn_CT = QPushButton('<', self.colorTrackingBox)
    # self.greenMinLeftBtn_CT.setGeometry(40, 152, w_btn2, h_btn2)
    # self.greenMinLeftBtn_CT.clicked.connect(self.greenMinLeftBtn_CT_clicked)
    # self.greenMinRightBtn_CT = QPushButton('>', self.colorTrackingBox)
    # self.greenMinRightBtn_CT.setGeometry(185, 152, w_btn2, h_btn2)
    # self.greenMinRightBtn_CT.clicked.connect(self.greenMinRightBtn_CT_clicked)
    # self.greenMinSlider = QSlider(Qt.Horizontal, self.colorTrackingBox)
    # self.greenMinSlider.setGeometry(60, 152, 120, h_btn2)
    # self.greenMinSlider.setMinimum(0)
    # self.greenMinSlider.setMaximum(255)
    # self.greenMinSlider.setValue(10)
    # self.greenMinSlider.sliderReleased.connect(self.singleColorSlider_released)
    # self.greenMinSlider.valueChanged.connect(self.singleColorSlider_released)
    # greenMaxTxt = QLabel('Max:', self.colorTrackingBox)
    # greenMaxTxt.setGeometry(x_cln1, 165, 100, h_txt)
    # self.greenMaxLeftBtn_CT = QPushButton('<', self.colorTrackingBox)
    # self.greenMaxLeftBtn_CT.setGeometry(40, 172, w_btn2, h_btn2)
    # self.greenMaxLeftBtn_CT.clicked.connect(self.greenMaxLeftBtn_CT_clicked)
    # self.greenMaxRightBtn_CT = QPushButton('>', self.colorTrackingBox)
    # self.greenMaxRightBtn_CT.setGeometry(185, 172, w_btn2, h_btn2)
    # self.greenMaxRightBtn_CT.clicked.connect(self.greenMaxRightBtn_CT_clicked)
    # self.greenMaxSlider = QSlider(Qt.Horizontal, self.colorTrackingBox)
    # self.greenMaxSlider.setGeometry(60, 172, 120, h_btn2)
    # self.greenMaxSlider.setMinimum(0)
    # self.greenMaxSlider.setMaximum(255)
    # self.greenMaxSlider.setValue(255)
    # self.greenMaxSlider.sliderReleased.connect(self.singleColorSlider_released)
    # self.greenMaxSlider.valueChanged.connect(self.singleColorSlider_released)
    # blueChannelTxt = QLabel('Blue channel:', self.colorTrackingBox)
    # blueChannelTxt.setGeometry(x_cln1, 185, 100, h_txt)
    # blueMinTxt = QLabel('Min:', self.colorTrackingBox)
    # blueMinTxt.setGeometry(x_cln1, 205, 100, h_txt)
    # self.blueMinLeftBtn_CT = QPushButton('<', self.colorTrackingBox)
    # self.blueMinLeftBtn_CT.setGeometry(40, 212, w_btn2, h_btn2)
    # self.blueMinLeftBtn_CT.clicked.connect(self.blueMinLeftBtn_CT_clicked)
    # self.blueMinRightBtn_CT = QPushButton('>', self.colorTrackingBox)
    # self.blueMinRightBtn_CT.setGeometry(185, 212, w_btn2, h_btn2)
    # self.blueMinRightBtn_CT.clicked.connect(self.blueMinRightBtn_CT_clicked)
    # self.blueMinSlider = QSlider(Qt.Horizontal, self.colorTrackingBox)
    # self.blueMinSlider.setGeometry(60, 212, 120, h_btn2)
    # self.blueMinSlider.setMinimum(0)
    # self.blueMinSlider.setMaximum(255)
    # self.blueMinSlider.sliderReleased.connect(self.singleColorSlider_released)
    # self.blueMinSlider.valueChanged.connect(self.singleColorSlider_released)
    # blueMaxTxt = QLabel('Max:', self.colorTrackingBox)
    # blueMaxTxt.setGeometry(x_cln1, 225, 100, h_txt)
    # self.blueMaxLeftBtn_CT = QPushButton('<', self.colorTrackingBox)
    # self.blueMaxLeftBtn_CT.setGeometry(40, 232, w_btn2, h_btn2)
    # self.blueMaxLeftBtn_CT.clicked.connect(self.blueMaxLeftBtn_CT_clicked)
    # self.blueMaxRightBtn_CT = QPushButton('>', self.colorTrackingBox)
    # self.blueMaxRightBtn_CT.setGeometry(185, 232, w_btn2, h_btn2)
    # self.blueMaxRightBtn_CT.clicked.connect(self.blueMaxRightBtn_CT_clicked)
    # self.blueMaxSlider = QSlider(Qt.Horizontal, self.colorTrackingBox)
    # self.blueMaxSlider.setGeometry(60, 232, 120, h_btn2)
    # self.blueMaxSlider.setMinimum(0)
    # self.blueMaxSlider.setMaximum(255)
    # self.blueMaxSlider.setValue(255)
    # self.blueMaxSlider.sliderReleased.connect(self.singleColorSlider_released)
    # self.blueMaxSlider.valueChanged.connect(self.singleColorSlider_released)

    # filterParticleTxt = QLabel('Filter particle:', self.colorTrackingBox)
    # filterParticleTxt.setGeometry(x_cln1, 250, 150, h_txt)
    # self.particleSldrMax = QLineEdit('1000', self.colorTrackingBox)
    # self.particleSldrMax.setGeometry(140, 253, 35, h_lbl)
    # self.filterParticleSldr_CT = QSlider(Qt.Horizontal, self.colorTrackingBox)
    # self.filterParticleSldr_CT.setGeometry(x_cln1, 275, 170, h_btn2)
    # self.filterParticleSldr_CT.setMinimum(1)
    # self.filterParticleSldr_CT.setMaximum(1000)
    # self.filterParticleSldr_CT.setValue(10)
    # self.filterParticleSldr_CT.sliderReleased.connect(self.filterParticleSldr_CT_released)
    #
    # avgLE_txt = QLabel('#px to locate edges:', self.colorTrackingBox)
    # avgLE_txt.setGeometry(x_cln1, 295, 100, h_txt)
    # self.avgLEIn_CT = QLineEdit('1', self.colorTrackingBox)
    # self.avgLEIn_CT.setGeometry(x_cln2, 300, 30, h_lbl)
    # connectivityTxt = QLabel('Connectivity (px):', self.colorTrackingBox)
    # connectivityTxt.setGeometry(x_cln1, 325, 100, h_txt)
    # self.connectivityBox = QComboBox(self.colorTrackingBox)
    # self.connectivityBox.setGeometry(x_cln2, 330, 35, h_btn-2)
    # self.connectivityBox.addItem('4')
    # self.connectivityBox.addItem('8')
    # self.connectivityBox.activated.connect(self.connectivityBoxCT_clicked)

    #second column
    # x_cln1 = 220
    # x_cln2 = 330
    # self.saveChannelsBtn_CT = QPushButton('Save filter values', self.colorTrackingBox)
    # self.saveChannelsBtn_CT.setGeometry(x_cln1, 15, 140, h_btn)
    # self.saveChannelsBtn_CT.clicked.connect(self.saveChannelsBtn_CT_clicked)
    # self.loadChannelsBtn_CT = QPushButton('Load filter values', self.colorTrackingBox)
    # self.loadChannelsBtn_CT.setGeometry(x_cln1, 45, 140, h_btn)
    # self.loadChannelsBtn_CT.clicked.connect(self.loadChannelsBtn_CT_clicked)
    # self.helpBtn_CT = QPushButton('Help', self.colorTrackingBox)
    # self.helpBtn_CT.setGeometry(x_cln1, 75, 140, h_btn)
    # self.helpBtn_CT.clicked.connect(self.helpBtn_CT_clicked)
    # trackingTxt = QLabel('Flame tracking:', self.colorTrackingBox)
    # trackingTxt.setGeometry(x_cln1, 100, 120, h_txt)
    # self.lightROIBtn_CT = QPushButton('Pick bright region', self.colorTrackingBox)
    # self.lightROIBtn_CT.setGeometry(x_cln1, 130, 140, h_btn)
    # self.lightROIBtn_CT.clicked.connect(self.lightROIBtn_CT_clicked)
    # self.filterLight_CT = QCheckBox('Ignore flashing light', self.colorTrackingBox)
    # self.filterLight_CT.setGeometry(x_cln1, 155, 140, h_btn)
    # movAvgTxt = QLabel('Moving avg points:', self.colorTrackingBox)
    # movAvgTxt.setGeometry(x_cln1, 185, 100, h_txt)
    # self.movAvgIn_CT = QLineEdit('2', self.colorTrackingBox)
    # self.movAvgIn_CT.setGeometry(x_cln2, 190, 30, h_lbl)
    # self.colorTrackingBtn = QPushButton('Start tracking', self.colorTrackingBox)
    # self.colorTrackingBtn.setGeometry(x_cln1, 220, 140, h_btn)
    # self.colorTrackingBtn.clicked.connect(self.colorTrackingBtn_clicked)
    # self.absValBtn_CT = QPushButton('Absolute values', self.colorTrackingBox)
    # self.absValBtn_CT.setGeometry(x_cln1, 250, 140, h_btn)
    # self.absValBtn_CT.clicked.connect(self.absValBtn_CT_clicked)
    # self.saveBtn_CT = QPushButton('Save data', self.colorTrackingBox)
    # self.saveBtn_CT.setGeometry(x_cln1, 280, 140, h_btn)
    # self.saveBtn_CT.clicked.connect(self.saveBtn_CT_clicked)

    # # first label
    # self.lbl1_CT = QLabel(self.colorTrackingBox)
    # self.lbl1_CT.setGeometry(370, 15, 330, 250)
    # self.lbl1_CT.setStyleSheet('background-color: white')
    # self.showEdges = QCheckBox('Show edges location', self.colorTrackingBox)
    # self.showEdges.setGeometry(780, 270, 120, h_btn)
    # self.showEdges.setChecked(True)
    # self.exportEdges_CT = QCheckBox('Output video analysis', self.colorTrackingBox)
    # self.exportEdges_CT.setGeometry(780, 290, 120, h_btn)
    #
    # # second label
    # self.lbl2_CT = QLabel(self.colorTrackingBox)
    # self.lbl2_CT.setGeometry(710, 15, 330, 250)
    # self.lbl2_CT.setStyleSheet('background-color: white')
    # self.showFrameLargeBtn_CT = QPushButton('Show frames', self.colorTrackingBox)
    # self.showFrameLargeBtn_CT.setGeometry(920, 270, 120, h_btn)
    # self.showFrameLargeBtn_CT.clicked.connect(self.showFrameLargeBtn_CT_clicked)

def HSVTrackingBox(self):
    if sys.platform == 'darwin':
        self.HSVTrackingBox = QGroupBox(' ', self.analysisGroupBox)
        self.HSVTrackingBox.setGeometry(0, 0, 1050, 390)

        # size of GUI labels:
        h_lbl = 22
        h_txt = 30
        h_btn = 30
        h_slider = 25

        # first column without hsv channels objects
        x1 = [ 10,   5,  10, 140,  10,  10, 145,  10, 120]
        y1 = [ 20,  45, 280, 283, 305, 330, 334, 360, 360]
        w1 = [100, 150, 150,  35, 170, 140,  30, 100,  60]

        # first column - 'hsv' objects
        x_hsv = [ 10,  10,  35, 175,  60,  10,  35, 175,  60]
        w_hsv = [100, 100,  30,  30, 120, 100,  30,  30, 120]

        y_h   = [ 70,  92,  90,  90,  95, 114, 112, 112, 117]
        y_s   = [140, 162, 160, 160, 165, 184, 182, 182, 187]
        y_v   = [210, 232, 230, 230, 235, 254, 252, 252, 257]

        # second column
        x2 = [210, 210, 210, 220, 210, 220, 220, 325, 210, 210, 210]
        y2 = [ 30,  60,  90, 120, 145, 170, 200, 204, 230, 260, 290]
        w2 = [150, 150, 150, 120, 150, 135, 130,  30, 150, 150, 150]

        # other objects
        x3 = [780, 930, 780, 780]
        y3 = [275, 275, 300, 325]
        w3 = [135, 115, 135, 130]

        # labels (since there's only two, in this case I wrote the entire set of coord.)
        lbl1 = [370,  25, 670, 125]
        lbl2 = [370, 150, 670, 125]

    elif sys.platform == 'win32':
        self.HSVTrackingBox = QGroupBox(' ', self.analysisGroupBox)
        self.HSVTrackingBox.setGeometry(0, 0, 1050, 390)

        # size of GUI labels:
        h_lbl = 22
        h_txt = 30
        h_btn = 30
        h_slider = 25

        # first column without hsv channels objects
        x1 = [ 10,   5,  10, 140,  10,  10, 145,  10, 120]
        y1 = [ 20,  45, 280, 283, 305, 330, 334, 360, 360]
        w1 = [100, 150, 150,  35, 170, 140,  30, 100,  60]

        # first column - 'hsv' objects
        x_hsv = [ 10,  10,  35, 175,  60,  10,  35, 175,  60]
        w_hsv = [100, 100,  30,  30, 120, 100,  30,  30, 120]

        y_h   = [ 70,  92,  90,  90,  95, 114, 112, 112, 117]
        y_s   = [140, 162, 160, 160, 165, 184, 182, 182, 187]
        y_v   = [210, 232, 230, 230, 235, 254, 252, 252, 257]

        # second column
        x2 = [210, 210, 210, 220, 210, 220, 220, 325, 210, 210, 210]
        y2 = [ 30,  60,  90, 120, 145, 170, 200, 204, 230, 260, 290]
        w2 = [150, 150, 150, 120, 150, 135, 130,  30, 150, 150, 150]

        # other objects
        x3 = [780, 930, 780, 780]
        y3 = [275, 275, 300, 325]
        w3 = [135, 115, 135, 130]

        # labels (since there's only two, in this case I wrote the entire set of coord.)
        lbl1 = [370,  25, 670, 125]
        lbl2 = [370, 150, 670, 125]

    elif sys.platform == 'linux':
        self.HSVTrackingBox = QGroupBox(' ', self.analysisGroupBox)
        self.HSVTrackingBox.setGeometry(0, 0, 1050, 390)

        # size of GUI labels:
        h_lbl = 22
        h_txt = 30
        h_btn = 30
        h_slider = 25

        # first column without hsv channels objects
        x1 = [ 10,   5,  10, 140,  10,  10, 145,  10, 120]
        y1 = [ 20,  45, 280, 283, 305, 330, 334, 360, 360]
        w1 = [100, 150, 150,  35, 170, 140,  30, 100,  60]

        # first column - 'hsv' objects
        x_hsv = [ 10,  10,  35, 175,  60,  10,  35, 175,  60]
        w_hsv = [100, 100,  30,  30, 120, 100,  30,  30, 120]

        y_h   = [ 70,  92,  90,  90,  95, 114, 112, 112, 117]
        y_s   = [140, 162, 160, 160, 165, 184, 182, 182, 187]
        y_v   = [210, 232, 230, 230, 235, 254, 252, 252, 257]

        # second column
        x2 = [210, 210, 210, 220, 210, 220, 220, 325, 210, 210, 210]
        y2 = [ 30,  60,  90, 120, 145, 170, 200, 204, 230, 260, 290]
        w2 = [150, 150, 150, 120, 150, 135, 130,  30, 150, 150, 150]

        # other objects
        x3 = [780, 930, 780, 780]
        y3 = [275, 275, 300, 325]
        w3 = [135, 115, 135, 130]

        # labels (since there's only two, in this case I wrote the entire set of coord.)
        lbl1 = [370,  25, 670, 125]
        lbl2 = [370, 150, 670, 125]


    self.HSVTrackingBox.setStyleSheet('background-color: None')

    # w_btn2 = 30
    # #first column
    # x_cln1 = 10
    directionBoxTxt = QLabel('Flame direction:', self.HSVTrackingBox)
    directionBoxTxt.setGeometry(x1[0], y1[0], w1[0], h_txt)
    self.directionBox = QComboBox(self.HSVTrackingBox)
    self.directionBox.setGeometry(x1[1], y1[1], w1[1], h_btn)
    self.directionBox.addItem('Left to right')
    self.directionBox.addItem('Right to left')
    self.directionBox.activated.connect(self.directionHT_clicked)

    filterParticleTxt = QLabel('Filter particles:', self.HSVTrackingBox)
    filterParticleTxt.setGeometry(x1[2], y1[2], w1[2], h_txt)
    self.particleSldrMax = QLineEdit('1000', self.HSVTrackingBox)
    self.particleSldrMax.setGeometry(x1[3], y1[3], w1[3], h_lbl)
    self.filterParticleSldr_HT = QSlider(Qt.Horizontal, self.HSVTrackingBox)
    self.filterParticleSldr_HT.setGeometry(x1[4], y1[4], w1[4], h_slider)
    self.filterParticleSldr_HT.setMinimum(1)
    self.filterParticleSldr_HT.setMaximum(1000)
    self.filterParticleSldr_HT.setValue(20) #	was defulted to 10, but experience says around ~1228 or ~350 to not filter too much
    self.filterParticleSldr_HT.sliderReleased.connect(self.filterParticleSldr_HT_released)
    avgLE_txt = QLabel('#px to locate edges:', self.HSVTrackingBox)
    avgLE_txt.setGeometry(x1[5], y1[5], w1[5], h_txt)
    self.avgLEIn_HT = QLineEdit('10', self.HSVTrackingBox) #was defaulted to 1, but experience says around 5-10
    self.avgLEIn_HT.setGeometry(x1[6], y1[6], w1[6], h_lbl)
    connectivityTxt = QLabel('Connectivity (px):', self.HSVTrackingBox)
    connectivityTxt.setGeometry(x1[7], y1[7], w1[7], h_txt)
    self.connectivityBox = QComboBox(self.HSVTrackingBox)
    self.connectivityBox.setGeometry(x1[8], y1[8], w1[8], h_btn)
    self.connectivityBox.addItem('4')
    self.connectivityBox.addItem('8')
    self.connectivityBox.activated.connect(self.connectivityBoxHT_clicked)

    hueChannelTxt = QLabel('Hue:', self.HSVTrackingBox)
    hueChannelTxt.setGeometry(x_hsv[0], y_h[0], w_hsv[0], h_txt)
    hueMinTxt = QLabel('Min:', self.HSVTrackingBox)
    hueMinTxt.setGeometry(x_hsv[1], y_h[1], w_hsv[1], h_txt)
    self.hueMinLeftBtn_HT = QPushButton('<', self.HSVTrackingBox)
    self.hueMinLeftBtn_HT.setGeometry(x_hsv[2], y_h[2], w_hsv[2], h_btn)
    self.hueMinLeftBtn_HT.clicked.connect(self.hueMinLeftBtn_HT_clicked)
    self.hueMinRightBtn_HT = QPushButton('>', self.HSVTrackingBox)
    self.hueMinRightBtn_HT.setGeometry(x_hsv[3], y_h[3], w_hsv[3], h_btn)
    self.hueMinRightBtn_HT.clicked.connect(self.hueMinRightBtn_HT_clicked)
    # CAS slider setting:
    self.hueMinSlider = QSlider(Qt.Horizontal, self.HSVTrackingBox)
    self.hueMinSlider.setGeometry(x_hsv[4], y_h[4], w_hsv[4], h_slider)
    self.hueMinSlider.setMinimum(0)
    self.hueMinSlider.setMaximum(180) # since stored as H/2 for 8-bit (normally 0-360)
    self.hueMinSlider.setValue(80) # Default to include blue values - 92=~185 deg Min Hue
    self.hueMinSlider.sliderReleased.connect(self.singleHSVSlider_released)
    self.hueMinSlider.valueChanged.connect(self.singleHSVSlider_released) #LC We need to check this line. I had to remove one from the other files (changed or released) because on Mac it counts twice
    hueMaxTxt = QLabel('Max:', self.HSVTrackingBox)
    hueMaxTxt.setGeometry(x_hsv[5], y_h[5], w_hsv[5], h_txt)
    self.hueMaxLeftBtn_HT = QPushButton('<', self.HSVTrackingBox)
    self.hueMaxLeftBtn_HT.setGeometry(x_hsv[6], y_h[6], w_hsv[6], h_btn)
    self.hueMaxLeftBtn_HT.clicked.connect(self.hueMaxLeftBtn_HT_clicked)
    self.hueMaxRightBtn_HT = QPushButton('>', self.HSVTrackingBox)
    self.hueMaxRightBtn_HT.setGeometry(x_hsv[7], y_h[7], w_hsv[7], h_btn)
    self.hueMaxRightBtn_HT.clicked.connect(self.hueMaxRightBtn_HT_clicked)
    # CAS slider setting:
    self.hueMaxSlider = QSlider(Qt.Horizontal, self.HSVTrackingBox)
    self.hueMaxSlider.setGeometry(x_hsv[8], y_h[8], w_hsv[8], h_slider)
    self.hueMaxSlider.setMinimum(0)
    self.hueMaxSlider.setMaximum(180) # since stored as H/2 for 8-bit (normally 0-360)
    self.hueMaxSlider.setValue(163) # Default to include blue values - 130=~260 deg Max Hue
    self.hueMaxSlider.sliderReleased.connect(self.singleHSVSlider_released)
    self.hueMaxSlider.valueChanged.connect(self.singleHSVSlider_released)

    satChannelTxt = QLabel('Saturation:', self.HSVTrackingBox)
    satChannelTxt.setGeometry(x_hsv[0], y_s[0], w_hsv[0], h_txt)
    satMinTxt = QLabel('Min:', self.HSVTrackingBox)
    satMinTxt.setGeometry(x_hsv[1], y_s[1], w_hsv[1], h_txt)
    self.satMinLeftBtn_HT = QPushButton('<', self.HSVTrackingBox)
    self.satMinLeftBtn_HT.setGeometry(x_hsv[2], y_s[2], w_hsv[2], h_btn)
    self.satMinLeftBtn_HT.clicked.connect(self.satMinLeftBtn_HT_clicked)
    self.satMinRightBtn_HT = QPushButton('>', self.HSVTrackingBox)
    self.satMinRightBtn_HT.setGeometry(x_hsv[3], y_s[3], w_hsv[3], h_btn)
    self.satMinRightBtn_HT.clicked.connect(self.satMinRightBtn_HT_clicked)
    # CAS slider setting:
    self.satMinSlider = QSlider(Qt.Horizontal, self.HSVTrackingBox)
    self.satMinSlider.setGeometry(x_hsv[4], y_s[4], w_hsv[4], h_slider)
    self.satMinSlider.setMinimum(0)
    self.satMinSlider.setMaximum(255)
    self.satMinSlider.setValue(30) # Default to include blue values - 100=~40% min Saturation
    self.satMinSlider.sliderReleased.connect(self.singleHSVSlider_released)
    self.satMinSlider.valueChanged.connect(self.singleHSVSlider_released)
    satMaxTxt = QLabel('Max:', self.HSVTrackingBox)
    satMaxTxt.setGeometry(x_hsv[5], y_s[5], w_hsv[5], h_txt)
    self.satMaxLeftBtn_HT = QPushButton('<', self.HSVTrackingBox)
    self.satMaxLeftBtn_HT.setGeometry(x_hsv[6], y_s[6], w_hsv[6], h_btn)
    self.satMaxLeftBtn_HT.clicked.connect(self.satMaxLeftBtn_HT_clicked)
    self.satMaxRightBtn_HT = QPushButton('>', self.HSVTrackingBox)
    self.satMaxRightBtn_HT.setGeometry(x_hsv[7], y_s[7], w_hsv[7], h_btn)
    self.satMaxRightBtn_HT.clicked.connect(self.satMaxRightBtn_HT_clicked)
    # CAS slider setting:
    self.satMaxSlider = QSlider(Qt.Horizontal, self.HSVTrackingBox)
    self.satMaxSlider.setGeometry(x_hsv[8], y_s[8], w_hsv[8], h_slider)
    self.satMaxSlider.setMinimum(0)
    self.satMaxSlider.setMaximum(255)
    self.satMaxSlider.setValue(255) # Default to some blue value - 255=~100% max Saturation
    self.satMaxSlider.sliderReleased.connect(self.singleHSVSlider_released)
    self.satMaxSlider.valueChanged.connect(self.singleHSVSlider_released)

    valChannelTxt = QLabel('Value:', self.HSVTrackingBox)
    valChannelTxt.setGeometry(x_hsv[0], y_v[0], w_hsv[0], h_txt)
    valMinTxt = QLabel('Min:', self.HSVTrackingBox)
    valMinTxt.setGeometry(x_hsv[1], y_v[1], w_hsv[1], h_txt)
    self.valMinLeftBtn_HT = QPushButton('<', self.HSVTrackingBox)
    self.valMinLeftBtn_HT.setGeometry(x_hsv[2], y_v[2], w_hsv[2], h_btn)
    self.valMinLeftBtn_HT.clicked.connect(self.valMinLeftBtn_HT_clicked)
    self.valMinRightBtn_HT = QPushButton('>', self.HSVTrackingBox)
    self.valMinRightBtn_HT.setGeometry(x_hsv[3], y_v[3], w_hsv[3], h_btn)
    self.valMinRightBtn_HT.clicked.connect(self.valMinRightBtn_HT_clicked)
    # CAS slider setting:
    self.valMinSlider = QSlider(Qt.Horizontal, self.HSVTrackingBox)
    self.valMinSlider.setGeometry(x_hsv[4], y_v[4], w_hsv[4], h_slider)
    self.valMinSlider.setMinimum(0)
    self.valMinSlider.setMaximum(255)
    self.valMinSlider.setValue(20) # Default to some blue value - 63=~25% min Value
    self.valMinSlider.sliderReleased.connect(self.singleHSVSlider_released)
    self.valMinSlider.valueChanged.connect(self.singleHSVSlider_released)
    valMaxTxt = QLabel('Max:', self.HSVTrackingBox)
    valMaxTxt.setGeometry(x_hsv[5], y_v[5], w_hsv[5], h_txt)
    self.valMaxLeftBtn_HT = QPushButton('<', self.HSVTrackingBox)
    self.valMaxLeftBtn_HT.setGeometry(x_hsv[6], y_v[6], w_hsv[6], h_btn)
    self.valMaxLeftBtn_HT.clicked.connect(self.valMaxLeftBtn_HT_clicked)
    self.valMaxRightBtn_HT = QPushButton('>', self.HSVTrackingBox)
    self.valMaxRightBtn_HT.setGeometry(x_hsv[7], y_v[7], w_hsv[7], h_btn)
    self.valMaxRightBtn_HT.clicked.connect(self.valMaxRightBtn_HT_clicked)
    # CAS slider setting:
    self.valMaxSlider = QSlider(Qt.Horizontal, self.HSVTrackingBox)
    self.valMaxSlider.setGeometry(x_hsv[8], y_v[8], w_hsv[8], h_slider)
    self.valMaxSlider.setMinimum(0)
    self.valMaxSlider.setMaximum(255)
    self.valMaxSlider.setValue(255) # Default to some blue value - 255=~100% max Value
    self.valMaxSlider.sliderReleased.connect(self.singleHSVSlider_released)
    self.valMaxSlider.valueChanged.connect(self.singleHSVSlider_released)

    #second column
    # x_cln1 = 220
    self.saveChannelsBtn_HT = QPushButton('Save filter values', self.HSVTrackingBox)
    self.saveChannelsBtn_HT.setGeometry(x2[0], y2[0], w2[0], h_btn)
    self.saveChannelsBtn_HT.clicked.connect(self.saveChannelsBtn_HT_clicked)
    self.loadChannelsBtn_HT = QPushButton('Load filter values', self.HSVTrackingBox)
    self.loadChannelsBtn_HT.setGeometry(x2[1], y2[1], w2[1], h_btn)
    self.loadChannelsBtn_HT.clicked.connect(self.loadChannelsBtn_HT_clicked)
    self.helpBtn_HT = QPushButton('Help', self.HSVTrackingBox)
    self.helpBtn_HT.setGeometry(x2[2], y2[2], w2[2], h_btn)
    self.helpBtn_HT.clicked.connect(self.helpBtn_HT_clicked)
    trackingTxt = QLabel('Flame tracking:', self.HSVTrackingBox)
    trackingTxt.setGeometry(x2[3], y2[3], w2[3], h_txt)

    self.lightROIBtn_HT = QPushButton('Pick bright region', self.HSVTrackingBox)
    self.lightROIBtn_HT.setGeometry(x2[4], y2[4], w2[4], h_btn)
    self.lightROIBtn_HT.clicked.connect(self.lightROIBtn_HT_clicked)
    self.filterLight_HT = QCheckBox('Ignore flashing light', self.HSVTrackingBox)
    self.filterLight_HT.setGeometry(x2[5], y2[5], w2[5], h_btn)
    movAvgTxt = QLabel('Moving avg points:', self.HSVTrackingBox)
    movAvgTxt.setGeometry(x2[6], y2[6], w2[6], h_txt)
    self.movAvgIn_HT = QLineEdit('5', self.HSVTrackingBox) #was defaulted to 2, experience says around 5 better
    self.movAvgIn_HT.setGeometry(x2[7], y2[7], w2[7], h_lbl)
    self.HSVTrackingBtn = QPushButton('Start tracking', self.HSVTrackingBox)
    self.HSVTrackingBtn.setGeometry(x2[8], y2[8], w2[8], h_btn)
    self.HSVTrackingBtn.clicked.connect(self.HSVTrackingBtn_clicked)
    self.absValBtn_HT = QPushButton('Absolute values', self.HSVTrackingBox)
    self.absValBtn_HT.setGeometry(x2[9], y2[9], w2[9], h_btn)
    self.absValBtn_HT.clicked.connect(self.absValBtn_HT_clicked)
    self.saveBtn_HT = QPushButton('Save data', self.HSVTrackingBox)
    self.saveBtn_HT.setGeometry(x2[10], y2[10], w2[10], h_btn)
    self.saveBtn_HT.clicked.connect(self.saveBtn_HT_clicked)

    # other objects
    self.showEdges = QCheckBox('Show edges location', self.HSVTrackingBox)
    self.showEdges.setGeometry(x3[0], y3[0], w3[0], h_btn)
    self.showEdges.setChecked(True)
    self.showFrameLargeBtn_HT = QPushButton('Show frames', self.HSVTrackingBox)
    self.showFrameLargeBtn_HT.setGeometry(x3[1], y3[1], w3[1], h_btn)
    self.showFrameLargeBtn_HT.clicked.connect(self.showFrameLargeBtn_HT_clicked)
    self.exportEdges_HT = QCheckBox('Output video analysis', self.HSVTrackingBox)
    self.exportEdges_HT.setGeometry(x3[2], y3[2], w3[2], h_btn)
    #CAS Export with tracking line
    self.exportTrackOverlay_HT = QCheckBox('Video Tracking Overlay', self.HSVTrackingBox)
    self.exportTrackOverlay_HT.setGeometry(x3[3], y3[3], w3[3], h_btn)

    # first label
    self.lbl1_HT = QLabel(self.HSVTrackingBox)
    self.lbl1_HT.setGeometry(lbl1[0], lbl1[1], lbl1[2], lbl1[3])
    self.lbl1_HT.setStyleSheet('background-color: white')

    # second label
    self.lbl2_HT = QLabel(self.HSVTrackingBox)
    self.lbl2_HT.setGeometry(lbl2[0], lbl2[1], lbl2[2], lbl2[3])
    self.lbl2_HT.setStyleSheet('background-color: white')
