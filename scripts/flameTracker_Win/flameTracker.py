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

import cv2
import numpy as np
import csv
import sys
import time
import re
import pyqtgraph as pg

from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from manualTracking import *
from lumaTracking import *
from colorTracking import *
from pyqtgraph import PlotWidget, plot

#To make sure the resolution is correct also in Windows
if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        print('''Flame Tracker - Copyright (C) 2020,2021 Luca Carmignani
        This program comes with ABSOLUTELY NO WARRANTY; See the GNU General
        Public License for more details.
        This is free software, and you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.''')

        self.setWindowTitle('Flame Tracker (v1.0.1)')
        self.setGeometry(25, 25, 1070, 740) #10,10,1000,720
        #Box to choose video parameters, widgets are listed below
        parametersBox = QGroupBox('Preview box', self)
        parametersBox.setGeometry(10, 5, 1050, 350)
        #This box changes for each analysis;
        #widgets must be declared in the specific py file
        self.analysisGroupBox = QGroupBox('Analysis box', self)
        self.analysisGroupBox.setGeometry(10, 360, 1050, 370)

        ### parametersBox
        # first column
        x_cln1 = 10
        x_cln2 = 105
        h_lbl = 20
        h_txt = 30
        h_btn = 25
        self.msgLabel = QLabel('Welcome to the Flame Tracker! \n\n Click on the Help button to get started.', parametersBox)
        self.msgLabel.setGeometry(x_cln1, 20, 140, h_btn + 55)
        self.msgLabel.setStyleSheet('background-color: white')
        self.msgLabel.setWordWrap(True)
        self.helpBtn = QPushButton('Help', parametersBox)
        self.helpBtn.setGeometry(x_cln1, 105, 140, h_btn)
        self.helpBtn.clicked.connect(self.helpBtn_clicked)
        self.openBtn = QPushButton('Open', parametersBox)
        self.openBtn.setGeometry(x_cln1, 135, 50, h_btn)
        self.openBtn.clicked.connect(self.openBtn_clicked)
        self.openSelectionBox = QComboBox(parametersBox)
        self.openSelectionBox.setGeometry(65, 136, 85, h_btn - 1)
        self.openSelectionBox.addItem('Video')
        self.openSelectionBox.addItem('Image(s)')
        self.openSelectionBox.activated[str].connect(self.openSelection_click)
        self.fNameLbl = QLabel('(file name)', parametersBox)
        self.fNameLbl.setGeometry(x_cln1, 170, 140, h_lbl)
        self.fNameLbl.setStyleSheet('background-color: white')
        vWidthTxt = QLabel('Width (px):', parametersBox)
        vWidthTxt.setGeometry(x_cln1, 195, 60, h_txt)
        self.vWidthLbl = QLabel(parametersBox)
        self.vWidthLbl.setGeometry(x_cln2, 200, 45, h_lbl)
        self.vWidthLbl.setStyleSheet('background-color: white')
        vHeightTxt = QLabel('Height (px):', parametersBox)
        vHeightTxt.setGeometry(x_cln1, 225, 60, h_txt)
        self.vHeightLbl = QLabel(parametersBox)
        self.vHeightLbl.setGeometry(x_cln2, 230, 45, h_lbl)
        self.vHeightLbl.setStyleSheet('background-color: white')
        vFpsTxt = QLabel('Frame rate (fps):', parametersBox)
        vFpsTxt.setGeometry(x_cln1, 255, 85, h_txt)
        self.vFpsLbl = QLabel(parametersBox)
        self.vFpsLbl.setGeometry(x_cln2, 260, 45, h_lbl)
        self.vFpsLbl.setStyleSheet('background-color: white')
        vFramesTxt = QLabel('Frames #:', parametersBox)
        vFramesTxt.setGeometry(x_cln1, 285, 65, h_txt)
        self.vFramesLbl = QLabel(parametersBox)
        self.vFramesLbl.setGeometry(x_cln2, 290, 45, h_lbl)
        self.vFramesLbl.setStyleSheet('background-color: white')
        vDurationTxt = QLabel('Duration (s):', parametersBox)
        vDurationTxt.setGeometry(x_cln1, 315, 65, h_txt)
        self.vDurationLbl = QLabel(parametersBox)
        self.vDurationLbl.setGeometry(x_cln2, 320, 45, h_lbl)
        self.vDurationLbl.setStyleSheet('background-color: white')

        #second column
        x_cln1 = 170
        x_cln2 = 260
        w_cln1 = 80
        w_cln2 = 50
        clmn2_Txt = QLabel(parametersBox)
        clmn2_Txt.setText('Video parameters:')
        clmn2_Txt.setGeometry(x_cln1, 10, 120, h_txt)
        self.firstFrameTxt = QLabel('First frame:', parametersBox)
        self.firstFrameTxt.setGeometry(x_cln1, 35, w_cln1, h_txt)
        self.firstFrameIn = QLineEdit(parametersBox)
        self.firstFrameIn.setGeometry(x_cln2, 40, w_cln2, h_lbl)
        self.lastFrameTxt = QLabel('Last frame:', parametersBox)
        self.lastFrameTxt.setGeometry(x_cln1, 65, w_cln1, h_txt)
        self.lastFrameIn = QLineEdit(parametersBox)
        self.lastFrameIn.setGeometry(x_cln2, 70, w_cln2, h_lbl)
        self.skipFrameTxt = QLabel('Skip frames:', parametersBox)
        self.skipFrameTxt.setGeometry(x_cln1, 95, w_cln1, h_txt)
        self.skipFrameIn = QLineEdit(parametersBox)
        self.skipFrameIn.setGeometry(x_cln2, 100, w_cln2, h_lbl)
        self.scaleTxt = QLabel('Scale (px/mm):', parametersBox)
        self.scaleTxt.setGeometry(x_cln1, 125, w_cln1, h_txt)
        self.scaleIn = QLineEdit(parametersBox)
        self.scaleIn.setGeometry(x_cln2, 130, w_cln2, h_lbl)
        self.measureScaleBtn = QPushButton('Measure scale', parametersBox)
        self.measureScaleBtn.setGeometry(x_cln1, 160, 140, h_btn)
        self.measureScaleBtn.clicked.connect(self.measureScaleBtn_clicked)
        self.roiOneTxt = QLabel('ROI, x:', parametersBox)
        self.roiOneTxt.setGeometry(x_cln1, 195, w_cln1, h_txt)
        self.roiOneIn = QLineEdit(parametersBox)
        self.roiOneIn.setGeometry(x_cln2, 200, w_cln2, h_lbl)
        self.roiTwoTxt = QLabel('ROI, y:', parametersBox)
        self.roiTwoTxt.setGeometry(x_cln1, 225, w_cln1, h_txt)
        self.roiTwoIn = QLineEdit(parametersBox)
        self.roiTwoIn.setGeometry(x_cln2, 230, w_cln2, h_lbl)
        self.roiThreeTxt = QLabel('ROI, w:', parametersBox)
        self.roiThreeTxt.setGeometry(x_cln1, 255, w_cln1, h_txt)
        self.roiThreeIn = QLineEdit(parametersBox)
        self.roiThreeIn.setGeometry(x_cln2, 260, w_cln2, h_lbl)
        self.roiFourTxt = QLabel('ROI, h:', parametersBox)
        self.roiFourTxt.setGeometry(x_cln1, 285, w_cln1, h_txt)
        self.roiFourIn = QLineEdit(parametersBox)
        self.roiFourIn.setGeometry(x_cln2, 290, w_cln2, h_lbl)
        self.roiBtn = QPushButton('Select ROI', parametersBox)
        self.roiBtn.setGeometry(x_cln1, 317, 140, h_btn)
        self.roiBtn.clicked.connect(self.roiBtn_clicked)

        #third column
        x_cln1 = 330
        x_cln2 = 420
        w_cln1 = 60
        w_cln2 = 50
        adjustFramesTxt = QLabel('Adjust frames:', parametersBox)
        adjustFramesTxt.setGeometry(x_cln1, 10, 100, h_txt)
        self.rotationAngleInTxt = QLabel('Rotation (deg):', parametersBox)
        self.rotationAngleInTxt.setGeometry(x_cln1, 35, 120, h_txt)
        self.rotationAngleIn = QLineEdit(parametersBox)
        self.rotationAngleIn.setGeometry(x_cln2, 39, w_cln2, h_lbl)
        self.brightnessTxt = QLabel('Brightness:', parametersBox)
        self.brightnessTxt.setGeometry(x_cln1, 65, 150, h_txt)
        self.brightnessSlider = QSlider(Qt.Horizontal, parametersBox)
        self.brightnessSlider.setGeometry(x_cln1, 95, 137, 15)
        self.brightnessSlider.setMinimum(-50)
        self.brightnessSlider.setMaximum(50)
        self.brightnessSlider.setValue(0)
        self.brightnessSlider.sliderReleased.connect(self.editFramesSlider_released)
        self.brightnessSlider.valueChanged.connect(self.editFramesSlider_released)
        self.brightnessLbl = QLabel('0', parametersBox)
        self.brightnessLbl.setGeometry(x_cln2, 70, w_cln2, h_lbl - 2)
        self.brightnessLbl.setStyleSheet('background-color: white')
        self.contrastTxt = QLabel('Contrast:', parametersBox)
        self.contrastTxt.setGeometry(x_cln1, 110, 150, h_txt)
        self.contrastSlider = QSlider(Qt.Horizontal, parametersBox)
        self.contrastSlider.setGeometry(x_cln1, 140, 137, 15)
        self.contrastSlider.setMinimum(-100)
        self.contrastSlider.setMaximum(+100)
        self.contrastSlider.setValue(0)
        self.contrastSlider.sliderReleased.connect(self.editFramesSlider_released)
        self.contrastSlider.valueChanged.connect(self.editFramesSlider_released)
        self.contrastLbl = QLabel('0', parametersBox)
        self.contrastLbl.setGeometry(x_cln2, 115, w_cln2, h_lbl - 2)
        self.contrastLbl.setStyleSheet('background-color: white')
        self.grayscale = QCheckBox('Grayscale', parametersBox)
        self.grayscale.setGeometry(x_cln1, 165, 100, h_btn)
        self.correctionTxt = QLabel('Correction lengths (mm):', parametersBox)
        self.correctionTxt.setGeometry(x_cln1, 195, 140, h_txt)
        self.sLengthTxt = QLabel('Horizontal:', parametersBox)
        self.sLengthTxt.setGeometry(x_cln1, 220, 130, h_txt)
        self.sLengthIn = QLineEdit('-', parametersBox)
        self.sLengthIn.setGeometry(x_cln2, 225, w_cln2, h_lbl)
        self.sWidthTxt = QLabel('Vertical:', parametersBox)
        self.sWidthTxt.setGeometry(x_cln1, 250, w_cln1, h_txt)
        self.sWidthIn = QLineEdit('-', parametersBox)
        self.sWidthIn.setGeometry(x_cln2, 255, w_cln2, h_lbl)
        self.perspectiveBtn = QPushButton('Correct Perspective', parametersBox)
        self.perspectiveBtn.setGeometry(x_cln1, 280, 140, h_btn)
        self.perspectiveBtn.clicked.connect(self.perspectiveBtn_clicked)
        self.originalBtn = QPushButton('Restore original', parametersBox)
        self.originalBtn.setGeometry(x_cln1, 315, 140, h_btn)
        self.originalBtn.clicked.connect(self.originalBtn_clicked)

        # fourth column
        x_cln1 = 490
        x_cln2 = 580
        analysisTxt = QLabel('Analysis:', parametersBox)
        analysisTxt.setGeometry(x_cln1, 10, w_cln1, h_txt)
        self.analysisSelectionBox = QComboBox(parametersBox)
        self.analysisSelectionBox.setGeometry(x_cln1, 35, 140, h_btn)
        self.analysisSelectionBox.addItem('Choose analysis')
        self.analysisSelectionBox.addItem('Manual tracking')
        self.analysisSelectionBox.addItem('Luma tracking')
        self.analysisSelectionBox.addItem('Color tracking')
        self.analysisSelectionBox.activated[str].connect(self.analysis_click)
        saveLoadTxt = QLabel('Save/Load:', parametersBox)
        saveLoadTxt.setGeometry(x_cln1, 60, w_cln1, h_txt)
        self.saveParBtn = QPushButton('Save Parameters', parametersBox)
        self.saveParBtn.setGeometry(x_cln1, 85, 140, h_btn)
        self.saveParBtn.clicked.connect(self.saveParBtn_clicked)
        self.loadParBtn = QPushButton('Load Parameters', parametersBox)
        self.loadParBtn.setGeometry(x_cln1, 115, 140, h_btn)
        self.loadParBtn.clicked.connect(self.loadParBtn_clicked)
        exportTxt = QLabel('Save edited video:', parametersBox)
        exportTxt.setGeometry(x_cln1, 150, 140, h_txt)
        self.newVideoHelpBtn = QPushButton('?', parametersBox)
        self.newVideoHelpBtn.setGeometry(x_cln2 + 30, 155, 20, h_btn - 5)
        self.newVideoHelpBtn.clicked.connect(self.newVideoHelpBtn_clicked)
        fpsTxt = QLabel('Frame rate (fps):', parametersBox)
        fpsTxt.setGeometry(x_cln1, 180, 120, h_txt)
        self.fpsIn = QLineEdit('24', parametersBox)
        self.fpsIn.setGeometry(x_cln2, 185, 50, h_lbl)
        codecTxt = QLabel('Codec:', parametersBox)
        codecTxt.setGeometry(x_cln1, 210, 100, h_txt)
        self.codecIn = QLineEdit('mp4v', parametersBox)
        self.codecIn.setGeometry(x_cln2, 215, 50, h_lbl)
        formatTxt = QLabel('Format:', parametersBox)
        formatTxt.setGeometry(x_cln1, 240, 100, h_txt)
        self.formatIn = QLineEdit('mp4', parametersBox)
        self.formatIn.setGeometry(x_cln2, 245, 50, h_lbl)
        self.exportVideoBtn = QPushButton('Export video', parametersBox)
        self.exportVideoBtn.setGeometry(x_cln1, 280, 140, h_btn)
        self.exportVideoBtn.clicked.connect(self.exportVideoBtn_clicked)

        # preview label
        x_cln1 = 650
        self.win1 = QLabel(parametersBox)
        self.win1.setGeometry(x_cln1, 15, 390, 270)
        self.win1.setStyleSheet('background-color: white')
        self.frameTxt = QLabel('Current frame:', parametersBox)
        self.frameTxt.setGeometry(x_cln1, 290, 120, h_txt)
        self.frameIn = QLineEdit('0', parametersBox)
        self.frameIn.setGeometry(x_cln1 + 90, 296, w_cln2, h_lbl)
        self.goToFrameBtn = QPushButton('Go to frame', parametersBox)
        self.goToFrameBtn.setGeometry(x_cln1 + 165, 293, 100, h_btn - 2)
        self.goToFrameBtn.clicked.connect(self.goToFrameBtn_clicked)
        self.previewSlider = QSlider(Qt.Horizontal, parametersBox)
        self.previewSlider.setGeometry(x_cln1, 325, 390, 15)
        self.showFrameLargeBtn = QPushButton('Show frame', parametersBox)
        self.showFrameLargeBtn.setGeometry(945, 293, 90, h_btn - 2)
        self.showFrameLargeBtn.clicked.connect(self.showFrameLargeBtn_clicked)

        #default variables
        self.openSelection = 'video'

