"""
Flame Tracker. This program is designed to track flames or bright objects in videos or images.
Copyright (C) 2020-2023  Luca Carmignani; 2021-2023 Charles Scudiere

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

from PyQt6 import QtGui
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from itertools import zip_longest

import cv2
import numpy as np
import csv
import sys, os
import platform
import time
import re
import pyqtgraph as pg

# local files for the flame tracking
import manualTracking as mt
import lumaTracking as lt
import RGBTracking as rt
import HSVTracking as ht
import boxesGUI_OS as gui

#To make sure the resolution is correct also in Windows
if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

def initVars(self): # define initial variables
    # global manualTrackingValue, lumaTrackingValue, RGBTrackingValue, HSVTrackingValue, editFrame
    self.openSelection = 'video'
    self.perspectiveValue = False
    self.rotationValue = False
    self.refPoint = []
    self.refPoint_ROI = []
    # editFrame = False
    self.trackingMethod = None

class FlameTrackerWindow(QMainWindow): #QWidget
    def __init__(self, parent=None):
        super(FlameTrackerWindow, self).__init__(parent)

        print('''Flame Tracker - Copyright (C) 2020-2023 Luca Carmignani; 2021-2023 Charles Scudiere
        This program comes with ABSOLUTELY NO WARRANTY; See the GNU General
        Public License for more details.
        This is free software, and you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.''')

        # Flame Tracker version
        self.version_FT = 'v1.2.1'

        # creating the toolbar
        toolbar = QToolBar('FT toolbar')
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        # list of actions available (used for both the toolbar and menubar)
        openV_ico = QStyle.StandardPixmap.SP_DialogOpenButton
        openV_ico = self.style().standardIcon(openV_ico)
        openVideo = QAction(openV_ico, 'Open video', self)
        openVideo.triggered.connect(self.openVideo_clicked)
        openI_ico = QStyle.StandardPixmap.SP_DirIcon
        openI_ico = self.style().standardIcon(openI_ico)
        openImages = QAction(openI_ico, 'Open image(s)', self)
        openImages.triggered.connect(self.openImages_clicked)
        savePar_ico = QStyle.StandardPixmap.SP_DialogSaveButton
        savePar_ico = self.style().standardIcon(savePar_ico)
        savePar = QAction(savePar_ico, 'Save parameters', self)
        savePar.triggered.connect(self.saveParBtn_clicked)
        loadPar_ico = QStyle.StandardPixmap.SP_DriveDVDIcon
        loadPar_ico = self.style().standardIcon(loadPar_ico)
        loadPar = QAction(loadPar_ico, 'Load parameters', self)
        loadPar.triggered.connect(self.loadParBtn_clicked)
        measureScale = QAction('Scale (px/mm)', self)
        measureScale.triggered.connect(self.measureScaleBtn_clicked)
        refPoint = QAction('Point coordinates', self)
        refPoint.triggered.connect(self.refPointBtn_clicked)
        measureLength = QAction('Length/distance', self)
        measureLength.triggered.connect(self.measureLenBtn_clicked)
        exportVideo = QAction('Export edited video', self)
        exportVideo.triggered.connect(self.exportVideo_clicked)

        selection_MT = QAction('Manual tracking', self, checkable=True, checked=False)
        selection_MT.triggered.connect(self.showManualTracking)
        selection_LT = QAction('Luma tracking', self, checkable=True, checked=False)
        selection_LT.triggered.connect(self.showLumaTracking)
        selection_RT = QAction('RGB tracking', self, checkable=True, checked=False)
        selection_RT.triggered.connect(self.showRGBTracking)
        selection_HT = QAction('HSV tracking', self, checkable=True, checked=False)
        selection_HT.triggered.connect(self.showHSVTracking)

        showFrame = QAction('Show frame in new window', self)
        showFrame.triggered.connect(self.showFrameLarge_clicked)

        self.figSize = QAction('Reduced-size windows', self)
        self.figSize.setCheckable(True)

        toolbar.addAction(openVideo)
        toolbar.addAction(openImages)
        toolbar.addSeparator()
        toolbar.addAction(savePar)
        toolbar.addAction(loadPar)
        toolbar.addSeparator()

        scaleBtn = QPushButton('Scale')
        scaleBtn.clicked.connect(self.measureScaleBtn_clicked)
        toolbar.addWidget(scaleBtn)
        refPointBtn = QPushButton('Point')
        refPointBtn.clicked.connect(self.refPointBtn_clicked)
        toolbar.addWidget(refPointBtn)
        lengthBtn = QPushButton('Length')
        lengthBtn.clicked.connect(self.measureLenBtn_clicked)
        toolbar.addWidget(lengthBtn)

        toolbar.addSeparator()

        showFrameBtn = QPushButton('Frame')
        showFrameBtn.clicked.connect(self.showFrameLarge_clicked)
        toolbar.addWidget(showFrameBtn)

        ## creating the menu bar
        self.menu = self.menuBar()
        fileMenu = self.menu.addMenu('&File')
        fileMenu.addAction(openVideo)
        fileMenu.addAction(openImages)
        fileMenu.addAction(savePar)
        fileMenu.addAction(loadPar)
        fileMenu.addAction(exportVideo)

        measureMenu = self.menu.addMenu('&Measure')
        measureMenu.addAction(measureScale)
        measureMenu.addAction(refPoint)
        measureMenu.addAction(measureLength)

        trackingMenu = self.menu.addMenu('&Tracking')
        trackingMenu.addAction(selection_MT)
        trackingMenu.addAction(selection_LT)
        trackingMenu.addAction(selection_RT)
        trackingMenu.addAction(selection_HT)
        self.trackingGroup = QActionGroup(self)
        self.trackingGroup.addAction(selection_MT)
        self.trackingGroup.addAction(selection_LT)
        self.trackingGroup.addAction(selection_RT)
        self.trackingGroup.addAction(selection_HT)
        self.trackingGroup.setExclusive(True)

        frameMenu = self.menu.addMenu('&Show')
        frameMenu.addAction(showFrame)
        frameMenu.addAction(self.figSize)

        help_FT = QAction('Flame Tracker', self)
        help_FT.triggered.connect(self.help_FT_clicked)
        help_MT = QAction('Manual tracking', self)
        help_MT.triggered.connect(self.help_MT_clicked)
        help_LT = QAction('Luma tracking', self)
        help_LT.triggered.connect(self.help_LT_clicked)
        help_RT = QAction('RGB tracking', self)
        help_RT.triggered.connect(self.help_RT_clicked)
        help_HT = QAction('HSV tracking', self)
        help_HT.triggered.connect(self.help_HT_clicked)
        helpMenu = self.menu.addMenu("&Help")
        helpMenu.addAction(help_FT)
        helpMenu.addAction(help_MT)
        helpMenu.addAction(help_LT)
        helpMenu.addAction(help_RT)
        helpMenu.addAction(help_HT)

        # this function contains all the initial variables to declare
        initVars(self)

        # initialize GUI
        gui.previewBox(self)

### methods
    def showManualTracking(self):
        removeExistingMethod(self)
        gui.manualTrackingBox(self)
        mt.initVars(self)

    def showLumaTracking(self):
        removeExistingMethod(self)
        gui.lumaTrackingBox(self)

    def showRGBTracking(self):
        removeExistingMethod(self)
        gui.RGBTrackingBox(self)
        rt.initVars(self)

    def showHSVTracking(self):
        removeExistingMethod(self)
        gui.HSVTrackingBox(self)
        ht.initVars(self) # include default variables in this function

    def openVideo_clicked(self):
        self.openSelection = 'video'
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

            #Set parameter defaults upon opening a new video
            self.roiOneIn.setText('0')
            self.roiTwoIn.setText('0')
            self.roiThreeIn.setText(str(self.vWidth - 1))
            self.roiFourIn.setText(str(self.vHeight - 1))
            self.firstFrameIn.setText('0')
            self.lastFrameIn.setText(str(self.vFrames - 1))
            self.skipFrameIn.setText('5') # with 5 you would obtain an even number of points with 24, 30, and 60 fps (not too relevant)
            self.frameIn.setText('0')
            self.frameNumber = 0
            self.previewSlider.setMinimum(int(self.firstFrameIn.text()))
            self.previewSlider.setMaximum(int(self.lastFrameIn.text()))
            self.previewSlider.setValue(int(self.frameIn.text()))
            self.rotationAngleIn.setText('0')

            showFrame(self, self.frameNumber)
            self.msgLabel.setText('Video read succesfully')
        except:
            print('Unexpected error:', sys.exc_info())
            self.msgLabel.setText('Error: the video could not be opened')

    def openImages_clicked(self):
        self.openSelection = 'image(s)'
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
            self.frameNumber = 0
            self.previewSlider.setMinimum(int(self.firstFrameIn.text()))
            self.previewSlider.setMaximum(int(self.lastFrameIn.text()))
            self.previewSlider.setValue(int(self.frameIn.text()))
            self.rotationAngleIn.setText('0')

            showFrame(self, self.frameNumber)
            self.msgLabel.setText('Image(s)read succesfully')
        except:
            self.msgLabel.setText('Error: the image(s) could not be opened')
            print('Unexpected error:', sys.exc_info())

    def help_FT_clicked(self):
        msg = QMessageBox(self)
        msg.setText('''The Flame Tracker is an image analysis program designed to detect and track a flame (or a luminous object) in images or videos.

        Instructions available on GitHub: https://github.com/combustionTools/flameTracker/wiki

        Contact: flametrackercontact@gmail.com
        ''')
        msg.exec()

    def help_MT_clicked(self):
        msg = QMessageBox(self)
        msg.setText('''Manual Tracking allows you to track a flame with a point-and-click method.

        Instructions available on GitHub: https://github.com/combustionTools/flameTracker/wiki/3.-Manual-tracking
        ''')
        msg.exec()

    def help_LT_clicked(self):
        msg = QMessageBox(self)
        msg.setText('''Luma Tracking allows you to track a flame in an automatic way by considering the luminance intensity of each pixel in the ROI.

        Instructions available on GitHub: https://github.com/combustionTools/flameTracker/wiki/4.-Luma-Tracking
        ''')
        msg.exec()

    def help_RT_clicked(self):
        msg = QMessageBox(self)
        msg.setText('''RGB Tracking allows you to track a flame in an automatic way by considering the color intensity of each pixel in the ROI.

        Instructions available on GitHub: https://github.com/combustionTools/flameTracker/wiki/5.-Color-Tracking
        ''')
        msg.exec()

    def help_HT_clicked(self):
        msg = QMessageBox(self)
        msg.setText('''HSV Tracking allows you to track a flame in an automatic way by considering the intensity in the HSV space of each pixel in the ROI.

        The flame region can be identified by choosing appropriate values of the HSV parameters (and particle size filtering). The HSV values vary depending on the colorspace of the frame/image - current implementation uses a hue from 0-180 (since 0-360 deg hue is stored as H/2 for 8-bit), value and saturation are set from 0 to 255.
        The code will consider the range between minimum and maximum of each of the HSV channels as adjusted with the sliders. Small particles can be filtered out. The value of the slider indicates the area (in px^2) of the regions to remove from the image/frame, and you can change the maximum value by typing a number in the text box next to 'Filter particles'.

        The preview box on the left shows the RGB image resulting from the filtering, while the preview box on the right shows the binary image with the particle filtering applied. The edges of the flame region are calculated as maximum and minimum locations.

        If there is a flashing or strobe light in the recorded video, you can click on 'Pick bright region' to choose a rectangular region (in the same way that the ROI is selected) that is illuminated when the light is on and dark when it is off (this region is independent from the ROI specified in the 'Preview box'). The frames where the light is on can be discarded during the analysis by checking the 'Ignore flashing light' box.
        ''')
        msg.exec()

    def goToFrameBtn_clicked(self):
        self.frameNumber = int(self.frameIn.text())
        if self.frameNumber < int(self.firstFrameIn.text()):
            self.firstFrameIn.setText(str(self.frameNumber))
        elif self.frameNumber > int(self.lastFrameIn.text()):
            self.lastFrameIn.setText(str(self.frameNumber))

        self.previewSlider.setValue(int(self.frameNumber))
        showFrame(self, self.frameNumber)
        checkAnalysisMethod(self, self.frameNumber)

    def sliderValue_released(self):
        self.previewSlider.setMinimum(int(self.firstFrameIn.text()))
        self.previewSlider.setMaximum(int(self.lastFrameIn.text()))
        self.frameNumber = self.previewSlider.value()
        self.frameIn.setText(str(self.frameNumber))

        showFrame(self, self.frameNumber)
        checkAnalysisMethod(self, self.frameNumber)

    def sliderValue_scrolled(self):
        self.previewSlider.setMinimum(int(self.firstFrameIn.text()))
        self.previewSlider.setMaximum(int(self.lastFrameIn.text()))
        self.frameNumber = self.previewSlider.value()
        self.frameIn.setText(str(self.frameNumber))

        showFrame(self, self.frameNumber)

    def roiBtn_clicked(self):
        try:
            frame, frameCrop = checkEditing(self, self.frameNumber)

            # Select Region Of Interest
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
            self.roiThreeIn.setText('10')
            self.roiFourIn.setText('10')

    def perspectiveBtn_clicked(self):
        global clk

        if self.sLengthIn.text() == '-' or self.sWidthIn.text() == '-':
            msg = QMessageBox(self)
            msg.setText('The reference length and width need to be specified')
            msg.exec()

        self.msgLabel.setText('1) top right, 2) bottom right, 3) bottom left, 4) top left')

        try:
            msg = QMessageBox(self)
            msg.setText('The click order is: 1) top right, 2) bottom right, 3) bottom left, 4) top left.')
            msg.exec()

            roiOne = int(self.roiOneIn.text())
            roiTwo = int(self.roiTwoIn.text())
            roiThree = int(self.roiThreeIn.text())
            roiFour = int(self.roiFourIn.text())
            sampleAspRatio = float(self.sLengthIn.text())/float(self.sWidthIn.text())
            if self.openSelection == 'video':
                self.fVideo.set(1, self.frameNumber)
                ret, frame = self.fVideo.read()
            elif self.openSelection == 'image(s)':
                imageNumber = self.imagesList[int(self.frameNumber)]
                frame = cv2.imread(imageNumber)

            # The following conditions are the same of checkEditing(), here they are checked for the correction
            self.anglePerspective = float(self.rotationAngleIn.text())
            if float(self.rotationAngleIn.text()) != 0:
                self.rotationValue = True
                frame = rotationCorrection(self, frame, self.anglePerspective)
            if int(self.brightnessSlider.value()) != 0 or int(self.contrastSlider.value()) != 0:
                frameContainer = np.zeros(frame.shape, frame.dtype)
                alpha = (int(self.contrastSlider.value()) + 100) * 2 / 200
                beta = int(self.brightnessSlider.value())    # Simple brightness control [0-100]. Instead, we have [-50-50]
                frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
            if self.grayscale.isChecked() == True:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # crop image
            frameCrop = frame[roiTwo : (roiTwo + roiFour), roiOne : (roiOne + roiThree)]
            cv2.namedWindow('Perspective correction', cv2.WINDOW_AUTOSIZE)
            cv2.setMouseCallback('Perspective correction', click)
            if self.figSize.isChecked() == True:
                newWidth = int(frameCrop.shape[1] / 2) #original width divided by 2
                newHeight = int(frameCrop.shape[0] / 2) #original height divided by 2
                halfFig = cv2.resize(frameCrop, (newWidth, newHeight))
                cv2.imshow('Perspective correction', halfFig)
            else:
                cv2.imshow('Perspective correction', frameCrop)

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
                    if self.figSize.isChecked() == True:
                        posX[str(n+1)].append(xPos * 2)
                        posY[str(n+1)].append(yPos * 2)
                    else:
                        posX[str(n+1)].append(xPos)
                        posY[str(n+1)].append(yPos)
                else:
                    if self.figSize.isChecked() == True:
                        posX[str(n+1)] = [xPos * 2]
                        posY[str(n+1)] = [yPos * 2]
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
            showFrame(self, self.frameNumber)

        except:
            self.msgLabel.setText('Ops! Something went wrong.')
            print('Unexpected error:', sys.exc_info())

    def originalBtn_clicked(self):
        self.perspectiveValue = False
        self.rotationValue = False
        self.brightnessSlider.setValue(0)
        self.contrastSlider.setValue(0)
        self.brightnessLbl.setText(str(self.brightnessSlider.value()))
        self.contrastLbl.setText(str(self.contrastSlider.value()))
        showFrame(self, self.frameNumber)

    def saveParBtn_clicked(self):
        name = QFileDialog.getSaveFileName(self, 'Save parameters')
        name = name[0]
        if not name[-4:] == '.csv':
            name = name + '.csv'
        if name == '.csv': #this avoids name issues when the user closes the dialog without saving
            self.msgLabel.setText('Ops! The file name was not valid and the parameters were not saved.')
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
                    writer.writerow(['Scale (px/mm):', str(self.scaleIn.text())])
                    writer.writerow([self.sLengthTxt.text(), str(self.sLengthIn.text())])
                    writer.writerow([self.sWidthTxt.text(), str(self.sWidthIn.text())])
                    writer.writerow([self.frameTxt.text(), str(self.frameIn.text())])
                    writer.writerow([self.rotationAngleInTxt.text(), str(self.rotationAngleIn.text())])
                    writer.writerow([self.brightnessTxt.text(), str(self.brightnessLbl.text())])
                    writer.writerow([self.contrastTxt.text(), str(self.contrastLbl.text())])
                    if self.rotationValue == True:
                        writer.writerow(['Pre-rotation', 'Yes'])
                        writer.writerow(['anglePerspective', str(self.anglePerspective)])
                    if self.perspectiveValue == True:
                        writer.writerow(['Perspective', 'Yes'])
                        writer.writerow(['sample', self.sample[0], self.sample[1], self.sample[2], self.sample[3]])
                        writer.writerow(['sampleMod', self.sampleMod[0], self.sampleMod[1], self.sampleMod[2], self.sampleMod[3]])

                    if self.refPoint != []:
                        writer.writerow(['Ref. point (abs):', [self.refPoint[0], self.refPoint[1]]])
                        writer.writerow(['Ref. point (ROI):', [self.refPoint_ROI[0], self.refPoint_ROI[1]]])

                    writer.writerow(['code version', str(self.version_FT)])
                    self.msgLabel.setText('Parameters saved.')
            except:
                self.msgLabel.setText('Ops! Parameters were not saved.')
                print('Unexpected error:', sys.exc_info())

    def loadParBtn_clicked(self):
        name = QFileDialog.getOpenFileName(self, 'Open parameters')
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
                    if 'Scale (px/mm):' in row:
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
                    if 'anglePerspective' in row:
                        self.rotationValue = True
                        self.anglePerspective = float(row[1])
                    if 'sample' in row:
                        self.perspectiveValue = True
                        self.sample = []
                        for i in range(1,5): #x,y are the pixel values for each corner
                            points = re.findall('^\[(.+)\]$', row[i]) #this creates a list without '[]'
                            points = points[0].strip() #gets rid of white spaces
                            x = re.findall('(^[0-9]+.[0-9]*\s)', points)
                            y = re.findall('\s([0-9]+.[0-9]*$)', points)
                            self.sample.append([np.float32(x[0]), np.float32(y[0])])
                        self.sample = np.array(self.sample)
                    if 'sampleMod' in row:
                        self.sampleMod = []
                        for i in range(1,5):
                            points = re.findall('^\[(.+)\]$', row[i]) #this creates a list without '[]'
                            points = points[0].strip() #gets rid of white spaces
                            x = re.findall('(^[0-9]+.[0-9]*\s)', points)
                            y = re.findall('\s([0-9]+.[0-9]*$)', points)
                            self.sampleMod.append([np.float32(x[0]), np.float32(y[0])])
                        self.sampleMod = np.array(self.sampleMod)
                    if 'Ref. point (abs):' in row:
                        x = re.findall('^\[(.+),', row[1])
                        y = re.findall('^\[.+,\s(.+)\]$', row[1])
                        self.refPointIn.setText(f'{x[0]}, {y[0]}')

            self.previewSlider.setMinimum(int(self.firstFrameIn.text()))
            self.previewSlider.setMaximum(int(self.lastFrameIn.text()))
            self.previewSlider.setValue(int(self.frameIn.text()))

            if self.perspectiveValue == True:
                self.msgLabel.setText('Parameters loaded. Perspective correction detected and applied')
            else:
                self.msgLabel.setText('Parameters loaded.')
        except:
            notParameters_dlg = QErrorMessage(self)
            notParameters_dlg.showMessage('Ops! There was a problem loading the parameters.')
            self.msgLabel.setText('Parameters not loaded correctly.')
            print('Unexpected error:', sys.exc_info())

    def measureScaleBtn_clicked(self, text):
        global clk
        clk = False # False unless the mouse is clicked
        try:
            roiOne = int(self.roiOneIn.text())
            roiTwo = int(self.roiTwoIn.text())
            roiThree = int(self.roiThreeIn.text())
            roiFour = int(self.roiFourIn.text())

            points = list()

            frame, frameCrop = checkEditing(self, self.frameNumber)

            cv2.namedWindow('MeasureScale', cv2.WINDOW_AUTOSIZE)
            cv2.setMouseCallback('MeasureScale', click)
            if self.figSize.isChecked() == True:
                newWidth = int(frameCrop.shape[1] / 2) #original width divided by 2
                newHeight = int(frameCrop.shape[0] / 2) #original height divided by 2
                halfFig = cv2.resize(frameCrop, (newWidth, newHeight))
                cv2.imshow('MeasureScale', halfFig)
            else:
                cv2.imshow('MeasureScale', frameCrop)

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
                if self.figSize.isChecked() == True:
                    points.append(xPos * 2)
                    points.append(yPos * 2)
                else:
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
            print('Unexpected error:', sys.exc_info())
            self.msgLabel.setText('Something went wrong and the scale was not measured.')

    def refPointBtn_clicked(self):
        global clk
        clk = False # False unless the mouse is clicked

        try:
            roiOne = int(self.roiOneIn.text())
            roiTwo = int(self.roiTwoIn.text())
            roiThree = int(self.roiThreeIn.text())
            roiFour = int(self.roiFourIn.text())

            frame, frameCrop = checkEditing(self, self.frameNumber)

            cv2.namedWindow('referencePoint', cv2.WINDOW_AUTOSIZE)
            cv2.setMouseCallback('referencePoint', click)
            if self.figSize.isChecked() == True:
                newWidth = int(frameCrop.shape[1] / 2) #original width divided by 2
                newHeight = int(frameCrop.shape[0] / 2) #original height divided by 2
                halfFig = cv2.resize(frameCrop, (newWidth, newHeight))
                cv2.imshow('referencePoint', halfFig)
            else:
                cv2.imshow('referencePoint', frame)

            # wait for the mouse event or 'escape' key to quit
            while (True):
                if clk == True:
                    xPos_abs = xPos #+ roiOne
                    yPos_abs = yPos #+ roiTwo
                    break

                if cv2.waitKey(1) == 27: #ord('q')
                    cv2.destroyAllWindows()
                    break

            if self.figSize.isChecked() == True:
                self.refPoint = [(xPos_abs * 2), (yPos_abs * 2)] #absolute point
                self.refPoint_ROI = [(xPos - roiOne) * 2, (yPos - roiTwo) * 2] #point function of ROI
            else:
                self.refPoint = [xPos_abs, yPos_abs] #absolute point
                self.refPoint_ROI = [xPos - roiOne, yPos - roiTwo] #point function of ROI

            self.msgLabel.setText(f'Reference point (absolute): ({self.refPoint[0]}, {self.refPoint[1]}); (ROI dependent): ({self.refPoint_ROI[0]}, {self.refPoint_ROI[1]})')
            self.refPointIn.setText(f'{self.refPoint[0]}, {self.refPoint[1]}')#str(self.refPoint) )
            cv2.destroyAllWindows()
        except:
            print('Unexpected error:', sys.exc_info())
            self.msgLabel.setText('Something went wrong and the reference point was not measured.')

    def measureLenBtn_clicked(self):
        self.msgLabel.setText('Click on two points to measure their distance.')
        global clk
        clk = False # False unless the mouse is clicked
        try:
            roiOne = int(self.roiOneIn.text())
            roiTwo = int(self.roiTwoIn.text())
            roiThree = int(self.roiThreeIn.text())
            roiFour = int(self.roiFourIn.text())

            points = list()

            frame, frameCrop = checkEditing(self, self.frameNumber)

            cv2.namedWindow('MeasureLength', cv2.WINDOW_AUTOSIZE)
            cv2.setMouseCallback('MeasureLength', click)
            if self.figSize.isChecked() == True:
                newWidth = int(frameCrop.shape[1] / 2) #original width divided by 2
                newHeight = int(frameCrop.shape[0] / 2) #original height divided by 2
                halfFig = cv2.resize(frameCrop, (newWidth, newHeight))
                cv2.imshow('MeasureLength', halfFig)
            else:
                cv2.imshow('MeasureLength', frameCrop)

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
                if self.figSize.isChecked() == True:
                    points.append(xPos * 2)
                    points.append(yPos * 2)
                else:
                    points.append(xPos)
                    points.append(yPos)

            length_px = ((points[3]-points[1])**2 + (points[2]-points[0])**2)**0.5
            length_px = np.round(length_px, 3)
            if str(self.scaleIn.text()):
                length_mm = length_px / float(self.scaleIn.text())
                length_mm = np.round(length_mm, 3)
                self.msgLabel.setText(f'Measured length: {length_px} px; {length_mm} mm')
            else:
                self.msgLabel.setText(f'Measured length: {length_px} px; insert scale for mm')

            cv2.destroyAllWindows()
        except:
            print('Unexpected error:', sys.exc_info())
            self.msgLabel.setText('Something went wrong and the length was not measured.')

    def editFramesSlider_released(self):
        self.brightnessLbl.setText(str(self.brightnessSlider.value()))
        self.contrastLbl.setText(str(self.contrastSlider.value()))
        showFrame(self, self.frameNumber)

    # def exportVideoBtn_clicked(self):
    #     self.w = MyPopup()
    #     self.w.setGeometry(QRect(100, 100, 400, 200))
    #     self.w.show()

    def newVideoHelpBtn_clicked(self):
        msg = QMessageBox(self)
        msg.setText('''To save the edited video, click on 'Export Video' after specifying the new properties.

        If 'Skip frames' is not zero, to keep the original time variation the new frame rate should be:
        fps(new) = fps(original)/(skipframes + 1)

        'Format' and 'Codec' depend on your operating system and the avaiable codecs (the best combination might require some trial and error).''')
        msg.exec()

    def showFrameLarge_clicked(self):
        cv2.namedWindow(('Frame: ' + str(self.frameNumber)), cv2.WINDOW_AUTOSIZE)
        if self.figSize.isChecked() == True:
            newWidth = int(self.currentFrame.shape[1] / 2) #original width divided by 2
            newHeight = int(self.currentFrame.shape[0] / 2) #original height divided by 2
            halfFig = cv2.resize(self.currentFrame, (newWidth, newHeight))
            cv2.imshow(('Frame: ' + str(self.frameNumber)), halfFig)
        else:
            cv2.imshow(('Frame: ' + str(self.frameNumber)), self.currentFrame)

        while True:
            if cv2.waitKey(1) == 27: #ord('q')
                cv2.destroyAllWindows()
                return

    ### Manual tracking block methods (defined in manualTracking.py)
    def manualTrackingBtn_clicked(self):
        mt.startTracking(self)
    def saveBtn_MT_clicked(self):
        mt.saveData(self)
    def absValBtn_MT_clicked(self):
        mt.absValue(self)
    def lightROIBtn_MT_clicked(self):
        mt.lightROIBtn(self)
    def updateGraphsBtn_MT_clicked(self):
        mt.updateGraphsBtn(self)

    ### Luma tracking block methods (defined in lumaTracking.py)
    def lumaTrackingBtn_clicked(self):
        lt.lumaTracking(self)
    def saveDataBtn_LT_clicked(self):
        lt.saveData(self)
    def absValBtn_LT_clicked(self):
        lt.absValue(self)
    def filterParticleSldr_LT_released(self):
        lt.filterParticleSldr(self)
    def lightROIBtn_LT_clicked(self):
        lt.lightROIBtn(self)
    def showFrameLargeBtn_LT_clicked(self):
        lt.showFrameLarge(self)
    def updateGraphsBtn_LT_clicked(self):
        lt.updateGraphsBtn(self)

    ### Color tracking methods (defined in RGBTracking.py)
    def singleColorSlider_released(self):
        rt.colorSlider_released(self)
    def redMinLeftBtn_RT_clicked(self):
        rt.redMinLeftBtn(self)
    def redMinRightBtn_RT_clicked(self):
        rt.redMinRightBtn(self)
    def redMaxLeftBtn_RT_clicked(self):
        rt.redMaxLeftBtn(self)
    def redMaxRightBtn_RT_clicked(self):
        rt.redMaxRightBtn(self)
    def greenMinLeftBtn_RT_clicked(self):
        rt.greenMinLeftBtn(self)
    def greenMinRightBtn_RT_clicked(self):
        rt.greenMinRightBtn(self)
    def greenMaxLeftBtn_RT_clicked(self):
        rt.greenMaxLeftBtn(self)
    def greenMaxRightBtn_RT_clicked(self):
        rt.greenMaxRightBtn(self)
    def blueMinLeftBtn_RT_clicked(self):
        rt.blueMinLeftBtn(self)
    def blueMinRightBtn_RT_clicked(self):
        rt.blueMinRightBtn(self)
    def blueMaxLeftBtn_RT_clicked(self):
        rt.blueMaxLeftBtn(self)
    def blueMaxRightBtn_RT_clicked(self):
        rt.blueMaxRightBtn(self)
    def filterParticleSldr_RT_released(self):
        rt.filterParticleSldr(self)
    def lightROIBtn_RT_clicked(self):
        rt.lightROIBtn(self)
    def saveChannelsBtn_RT_clicked(self):
        rt.saveChannelsBtn(self)
    def loadChannelsBtn_RT_clicked(self):
        rt.loadChannelsBtn(self)
    def RGBTrackingBtn_clicked(self):
        rt.RGBTracking(self)
    def absValBtn_RT_clicked(self):
        rt.absValBtn(self)
    def saveBtn_RT_clicked(self):
        rt.saveBtn(self)
    def showFrameLargeBtn_RT_clicked(self):
        rt.showFrameLarge(self)
    def updateGraphsBtn_RT_clicked(self):
        rt.updateGraphsBtn(self)

    ### HSV tracking methods (defined in HSVTracking.py)
    def singleHSVSlider_released(self):
        ht.HSVSlider_released(self)
    def hueMinLeftBtn_HT_clicked(self):
        ht.hueMinLeftBtn(self)
    def hueMinRightBtn_HT_clicked(self):
        ht.hueMinRightBtn(self)
    def hueMaxLeftBtn_HT_clicked(self):
        ht.hueMaxLeftBtn(self)
    def hueMaxRightBtn_HT_clicked(self):
        ht.hueMaxRightBtn(self)
    def satMinLeftBtn_HT_clicked(self):
        ht.satMinLeftBtn(self)
    def satMinRightBtn_HT_clicked(self):
        ht.satMinRightBtn(self)
    def satMaxLeftBtn_HT_clicked(self):
        ht.satMaxLeftBtn(self)
    def satMaxRightBtn_HT_clicked(self):
        ht.satMaxRightBtn(self)
    def valMinLeftBtn_HT_clicked(self):
        ht.valMinLeftBtn(self)
    def valMinRightBtn_HT_clicked(self):
        ht.valMinRightBtn(self)
    def valMaxLeftBtn_HT_clicked(self):
        ht.valMaxLeftBtn(self)
    def valMaxRightBtn_HT_clicked(self):
        ht.valMaxRightBtn(self)
    def lightROIBtn_HT_clicked(self):
        ht.lightROIBtn(self)
    def filterParticleSldr_HT_released(self):
        ht.filterParticleSldr(self)
    def saveChannelsBtn_HT_clicked(self):
        ht.saveChannelsBtn(self)
    def loadChannelsBtn_HT_clicked(self):
        ht.loadChannelsBtn(self)
    def HSVTrackingBtn_clicked(self):
        ht.HSVTracking(self)
    def absValBtn_HT_clicked(self):
        ht.absValBtn(self)
    def saveBtn_HT_clicked(self):
        ht.saveBtn(self)
    def showFrameLargeBtn_HT_clicked(self):
        ht.showFrameLarge(self)
    def updateGraphsBtn_HT_clicked(self):
        ht.updateGraphsBtn(self)

    def exportVideo_clicked(self):
        # Open pop-up window to ask about frame rate, codec and format
        self.expV_win = MyPopup(self)
        self.expV_win.setGeometry(QRect(100, 100, 400, 200))
        self.expV_win.show()

    def getFormat_clicked(self):
        # Open pop-up window to ask about codec and format before exporting a video
        self.format_win = vFormatPopup(self)
        self.format_win.setGeometry(QRect(100, 100, 400, 200))
        self.format_win.show()

    def nextBtn_clicked(self, self2):
        fps = float(self.expV_win.fpsLine.text())
        codec = str(self.expV_win.codecLine.text())
        format = str(self.expV_win.formatLine.text())
        self.expV_win.close()

        path = QFileDialog.getSaveFileName(self, 'Save edited video')
        path = path[0]

        if not path[-len(format):] == format:
            # print('Appending', vFormat, 'to filename')
            path = str(path) + '.' + str(format)
        fourcc = cv2.VideoWriter_fourcc(*codec)
        size = (int(self.roiThreeIn.text()), int(self.roiFourIn.text()))
        name = re.findall('.*[/](.*)?', path)
        if path != '.' + str(format): # if the name is not empty
            # open and set properties
            vout = cv2.VideoWriter()
            if self.grayscale.isChecked() == True:
                vout.open(path, fourcc, fps, size, isColor = False)
            else:
                vout.open(path, fourcc, fps, size,True)

            firstFrame = int(self.firstFrameIn.text())
            lastFrame = int(self.lastFrameIn.text())
            currentFrame = firstFrame

            while (currentFrame < lastFrame):
                frame, frameCrop = checkEditing(self, currentFrame)
                vout.write(frameCrop)
                print('Progress: ', round((currentFrame - firstFrame)/(lastFrame - firstFrame) * 1000)/10, '%',  end='\r')
                currentFrame = currentFrame + 1 + int(self.skipFrameIn.text())

            vout.release()
            print(f'Progress: 100 %, {name[0]} has been exported.')
            self.msgLabel.setText(f'{name[0]} has been exported.')
        else:
            self.msgLabel.setText('Error: Enter a valid video name')

    def doneBtn_clicked(self, self3):
        self.codec = str(self.format_win.codecLine.text())
        self.vFormat = str(self.format_win.formatLine.text())
        self.format_win.close()

def removeExistingMethod(self):
    if self.trackingMethod == 'Manual tracking':
        self.menu_MT.clear()
    if self.trackingMethod == 'Luma tracking':
        self.menu_LT.clear()
    if self.trackingMethod == 'RGB tracking':
        self.menu_RT.clear()
    if self.trackingMethod == 'HSV tracking':
        self.menu_HT.clear()

    methodSelected = self.trackingGroup.checkedAction()
    methodSelected = methodSelected.text()
    self.trackingMethod = methodSelected

    for i in reversed(range(self.box_layout.count())):
        self.box_layout.itemAt(i).widget().deleteLater()

    self.box_layout.removeItem(self.box_layout)

# this function waits for the next mouse click
def click(event, x, y, flags, param):
    global xPos, yPos, clk

    if event == cv2.EVENT_LBUTTONUP:
        xPos = x
        yPos = y
        clk = True

def showFrame(self, frameNumber):
    frame, frameCrop = checkEditing(self, frameNumber)

    # create the rectangle based on the ROI and show it in preview
    firstPoint = (int(self.roiOneIn.text()), int(self.roiTwoIn.text()))
    secondPoint = (int(self.roiOneIn.text()) + int(self.roiThreeIn.text()), int(self.roiTwoIn.text()) + int(self.roiFourIn.text()))
    cv2.rectangle(frame, firstPoint, secondPoint, (255, 255, 255), 3)
    if self.grayscale.isChecked() == True:
        bytes = frame.shape[1]
        self.image = QImage(frame.data, frame.shape[1], frame.shape[0], bytes, QImage.Format.Format_Grayscale8)
    else:
        bytes = 3 * frame.shape[1] #bytes per line, necessary to avoid distortion in the opened file
        self.image = QImage(frame.data, frame.shape[1], frame.shape[0], bytes, QImage.Format.Format_RGB888).rgbSwapped()

    self.currentFrame = frame
    self.image = self.image.scaled(self.win1.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    self.win1.setPixmap(QPixmap.fromImage(self.image))

def perspectiveCorrection(self, frame):
    # M is the matrix transformation calculated with the size of the sample (calculated from user input), and the sampleMod from the user clicks
    M = cv2.getPerspectiveTransform(self.sample, self.sampleMod)
    # If the perspective is done on a rotated video, the corrected image might have a much larger size than the original one, here we check this
    originalFrame = np.float32([[0,0], [self.vWidth, 0], [self.vWidth, self.vHeight], [0, self.vHeight]])
    width = int(frame.shape[1])
    height = int(frame.shape[0])
    for point in self.sampleMod:
        if point[0] > width:
            width = int(point[0])
        if point[1] > height:
            height = int(point[1])

    frame = cv2.warpPerspective(frame, M, (width, height))
    return(frame)

def rotationCorrection(self, frame, angle):
    # rotation matrix:
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

def checkEditing(self, frameNumber):
    if self.openSelection == 'video':
        self.fVideo.set(1, frameNumber)
        ret, frame = self.fVideo.read()
    elif self.openSelection == 'image(s)':
        imageNumber = self.imagesList[int(frameNumber)]
        frame = cv2.imread(imageNumber)

    if self.perspectiveValue == True:
        if self.rotationValue == True:
            frame = rotationCorrection(self, frame, self.anglePerspective)
        frame = perspectiveCorrection(self, frame)
        # the following two lines update the size of the frame after the correction
        self.vWidthLbl.setText(str(frame.shape[1]))
        self.vHeightLbl.setText(str(frame.shape[0]))
        #the rotation has already been included in the perspective correction, but it could happen that a further rotation is needed after the correction (e.g. for the analysis)
        if self.anglePerspective != float(self.rotationAngleIn.text()):
            angle = float(self.rotationAngleIn.text()) - self.anglePerspective
            frame = rotationCorrection(self, frame, angle)
    elif float(self.rotationAngleIn.text()) != 0: #in case there is no perspective correction
        angle = float(self.rotationAngleIn.text())
        frame = rotationCorrection(self, frame, angle)
    if int(self.brightnessSlider.value()) != 0 or int(self.contrastSlider.value()) != 0:
        frameContainer = np.zeros(frame.shape, frame.dtype)
        # alpha would go from 0 to 3, with lower contrast in 0-1. The scale is normalized in percentile
        alpha = (int(self.contrastSlider.value()) + 100) * 2 / 200
        beta = int(self.brightnessSlider.value())    # Simple brightness control [0-100]
        frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
    if self.grayscale.isChecked() == True:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # crop frame
    frameCrop = frame[int(self.roiTwoIn.text()) : (int(self.roiTwoIn.text()) + int(self.roiFourIn.text())), int(self.roiOneIn.text()) : (int(self.roiOneIn.text()) + int(self.roiThreeIn.text()))]

    return(frame, frameCrop)

def checkAnalysisMethod(self, frameNumber):
    if self.trackingMethod == 'Manual tracking':

        frame, frameCrop = checkEditing(self, frameNumber)
        # create the ROI rectangle and show it in label1
        firstPoint = (int(self.roiOneIn.text()), int(self.roiTwoIn.text()))
        secondPoint = (int(self.roiOneIn.text()) + int(self.roiThreeIn.text()), int(self.roiTwoIn.text()) + int(self.roiFourIn.text()))
        cv2.rectangle(frame, firstPoint, secondPoint, (255, 255, 255), 3)
        if self.lightROI_MT_recorded == True:
            firstPoint = (int(self.lightROI_MT[0]), int(self.lightROI_MT[1]))
            secondPoint = (int(self.lightROI_MT[0]) + int(self.lightROI_MT[2]), int(self.lightROI_MT[1]) + int(self.lightROI_MT[3]))
            cv2.rectangle(frame, firstPoint, secondPoint, (255, 0, 0), 5)
        bytes1 = 3 * frame.shape[1] #bytes per line, necessary to avoid distortion in the opened file
        image1 = QImage(frame.data, frame.shape[1], frame.shape[0], bytes1, QImage.Format.Format_RGB888).rgbSwapped()
        image1 = image1.scaled(self.lbl1_MT.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.lbl1_MT.setPixmap(QPixmap.fromImage(image1)) # this line was added (again?) in v1.1.7 to show the preview frame in the analysis box
        self.win1_MT.setCurrentIndex(0) #to activate the preview tab in the analysis box

    if self.trackingMethod == 'Luma tracking':

        if self.grayscale.isChecked() == True:
            self.msgLabel.setText('Grayscale images not supported with this feature')
        frame, frameCrop = checkEditing(self, frameNumber)
        lt.getFilteredFrame(self, frameCrop)
        self.lbl1_LT.setPixmap(QPixmap.fromImage(self.frameY))
        self.lbl2_LT.setPixmap(QPixmap.fromImage(self.frameBW))
        self.win1_LT.setCurrentIndex(0) #to activate the preview tab in the analysis box
        self.win2_LT.setCurrentIndex(0)

    if self.trackingMethod == 'RGB tracking':
        self.lbl1_RT.setStyleSheet('background-color: white')
        self.lbl2_RT.setStyleSheet('background-color: white')
        if self.grayscale.isChecked() == True:
            self.msgLabel.setText('Grayscale images are not supported for the RGB tracking method')
        frame, frameCrop = checkEditing(self, frameNumber)
        rt.getFilteredFrame(self, frameCrop)

        self.lbl1_RT.setPixmap(QPixmap.fromImage(self.frame))
        self.lbl2_RT.setPixmap(QPixmap.fromImage(self.frameBW))

        self.win1_RT.setCurrentIndex(0) #to activate the preview tab in the analysis box
        self.win2_RT.setCurrentIndex(0)

    if self.trackingMethod == 'HSV tracking':
        if self.grayscale.isChecked() == True:
            self.msgLabel.setText('Grayscale images not supported with this feature')
        frame, frameCrop = checkEditing(self, frameNumber)
        ht.getFilteredFrame(self, frameCrop)
        self.lbl1_HT.setPixmap(QPixmap.fromImage(self.frame))
        self.lbl2_HT.setPixmap(QPixmap.fromImage(self.frameBW))
        self.win1_HT.setCurrentIndex(0) #to activate the preview tab in the analysis box
        self.win2_HT.setCurrentIndex(0)


class MyPopup(QWidget):
    def __init__(self2, self):
        mainWin = self
        QWidget.__init__(self2)

        self2.setWindowTitle('Select video format')
        grid = QGridLayout()
        # grid.setRowStretch(grid.rowCount(), 1)
        # grid.setColumnStretch(grid.columnCount(), 4)
        # grid.setSpacing(10)

        info1Txt = QLabel('To keep the original time: \nfps(new) = fps(original)/(skipframes + 1)', self2)
        info2Txt = QLabel('Video codec and format depend on your OS and available packages \n(the best combination may require some trial and error).', self2)

        fpsTxt = QLabel('New frame rate (fps):')
        self2.fpsLine = QLineEdit('30')
        codecTxt = QLabel('Video codec:')
        self2.codecLine = QLineEdit('mp4v')
        formatTxt = QLabel('Video format:')
        self2.formatLine = QLineEdit('mp4')
        nextBtn = QPushButton('Next')
        nextBtn.clicked.connect(mainWin.nextBtn_clicked)

        grid.addWidget(info1Txt, 0, 0, 1, 1) #row, clmn, row span, clmn span
        grid.addWidget(info2Txt, 1, 0, 1, 2)
        grid.addWidget(fpsTxt, 2, 0)
        grid.addWidget(self2.fpsLine, 2, 1)
        grid.addWidget(codecTxt, 3, 0)
        grid.addWidget(self2.codecLine, 3, 1)
        grid.addWidget(formatTxt, 4, 0)
        grid.addWidget(self2.formatLine, 4, 1)
        grid.addWidget(nextBtn, 5, 1)
        # grid.addWidget(stopBtn, 6, 1)

        self2.setLayout(grid)

        self2.winTest = False

class vFormatPopup(QWidget):
    def __init__(self3, self):
        mainWin = self
        QWidget.__init__(self3)

        self3.setWindowTitle('Select video format')
        grid = QGridLayout()

        infoTxt = QLabel('Video codec and format depend on your OS and available packages \n(the best combination may require some trial and error).', self3)

        # fpsTxt = QLabel('New frame rate (fps):')
        # self2.fpsLine = QLineEdit('30')
        codecTxt = QLabel('Video codec:')
        self3.codecLine = QLineEdit('mp4v')
        formatTxt = QLabel('Video format:')
        self3.formatLine = QLineEdit('mp4')
        doneBtn = QPushButton('Done')
        doneBtn.clicked.connect(mainWin.doneBtn_clicked)

        # grid.addWidget(info1Txt, 0, 0, 1, 1) #row, clmn, row span, clmn span
        grid.addWidget(infoTxt, 0, 0, 1, 2)
        # grid.addWidget(fpsTxt, 1, 0)
        # grid.addWidget(self3.fpsLine, 1, 1)
        grid.addWidget(codecTxt, 1, 0)
        grid.addWidget(self3.codecLine, 1, 1)
        grid.addWidget(formatTxt, 2, 0)
        grid.addWidget(self3.formatLine, 2, 1)
        grid.addWidget(doneBtn, 3, 1)
        # grid.addWidget(stopBtn, 6, 1)

        self3.setLayout(grid)

        self3.winTest = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FlameTrackerWindow()
    window.show()
    if QT_VERSION_STR[0] == '5':
        sys.exit(app.exec_())
    elif QT_VERSION_STR[0] == '6':
        sys.exit(app.exec())
