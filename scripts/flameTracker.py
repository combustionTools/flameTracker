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

import cv2
import numpy as np
import csv
import sys
import platform
import time
import re
import pyqtgraph as pg

from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from itertools import zip_longest
from pyqtgraph import PlotWidget, plot

from manualTracking import *
from lumaTracking import *
from colorTracking import *
from HSVTracking import *
from boxesGUI_OS import *

#To make sure the resolution is correct also in Windows
if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        print('''Flame Tracker - Copyright (C) 2020,2021 Luca Carmignani; 2021 Charles Scudiere
        This program comes with ABSOLUTELY NO WARRANTY; See the GNU General
        Public License for more details.
        This is free software, and you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.''')

        if sys.platform == 'darwin':
            previewBox_Mac(self)
            self.OStype = 'mac'
        elif sys.platform == 'win32':
            previewBox_Win(self)
            self.OStype = 'win'
        elif sys.platform == 'linux':
            previewBox_Linux(self)
            self.OStype = 'lin'
        else:
            print('\n!!! Warning: Unable to detect OS!!!')

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
                self.skipFrameIn.setText('5') # with 5 you would obtain an even number of points with 24, 30, and 60 fps (not too relevant)
                self.frameIn.setText('0')
                self.frameNumber = 0
                self.previewSlider.setMinimum(int(self.firstFrameIn.text()))
                self.previewSlider.setMaximum(int(self.lastFrameIn.text()))
                self.previewSlider.setValue(int(self.frameIn.text()))
                self.rotationAngleIn.setText('0')
                self.perspectiveValue = False
                self.rotationValue = False
                self.manualTrackingValue = False
                self.lumaTrackingValue = False
                self.colorTrackingValue = False
                self.HSVTrackingValue = False
                self.editFrame = False
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
                self.frameNumber = 0
                self.previewSlider.setMinimum(int(self.firstFrameIn.text()))
                self.previewSlider.setMaximum(int(self.lastFrameIn.text()))
                self.previewSlider.setValue(int(self.frameIn.text()))
                self.rotationAngleIn.setText('0')
                self.perspectiveValue = False
                self.rotationValue = False
                self.manualTrackingValue = False
                self.lumaTrackingValue = False
                self.colorTrackingValue = False
                self.HSVTrackingValue = False
                self.editFrame = False
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
        self.frameNumber = int(self.frameIn.text())
        if self.frameNumber < int(self.firstFrameIn.text()):
            self.firstFrameIn.setText(str(self.frameNumber))
        elif self.frameNumber > int(self.lastFrameIn.text()):
            self.lastFrameIn.setText(str(self.frameNumber))
        if self.openSelection == 'video':
            self.fVideo.set(1, self.frameNumber)
            ret, frame = self.fVideo.read()
        elif self.openSelection == 'image(s)':
            imageNumber = self.imagesList[self.frameNumber]
            frame = cv2.imread(imageNumber)

        self.previewSlider.setValue(int(self.frameNumber)) #CAS - update slider to reflect new goto frame value
        showFrame(self, frame, self.frameNumber)
        checkAnalysisBox(self, self.frameNumber)

    def sliderValue_released(self):
        self.previewSlider.setMinimum(int(self.firstFrameIn.text()))
        self.previewSlider.setMaximum(int(self.lastFrameIn.text()))
        self.frameNumber = self.previewSlider.value()
        self.frameIn.setText(str(self.frameNumber))
        if self.openSelection == 'video':
            self.fVideo.set(1, self.frameNumber)
            ret, frame = self.fVideo.read()
        elif self.openSelection == 'image(s)':
            imageNumber = self.imagesList[self.frameNumber]
            frame = cv2.imread(imageNumber)

        showFrame(self, frame, self.frameNumber)
        checkAnalysisBox(self, self.frameNumber)

    def roiBtn_clicked(self):
        try:
            if self.openSelection == 'video':
                self.fVideo.set(1, int(self.frameNumber))
                ret, frame = self.fVideo.read()
            elif self.openSelection == 'image(s)':
                imageNumber = self.imagesList[int(self.frameNumber)]
                frame = cv2.imread(imageNumber)

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
            self.roiThreeIn.setText('10')
            self.roiFourIn.setText('10')

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
            if self.openSelection == 'video':
                self.fVideo.set(1, self.frameNumber)
                ret, frame = self.fVideo.read()
            elif self.openSelection == 'image(s)':
                imageNumber = self.imagesList[int(self.frameNumber)]
                frame = cv2.imread(imageNumber)

            # The following conditions are the same of checkEditing(), here they are checked for the correction
            self.anglePerspective = float(self.rotationAngleIn.text())
            if float(self.rotationAngleIn.text()) != 0:
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
            cv2.imshow('Perspective correction', frameCrop)
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
            showFrame(self, frame, self.frameNumber)
            # The rotation value has to be set after showing the frame to avoid double editing in the first preview
            if float(self.rotationAngleIn.text()) != 0:
                self.rotationValue = True

        except:
            self.msgLabel.setText('Ops! Something went wrong.')

    def originalBtn_clicked(self):
        self.perspectiveValue = False
        self.rotationValue = False
        self.brightnessSlider.setValue(0)
        self.contrastSlider.setValue(0)
        self.brightnessLbl.setText(str(self.brightnessSlider.value()))
        self.contrastLbl.setText(str(self.contrastSlider.value()))
        if self.openSelection == 'video':
            self.fVideo.set(1, self.frameNumber)
            ret, frame = self.fVideo.read()
        elif self.openSelection == 'image(s)':
            imageNumber = self.imagesList[int(self.frameNumber)]
            frame = cv2.imread(imageNumber)
        showFrame(self, frame, self.frameNumber)

    def saveParBtn_clicked(self):
        name = QFileDialog.getSaveFileName(self, 'Save parameters')
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
                    if self.rotationValue == True:
                        writer.writerow(['Pre-rotation', 'Yes'])
                        writer.writerow(['anglePerspective', str(self.anglePerspective)])
                    if self.perspectiveValue == True:
                        writer.writerow(['Perspective', 'Yes'])
                        writer.writerow(['sample', self.sample[0], self.sample[1], self.sample[2], self.sample[3]])
                        writer.writerow(['sampleMod', self.sampleMod[0], self.sampleMod[1], self.sampleMod[2], self.sampleMod[3]])

                    #CAS Add to save reference txt
                    # LC we will include a button for this in the next version
                    writer.writerow([self.xrefTxt.text(), str(self.xref.text())]) #CAS Add to save reference txt

                self.msgLabel.setText('Parameters saved.')
            except:
                self.msgLabel.setText('Ops! Parameters were not saved.')

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

                    #CAS Add to save reference txt
                    if self.xrefTxt.text() in row:
                        self.xref.setText(row[1]) #CAS Add to save reference txt.
                        #print('xRef loaded:', self.xrefTxt.text(), '=', self.xref.text())

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

    # selection connected to the specific file, getting rid of what was showing before
    def analysis_click(self, text):
        selection = self.analysisSelectionBox.currentText()
        if selection == 'Choose analysis':
            for children in self.analysisGroupBox.findChildren(QGroupBox):
                children.setParent(None)
            self.manualTrackingValue = False
            self.lumaTrackingValue = False
            self.colorTrackingValue = False
            self.HSVTrackingValue = False
        elif selection == 'Manual tracking':
            for children in self.analysisGroupBox.findChildren(QGroupBox):
                children.setParent(None)
            createManualTrackingBox(self)
            self.lumaTrackingValue = False
            self.colorTrackingValue = False
            self.HSVTrackingValue = False
        elif selection == 'Luma tracking':
            for children in self.analysisGroupBox.findChildren(QGroupBox):
                children.setParent(None)
            createLumaTrackingBox(self)
            self.manualTrackingValue = False
            self.colorTrackingValue = False
            self.HSVTrackingValue = False
        elif selection == 'Color tracking':
            for children in self.analysisGroupBox.findChildren(QGroupBox):
                children.setParent(None)
            createColorTrackingBox(self)
            self.manualTrackingValue = False
            self.lumaTrackingValue = False
            self.HSVTrackingValue = False
        elif selection == 'HSV tracking':
            for children in self.analysisGroupBox.findChildren(QGroupBox):
                children.setParent(None)
            createHSVTrackingBox(self)
            self.lumaTrackingValue = False
            self.manualTrackingValue = False
            self.colorTrackingValue = False

    def measureScaleBtn_clicked(self, text):
        try:
            roiOne = int(self.roiOneIn.text())
            roiTwo = int(self.roiTwoIn.text())
            roiThree = int(self.roiThreeIn.text())
            roiFour = int(self.roiFourIn.text())
            global clk
            clk = False # False unless the mouse is clicked
            points = list()

            if self.openSelection == 'video':
                self.fVideo.set(1, self.frameNumber)
                ret, frame = self.fVideo.read()
            elif self.openSelection == 'image(s)':
                imageNumber = self.imagesList[self.frameNumber]
                frame = cv2.imread(imageNumber)

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

                        #CAS soft add to save reference txt, relative to frameCrop...
                        if ('xPos' in globals()): # or 'xPos' in locals()): # and xPos:
                            # If selected a point, interpreted as a reference point usually stored in globals, (but could also check locals just in case?)
                            refLoc_x = xPos + roiOne
                            refLoc_y = yPos + roiTwo
                            self.xref.setText(str([refLoc_x, refLoc_y])) #CAS Use absolute and convert on own...to prevent issues with different cropping
                            self.msgLabel.setText('xRef measured.')

                        return

                # update each position and frame list for the current click
                points.append(xPos)
                points.append(yPos)

            length_mm, done1 = QInputDialog.getText(self, 'Measure scale', 'Measured length in mm:')
            length_px = ((points[3]-points[1])**2 + (points[2]-points[0])**2)**0.5
            scale = length_px / float(length_mm)
            scale = np.round(scale, 3)

            self.scaleIn.setText(str(scale))
            self.msgLabel.setText('Scale & Ref succesfully measured')
            cv2.destroyAllWindows()
        except:
            print('Unexpected error:', sys.exc_info())
            self.msgLabel.setText('Something went wrong and the scale was not measured.')


    def editFramesSlider_released(self):
        if self.openSelection == 'video':
            self.fVideo.set(1, self.frameNumber)
            ret, frame = self.fVideo.read()
        elif self.openSelection == 'image(s)':
            imageNumber = self.imagesList[self.frameNumber]
            frame = cv2.imread(imageNumber)
        self.brightnessLbl.setText(str(self.brightnessSlider.value()))
        self.contrastLbl.setText(str(self.contrastSlider.value()))
        showFrame(self, frame, self.frameNumber)

    def exportVideoBtn_clicked(self):
        fps = round(float(self.fpsIn.text()))
        codec = str(self.codecIn.text())
        vFormat = str(self.formatIn.text())
        vName = QFileDialog.getSaveFileName(self, 'Save File')
        vName = vName[0]
        if not vName[-len(vFormat):] == vFormat:
            print('Appending', vFormat, 'to filename')
            vName = str(vName) + '.' + str(vFormat) # alternative: 'output.{}'.format(vFormat)
        fourcc = cv2.VideoWriter_fourcc(*codec)
        size = (int(self.roiThreeIn.text()), int(self.roiFourIn.text()))

        if vName != '.' + str(vFormat): # if the name is not empty
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
                    imageNumber = self.imagesList[currentFrame]
                    frame = cv2.imread(imageNumber)

                frame = checkEditing(self, frame)
                frameCrop = frame[int(self.roiTwoIn.text()) : (int(self.roiTwoIn.text()) + int(self.roiFourIn.text())), int(self.roiOneIn.text()) : (int(self.roiOneIn.text()) + int(self.roiThreeIn.text()))]
                vout.write(frameCrop)
                print('Progress: ', round((currentFrame - firstFrame)/(lastFrame - firstFrame) * 10000)/100, '%')
                currentFrame = currentFrame + 1 + int(self.skipFrameIn.text())

            vout.release()
            print('Progress: 100 %, the video has been created.')
            self.msgLabel.setText('The video has been created.')
        else:
            self.msgLabel.setText('Error: Enter a valid video name')

    def newVideoHelpBtn_clicked(self):
        msg = QMessageBox(self)
        msg.setText('''To save the video editing, after specifying the properties of the new video, click on 'Export Video'.

        If Skip frames is not zero, to keep the same time of the original video, the new frame rate should be:
        fps(new) = fps(original)/(skipframes + 1)

        Format and codec will depend on your operating system and the avaiable codecs (the best combination might require some trial and error).''')
        msg.exec_()

    def showFrameLargeBtn_clicked(self):
        cv2.namedWindow(('Frame: ' + str(self.frameNumber)), cv2.WINDOW_AUTOSIZE)
        cv2.imshow(('Frame: ' + str(self.frameNumber)), self.currentFrame)
        while True:
            if cv2.waitKey(1) == 27: #ord('q')
                cv2.destroyAllWindows()
                return

    ### Manual tracking block methods (defined in manualTracking.py)
    def directionMT_clicked(self, text):
        chooseFlameDirection_MT(self, text)
    def manualTrackingBtn_clicked(self):
        manualTracking(self)
    def saveBtn_MT_clicked(self):
        saveData_MT(self)
    def absValBtn_MT_clicked(self):
        absValue_MT(self)
    def filterLight_MT_clicked(self, text):
        chooseLightFilter_MT(self, text)
    def lightROIBtn_MT_clicked(self):
        lightROIBtn_MT(self)
    def helpBtn_MT_clicked(self):
        helpBtn_MT(self)

    ### Luma tracking block methods (defined in lumaTracking.py)
    def lumaTrackingBtn_clicked(self):
        lumaTracking(self)
    def directionLT_clicked(self, text):
        chooseFlameDirection_LT(self, text)
    def saveDataBtn_LT_clicked(self):
        saveData_LT(self)
    def absValBtn_LT_clicked(self):
        absValue_LT(self)
    def filterParticleSldr_LT_released(self):
        filterParticleSldr_LT(self)
    def lightROIBtn_LT_clicked(self):
        lightROIBtn_LT(self)
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
    def lightROIBtn_CT_clicked(self):
        lightROIBtn_CT(self)
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

    ### HSV tracking methods (defined in HSVTracking.py)
    def singleHSVSlider_released(self):
        HSVSlider_released(self)
    def hueMinLeftBtn_HT_clicked(self):
        hueMinLeftBtn_HT(self)
    def hueMinRightBtn_HT_clicked(self):
        hueMinRightBtn_HT(self)
    def hueMaxLeftBtn_HT_clicked(self):
        hueMaxLeftBtn_HT(self)
    def hueMaxRightBtn_HT_clicked(self):
        hueMaxRightBtn_HT(self)
    def satMinLeftBtn_HT_clicked(self):
        satMinLeftBtn_HT(self)
    def satMinRightBtn_HT_clicked(self):
        satMinRightBtn_HT(self)
    def satMaxLeftBtn_HT_clicked(self):
        satMaxLeftBtn_HT(self)
    def satMaxRightBtn_HT_clicked(self):
        satMaxRightBtn_HT(self)
    def valMinLeftBtn_HT_clicked(self):
        valMinLeftBtn_HT(self)
    def valMinRightBtn_HT_clicked(self):
        valMinRightBtn_HT(self)
    def valMaxLeftBtn_HT_clicked(self):
        valMaxLeftBtn_HT(self)
    def valMaxRightBtn_HT_clicked(self):
        valMaxRightBtn_HT(self)
    def filterParticleSldr_HT_released(self):
        filterParticleSldr_HT(self)
    def directionHT_clicked(self, text):
        chooseFlameDirection_HT(self, text)
    def connectivityBoxHT_clicked(self, text):
        connectivityBox_HT(self, text)
    def saveChannelsBtn_HT_clicked(self):
        saveChannelsBtn_HT(self)
    def loadChannelsBtn_HT_clicked(self):
        loadChannelsBtn_HT(self)
    def HSVTrackingBtn_clicked(self):
        HSVTracking(self)
    def absValBtn_HT_clicked(self):
        absValBtn_HT(self)
    def saveBtn_HT_clicked(self):
        saveBtn_HT(self)
    def showFrameLargeBtn_HT_clicked(self):
        showFrameLarge_HT(self)
    def helpBtn_HT_clicked(self):
        helpBtn_HT(self)


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

