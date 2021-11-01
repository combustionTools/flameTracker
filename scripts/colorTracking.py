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

#from flameTracker import *
#from boxesGUI_OS import *
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from itertools import zip_longest

import flameTracker as ft
import boxesGUI_OS as gui
import csv
import cv2
import pyqtgraph as pg
import numpy as np

def initVars(self):
    global flameDir, connectivity_CT
    flameDir = 'toRight'
    connectivity_CT = 4
    self.lightROI_CT_recorded = False

# def createTrackingBox(self):
#     #self.colorTrackingValue = True
#
#     gui.colorTrackingBox(self)
#
#     # if self.OStype == 'mac' or self.OStype == 'lin':
#     #     gui.colorTrackingBox_Mac(self)
#     # elif self.OStype == 'win':
#     #     gui.colorTrackingBox_Win(self)
#
#     initiateVariables(self)
#     # default variables
#     #self.flameDir = 'toRight'
#     #self.connectivity_CT = 4
#     #self.lightROI_CT_recorded = False
#
#     self.colorTrackingBox.show()

# def checkEditing(self, frameNumber):
#     if self.openSelection == 'video':
#         self.fVideo.set(1, frameNumber)
#         ret, frame = self.fVideo.read()
#     elif self.openSelection == 'image(s)':
#         imageNumber = self.imagesList[int(frameNumber)]
#         frame = cv2.imread(imageNumber)
#     # check for previous corrections
#     if self.perspectiveValue == True:
#         if self.rotationValue == True:
#             frame = rotationCorrection(self, frame, self.anglePerspective)
#         frame = perspectiveCorrection(self, frame)
#         #the rotation has already been included in the perspective correction, but it could happen that a further rotation is needed after the correction (e.g. for the analysis)
#         if self.anglePerspective != float(self.rotationAngleIn.text()):
#             angle = float(self.rotationAngleIn.text()) - self.anglePerspective
#             frame = rotationCorrection(self, frame, angle)
#     elif float(self.rotationAngleIn.text()) != 0: #in case there is no perspective correction
#             angle = float(self.rotationAngleIn.text())
#             frame = rotationCorrection(self, frame, angle)
#     if int(self.brightnessSlider.value()) != 0 or int(self.contrastSlider.value()) != 0:
#         frameContainer = np.zeros(frame.shape, frame.dtype)
#         alpha = (int(self.contrastSlider.value()) + 100) * 2 / 200
#         beta = int(self.brightnessSlider.value())    # Simple brightness control [0-100]. Instead, we have [-50-50]
#         frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
#
#     # crop frame
#     frameCrop = frame[int(self.roiTwoIn.text()) : (int(self.roiTwoIn.text()) + int(self.roiFourIn.text())), int(self.roiOneIn.text()) : (int(self.roiOneIn.text()) + int(self.roiThreeIn.text()))]
#     return(frame, frameCrop)