### methods
    def openSelection_click(self, text):
        selection = self.openSelectionBox.currentText()
        if selection == 'Video':
            self.openSelection = 'video'
        elif selection == 'Image(s)':
            self.openSelection = 'image(s)'

    def openBtn_clicked(self):
        if self.openSelection == 'video':
            try:
                self.fPath, fFilter = QFileDialog.getOpenFileName(self, 'Open File')
                # look for the name: look for '/' after any character (.), repeated any times (*), and extract everything that comes after in a non-greedy way
                self.fName = re.findall('.*[/](.*)?', self.fPath)
                self.fNameLbl.setText(str(self.fName[0]))
                self.fVideo = cv2.VideoCapture(self.fPath)
                self.vFrames = int(self.fVideo.get(cv2.CAP_PROP_FRAME_COUNT)) #get(7)
                self.vHeight = int(self.fVideo.get(cv2.CAP_PROP_FRAME_HEIGHT))
                self.vWidth = int(self.fVideo.get(cv2.CAP_PROP_FRAME_WIDTH))
                self.vFps = round(self.fVideo.get(cv2.CAP_PROP_FPS) * 100) / 100 #(get(5))
                self.vFramesLbl.setText(str(self.vFrames))
                self.vWidthLbl.setText(str(self.vWidth))
                self.vHeightLbl.setText(str(self.vHeight))
                self.vFpsLbl.setText(str(self.vFps))
                self.vDuration = self.vFrames / self.vFps
                self.vDuration = round(self.vDuration * 100) / 100 #only 2 decimals for duration
                self.vDurationLbl.setText(str(self.vDuration))
                self.roiOneIn.setText('0')
                self.roiTwoIn.setText('0')
                self.roiThreeIn.setText(str(self.vWidth - 1))
                self.roiFourIn.setText(str(self.vHeight - 1))
                self.firstFrameIn.setText('0')
                self.lastFrameIn.setText(str(self.vFrames - 1))
                self.skipFrameIn.setText('0')
                self.previewSlider.setMinimum(int(self.firstFrameIn.text()))
                self.previewSlider.setMaximum(int(self.lastFrameIn.text()))
                self.previewSlider.setValue(int(self.frameIn.text()))
                self.previewSlider.sliderReleased.connect(self.sliderValue_released)
                self.previewSlider.valueChanged.connect(self.sliderValue_released)
                self.frameIn.setText('0')
                self.rotationAngleIn.setText('0')
                self.perspectiveValue = False
                self.lumaTrackingValue = False
                self.colorTrackingValue = False
                self.editFrame = False
                self.colorTrackingValue = False
                self.rotationValue = False
                self.fVideo.set(1, 0)
                ret, frame = self.fVideo.read()
                showFrame(self, frame, 0)
                self.msgLabel.setText('Video read succesfully')
                for children in self.analysisGroupBox.findChildren(QGroupBox):
                    children.setParent(None)
            except:
                self.msgLabel.setText('Error: the video could not be opened')
        elif self.openSelection == 'image(s)':
            try:
                self.fPath, fFilter = QFileDialog.getOpenFileNames(self, 'Open Images')
                self.imagesList = list()
                for name in self.fPath:
                    self.imagesList.append(name)

                if len(self.imagesList) == 1:
                    self.fName = re.findall('.*[/](.*)?', self.fPath[0])
                    self.fNameLbl.setText(str(self.fName[0]))
                    fps = 1
                elif len(self.imagesList) > 1:
                    self.fName = re.findall('.*[/](.*)?', self.fPath[0])
                    self.fNameLbl.setText(str(self.fName[0] + ', ...'))
                    fps, done1 = QInputDialog.getText(self, 'Input Dialog', 'Please specify frames per second:')
                    if not fps:
                        fps = 1

                image = cv2.imread(self.imagesList[0])

                self.vFrames = len(self.imagesList)
                self.vHeight = int(image.shape[0])
                self.vWidth = int(image.shape[1])
                self.vFps = fps
                self.vFramesLbl.setText(str(self.vFrames))
                self.vWidthLbl.setText(str(self.vWidth))
                self.vHeightLbl.setText(str(self.vHeight))
                self.vFpsLbl.setText(str(self.vFps))
                self.vDuration = self.vFrames / float(self.vFps)
                self.vDuration = round(self.vDuration * 100) / 100 #only 2 decimals for duration
                self.vDurationLbl.setText(str(self.vDuration))
                self.roiOneIn.setText('0')
                self.roiTwoIn.setText('0')
                self.roiThreeIn.setText(str(self.vWidth - 1))
                self.roiFourIn.setText(str(self.vHeight - 1))
                self.firstFrameIn.setText('0')
                self.lastFrameIn.setText(str(self.vFrames - 1))
                self.skipFrameIn.setText('0')
                self.frameIn.setText('0')
                self.previewSlider.setMinimum(int(self.firstFrameIn.text()))
                self.previewSlider.setMaximum(int(self.lastFrameIn.text()))
                self.previewSlider.setValue(int(self.frameIn.text()))
                self.previewSlider.sliderReleased.connect(self.sliderValue_released)
                self.previewSlider.valueChanged.connect(self.sliderValue_released)
                self.rotationAngleIn.setText('0')
                self.perspectiveValue = False
                self.lumaTrackingValue = False
                self.colorTrackingValue = False
                self.editFrame = False
                self.colorTrackingValue = False
                self.rotationValue = False
                frameNumber = self.imagesList[0]
                frame = cv2.imread(frameNumber)
                showFrame(self, frame, 0)
                self.msgLabel.setText('Image(s)read succesfully')
                for children in self.analysisGroupBox.findChildren(QGroupBox):
                    children.setParent(None)
            except:
                self.msgLabel.setText('Error: the image(s) could not be opened')

    def goToFrameBtn_clicked(self):
        newFrame = int(self.frameIn.text())
        if newFrame < int(self.firstFrameIn.text()):
            self.firstFrameIn.setText(str(newFrame))
        elif newFrame > int(self.lastFrameIn.text()):
            self.lastFrameIn.setText(str(newFrame))
        if self.openSelection == 'video':
            self.fVideo.set(1, newFrame)
            ret, frame = self.fVideo.read()
        elif self.openSelection == 'image(s)':
            imageName = self.imagesList[newFrame]
            frame = cv2.imread(imageName)

        showFrame(self, frame, newFrame)
        self.previewSlider.setValue(newFrame)

    def sliderValue_released(self):
        self.previewSlider.setMinimum(int(self.firstFrameIn.text()))
        self.previewSlider.setMaximum(int(self.lastFrameIn.text()))
        newFrame = self.previewSlider.value()
        if self.openSelection == 'video':
            self.fVideo.set(1, newFrame)
            ret, frame = self.fVideo.read()
        elif self.openSelection == 'image(s)':
            frameNumber = self.imagesList[newFrame]
            frame = cv2.imread(frameNumber)

        showFrame(self, frame, newFrame)
        # true value when the analysis is selected
        if self.lumaTrackingValue == True:
            # the labels might have become plot widgets, so we need to update them again
            self.lbl1_LT = QLabel(self.lumaTrackingBox)
            self.lbl1_LT.setGeometry(190, 15, 420, 300)
            self.lbl1_LT.setStyleSheet('background-color: white')
            self.lbl2_LT = QLabel(self.lumaTrackingBox)
            self.lbl2_LT.setGeometry(620, 15, 420, 300)
            self.lbl2_LT.setStyleSheet('background-color: white')
            if self.grayscale.isChecked() == True:
                self.msgLabel.setText('Grayscale images not supported with this feature')
            getLumaFrame(self, newFrame)
            self.lbl1_LT.setPixmap(QPixmap.fromImage(self.frameY))
            self.lbl2_LT.setPixmap(QPixmap.fromImage(self.frameBW))
            self.lbl1_LT.show()
            self.lbl2_LT.show()

        if self.colorTrackingValue == True:
            self.lbl1_CT = QLabel(self.colorTrackingBox)
            self.lbl1_CT.setGeometry(370, 15, 330, 250)
            self.lbl1_CT.setStyleSheet('background-color: white')
            self.lbl2_CT = QLabel(self.colorTrackingBox)
            self.lbl2_CT.setGeometry(710, 15, 330, 250)
            self.lbl2_CT.setStyleSheet('background-color: white')
            if self.grayscale.isChecked() == True:
                self.msgLabel.setText('Grayscale images not supported with this feature')
            getColorFilteredFrame(self, newFrame)
            self.lbl1_CT.setPixmap(QPixmap.fromImage(self.frame))
            self.lbl2_CT.setPixmap(QPixmap.fromImage(self.frameBW))
            self.lbl1_CT.show()
            self.lbl2_CT.show()

    def roiBtn_clicked(self):
        try:
            currentFrame = self.frameIn.text()
            if self.openSelection == 'video':
                self.fVideo.set(1, int(currentFrame))
                ret, frame = self.fVideo.read()
            elif self.openSelection == 'image(s)':
                frame = self.imagesList[int(currentFrame)]
                frame = cv2.imread(frame)

            frame = checkEditing(self, frame)

            # Select ROI
            self.roi = cv2.selectROI(frame)
            self.roiOneIn.setText(str(self.roi[0]))
            self.roiTwoIn.setText(str(self.roi[1]))
            self.roiThreeIn.setText(str(self.roi[2]))
            self.roiFourIn.setText(str(self.roi[3]))
            cv2.destroyAllWindows()
        except:
            self.msgLabel.setText('Ops! Something went wrong!')
            self.roiOneIn.setText('1')
            self.roiTwoIn.setText('1')
            self.roiThreeIn.setText('2')
            self.roiFourIn.setText('2')

        if self.colorTrackingValue == True:
            self.filterParticleSldr_CT.setMaximum(int((int(self.roiThreeIn.text()) * int(self.roiFourIn.text())) / 20))
        elif self.lumaTrackingValue == True:
            self.filterParticleSldr_LT.setMaximum(int((int(self.roiThreeIn.text()) * int(self.roiFourIn.text())) / 20))

    def perspectiveBtn_clicked(self):
        if self.sLengthIn.text() == '-' or self.sWidthIn.text() == '-':
            msg = QMessageBox(self)
            msg.setText('The reference length and width need to be specified')
            msg.exec_()

        try:
            msg = QMessageBox(self)
            msg.setText('The point order is: 1) top right, 2) bottom right, 3) bottom left, 4) top left.')
            msg.exec_()
            self.msgLabel.setText('1) top right, 2) bottom right, 3) bottom left, 4) top left')

            roiOne = int(self.roiOneIn.text())
            roiTwo = int(self.roiTwoIn.text())
            roiThree = int(self.roiThreeIn.text())
            roiFour = int(self.roiFourIn.text())
            sampleAspRatio = float(self.sLengthIn.text())/float(self.sWidthIn.text())
            frameNumber = int(self.frameIn.text())
            if self.openSelection == 'video':
                self.fVideo.set(1, frameNumber)
                ret, frame = self.fVideo.read()
            elif self.openSelection == 'image(s)':
                frame = self.imagesList[int(frameNumber)]
                frame = cv2.imread(frame)

            if int(self.brightnessSlider.value()) != 0 or int(self.contrastSlider.value()) != 0:
                frameContainer = np.zeros(frame.shape, frame.dtype)
                alpha = (int(self.contrastSlider.value()) + 100) * 2 / 200
                beta = int(self.brightnessSlider.value())    # Simple brightness control [0-100]. Instead, we have [-50-50]
                frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
            if self.grayscale.isChecked() == True:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # crop image
            frameCrop = frame[roiTwo : (roiTwo + roiFour), roiOne : (roiOne + roiThree)]
            cv2.namedWindow('Perspective Correction', cv2.WINDOW_AUTOSIZE)
            cv2.setMouseCallback('Perspective Correction', click)
            cv2.imshow('Perspective Correction', frameCrop)
            global clk
            clk = False # False unless the mouse is clicked
            posX = dict()
            posY = dict()

            for n in range(4):
                # wait for the mouse event or 'escape' key to quit
                while (True):
                    if clk == True:
                        clk = False
                        break

                    if cv2.waitKey(1) == 27:
                        cv2.destroyAllWindows()
                        return
                # update each position and frame list for the current click
                if str(n+1) in posX:
                    posX[str(n+1)].append(xPos)
                    posY[str(n+1)].append(yPos)
                else:
                    posX[str(n+1)] = [xPos]
                    posY[str(n+1)] = [yPos]

            cv2.destroyAllWindows()
            self.topRight = [(posX['1'][0] + roiOne), (posY['1'][0] + roiTwo)]
            self.bottomRight = [posX['2'][0] + roiOne, posY['2'][0] + roiTwo]
            self.bottomLeft = [posX['3'][0] + roiOne, posY['3'][0] + roiTwo]
            self.topLeft = [posX['4'][0] + roiOne, posY['4'][0] + roiTwo]
            # the following block allows the perspective correction in every direction
            if self.topLeft[1] > self.topRight[1]:
                sampleW = self.bottomRight[1] - self.topRight[1]
                sampleL = sampleW * sampleAspRatio
                self.topRightMod = self.topRight
                self.bottomRightMod = self.bottomRight
                self.bottomLeftMod = [(self.bottomRight[0] - sampleL), self.bottomRight[1]]
                self.topLeftMod = [(self.topRight[0] - sampleL), self.topRight[1]]
            else:
                sampleW = self.bottomLeft[1] - self.topLeft[1]
                sampleL = sampleW * sampleAspRatio
                self.topRightMod = [(self.topLeft[0] + sampleL), self.topLeft[1]]
                self.bottomRightMod = [(self.bottomLeft[0] + sampleL), self.bottomLeft[1]]
                self.bottomLeftMod = self.bottomLeft
                self.topLeftMod = self.topLeft

            self.sample = np.float32([self.topLeft, self.topRight, self.bottomRight, self.bottomLeft])
            self.sampleMod = np.float32([self.topLeftMod, self.topRightMod, self.bottomRightMod, self.bottomLeftMod])
            self.perspectiveValue = True # this value tells us if a flame is distorted or not
            self.msgLabel.setText('Image successfully corrected')
            showFrame(self, frame, frameNumber)

        except:
            self.msgLabel.setText('Ops! Something went wrong.')

    def originalBtn_clicked(self):
        self.perspectiveValue = False
        self.brightnessSlider.setValue(0)
        self.contrastSlider.setValue(0)

    def saveParBtn_clicked(self):
        name = QFileDialog.getSaveFileName(self, 'Save Parameters')
        name = name[0]
        if not name[-4:] == '.csv':
            name = name + '.csv'
        if name == '.csv': #this avoids name issues when the user closes the dialog without saving
            self.msgLabel.setText('Ops! Something was wrong with the file name.')
        else:
            try:
                with open(name, 'w', newline = '') as csvfile:
                    writer = csv.writer(csvfile, delimiter = ',')
                    writer.writerow(['File', self.fNameLbl.text()])
                    writer.writerow(['ROI', 'Value'])
                    writer.writerow([self.roiOneTxt.text(), str(self.roiOneIn.text())])
                    writer.writerow([self.roiTwoTxt.text(), str(self.roiTwoIn.text())])
                    writer.writerow([self.roiThreeTxt.text(), str(self.roiThreeIn.text())])
                    writer.writerow([self.roiFourTxt.text(), str(self.roiFourIn.text())])
                    writer.writerow([self.firstFrameTxt.text(), str(self.firstFrameIn.text())])
                    writer.writerow([self.lastFrameTxt.text(), str(self.lastFrameIn.text())])
                    writer.writerow([self.skipFrameTxt.text(), str(self.skipFrameIn.text())])
                    writer.writerow([self.scaleTxt.text(), str(self.scaleIn.text())])
                    writer.writerow([self.sLengthTxt.text(), str(self.sLengthIn.text())])
                    writer.writerow([self.sWidthTxt.text(), str(self.sWidthIn.text())])
                    writer.writerow([self.frameTxt.text(), str(self.frameIn.text())])
                    writer.writerow([self.rotationAngleInTxt.text(), str(self.rotationAngleIn.text())])
                    writer.writerow([self.brightnessTxt.text(), str(self.brightnessLbl.text())])
                    writer.writerow([self.contrastTxt.text(), str(self.contrastLbl.text())])
                self.msgLabel.setText('Parameters saved.')
            except:
                self.msgLabel.setText('Ops! Parameters were not saved.')

    def loadParBtn_clicked(self):
        name = QFileDialog.getOpenFileName(self, 'Open Parameters')
        try:
            with open(name[0], 'r') as csvfile:
                    reader = csv.reader(csvfile, delimiter = ',')
                    for row in reader:
                        if self.roiOneTxt.text() in row:
                            self.roiOneIn.setText(row[1])
                        if self.roiTwoTxt.text() in row:
                            self.roiTwoIn.setText(row[1])
                        if self.roiThreeTxt.text() in row:
                            self.roiThreeIn.setText(row[1])
                        if self.roiFourTxt.text() in row:
                            self.roiFourIn.setText(row[1])
                        if self.firstFrameTxt.text() in row:
                            self.firstFrameIn.setText(row[1])
                        if self.lastFrameTxt.text() in row:
                            self.lastFrameIn.setText(row[1])
                        if self.firstFrameTxt.text() in row:
                            self.firstFrameIn.setText(row[1])
                        if self.skipFrameTxt.text() in row:
                            self.skipFrameIn.setText(row[1])
                        if self.scaleTxt.text() in row:
                            self.scaleIn.setText(row[1])
                        if self.sLengthTxt.text() in row:
                            self.sLengthIn.setText(row[1])
                        if self.sWidthTxt.text() in row:
                            self.sWidthIn.setText(row[1])
                        if self.frameTxt.text() in row:
                            self.frameIn.setText(row[1])
                        if self.rotationAngleInTxt.text() in row:
                            self.rotationAngleIn.setText(row[1])
                        if self.brightnessTxt.text() in row:
                            self.brightnessLbl.setText(row[1])
                        if self.contrastTxt.text() in row:
                            self.contrastLbl.setText(row[1])
            self.msgLabel.setText('Parameters loaded.')
        except:
            notParameters_dlg = QErrorMessage(self)
            notParameters_dlg.showMessage('Ops! There was a problem loading the parameters.')
            self.msgLabel.setText('Parameters not loaded correctly.')
    # selection connected to the specific file, getting rid of what was showing before
    def analysis_click(self, text):
        selection = self.analysisSelectionBox.currentText()
        if selection == 'Choose analysis':
            for children in self.analysisGroupBox.findChildren(QGroupBox):
                children.setParent(None)
        elif selection == 'Manual tracking':
            for children in self.analysisGroupBox.findChildren(QGroupBox):
                children.setParent(None)
            createManualTrackingBox(self)
        elif selection == 'Luma tracking':
            for children in self.analysisGroupBox.findChildren(QGroupBox):
                children.setParent(None)
            createLumaTrackingBox(self)
        elif selection == 'Color tracking':
            for children in self.analysisGroupBox.findChildren(QGroupBox):
                children.setParent(None)
            createColorTrackingBox(self)

    def measureScaleBtn_clicked(self, text):
        try:
            roiOne = int(self.roiOneIn.text())
            roiTwo = int(self.roiTwoIn.text())
            roiThree = int(self.roiThreeIn.text())
            roiFour = int(self.roiFourIn.text())
            frameNumber = int(self.frameIn.text())
            global clk
            clk = False # False unless the mouse is clicked
            points = list()

            if self.openSelection == 'video':
                self.fVideo.set(1, frameNumber)
                ret, frame = self.fVideo.read()
            elif self.openSelection == 'image(s)':
                frame = self.imagesList[frameNumber]
                frame = cv2.imread(frame)

            frame = checkEditing(self, frame)

            # crop image
            frameCrop = frame[roiTwo : (roiTwo + roiFour), roiOne : (roiOne + roiThree)]

            cv2.namedWindow('MeasureScale', cv2.WINDOW_AUTOSIZE)
            cv2.setMouseCallback('MeasureScale', click)
            cv2.imshow('MeasureScale',frameCrop)
            for n in range(2):
                # wait for the mouse event or 'escape' key to quit
                while (True):
                    if clk == True:
                        clk = False
                        break

                    if cv2.waitKey(1) == 27: #ord('q')
                        cv2.destroyAllWindows()
                        return
                # update each position and frame list for the current click
                points.append(xPos)
                points.append(yPos)

            length_mm, done1 = QInputDialog.getText(self, 'Measure scale', 'Measured length in mm:')
            length_px = ((points[3]-points[1])**2 + (points[2]-points[0])**2)**0.5
            scale = length_px / float(length_mm)
            scale = np.round(scale, 3)
            self.scaleIn.setText(str(scale))
            self.msgLabel.setText('Scale succesfully measured')
            cv2.destroyAllWindows()
        except:
            self.msgLabel.setText('Something went wrong and the scale was not measured.')

    def editFramesSlider_released(self):
        frameNumber = self.previewSlider.value()
        if self.openSelection == 'video':
            self.fVideo.set(1, frameNumber)
            ret, frame = self.fVideo.read()
        elif self.openSelection == 'image(s)':
            frame = self.imagesList[frameNumber]
            frame = cv2.imread(frame)
        self.brightnessLbl.setText(str(self.brightnessSlider.value()))
        self.contrastLbl.setText(str(self.contrastSlider.value()))
        showFrame(self, frame, frameNumber)

    def exportVideoBtn_clicked(self):
        fps = round(float(self.fpsIn.text()))
        codec = str(self.codecIn.text())
        vFormat = str(self.formatIn.text())
        vName = QFileDialog.getSaveFileName(self, 'Save File')
        vName = vName[0]
        vName = str(vName) + '.' + str(vFormat) # alternative: 'output.{}'.format(vFormat)
        fourcc = cv2.VideoWriter_fourcc(*codec)
        size = (int(self.roiThreeIn.text()), int(self.roiFourIn.text()))

        # open and set properties
        vout = cv2.VideoWriter()
        if self.grayscale.isChecked() == True:
            vout.open(vName,fourcc,fps,size, isColor = False)
        else:
            vout.open(vName,fourcc,fps,size,True)

        firstFrame = int(self.firstFrameIn.text())
        lastFrame = int(self.lastFrameIn.text())
        currentFrame = firstFrame

        while (currentFrame < lastFrame):
            if self.openSelection == 'video':
                self.fVideo.set(1, currentFrame)
                ret, frame = self.fVideo.read()
            elif self.openSelection == 'image(s)':
                frameNumber = self.imagesList[currentFrame]
                frame = cv2.imread(frameNumber)

            frame = checkEditing(self, frame)
            frameCrop = frame[int(self.roiTwoIn.text()) : (int(self.roiTwoIn.text()) + int(self.roiFourIn.text())), int(self.roiOneIn.text()) : (int(self.roiOneIn.text()) + int(self.roiThreeIn.text()))]
            vout.write(frameCrop)
            print('Progress: ', round((currentFrame - firstFrame)/(lastFrame - firstFrame) * 10000)/100, '%')
            currentFrame = currentFrame + 1 + int(self.skipFrameIn.text())

        vout.release()
        print('Progress: 100 %, the video has been created.')
        self.msgLabel.setText('The video has been created.')

    def newVideoHelpBtn_clicked(self):
        msg = QMessageBox(self)
        msg.setText('''To save the video editing, after specifying the properties of the new video, click on 'Export Video'.

        If Skip frames is not zero, to keep the same time of the original video, the new frame rate should be:
        fps(new) = fps(original)/(skipframes + 1)

        Format and codec will depend on your operating system and the avaiable codecs (the best combination might require some trial and error).''')
        msg.exec_()

    def showFrameLargeBtn_clicked(self):
        cv2.namedWindow(('Frame: ' + self.frameIn.text()), cv2.WINDOW_AUTOSIZE)
        cv2.imshow(('Frame: ' + self.frameIn.text()), self.currentFrame)
        while True:
            if cv2.waitKey(1) == 27: #ord('q')
                cv2.destroyAllWindows()
                return

    ### Manual tracking block methods (defined in manualTracking.py)
    def directionMT_clicked(self, text):
        chooseFlameDirection_MT(self, text)
    def manualTrackingBtn_clicked(self):
        manualTracking(self)
    def saveData_clicked(self):
        saveData_ManualTracking(self)
    def absValBtnMT_clicked(self):
        absValueMT(self)
    def filterLightMT_clicked(self, text):
        chooseLightFilterMT(self, text)
    def helpBtn_MT_clicked(self):
        helpBtn_MT(self)

    ### Luma tracking block methods (defined in lumaTracking.py)
    def lumaTrackingBtn_clicked(self):
        lumaTracking(self)
    def directionLT_clicked(self, text):
        chooseFlameDirection_LT(self, text)
    def lumaSaveData_clicked(self):
        lumaSaveData(self)
    def absValBtnLT_clicked(self):
        absValueLT(self)
    def filterParticleSldr_LT_released(self):
        filterParticleSldr_LT(self)
    def showFrameLargeBtn_LT_clicked(self):
        showFrameLarge_LT(self)
    def helpBtn_LT_clicked(self):
        helpBtn_LT(self)

    ### Color tracking methods (defined in colorTracking.py)
    def singleColorSlider_released(self):
        colorSlider_released(self)
    def redMinLeftBtn_CT_clicked(self):
        redMinLeftBtn_CT(self)
    def redMinRightBtn_CT_clicked(self):
        redMinRightBtn_CT(self)
    def redMaxLeftBtn_CT_clicked(self):
        redMaxLeftBtn_CT(self)
    def redMaxRightBtn_CT_clicked(self):
        redMaxRightBtn_CT(self)
    def greenMinLeftBtn_CT_clicked(self):
        greenMinLeftBtn_CT(self)
    def greenMinRightBtn_CT_clicked(self):
        greenMinRightBtn_CT(self)
    def greenMaxLeftBtn_CT_clicked(self):
        greenMaxLeftBtn_CT(self)
    def greenMaxRightBtn_CT_clicked(self):
        greenMaxRightBtn_CT(self)
    def blueMinLeftBtn_CT_clicked(self):
        blueMinLeftBtn_CT(self)
    def blueMinRightBtn_CT_clicked(self):
        blueMinRightBtn_CT(self)
    def blueMaxLeftBtn_CT_clicked(self):
        blueMaxLeftBtn_CT(self)
    def blueMaxRightBtn_CT_clicked(self):
        blueMaxRightBtn_CT(self)
    def filterParticleSldr_CT_released(self):
        filterParticleSldr_CT(self)
    def directionCT_clicked(self, text):
        chooseFlameDirection_CT(self, text)
    def connectivityBoxCT_clicked(self, text):
        connectivityBox_CT(self, text)
    def saveChannelsBtn_CT_clicked(self):
        saveChannelsBtn_CT(self)
    def loadChannelsBtn_CT_clicked(self):
        loadChannelsBtn_CT(self)
    def colorTrackingBtn_clicked(self):
        colorTracking(self)
    def absValBtn_CT_clicked(self):
        absValBtn_CT(self)
    def saveBtn_CT_clicked(self):
        saveBtn_CT(self)
    def showFrameLargeBtn_CT_clicked(self):
        showFrameLarge_CT(self)
    def helpBtn_CT_clicked(self):
        helpBtn_CT(self)

    def helpBtn_clicked(self):
        msg = QMessageBox(self)
        msg.setText('''Flame Tracker is an image analysis program to detect and track a flame (or a luminous object) in images or videos (select the desired option before clicking on 'Open'). When opening folders with a large number of images, check that the number of frames corresponds to the correct number of images. Note that by opening more than one image a pop-up message will ask for the corresponding frame rate.

        First column - information of the opened file such as size, duration, etc.

        Second column -  shows initial and ending frames; only the selected range will show in the preview (the slider range will change as well). It is possible to skip frames for the analysis, but this number will not change the preview. The value of px/mm (scale) has to be specified before running any anlyses, and can be determined by clicking on 'Measure scale' and clicking on two reference points in the selected frame (a separate window will show up). A Region of Interest (ROI) can also be selected by dragging a rectangle in the selected frame after clicking on the button 'Select ROI'. Press 'Esc' keyboard to close the opened windows.

        Third column - optional adjustments: rotation, brightness and contrast. In case the perspective has to be corrected, two reference lengths have to be indicated (true values of horizontal and vertical lengths), corresponding to two length scales that will be selected in the frame. By clicking on 'Correct perspective' the order of mouse clicks is indicated.

        Fourth column - choose the type of analysis (specific instructions are available for each selection), save/load parameters. Furthermore, it is possible to specify frame rate, codec and format (according to the operative system), and create a new video with all the desired modifications (only the ROI will be exported). The button '?' offers suggestions related to the frame rate to choose for the new video.
        ''')
        msg.exec_()

