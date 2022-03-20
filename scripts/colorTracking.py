"""
Flame Tracker. This program is designed to track flames or bright objects in videos or images.
Copyright (C) 2020-2022  Luca Carmignani

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

# from PyQt6 import QtGui
# from PyQt6.QtGui import *
# from PyQt6.QtWidgets import *
# from PyQt6.QtCore import *
# from itertools import zip_longest

import flameTracker as ft
import boxesGUI_OS as gui
# import csv
# import ft.cv2
# import pyqtgraph as pg
# import numpy as np
# import sys

def initVars(self): # define initial variables
    # global connectivity_CT #, flameDir
    # # flameDir = 'toRight'
    # connectivity_CT = 4
    self.lightROI_CT_recorded = False

def getFilteredFrame(self, frame):
    blueLow = self.blueMinSlider.value()
    blueHigh = self.blueMaxSlider.value()
    greenLow = self.greenMinSlider.value()
    greenHigh = self.greenMaxSlider.value()
    redLow = self.redMinSlider.value()
    redHigh = self.redMaxSlider.value()
    low = ([blueLow, greenLow, redLow])
    high = ([blueHigh, greenHigh, redHigh])
    low = ft.np.array(low, dtype = 'uint8') #this conversion is necessary
    high = ft.np.array(high, dtype = 'uint8')
    newMask = ft.cv2.inRange(frame, low, high)
    frame = ft.cv2.bitwise_and(frame, frame, mask = newMask)
    grayFrame = ft.cv2.cvtColor(frame, ft.cv2.COLOR_BGR2GRAY)
    (threshold, frameBW) = ft.cv2.threshold(grayFrame, 0, 255, ft.cv2.THRESH_BINARY)

    # Find all the connected components (8 means in the four directions and diagonals)
    componentNum, componentLbl, stats, centroids = ft.cv2.connectedComponentsWithStats(frameBW, connectivity = int(self.connectivityBox.currentText()))
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

    flamePx = ft.np.where(frameBW == [255]) # total area in px

    findFlameEdges(self, frameBW, flamePx)

    if self.showEdges.isChecked() == True:
        ft.cv2.line(frame, (self.xMax, 0),(self.xMax, int(self.roiFourIn.text())), (255, 255, 255), 2)
        ft.cv2.line(frame, (self.xMin, 0),(self.xMin, int(self.roiFourIn.text())), (255, 255, 255), 2)
        ft.cv2.line(frameBW, (self.xMax, 0),(self.xMax, int(self.roiFourIn.text())), (255, 255, 255), 2)
        ft.cv2.line(frameBW, (self.xMin, 0),(self.xMin, int(self.roiFourIn.text())), (255, 255, 255), 2)

    self.currentFrameRGB_CT = frame
    # calculate the total number of bytes in the frame for lbl1
    totalBytes = frame.nbytes
    # divide by the number of rows
    bytesPerLine = int(totalBytes/frame.shape[0]) #I had to introduce it to avoid distortion in the opened file for some of the videos
    if self.pyqtVer == '5':
        self.frame = ft.QImage(frame.data, frame.shape[1], frame.shape[0], bytesPerLine, ft.QImage.Format_BGR888)#.rgbSwapped() #shape[0] = height, [1] = width QImage.Format_Indexed8 BGR888
        self.frame = self.frame.scaled(self.lbl1_CT.size(), ft.Qt.KeepAspectRatio, ft.Qt.SmoothTransformation)
    elif self.pyqtVer == '6':
        self.frame = ft.QImage(frame.data, frame.shape[1], frame.shape[0], bytesPerLine, ft.QImage.Format.Format_BGR888)#.rgbSwapped() #shape[0] = height, [1] = width QImage.Format_Indexed8 BGR888
        self.frame = self.frame.scaled(self.lbl1_CT.size(), ft.Qt.AspectRatioMode.KeepAspectRatio, ft.Qt.TransformationMode.SmoothTransformation)

    self.currentFrameBW_CT = frameBW
    # calculate the total number of bytes in the frame for lbl2
    totalBytesBW = frameBW.nbytes
    # divide by the number of rows
    bytesPerLineBW = int(totalBytesBW/frameBW.shape[0]) #I had to introduce it to avoid distortion in the opened file for some of the videos
    if self.pyqtVer == '5':
        self.frameBW = ft.QImage(frameBW.data, frameBW.shape[1], frameBW.shape[0], bytesPerLineBW, ft.QImage.Format_Grayscale8)#.rgbSwapped() #shape[0] = height, [1] = width QImage.Format_Indexed8 or Grayscale8 BGR888
        self.frameBW = self.frameBW.scaled(self.lbl1_CT.size(), ft.Qt.KeepAspectRatio, ft.Qt.SmoothTransformation)
    elif self.pyqtVer == '6':
        self.frameBW = ft.QImage(frameBW.data, frameBW.shape[1], frameBW.shape[0], bytesPerLineBW, ft.QImage.Format.Format_Grayscale8)#.rgbSwapped() #shape[0] = height, [1] = width QImage.Format_Indexed8 or Grayscale8 BGR888
        self.frameBW = self.frameBW.scaled(self.lbl1_CT.size(), ft.Qt.AspectRatioMode.KeepAspectRatio, ft.Qt.TransformationMode.SmoothTransformation)

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
        # if flameDir == 'toRight':
        if self.directionBox.currentText() == 'Left to right':
            self.xRight = int(self.roiOneIn.text()) + self.xMax
            self.xLeft = int(self.roiOneIn.text()) + self.xMin
        elif self.directionBox.currentText() == 'Right to left':
            self.xRight = self.vWidth - int(self.roiOneIn.text()) - self.xMax
            self.xLeft = self.vWidth - int(self.roiOneIn.text()) - self.xMin
    except:
        self.msgLabel.setText('Flame not found in some frames')

def colorTracking(self):
    scale = True
    if not self.scaleIn.text():
        scale = False
        msg = ft.QMessageBox(self)
        msg.setText('The scale [px/mm] has not been specified')
        if self.pyqtVer == '5':
            msg.exec_()
        elif self.pyqtVer == '6':
            msg.exec()

    firstFrame = int(self.firstFrameIn.text())
    lastFrame = int(self.lastFrameIn.text())
    currentFrame = firstFrame
    self.xRight_px = list()
    self.xLeft_px = list()
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
        fourcc = ft.cv2.VideoWriter_fourcc(*codec)
        size = (int(self.roiThreeIn.text()), int(self.roiFourIn.text()))
        # open and set properties
        vout = ft.cv2.VideoWriter()
        vout.open(vName, fourcc, fps, size, True)

    if scale: #this condition prevents crashes in case the scale is not specified
        xAxis_lbl1 = self.xAxis_lbl1.currentText()
        yAxis_lbl1 = self.yAxis_lbl1.currentText()
        xAxis_lbl2 = self.xAxis_lbl2.currentText()
        yAxis_lbl2 = self.yAxis_lbl2.currentText()
        while (currentFrame < lastFrame):
            # print('Frame #:', currentFrame)
            frame, frameCrop = ft.checkEditing(self, currentFrame)
            if self.filterLight_CT.isChecked() == True:
                if self.lightROI_CT_recorded == True: #beta
                    # looking for frames with a light on (which would increase the red and green channel values of the background)
                    low = ([5, 5, 10]) # blueLow, greenLow, redLow (see color tracking)
                    high = ([255, 255, 255]) # blueHigh, greenHigh, redHigh
                    low = ft.np.array(low, dtype = 'uint8') #this conversion is necessary
                    high = ft.np.array(high, dtype = 'uint8')
                    currentLightROI = frame[self.lightROI_CT[1] : (self.lightROI_CT[1] + self.lightROI_CT[3]), self.lightROI_CT[0] : (self.lightROI_CT[0] + self.lightROI_CT[2])]
                    newMask = ft.cv2.inRange(currentLightROI, low, high)
                    frame_light = ft.cv2.bitwise_and(currentLightROI, currentLightROI, mask = newMask)
                    grayFrame_light = ft.cv2.cvtColor(frame_light, ft.cv2.COLOR_BGR2GRAY)
                    (thresh_light, frameBW_light) = ft.cv2.threshold(grayFrame_light, 0, 255, ft.cv2.THRESH_BINARY)
                    flamePx_light = ft.np.where(frameBW_light == [255]) #beta
                    area_lightROI = int(self.lightROI_CT[3] * self.lightROI_CT[2])
                else:
                    msg = ft.QMessageBox(self)
                    msg.setText('Before the tracking, please click on "Pick a bright region" to select a region where the light is visible.')
                    if self.pyqtVer == '5':
                        msg.exec_()
                    elif self.pyqtVer == '6':
                        msg.exec()
                    break

                if len(flamePx_light[0]) < 0.5 * area_lightROI: #if the bright area is larger than the ROI area
                    getFilteredFrame(self, frameCrop)
                    # print('frame counted')
                else:
                    currentFrame = currentFrame + 1 + int(self.skipFrameIn.text())
                    # print('frame not counted')
                    continue
            else:
                getFilteredFrame(self, frameCrop)

            self.xRight_px.append(self.xRight)
            self.xLeft_px.append(self.xLeft)
            self.xRight_mm.append(self.xRight / float(self.scaleIn.text()))
            self.xLeft_mm.append(self.xLeft / float(self.scaleIn.text()))
            flameArea.append(self.flameArea)
            self.frameCount.append(currentFrame)
            if self.exportEdges_CT.isChecked():
                vout.write(self.currentFrameRGB_CT)
            print('Progress: ', round((currentFrame - firstFrame)/(lastFrame - firstFrame) * 10000)/100, '%', '(Frame #: ', currentFrame, ')', end='\r')
            currentFrame = currentFrame + 1 + int(self.skipFrameIn.text())

        try:
            self.flameArea = [areaN / (float(self.scaleIn.text())**2) for areaN in flameArea]
            self.flameArea = ft.np.round(self.flameArea, 3)
            self.flameArea = self.flameArea.tolist()
            self.timeCount = [frameN / float(self.vFpsLbl.text()) for frameN in self.frameCount]
        except:
            pass

        for i in range(len(self.xRight_mm)):
            flameLength_mm.append(abs(self.xRight_mm[i] - self.xLeft_mm[i]))

        flameLength_mm = ft.np.round(flameLength_mm, 2)
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
                xCoeffRight = ft.np.polyfit(self.timeCount[(i):(i + 2)], self.xRight_mm[(i):(i + 2)], 1)
                xCoeffLeft = ft.np.polyfit(self.timeCount[(i):(i + 2)], self.xLeft_mm[(i):(i + 2)], 1)
                self.spreadRateRight.append(xCoeffRight[0])
                self.spreadRateLeft.append(xCoeffLeft[0])
            #repeat the last value
            self.spreadRateRight.append(xCoeffRight[0])
            self.spreadRateLeft.append(xCoeffLeft[0])
        else: #here we calculate the instantaneous spread rate based on the moving avg. I also included the initial and final points
            for i in range(len(self.timeCount)):
                if i - movAvgPt < 0:
                    xCoeffRight = ft.np.polyfit(self.timeCount[0:(i + movAvgPt + 1)], self.xRight_mm[0:(i + movAvgPt + 1)], 1)
                    xCoeffLeft = ft.np.polyfit(self.timeCount[0:(i + movAvgPt + 1)], self.xLeft_mm[0:(i + movAvgPt + 1)], 1)
                    self.spreadRateRight.append(xCoeffRight[0])
                    self.spreadRateLeft.append(xCoeffLeft[0])
                elif i >= movAvgPt:
                    xCoeffRight = ft.np.polyfit(self.timeCount[(i - movAvgPt):(i + movAvgPt + 1)], self.xRight_mm[(i - movAvgPt):(i + movAvgPt + 1)], 1)
                    xCoeffLeft = ft.np.polyfit(self.timeCount[(i - movAvgPt):(i + movAvgPt + 1)], self.xLeft_mm[(i - movAvgPt):(i + movAvgPt + 1)], 1)
                    self.spreadRateRight.append(xCoeffRight[0])
                    self.spreadRateLeft.append(xCoeffLeft[0])
                elif i + movAvgPt > len(self.timeCount):
                    xCoeffRight = ft.np.polyfit(self.timeCount[(i - movAvgPt):], self.xRight_mm[(i - movAvgPt):], 1)
                    xCoeffLeft = ft.np.polyfit(self.timeCount[(i - movAvgPt):], self.xLeft_mm[(i - movAvgPt):], 1)
                    self.spreadRateRight.append(xCoeffRight[0])
                    self.spreadRateLeft.append(xCoeffLeft[0])

        self.spreadRateRight = ft.np.round(self.spreadRateRight, 3)
        self.spreadRateRight = self.spreadRateRight.tolist()
        self.spreadRateLeft = ft.np.round(self.spreadRateLeft, 3)
        self.spreadRateLeft = self.spreadRateLeft.tolist()

        self.lbl1_CT = ft.pg.PlotWidget(self.colorTrackingBox)
        self.lbl2_CT = ft.pg.PlotWidget(self.colorTrackingBox)
        if ft.sys.platform == 'darwin':
            lbl1 = [370, 25, 330, 250]
            lbl2 = [710, 25, 330, 250]
        elif ft.sys.platform == 'win32':
            lbl1 = [370, 15, 330, 250]
            lbl2 = [710, 15, 330, 250]
        elif ft.sys.platform == 'linux':
            lbl1 = [370, 25, 330, 250]
            lbl2 = [710, 25, 330, 250]

        self.lbl1_CT.setGeometry(lbl1[0], lbl1[1], lbl1[2], lbl1[3])
        self.lbl2_CT.setGeometry(lbl2[0], lbl2[1], lbl2[2], lbl2[3])
        self.lbl1_CT.setBackground('w')
        # self.lbl1_CT.setLabel('left', 'Position [mm]', color='black', size=14)
        # self.lbl1_CT.setLabel('bottom', 'Time [s]', color='black', size=14)
        self.lbl1_CT.setLabel('left', str(yAxis_lbl1), color='black', size=14)
        self.lbl1_CT.setLabel('bottom', str(xAxis_lbl1), color='black', size=14)
        self.lbl1_CT.getAxis('bottom').setPen(color=(0, 0, 0))
        self.lbl1_CT.getAxis('left').setPen(color=(0, 0, 0))
        self.lbl1_CT.addLegend(offset = [1, 0.1]) # background color modified in line 122 and 123 of Versions/3.7/lib/python3.7/site-packages/pyqtgraph/graphicsItems
        self.lbl2_CT.setBackground('w')
        # self.lbl2_CT.setLabel('left', 'Spread Rate [mm/s]', color='black', size=14)
        # self.lbl2_CT.setLabel('bottom', 'Time [s]', color='black', size=14)
        self.lbl2_CT.setLabel('left', str(yAxis_lbl2), color='black', size=14)
        self.lbl2_CT.setLabel('bottom', str(xAxis_lbl2), color='black', size=14)
        self.lbl2_CT.getAxis('bottom').setPen(color=(0, 0, 0))
        self.lbl2_CT.getAxis('left').setPen(color=(0, 0, 0))
        self.lbl2_CT.addLegend(offset = [1, 0.1]) # background color modified in line 122 and 123 of Versions/3.7/lib/python3.7/site-packages/pyqtgraph/graphicsItems

        xPlot1, yRight1, yLeft1 = selectAxes(self, xAxis_lbl1, yAxis_lbl1)
        xPlot2, yRight2, yLeft2 = selectAxes(self, xAxis_lbl2, yAxis_lbl2)

        if yAxis_lbl1 == 'Flame length [mm]':
            colorTrackingPlot(self.lbl1_CT, xPlot1, yRight1, 'flame length', 'o', 'b')
        else:
            colorTrackingPlot(self.lbl1_CT, xPlot1, yRight1, 'right edge', 'o', 'b')
            colorTrackingPlot(self.lbl1_CT, xPlot1, yLeft1, 'left edge', 't', 'r')

        if yAxis_lbl2 == 'Flame length [mm]':
            colorTrackingPlot(self.lbl2_CT, xPlot2, yRight2, 'flame length', 'o', 'b')
        else:
            colorTrackingPlot(self.lbl2_CT, xPlot2, yRight2, 'right edge', 'o', 'b')
            colorTrackingPlot(self.lbl2_CT, xPlot2, yLeft2, 'left edge', 't', 'r')

        # colorTrackingPlot(self.lbl1_CT, self.timeCount, self.xRight_mm, 'right edge', 'o', 'b')
        # colorTrackingPlot(self.lbl1_CT, self.timeCount, self.xLeft_mm, 'left edge', 't', 'r')
        # colorTrackingPlot(self.lbl2_CT, self.timeCount, self.spreadRateRight, 'right edge', 'o', 'b')
        # colorTrackingPlot(self.lbl2_CT, self.timeCount, self.spreadRateLeft, 'left edge', 't', 'r')

        self.lbl1_CT.show()
        self.lbl2_CT.show()

def colorTrackingPlot(label, x, y, name, symbol, color):
    pen = ft.pg.mkPen(color)
    label.plot(x, y, pen = pen, name = name, symbol = symbol, symbolSize = 7, symbolBrush = (color))

def colorSlider_released(self):
    frame, frameCrop = ft.checkEditing(self, self.frameNumber)
    getFilteredFrame(self, frameCrop)
    self.lbl1_CT.setPixmap(ft.QPixmap.fromImage(self.frame))
    self.lbl2_CT.setPixmap(ft.QPixmap.fromImage(self.frameBW))

def filterParticleSldr(self):
    frame, frameCrop = ft.checkEditing(self, self.frameNumber)
    getFilteredFrame(self, frameCrop)
    self.lbl1_CT.setPixmap(ft.QPixmap.fromImage(self.frame))
    self.lbl2_CT.setPixmap(ft.QPixmap.fromImage(self.frameBW))
    self.filterParticleSldr_CT.setMaximum(int(self.particleSldrMax.text()))

# def chooseFlameDirection(self, text):
#     global flameDir
#     selection = self.directionBox.currentText()
#     if selection == 'Left to right':
#         flameDir = 'toRight'
#     elif selection == 'Right to left':
#         flameDir = 'toLeft'

# def connectivityBox(self, text):
#     global connectivity_CT
#     selection = self.connectivityBox.currentText()
#     if selection == '4':
#         connectivity_CT = 4
#     elif selection == '8':
#         connectivity_CT = 8

def saveChannelsBtn(self):
    name = ft.QFileDialog.getSaveFileName(self, 'Save channel values')
    name = name[0]
    if not name[-4:] == '.csv':
        name = name + '.csv'
    if name == '.csv': #this prevents name issues when the user closes the dialog without saving
        self.msgLabel.setText('Ops! The file name was not valid and the parameters were not saved.')
    else:
        try:
            with open(name, 'w', newline = '') as csvfile:
                writer = ft.csv.writer(csvfile, delimiter = ',')
                writer.writerow(['File', self.fNameLbl.text()])
                writer.writerow(['Channel', 'Minimum', 'Maximum'])
                writer.writerow(['Red', str(self.redMinSlider.value()), str(self.redMaxSlider.value())])
                writer.writerow(['Green', str(self.greenMinSlider.value()), str(self.greenMaxSlider.value())])
                writer.writerow(['Blue', str(self.blueMinSlider.value()), str(self.blueMaxSlider.value())])
                writer.writerow([''])
                writer.writerow(['Particle size', str(self.filterParticleSldr_CT.value())])
                writer.writerow(['Moving average', str(self.movAvgIn_CT.text())])
                writer.writerow(['Points LE', str(self.avgLEIn_CT.text())])
                writer.writerow(['Connectivity', self.connectivityBox.currentText()])
            self.msgLabel.setText('Channel values saved.')
        except:
            self.msgLabel.setText('Ops! The values were not saved.')
            print('Unexpected error:', ft.sys.exc_info())

def loadChannelsBtn(self):
    name = ft.QFileDialog.getOpenFileName(self, 'Load channel values')
    try:
        with open(name[0], 'r') as csvfile:
            reader = ft.csv.reader(csvfile, delimiter = ',')
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
        notParameters_dlg = ft.QErrorMessage(self)
        notParameters_dlg.showMessage('Ops! There was a problem loading the parameters.')
        self.msgLabel.setText('Ops! Parameters were not loaded.')
        print('Unexpected error:', ft.sys.exc_info())

def absValBtn(self):
    xAxis_lbl1 = self.xAxis_lbl1.currentText()
    yAxis_lbl1 = self.yAxis_lbl1.currentText()
    xAxis_lbl2 = self.xAxis_lbl2.currentText()
    yAxis_lbl2 = self.yAxis_lbl2.currentText()

    abs_frames = list()
    abs_time = list()
    abs_xRight_px = list()
    abs_xLeft_px = list()
    abs_xRight_mm = list()
    abs_xLeft_mm = list()

    for i in self.frameCount:
        abs_frames.append(i - self.frameCount[0])

    for i in self.timeCount:
        abs_time.append(i - self.timeCount[0])

    for i in self.xRight_px:
        abs_xRight_px.append(i - self.xRight_px[0])

    for i in self.xLeft_px:
        abs_xLeft_px.append(i - self.xRight_px[0])

    for i in self.xRight_mm:
        abs_xRight_mm.append(i - self.xRight_mm[0])

    for i in self.xLeft_mm:
        abs_xLeft_mm.append(i - self.xRight_mm[0])

    self.frameCount = abs_frames
    self.timeCount = abs_time
    self.xRight_px = abs_xRight_px
    self.xLeft_px = abs_xLeft_px
    self.xRight_mm = abs_xRight_mm
    self.xLeft_mm = abs_xLeft_mm

    self.lbl1_CT.clear()
    self.lbl2_CT.clear()

    xPlot1, yRight1, yLeft1 = selectAxes(self, xAxis_lbl1, yAxis_lbl1)
    xPlot2, yRight2, yLeft2 = selectAxes(self, xAxis_lbl2, yAxis_lbl2)

    if yAxis_lbl1 == 'Flame length [mm]':
        colorTrackingPlot(self.lbl1_CT, xPlot1, yRight1, 'flame length', 'o', 'b')
    else:
        colorTrackingPlot(self.lbl1_CT, xPlot1, yRight1, 'right edge', 'o', 'b')
        colorTrackingPlot(self.lbl1_CT, xPlot1, yLeft1, 'left edge', 't', 'r')
    if yAxis_lbl2 == 'Flame length [mm]':
        colorTrackingPlot(self.lbl2_CT, xPlot2, yRight2, 'flame length', 'o', 'b')
    else:
        colorTrackingPlot(self.lbl2_CT, xPlot2, yRight2, 'right edge', 'o', 'b')
        colorTrackingPlot(self.lbl2_CT, xPlot2, yLeft2, 'left edge', 't', 'r')

    # colorTrackingPlot(self.lbl1_CT, self.timeCount, self.xRight_mm, '', 'o', 'b')
    # colorTrackingPlot(self.lbl1_CT, self.timeCount, self.xLeft_mm, '','t', 'r')
    # colorTrackingPlot(self.lbl2_CT, self.timeCount, self.spreadRateRight, '', 'o', 'b')
    # colorTrackingPlot(self.lbl2_CT, self.timeCount, self.spreadRateLeft, '','t', 'r')

def saveBtn(self):
    fileName = ft.QFileDialog.getSaveFileName(self, 'Save tracking data')
    fileName = fileName[0]
    if not fileName[-4:] == '.csv':
        fileName = fileName + '.csv'

    fileInfo = ['Name', self.fNameLbl.text(), 'Scale [px/mm]', self.scaleIn.text(), 'Color Tracking', 'Flame dir.:', self.directionBox.currentText(), 'Moving avg', self.movAvgIn_CT.text(), 'Points LE', self.avgLEIn_CT.text()]
    if self.refPoint != []:
        fileInfo = fileInfo + ['Ref. point (abs)', [self.refPoint[0], self.refPoint[1]]]
    fileInfo = fileInfo + ['Code version', str(self.FTversion)]

    lbl = ['File info', 'Frame', 'Time [s]', 'Right Edge [mm]', 'Left Edge [mm]', 'Length [mm]', 'Spread Rate RE [mm/s]', 'Spread Rate LE [mm/s]', 'Area [mm^2]']
    clms = [fileInfo, self.frameCount, self.timeCount, self.xRight_mm, self.xLeft_mm, self.flameLength_mm, self.spreadRateRight, self.spreadRateLeft, self.flameArea]
    clms_zip = ft.zip_longest(*clms)

    if fileName == '.csv': #this prevents name issues when the user closes the dialog without saving
        self.msgLabel.setText('Ops! The file name was not valid and the parameters were not saved.')
    else:
        try:
            with open(fileName, 'w', newline = '') as csvfile:
                writer = ft.csv.writer(csvfile, delimiter = ',')
                writer.writerow(lbl)
                for row in clms_zip:
                    writer.writerow(row)
            self.msgLabel.setText('Data succesfully saved.')
        except:
            self.msgLabel.setText('Ops! The values were not saved.')
            print('Unexpected error:', ft.sys.exc_info())

def showFrameLarge(self):
    ft.cv2.namedWindow(('Frame (RGB): ' + self.frameIn.text()), ft.cv2.WINDOW_AUTOSIZE)
    ft.cv2.imshow(('Frame (RGB): ' + self.frameIn.text()), self.currentFrameRGB_CT)
    ft.cv2.namedWindow(('Frame (black/white): ' + self.frameIn.text()), ft.cv2.WINDOW_AUTOSIZE)
    ft.cv2.imshow(('Frame (black/white): ' + self.frameIn.text()), self.currentFrameBW_CT)
    while True:
        if ft.cv2.waitKey(1) == 27: #ord('Esc')
            ft.cv2.destroyAllWindows()
            return

def lightROIBtn(self):
    frame, frameCrop = ft.checkEditing(self, self.frameNumber)
    self.lightROI_CT = ft.cv2.selectROI(frame)
    ft.cv2.destroyAllWindows()
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

def selectAxes(self, xAxis_lbl, yAxis_lbl):

    if xAxis_lbl == 'Time [s]':
        xPlot = self.timeCount
    elif xAxis_lbl == 'Frame #':
        xPlot = self.frameCount
    if yAxis_lbl == 'Position [mm]':
        yRight = self.xRight_mm
        yLeft = self.xLeft_mm
    if yAxis_lbl == 'Position [px]':
        yRight = self.xRight_px
        yLeft = self.xLeft_px
    elif yAxis_lbl == 'Flame length [mm]':
        yRight = self.flameLength_mm
        yLeft = 0
    elif yAxis_lbl == 'Spread rate [mm/s]':
        yRight = self.spreadRateRight
        yLeft = self.spreadRateLeft

    return(xPlot, yRight, yLeft)

def updateGraphsBtn(self):
    try:
        xAxis_lbl1 = self.xAxis_lbl1.currentText()
        yAxis_lbl1 = self.yAxis_lbl1.currentText()
        xAxis_lbl2 = self.xAxis_lbl2.currentText()
        yAxis_lbl2 = self.yAxis_lbl2.currentText()
        self.lbl1_CT.clear()
        self.lbl2_CT.clear()
        self.lbl1_CT.addLegend(offset = [1, 0.1])
        self.lbl2_CT.addLegend(offset = [1, 0.1])

        xPlot1, yRight1, yLeft1 = selectAxes(self, xAxis_lbl1, yAxis_lbl1)
        xPlot2, yRight2, yLeft2 = selectAxes(self, xAxis_lbl2, yAxis_lbl2)

        self.lbl1_CT.setLabel('left', str(yAxis_lbl1), color='black', size=14)
        self.lbl1_CT.setLabel('bottom', str(xAxis_lbl1), color='black', size=14)
        self.lbl2_CT.setLabel('left', str(yAxis_lbl2), color='black', size=14)
        self.lbl2_CT.setLabel('bottom', str(xAxis_lbl2), color='black', size=14)

        if yAxis_lbl1 == 'Flame length [mm]':
            colorTrackingPlot(self.lbl1_CT, xPlot1, yRight1, 'flame length', 'o', 'b')
        else:
            colorTrackingPlot(self.lbl1_CT, xPlot1, yRight1, 'right edge', 'o', 'b')
            colorTrackingPlot(self.lbl1_CT, xPlot1, yLeft1, 'left edge', 't', 'r')
        if yAxis_lbl2 == 'Flame length [mm]':
            colorTrackingPlot(self.lbl2_CT, xPlot2, yRight2, 'flame length', 'o', 'b')
        else:
            colorTrackingPlot(self.lbl2_CT, xPlot2, yRight2, 'right edge', 'o', 'b')
            colorTrackingPlot(self.lbl2_CT, xPlot2, yLeft2, 'left edge', 't', 'r')

        self.lbl1_CT.show()
        self.lbl2_CT.show()
    except:
        print('Unexpected error:', ft.sys.exc_info())
        self.msgLabel.setText('Error: the graphs could not be updated.')

def helpBtn(self):
    msg = ft.QMessageBox(self)
    msg.setText("""Color Tracking allows you to track a flame in an automatic way by considering the color intensity of each pixel in the ROI.

    The flame region is identified by isolating the pixels in the image/frame ROI with the minimum and maximum intensity for each RGB channel in the range specified with the sliders. The channel values vary between 0 and 255, and can be saved or loaded by clicking on the 'Save RGB values' and 'Load RGB values'. The resulting image is shown on the left window when the slider in the 'Preview box' is used, while the corresponding binary image is shown on the right. The left and right edges of the flame region are calculated as maximum and minimum locations of the binary image. '#px to locate edges' controls the number of pixels considered to calculate these locations.

    Small bright regions can be filtered out with the 'Filter particles' slider. The value of the slider indicates the area (in px^2) of the regions to remove from the image/frame, and you can change the maximum value by typing a number in the text box next to 'Filter particles'.

    If there is a flashing or strobe light in the recorded video, you can click on 'Pick bright region' to choose a rectangular region (in the same way that the ROI is selected) that is illuminated when the light is on and dark when it is off (this region is independent from the ROI specified in the 'Preview box'). The frames where the light is on can be discarded during the analysis by checking the 'Ignore flashing light' box.

    Flame position and spread rates are calculated automatically after clicking on 'Start Tracking' (the Flame Tracker interface will not be responsive during the analysis, but the progress can be monitored in the terminal window). The instantaneous spread rates are averaged with a moving average (with a number of points specified by the 'Moving avg points' text box. Note that this value is doubled for the calculation of the spread rate, i.e. 'Moving avg points' = 2 considers two points before and two points after an instantaneous value). The 'Flame direction' determines the positive increment of the flame location along the horizontal coordinate.

    By clicking on 'Absolute values', the x-axis of the tracked data will be shifted to the origin.

    Click on 'Save data' to export a csv file with all the tracking results (position of left and right edges, their spread rates and their distance variation in time, as well as the area of the flame region).

    If 'Video output' is checked, the filtered frames are exported as a new video, which could be used to visually check the tracking accuracy.

    """)
    if self.pyqtVer == '5':
        msg.exec_()
    elif self.pyqtVer == '6':
        msg.exec()