def checkEditing(self, frame):
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
    return(frame)

def checkAnalysisBox(self, frameNumber):
    # true value when the analysis is selected
    if self.manualTrackingValue == True:
        # label 1 might have become a plot widget, so we need to update them again
        self.lbl1_MT = QLabel(self.manualTrackingBox)
        self.lbl1_MT.setGeometry(190, 25, 420, 300)
        self.lbl1_MT.setStyleSheet('background-color: white')

        frame, frameCrop = checkEditing_MT(self, frameNumber)
        # create the ROI rectangle and show it in label1
        firstPoint = (int(self.roiOneIn.text()), int(self.roiTwoIn.text()))
        secondPoint = (int(self.roiOneIn.text()) + int(self.roiThreeIn.text()), int(self.roiTwoIn.text()) + int(self.roiFourIn.text()))
        cv2.rectangle(frame, firstPoint, secondPoint, (255, 255, 255), 3)
        if self.lightROI_MT_recorded == True:
            firstPoint = (int(self.lightROI_MT[0]), int(self.lightROI_MT[1]))
            secondPoint = (int(self.lightROI_MT[0]) + int(self.lightROI_MT[2]), int(self.lightROI_MT[1]) + int(self.lightROI_MT[3]))
            cv2.rectangle(frame, firstPoint, secondPoint, (255, 0, 0), 5)
        bytes1 = 3 * frame.shape[1] #bytes per line, necessary to avoid distortion in the opened file
        image1 = QImage(frame.data, frame.shape[1], frame.shape[0], bytes1, QImage.Format_RGB888).rgbSwapped()
        image1 = image1.scaled(self.lbl1_MT.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.lbl1_MT.setPixmap(QPixmap.fromImage(image1))
        self.lbl1_MT.show()

    if self.lumaTrackingValue == True:
        # the labels might have become plot widgets, so we need to update them again
        self.lbl1_LT = QLabel(self.lumaTrackingBox)
        self.lbl2_LT = QLabel(self.lumaTrackingBox)
        if self.OStype == 'mac':
            self.lbl1_LT.setGeometry(190, 25, 420, 300)
            self.lbl2_LT.setGeometry(620, 25, 420, 300)
        elif self.OStype == 'win':
            self.lbl1_LT.setGeometry(190, 15, 420, 300)
            self.lbl2_LT.setGeometry(620, 15, 420, 300)
        elif self.OStype == 'lin':
            self.lbl1_LT.setGeometry(190, 25, 420, 300)
            self.lbl2_LT.setGeometry(620, 25, 420, 300)

        self.lbl1_LT.setStyleSheet('background-color: white')
        self.lbl2_LT.setStyleSheet('background-color: white')

        if self.grayscale.isChecked() == True:
            self.msgLabel.setText('Grayscale images not supported with this feature')
        frame, frameCrop = checkEditing_LT(self, frameNumber)
        getLumaFrame(self, frameCrop)
        self.lbl1_LT.setPixmap(QPixmap.fromImage(self.frameY))
        self.lbl2_LT.setPixmap(QPixmap.fromImage(self.frameBW))
        self.lbl1_LT.show()
        self.lbl2_LT.show()

    if self.colorTrackingValue == True:
        self.lbl1_CT = QLabel(self.colorTrackingBox)
        self.lbl2_CT = QLabel(self.colorTrackingBox)
        if self.OStype == 'mac':
            self.lbl1_CT.setGeometry(370, 25, 330, 250)
            self.lbl2_CT.setGeometry(710, 25, 330, 250)
        elif self.OStype == 'win':
            self.lbl1_CT.setGeometry(370, 15, 330, 250)
            self.lbl2_CT.setGeometry(710, 15, 330, 250)
        elif self.OStype == 'lin':
            self.lbl1_CT.setGeometry(370, 25, 330, 250)
            self.lbl2_CT.setGeometry(710, 25, 330, 250)

        self.lbl1_CT.setStyleSheet('background-color: white')
        self.lbl2_CT.setStyleSheet('background-color: white')
        if self.grayscale.isChecked() == True:
            self.msgLabel.setText('Grayscale images not supported with this feature')
        frame, frameCrop = checkEditing_CT(self, frameNumber)
        getColorFilteredFrame(self, frameCrop)
        self.lbl1_CT.setPixmap(QPixmap.fromImage(self.frame))
        self.lbl2_CT.setPixmap(QPixmap.fromImage(self.frameBW))
        self.lbl1_CT.show()
        self.lbl2_CT.show()

    if self.HSVTrackingValue == True:
        self.lbl1_HT = QLabel(self.HSVTrackingBox)
        self.lbl2_HT = QLabel(self.HSVTrackingBox)

        if self.OStype == 'mac':
            #self.lbl1_HT.setGeometry(370, 25, 330, 250)
            self.lbl1_HT.setGeometry(370, 25, 670, 125) #CAS Changed geometry for fitting lengthwise
            #self.lbl2_HT.setGeometry(710, 25, 330, 250)
            self.lbl2_HT.setGeometry(370, 150, 670, 125) #CAS Changed geometry for fitting lengthwise
        elif self.OStype == 'win':
            self.lbl1_HT.setGeometry(370, 15, 330, 250)
            self.lbl2_HT.setGeometry(710, 15, 330, 250)
        elif self.OStype == 'lin':
            self.lbl1_HT.setGeometry(370, 25, 670, 125) #CAS Changed geometry for fitting lengthwise
            self.lbl2_HT.setGeometry(370, 150, 670, 125) #CAS Changed geometry for fitting lengthwise

        self.lbl1_HT.setStyleSheet('background-color: white')
        self.lbl2_HT.setStyleSheet('background-color: white')
        if self.grayscale.isChecked() == True:
            self.msgLabel.setText('Grayscale images not supported with this feature')
        getHSVFilteredFrame(self, self.frameNumber)
        self.lbl1_HT.setPixmap(QPixmap.fromImage(self.frame))
        self.lbl2_HT.setPixmap(QPixmap.fromImage(self.frameBW))
        self.lbl1_HT.show()
        self.lbl2_HT.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