# this function waits for the next mouse click
def click(event, x, y, flags, param):
    global xPos, yPos, clk

    if event == cv2.EVENT_LBUTTONUP:
        xPos = x
        yPos = y
        clk = True

def showFrame(self, frame, frameNumber):
    frame = checkEditing(self, frame)

    # create the rectangle based on the ROI and show it in preview
    firstPoint = (int(self.roiOneIn.text()), int(self.roiTwoIn.text()))
    secondPoint = (int(self.roiOneIn.text()) + int(self.roiThreeIn.text()), int(self.roiTwoIn.text()) + int(self.roiFourIn.text()))
    cv2.rectangle(frame, firstPoint, secondPoint, (255, 255, 255), 3)
    if self.grayscale.isChecked() == True:
        bytes = frame.shape[1]
        self.image = QImage(frame.data, frame.shape[1], frame.shape[0], bytes, QImage.Format_Grayscale8)
    else:
        bytes = 3 * frame.shape[1] #bytes per line, necessary to avoid distortion in the opened file
        self.image = QImage(frame.data, frame.shape[1], frame.shape[0], bytes, QImage.Format_RGB888).rgbSwapped()

    self.currentFrame = frame
    self.image = self.image.scaled(self.win1.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
    self.win1.setPixmap(QPixmap.fromImage(self.image))
    self.frameIn.setText(str(frameNumber))

def perspectiveCorrection(self, frame):
    M = cv2.getPerspectiveTransform(self.sample, self.sampleMod)
    frame = cv2.warpPerspective(frame, M, (frame.shape[1], frame.shape[0]))
    return(frame)

def rotationCorrection(self, frame):
    self.rotationValue = True
    # rotation matrix:
    angle = float(self.rotationAngleIn.text())
    width = int(self.vWidth)
    height = int(self.vHeight)
    center = (width/2, height/2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1) #center of rotation, angle, zoom In/zoom Out
    # rotation calculates the cos and sin, taking absolutes of those (these extra steps are used to avoid cropping)
    abs_cos = abs(matrix[0,0])
    abs_sin = abs(matrix[0,1])
    # find the new width and height bounds
    region_w = int(height * abs_sin + width * abs_cos)
    region_h = int(height * abs_cos + width * abs_sin)
    # subtract old image center (bringing image back to origin) and adding the new image center coordinates
    matrix[0, 2] += region_w/2 - center[0]
    matrix[1, 2] += region_h/2 - center[1]
    frame = cv2.warpAffine(frame, matrix, (region_w, region_h)) #resolution is specified
    return(frame)

def checkEditing(self, frame):
    if self.perspectiveValue == True:
        frame = perspectiveCorrection(self, frame)
        self.msgLabel.setText('Perspective corrected')
    if float(self.rotationAngleIn.text()) != 0:
        frame = rotationCorrection(self, frame)
    if int(self.brightnessSlider.value()) != 0 or int(self.contrastSlider.value()) != 0:
        frameContainer = np.zeros(frame.shape, frame.dtype)
        # alpha would go from 0 to 3, with lower contrast in 0-1. The scale is normalized in percentile
        alpha = (int(self.contrastSlider.value()) + 100) * 2 / 200
        beta = int(self.brightnessSlider.value())    # Simple brightness control [0-100]
        frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
    if self.grayscale.isChecked() == True:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return(frame)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