def getFilteredFrame(self, frame):
    blueLow = self.blueMinSlider.value()
    blueHigh = self.blueMaxSlider.value()
    greenLow = self.greenMinSlider.value()
    greenHigh = self.greenMaxSlider.value()
    redLow = self.redMinSlider.value()
    redHigh = self.redMaxSlider.value()
    low = ([blueLow, greenLow, redLow])
    high = ([blueHigh, greenHigh, redHigh])
    low = np.array(low, dtype = 'uint8') #this conversion is necessary
    high = np.array(high, dtype = 'uint8')
    newMask = cv2.inRange(frame, low, high)
    frame = cv2.bitwise_and(frame, frame, mask = newMask)
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    (threshold, frameBW) = cv2.threshold(grayFrame, 0, 255, cv2.THRESH_BINARY)

    # Find all the connected components (8 means in the four directions and diagonals)
    componentNum, componentLbl, stats, centroids = cv2.connectedComponentsWithStats(frameBW, connectivity = connectivity_CT)
    ### 1 = number of labels; 2 = array; 3 = [[x location (left), y location (top), width, height, area]] for each label; 4 = [centroid of each label, x and y]. Note: the background is the first component

    # minimum area (measured in px) for filtering the components
    minArea = self.filterParticleSldr_CT.value()
    componentAreas = stats[:, 4] # stats is a list of list, here we start from 0 (the background), and we consider the last elements (area)

    # keep only the components with area larger than minArea, starting from 1 to avoid the background
    for i in range(1, componentNum):
        if componentAreas[i] >= minArea:
            frameBW[componentLbl == i] = 255
        else:
            frameBW[componentLbl == i] = 0

    flamePx = np.where(frameBW == [255]) # total area in px

    findFlameEdges(self, frameBW, flamePx)

    if self.showEdges.isChecked() == True:
        cv2.line(frame, (self.xMax, 0),(self.xMax, int(self.roiFourIn.text())), (255, 255, 255), 2)
        cv2.line(frame, (self.xMin, 0),(self.xMin, int(self.roiFourIn.text())), (255, 255, 255), 2)
        cv2.line(frameBW, (self.xMax, 0),(self.xMax, int(self.roiFourIn.text())), (255, 255, 255), 2)
        cv2.line(frameBW, (self.xMin, 0),(self.xMin, int(self.roiFourIn.text())), (255, 255, 255), 2)

    self.currentFrameRGB_CT = frame
    # calculate the total number of bytes in the frame for lbl1
    totalBytes = frame.nbytes
    # divide by the number of rows
    bytesPerLine = int(totalBytes/frame.shape[0]) #I had to introduce it to avoid distortion in the opened file for some of the videos
    self.frame = QImage(frame.data, frame.shape[1], frame.shape[0], bytesPerLine, QImage.Format_BGR888)#.rgbSwapped() #shape[0] = height, [1] = width QImage.Format_Indexed8 BGR888
    self.frame = self.frame.scaled(self.lbl1_CT.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

    self.currentFrameBW_CT = frameBW
    # calculate the total number of bytes in the frame for lbl2
    totalBytesBW = frameBW.nbytes
    # divide by the number of rows
    bytesPerLineBW = int(totalBytesBW/frameBW.shape[0]) #I had to introduce it to avoid distortion in the opened file for some of the videos
    self.frameBW = QImage(frameBW.data, frameBW.shape[1], frameBW.shape[0], bytesPerLineBW, QImage.Format_Grayscale8)#.rgbSwapped() #shape[0] = height, [1] = width QImage.Format_Indexed8 or Grayscale8 BGR888
    self.frameBW = self.frameBW.scaled(self.lbl1_CT.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

def findFlameEdges(self, frameBW, flamePx):
    self.flameArea = len(flamePx[0])
    self.xMax = 0
    self.xMin = 0
    self.xRight = 0
    self.xLeft = 0
    sortedBWx = sorted(flamePx[1])
    i = 0
    try:
        # average of the flame location based on the n# of points indicated by the user
        for x in range(int(self.avgLEIn_CT.text())):
            i = i + 1
            self.xMax = self.xMax + sortedBWx[-i]
            self.xMin = self.xMin + sortedBWx[i]

        self.xMax = int(self.xMax/int(self.avgLEIn_CT.text()))
        self.xMin = int(self.xMin/int(self.avgLEIn_CT.text()))
        if flameDir == 'toRight':
            self.xRight = int(self.roiOneIn.text()) + self.xMax
            self.xLeft = int(self.roiOneIn.text()) + self.xMin
        elif flameDir == 'toLeft':
            self.xRight = self.vWidth - int(self.roiOneIn.text()) - self.xMax
            self.xLeft = self.vWidth - int(self.roiOneIn.text()) - self.xMin
    except:
        self.msgLabel.setText('Flame not found in some frames')

def colorTracking(self):
    scale = True
    if not self.scaleIn.text():
        scale = False
        msg = QMessageBox(self)
        msg.setText('The scale [px/mm] has not been specified')
        msg.exec_()

    firstFrame = int(self.firstFrameIn.text())
    lastFrame = int(self.lastFrameIn.text())
    currentFrame = firstFrame
    self.xRight_mm = list()
    self.xLeft_mm = list()
    flameLength_mm = list()
    self.frameCount = list()
    flameArea = list()

    if self.exportEdges_CT.isChecked():
        fps = (float(self.vFpsLbl.text()))/(int(self.skipFrameIn.text()) + 1) #fps(new) = fps(original)/(skipframes + 1)
        codec = str(self.codecIn.text())
        vFormat = str(self.formatIn.text())
        vName = self.fPath + '-trackedVideo.' + str(vFormat) # alternative: 'output.{}'.format(vFormat);   self.fNameLbl.text()
        fourcc = cv2.VideoWriter_fourcc(*codec)
        size = (int(self.roiThreeIn.text()), int(self.roiFourIn.text()))
        # open and set properties
        vout = cv2.VideoWriter()
        vout.open(vName, fourcc, fps, size, True)

    if scale: #this condition prevents crashes in case the scale is not specified
        while (currentFrame < lastFrame):
            print('Frame #:', currentFrame) #beta
            frame, frameCrop = ft.checkEditing(self, currentFrame)
            if self.filterLight_CT.isChecked() == True:
                if self.lightROI_CT_recorded == True: #beta
                    # looking for frames with a light on (which would increase the red and green channel values of the background)
                    low = ([5, 5, 10]) # blueLow, greenLow, redLow (see color tracking)
                    high = ([255, 255, 255]) # blueHigh, greenHigh, redHigh
                    low = np.array(low, dtype = 'uint8') #this conversion is necessary
                    high = np.array(high, dtype = 'uint8')
                    currentLightROI = frame[self.lightROI_CT[1] : (self.lightROI_CT[1] + self.lightROI_CT[3]), self.lightROI_CT[0] : (self.lightROI_CT[0] + self.lightROI_CT[2])]
                    newMask = cv2.inRange(currentLightROI, low, high)
                    frame_light = cv2.bitwise_and(currentLightROI, currentLightROI, mask = newMask)
                    grayFrame_light = cv2.cvtColor(frame_light, cv2.COLOR_BGR2GRAY)
                    (thresh_light, frameBW_light) = cv2.threshold(grayFrame_light, 0, 255, cv2.THRESH_BINARY)
                    flamePx_light = np.where(frameBW_light == [255]) #beta
                    area_lightROI = int(self.lightROI_CT[3] * self.lightROI_CT[2])
                else:
                    msg = QMessageBox(self)
                    msg.setText('Before the tracking, please click on "Pick a bright region" to select a region where the light is visible.')
                    msg.exec_()
                    break

                if len(flamePx_light[0]) < 0.5 * area_lightROI: #if the bright area is larger than the ROI area
                    getFilteredFrame(self, frameCrop)
                    print('frame counted')
                else:
                    currentFrame = currentFrame + 1 + int(self.skipFrameIn.text())
                    print('frame not counted')
                    continue
            else:
                getFilteredFrame(self, frameCrop)

            self.xRight_mm.append(self.xRight / float(self.scaleIn.text()))
            self.xLeft_mm.append(self.xLeft / float(self.scaleIn.text()))
            flameArea.append(self.flameArea)
            self.frameCount.append(currentFrame)
            if self.exportEdges_CT.isChecked():
                vout.write(self.currentFrameRGB_CT)
            print('Progress: ', round((currentFrame - firstFrame)/(lastFrame - firstFrame) * 10000)/100, '%')
            currentFrame = currentFrame + 1 + int(self.skipFrameIn.text())

        try:
            self.flameArea = [areaN / (float(self.scaleIn.text())**2) for areaN in flameArea]
            self.flameArea = np.round(self.flameArea, 3)
            self.flameArea = self.flameArea.tolist()
            self.timeCount = [frameN / float(self.vFpsLbl.text()) for frameN in self.frameCount]
        except:
            pass

        for i in range(len(self.xRight_mm)):
            flameLength_mm.append(abs(self.xRight_mm[i] - self.xLeft_mm[i]))

        flameLength_mm = np.round(flameLength_mm, 2)
        self.flameLength_mm = flameLength_mm.tolist()
        print('Progress: 100 % - Tracking completed')
        self.msgLabel.setText('Tracking completed')

        if self.exportEdges_CT.isChecked():
            vout.release()
            self.msgLabel.setText('Tracking completed and video created.')

        # the following approach to calculate the spread rate is the same one used for lumaTracking
        movAvgPt = int(self.movAvgIn_CT.text()) #this number is half of the interval considered for the spread rate (movAvgPt = 2 means I am considering a total of 5 points (my point, 2 before and 2 after))
        self.spreadRateRight = list()
        self.spreadRateLeft = list()

        if movAvgPt == 0:
            for i in range(len(self.timeCount)-1):
                xCoeffRight = np.polyfit(self.timeCount[(i):(i + 2)], self.xRight_mm[(i):(i + 2)], 1)
                xCoeffLeft = np.polyfit(self.timeCount[(i):(i + 2)], self.xLeft_mm[(i):(i + 2)], 1)
                self.spreadRateRight.append(xCoeffRight[0])
                self.spreadRateLeft.append(xCoeffLeft[0])
            #repeat the last value
            self.spreadRateRight.append(xCoeffRight[0])
            self.spreadRateLeft.append(xCoeffLeft[0])
        else: #here we calculate the instantaneous spread rate based on the moving avg. I also included the initial and final points
            for i in range(len(self.timeCount)):
                if i - movAvgPt < 0:
                    xCoeffRight = np.polyfit(self.timeCount[0:(i + movAvgPt + 1)], self.xRight_mm[0:(i + movAvgPt + 1)], 1)
                    xCoeffLeft = np.polyfit(self.timeCount[0:(i + movAvgPt + 1)], self.xLeft_mm[0:(i + movAvgPt + 1)], 1)
                    self.spreadRateRight.append(xCoeffRight[0])
                    self.spreadRateLeft.append(xCoeffLeft[0])
                elif i >= movAvgPt:
                    xCoeffRight = np.polyfit(self.timeCount[(i - movAvgPt):(i + movAvgPt + 1)], self.xRight_mm[(i - movAvgPt):(i + movAvgPt + 1)], 1)
                    xCoeffLeft = np.polyfit(self.timeCount[(i - movAvgPt):(i + movAvgPt + 1)], self.xLeft_mm[(i - movAvgPt):(i + movAvgPt + 1)], 1)
                    self.spreadRateRight.append(xCoeffRight[0])
                    self.spreadRateLeft.append(xCoeffLeft[0])
                elif i + movAvgPt > len(self.timeCount):
                    xCoeffRight = np.polyfit(self.timeCount[(i - movAvgPt):], self.xRight_mm[(i - movAvgPt):], 1)
                    xCoeffLeft = np.polyfit(self.timeCount[(i - movAvgPt):], self.xLeft_mm[(i - movAvgPt):], 1)
                    self.spreadRateRight.append(xCoeffRight[0])
                    self.spreadRateLeft.append(xCoeffLeft[0])

        self.spreadRateRight = np.round(self.spreadRateRight, 3)
        self.spreadRateRight = self.spreadRateRight.tolist()
        self.spreadRateLeft = np.round(self.spreadRateLeft, 3)
        self.spreadRateLeft = self.spreadRateLeft.tolist()

        self.lbl1_CT = pg.PlotWidget(self.colorTrackingBox)
        self.lbl2_CT = pg.PlotWidget(self.colorTrackingBox)
        if self.OStype == 'mac' or self.OStype == 'lin':
            self.lbl1_CT.setGeometry(370, 25, 330, 250)
            self.lbl2_CT.setGeometry(710, 25, 330, 250)
        elif self.OStype == 'win':
            self.lbl1_CT.setGeometry(370, 15, 330, 250)
            self.lbl2_CT.setGeometry(710, 15, 330, 250)
        #self.lbl1_CT.setGeometry(370, 25, 330, 250)
        self.lbl1_CT.setBackground('w')
        self.lbl1_CT.setLabel('left', 'Position [mm]', color='black', size=14)
        self.lbl1_CT.setLabel('bottom', 'Time [s]', color='black', size=14)
        self.lbl1_CT.getAxis('bottom').setPen(color=(0, 0, 0))
        self.lbl1_CT.getAxis('left').setPen(color=(0, 0, 0))
        self.lbl1_CT.addLegend(offset = [1, 0.1]) # background color modified in line 122 and 123 of Versions/3.7/lib/python3.7/site-packages/pyqtgraph/graphicsItems
        self.lbl2_CT.setBackground('w')
        self.lbl2_CT.setLabel('left', 'Spread Rate [mm/s]', color='black', size=14)
        self.lbl2_CT.setLabel('bottom', 'Time [s]', color='black', size=14)
        self.lbl2_CT.getAxis('bottom').setPen(color=(0, 0, 0))
        self.lbl2_CT.getAxis('left').setPen(color=(0, 0, 0))
        self.lbl2_CT.addLegend(offset = [1, 0.1]) # background color modified in line 122 and 123 of Versions/3.7/lib/python3.7/site-packages/pyqtgraph/graphicsItems

        colorTrackingPlot(self.lbl1_CT, self.timeCount, self.xRight_mm, 'right edge', 'o', 'b')
        colorTrackingPlot(self.lbl1_CT, self.timeCount, self.xLeft_mm, 'left edge', 't', 'r')
        colorTrackingPlot(self.lbl2_CT, self.timeCount, self.spreadRateRight, 'right edge', 'o', 'b')
        colorTrackingPlot(self.lbl2_CT, self.timeCount, self.spreadRateLeft, 'left edge', 't', 'r')

        self.lbl1_CT.show()
        self.lbl2_CT.show()

def colorTrackingPlot(label, x, y, name, symbol, color):
    pen = pg.mkPen(color)
    label.plot(x, y, pen = pen, name = name, symbol = symbol, symbolSize = 7, symbolBrush = (color))

def colorSlider_released(self):
    frame, frameCrop = ft.checkEditing(self, self.frameNumber)
    getFilteredFrame(self, frameCrop)
    self.lbl1_CT.setPixmap(QPixmap.fromImage(self.frame))
    self.lbl2_CT.setPixmap(QPixmap.fromImage(self.frameBW))

def filterParticleSldr(self):
    frame, frameCrop = ft.checkEditing(self, self.frameNumber)
    getFilteredFrame(self, frameCrop)
    self.lbl1_CT.setPixmap(QPixmap.fromImage(self.frame))
    self.lbl2_CT.setPixmap(QPixmap.fromImage(self.frameBW))
    self.filterParticleSldr_CT.setMaximum(int(self.particleSldrMax.text()))

# def perspectiveCorrection(self, frame):
#     # M is the matrix transformation calculated with the size of the sample (calculated from user input), and the sampleMod from the user clicks
#     M = cv2.getPerspectiveTransform(self.sample, self.sampleMod)
#     # If the perspective is done on a rotated video, the corrected image might have a much larger size than the original one, here we check this
#     originalFrame = np.float32([[0,0], [self.vWidth, 0], [self.vWidth, self.vHeight], [0, self.vHeight]])
#     width = int(frame.shape[1])
#     height = int(frame.shape[0])
#     for point in self.sampleMod:
#         if point[0] > width:
#             width = int(point[0])
#         if point[1] > height:
#             height = int(point[1])
#
#     frame = cv2.warpPerspective(frame, M, (width, height))
#     return(frame)

# def rotationCorrection(self, frame, angle):
#     # rotation matrix:
#     width = int(self.vWidth)
#     height = int(self.vHeight)
#     center = (width/2, height/2)
#     matrix = cv2.getRotationMatrix2D(center, angle, 1) #center of rotation, angle, zoom In/zoom Out
#     # rotation calculates the cos and sin, taking absolutes of those (these extra steps are used to avoid cropping )
#     abs_cos = abs(matrix[0,0])
#     abs_sin = abs(matrix[0,1])
#     # find the new width and height bounds
#     region_w = int(height * abs_sin + width * abs_cos)
#     region_h = int(height * abs_cos + width * abs_sin)
#     # subtract old image center (bringing image back to origo) and adding the new image center coordinates
#     matrix[0, 2] += region_w/2 - center[0]
#     matrix[1, 2] += region_h/2 - center[1]
#     frame = cv2. warpAffine(frame, matrix, (region_w, region_h)) #resolution is specified
#     return(frame)

def chooseFlameDirection(self, text):
    global flameDir
    selection = self.directionBox.currentText()
    if selection == 'Left to right':
        flameDir = 'toRight'
    elif selection == 'Right to left':
        flameDir = 'toLeft'

def connectivityBox(self, text):
    global connectivity_CT
    selection = self.connectivityBox.currentText()
    if selection == '4':
        connectivity_CT = 4
    elif selection == '8':
        connectivity_CT = 8

def saveChannelsBtn(self):
    name = QFileDialog.getSaveFileName(self, 'Save channel values')
    name = name[0]
    if not name[-4:] == '.csv':
        name = name + '.csv'
    if name == '.csv': #this prevents name issues when the user closes the dialog without saving
        self.msgLabel.setText('Ops! Parameters were not saved.')
    else:
        try:
            with open(name, 'w', newline = '') as csvfile:
                writer = csv.writer(csvfile, delimiter = ',')
                writer.writerow(['File', self.fNameLbl.text()])
                writer.writerow(['Channel', 'Minimum', 'Maximum'])
                writer.writerow(['Red', str(self.redMinSlider.value()), str(self.redMaxSlider.value())])
                writer.writerow(['Green', str(self.greenMinSlider.value()), str(self.greenMaxSlider.value())])
                writer.writerow(['Blue', str(self.blueMinSlider.value()), str(self.blueMaxSlider.value())])
                writer.writerow([''])
                writer.writerow(['Particle size', str(self.filterParticleSldr_CT.value())])
                writer.writerow(['Moving average', str(self.movAvgIn_CT.text())])
                writer.writerow(['Points LE', str(self.avgLEIn_CT.text())])
                writer.writerow(['Connectivity', str(connectivity_CT)])
            self.msgLabel.setText('Channel values saved.')
        except:
            self.msgLabel.setText('Ops! The values were not saved.')

def loadChannelsBtn(self):
    name = QFileDialog.getOpenFileName(self, 'Load channel values')
    try:
        with open(name[0], 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for row in reader:
                if 'Red' in row:
                    self.redMinSlider.setValue(int(row[1]))
                    self.redMaxSlider.setValue(int(row[2]))
                elif 'Green' in row:
                    self.greenMinSlider.setValue(int(row[1]))
                    self.greenMaxSlider.setValue(int(row[2]))
                elif 'Blue' in row:
                    self.blueMinSlider.setValue(int(row[1]))
                    self.blueMaxSlider.setValue(int(row[2]))
                elif 'Particle size' in row:
                    self.filterParticleSldr_CT.setValue(int(row[1]))
                elif 'Moving average' in row:
                    self.movAvgIn_CT.setText(row[1])
                elif 'Points LE' in row:
                    self.avgLEIn_CT.setText(row[1])

        self.msgLabel.setText('Channel values loaded.')
    except:
        notParameters_dlg = QErrorMessage(self)
        notParameters_dlg.showMessage('Ops! There was a problem loading the parameters.')
        self.msgLabel.setText('Ops! Parameters were not loaded.')

def absValBtn(self):
    abs_frames = list()
    abs_time = list()
    abs_xRight_mm = list()
    abs_xLeft_mm = list()

    for i in self.frameCount:
        abs_frames.append(i - self.frameCount[0])

    for i in self.timeCount:
        abs_time.append(i - self.timeCount[0])

    for i in self.xRight_mm:
        abs_xRight_mm.append(i - self.xRight_mm[0])

    for i in self.xLeft_mm:
        abs_xLeft_mm.append(i - self.xRight_mm[0])

    self.frameCount = abs_frames
    self.timeCount = abs_time
    self.xRight_mm = abs_xRight_mm
    self.xLeft_mm = abs_xLeft_mm

    self.lbl1_CT.clear()
    self.lbl2_CT.clear()

    colorTrackingPlot(self.lbl1_CT, self.timeCount, self.xRight_mm, '', 'o', 'b')
    colorTrackingPlot(self.lbl1_CT, self.timeCount, self.xLeft_mm, '','t', 'r')
    colorTrackingPlot(self.lbl2_CT, self.timeCount, self.spreadRateRight, '', 'o', 'b')
    colorTrackingPlot(self.lbl2_CT, self.timeCount, self.spreadRateLeft, '','t', 'r')

def saveBtn(self):
    fileName = QFileDialog.getSaveFileName(self, 'Save tracking data')
    fileName = fileName[0]
    if not fileName[-4:] == '.csv':
        fileName = fileName + '.csv'

    fileInfo = ['Name', self.fNameLbl.text(), 'Scale [px/mm]', self.scaleIn.text(), 'Moving avg', self.movAvgIn_CT.text(), 'Points LE', self.avgLEIn_CT.text(), 'Flame dir.:', flameDir]
    lbl = ['File info', 'Frame', 'Time [s]', 'Right Edge [mm]', 'Left Edge [mm]', 'Length [mm]', 'Spread Rate RE [mm/s]', 'Spread Rate LE [mm/s]', 'Area [mm^2]']
    clms = [fileInfo, self.frameCount, self.timeCount, self.xRight_mm, self.xLeft_mm, self.flameLength_mm, self.spreadRateRight, self.spreadRateLeft, self.flameArea]
    clms_zip = zip_longest(*clms)

    if fileName == '.csv': #this prevents name issues when the user closes the dialog without saving
        self.msgLabel.setText('Ops! The values were not saved.')
    else:
        try:
            with open(fileName, 'w', newline = '') as csvfile:
                writer = csv.writer(csvfile, delimiter = ',')
                writer.writerow(lbl)
                for row in clms_zip:
                    writer.writerow(row)
            self.msgLabel.setText('Data succesfully saved.')
        except:
            self.msgLabel.setText('Ops! The values were not saved.')

def showFrameLarge(self):
    cv2.namedWindow(('Frame (RGB): ' + self.frameIn.text()), cv2.WINDOW_AUTOSIZE)
    cv2.imshow(('Frame (RGB): ' + self.frameIn.text()), self.currentFrameRGB_CT)
    cv2.namedWindow(('Frame (black/white): ' + self.frameIn.text()), cv2.WINDOW_AUTOSIZE)
    cv2.imshow(('Frame (black/white): ' + self.frameIn.text()), self.currentFrameBW_CT)
    while True:
        if cv2.waitKey(1) == 27: #ord('Esc')
            cv2.destroyAllWindows()
            return

def lightROIBtn(self):
    frame, frameCrop = ft.checkEditing(self, self.frameNumber)
    self.lightROI_CT = cv2.selectROI(frame)
    cv2.destroyAllWindows()
    self.lightROI_CT_recorded = True

def redMinLeftBtn(self):
    currentValue = self.redMinSlider.value()
    self.redMinSlider.setValue(currentValue - 1)
    colorSlider_released(self)
def redMinRightBtn(self):
    currentValue = self.redMinSlider.value()
    self.redMinSlider.setValue(currentValue + 1)
    colorSlider_released(self)
def redMaxLeftBtn(self):
    currentValue = self.redMaxSlider.value()
    self.redMaxSlider.setValue(currentValue - 1)
    colorSlider_released(self)
def redMaxRightBtn(self):
    currentValue = self.redMaxSlider.value()
    self.redMaxSlider.setValue(currentValue + 1)
    colorSlider_released(self)
def greenMinLeftBtn(self):
    currentValue = self.greenMinSlider.value()
    self.greenMinSlider.setValue(currentValue - 1)
    colorSlider_released(self)
def greenMinRightBtn(self):
    currentValue = self.greenMinSlider.value()
    self.greenMinSlider.setValue(currentValue + 1)
    colorSlider_released(self)
def greenMaxLeftBtn(self):
    currentValue = self.greenMaxSlider.value()
    self.greenMaxSlider.setValue(currentValue - 1)
    colorSlider_released(self)
def greenMaxRightBtn(self):
    currentValue = self.greenMaxSlider.value()
    self.greenMaxSlider.setValue(currentValue + 1)
    colorSlider_released(self)
def blueMinLeftBtn(self):
    currentValue = self.blueMinSlider.value()
    self.blueMinSlider.setValue(currentValue - 1)
    colorSlider_released(self)
def blueMinRightBtn(self):
    currentValue = self.blueMinSlider.value()
    self.blueMinSlider.setValue(currentValue + 1)
    colorSlider_released(self)
def blueMaxLeftBtn(self):
    currentValue = self.blueMaxSlider.value()
    self.blueMaxSlider.setValue(currentValue - 1)
    colorSlider_released(self)
def blueMaxRightBtn(self):
    currentValue = self.blueMaxSlider.value()
    self.blueMaxSlider.setValue(currentValue + 1)
    colorSlider_released(self)

def helpBtn(self):
    msg = QMessageBox(self)
    msg.setText("""In this analysis the flame is tracked based on the image colors. After specifying the video parameters and the flame direction, the flame region can be identified by choosing appropriate values of the RGB channels. The channel values vary between 0 and 255, and the code will consider the range between minimum and maximum of each channel adjusted with the sliders.

    Small bright regions can be filtered out with the 'Filter particles' slider. The value of the slider indicates the area (in px^2) of the regions to remove from the images, and you can change the maximum value by typing a number in the text box next to 'Filter particles'.

    The preview window on the left shows the RGB image resulting from the filtering, while the window on the right shows the binary image with the particle filtering applied. The edges of the flame region are calculated as maximum and minimum locations of the binary image. The number of points considered to calculate these locations ('#px to locate edges:') can be adjusted as needed.

    If there is a flashing light in the video, the illuminated frames can be discarded in the analysis by checking the 'Ignore flashing light' box. Before starting the analysis, click on 'Pick bright region' to select a (small) Region of Interest (ROI) where the effect of the light is visible. Note that this ROI is independent from the ROI specified in the 'Preview box'.

    Flame position and spread rates are calculated automatically once 'Start tracking' is clicked. The instantaneous spread rates are averaged according to the number of points specified by the user ('Moving avg points'). Note that the 'Moving avg points' value is doubled for the calculation of the spread rate (i.e. 'Moving avg points' = 2 considers two points before and two points after the instantaneous value).

    'Absolute values' can be used to make the counts of flame position and time starting from zero.

    Click on 'Save data' to export a csv file with all the tracked information. The channel values and particle size are saved separately with 'Save filter values'.

    By checking 'Video output' all the considered frames in the analysis (filtered images) will be exported as a video.

    """)
    msg.exec_()
