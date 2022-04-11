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
# import cv2
# import pyqtgraph as pg
# import numpy as np
# import sys

# def initVars(self): # define initial variables
#     # global flameDir
#     # flameDir = 'toRight'

def getFilteredFrame(self, frame):
    # Transform the frame into the YCC space
    frameYCC = ft.cv2.cvtColor(frame, ft.cv2.COLOR_BGR2YCR_CB)
    Y, C, C = ft.cv2.split(frameYCC)

    # Isolate flame region with user specified threshold
    (thresh, frameBW) = ft.cv2.threshold(Y, int(self.thresholdIn.text()), 255, ft.cv2.THRESH_BINARY)

    # Find all the connected components (8 means in the four directions and diagonals)
    componentNum, componentLbl, stats, centroids = ft.cv2.connectedComponentsWithStats(frameBW, connectivity=8)
    ### 1 = number of labels; 2 = array; 3 = [[x location (left), y location (top), width, height, area]] for each label; 4 = [centroid of each label, x and y]. Note: the background is the first component

    # minimum area (measured in px) for filtering the components
    minArea = self.filterParticleSldr_LT.value()
    componentAreas = stats[:, 4] # stats is a list of lists, here we start from 0 (the background), and we consider the last elements (area)

    # keep only the components with area larger than minArea, starting from 1 to avoid the background
    for i in range(1, componentNum):
        if componentAreas[i] >= minArea:
            frameBW[componentLbl == i] = 255
        else:
            frameBW[componentLbl == i] = 0

    flamePx = ft.np.where(frameBW == [255])

    findFlameEdges(self, frameBW, flamePx)

    if self.showEdges_LT.isChecked() == True:
        ft.cv2.line(Y, (self.xMax, 0),(self.xMax, int(self.roiFourIn.text())), (255, 255, 255), 2)
        ft.cv2.line(Y, (self.xMin, 0),(self.xMin, int(self.roiFourIn.text())), (255, 255, 255), 2)

    self.currentFrameY_LT = Y
    # calculate the total number of bytes in the frame
    totalBytes = Y.nbytes
    # divide by the number of rows
    bytesPerLine = int(totalBytes/Y.shape[0]) #I had to introduce it to avoid distortion in the opened file for some of the videos
    if self.pyqtVer == '5':
        self.frameY = ft.QImage(Y.data, Y.shape[1], Y.shape[0], bytesPerLine, ft.QImage.Format_Grayscale8) #shape[0] = height, [1] = width
        self.frameY = self.frameY.scaled(self.lbl1_LT.size(), ft.Qt.KeepAspectRatio, ft.Qt.SmoothTransformation)
    elif self.pyqtVer == '6':
        self.frameY = ft.QImage(Y.data, Y.shape[1], Y.shape[0], bytesPerLine, ft.QImage.Format.Format_Grayscale8) #shape[0] = height, [1] = width
        self.frameY = self.frameY.scaled(self.lbl1_LT.size(), ft.Qt.AspectRatioMode.KeepAspectRatio, ft.Qt.TransformationMode.SmoothTransformation)

def findFlameEdges(self, frameBW, flamePx):
    self.flameArea = len(flamePx[0])
    self.xMax = 0
    self.xMin = 0
    self.xRight = 0
    self.xLeft = 0
    i = 0
    sortedBWx = sorted(flamePx[1])
    try:
        # average of the flame location based on the n. of points indicated by the user
        for x in range(int(self.avgLEIn_LT.text())):
            i = i + 1
            self.xMax = self.xMax + sortedBWx[-i]
            self.xMin = self.xMin + sortedBWx[i]
    except:
        pass

    self.xMax = int(self.xMax/int(self.avgLEIn_LT.text()))
    self.xMin = int(self.xMin/int(self.avgLEIn_LT.text()))

    # if flameDir == 'toRight':
    if self.directionBox.currentText() == 'Left to right':
        self.xRight = int(self.roiOneIn.text()) + self.xMax
        self.xLeft = int(self.roiOneIn.text()) + self.xMin
    elif self.directionBox.currentText() == 'Right to left':
    # elif flameDir == 'toLeft':
        self.xRight = self.vWidth - int(self.roiOneIn.text()) - self.xMax
        self.xLeft = self.vWidth - int(self.roiOneIn.text()) - self.xMin

    if self.showEdges_LT.isChecked() == True:
        ft.cv2.line(frameBW, (self.xMax, 0),(self.xMax, int(self.roiFourIn.text())), (255, 255, 255), 2)
        ft.cv2.line(frameBW, (self.xMin, 0),(self.xMin, int(self.roiFourIn.text())), (255, 255, 255), 2)

    self.currentFrameBW_LT = frameBW
    totalBytes = frameBW.nbytes
    bytesPerLine = int(totalBytes/frameBW.shape[0])
    if self.pyqtVer == '5':
        self.frameBW = ft.QImage(frameBW.data, frameBW.shape[1], frameBW.shape[0], bytesPerLine, ft.QImage.Format_Grayscale8)
        self.frameBW = self.frameBW.scaled(self.lbl2_LT.size(), ft.Qt.KeepAspectRatio, ft.Qt.SmoothTransformation)
    elif self.pyqtVer == '6':
        self.frameBW = ft.QImage(frameBW.data, frameBW.shape[1], frameBW.shape[0], bytesPerLine, ft.QImage.Format.Format_Grayscale8)
        self.frameBW = self.frameBW.scaled(self.lbl2_LT.size(), ft.Qt.AspectRatioMode.KeepAspectRatio, ft.Qt.TransformationMode.SmoothTransformation)

def lumaTracking(self):
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
    iCount = 0
    flameArea = list()

    if self.exportEdges_LT.isChecked():
        #fps = (float(self.vFpsLbl.text()))/(int(self.skipFrameIn.text()) + 1) #fps(new) = fps(original)/(skipframes + 1)
        fps = float(self.fpsIn.text())
        codec = str(self.codecIn.text())
        vFormat = str(self.formatIn.text())
        vName = self.fPath + '-YVideo.' + str(vFormat) # alternative: 'output.{}'.format(vFormat); self.fNameLbl.text() +
        fourcc = ft.cv2.VideoWriter_fourcc(*codec)
        size = (int(self.roiThreeIn.text()), int(self.roiFourIn.text()))
        # open and set properties
        vout = ft.cv2.VideoWriter()
        vout.open(vName, fourcc, fps, size, 0)

    if scale: #this condition prevents crashes in case the scale is not specified
        xAxis_lbl1 = self.xAxis_lbl1.currentText()
        yAxis_lbl1 = self.yAxis_lbl1.currentText()
        xAxis_lbl2 = self.xAxis_lbl2.currentText()
        yAxis_lbl2 = self.yAxis_lbl2.currentText()
        while (currentFrame < lastFrame):
            # print('Frame #:', currentFrame,  end='\r')
            frame, frameCrop = ft.checkEditing(self, currentFrame)
            if self.filterLight.isChecked() == True:
                if self.lightROI_LT_recorded == True:
                    # looking for frames with a light on (which would increase the red and green channel values of the background)
                    # low and high are the thresholds for each color channel
                    low = ([5, 5, 10]) # blueLow, greenLow, redLow
                    high = ([255, 255, 255]) # blueHigh, greenHigh, redHigh
                    low = ft.np.array(low, dtype = 'uint8') #this conversion is necessary
                    high = ft.np.array(high, dtype = 'uint8')
                    currentLightROI = frame[self.lightROI_LT[1] : (self.lightROI_LT[1] + self.lightROI_LT[3]), self.lightROI_LT[0] : (self.lightROI_LT[0] + self.lightROI_LT[2])]
                    newMask = ft.cv2.inRange(currentLightROI, low, high)
                    frame_light = ft.cv2.bitwise_and(currentLightROI, currentLightROI, mask = newMask)
                    grayFrame_light = ft.cv2.cvtColor(frame_light, ft.cv2.COLOR_BGR2GRAY)
                    (thresh_light, frameBW_light) = ft.cv2.threshold(grayFrame_light, 0, 255, ft.cv2.THRESH_BINARY)
                    flamePx_light = ft.np.where(frameBW_light == [255])
                    area_light = int(self.lightROI_LT[3] * self.lightROI_LT[2])
                else:
                    msg = ft.QMessageBox(self)
                    msg.setText('Before the tracking, please click on "Pick a bright region" to select a region where the light is visible.')
                    if self.pyqtVer == '5':
                        msg.exec_()
                    elif self.pyqtVer == '6':
                        msg.exec()
                    break

                if len(flamePx_light[0]) < 0.5 * area_light:
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
            if self.exportEdges_LT.isChecked():
                vout.write(self.currentFrameY_LT)
            # print('Frame #:', currentFrame,  end='\r')
            print('Progress: ', round((currentFrame - firstFrame)/(lastFrame - firstFrame) * 10000)/100, '%', '(Frame #: ', currentFrame, ')', end='\r')
            currentFrame = currentFrame + 1 + int(self.skipFrameIn.text())

        print('Progress: 100 % - Tracking completed')
        self.msgLabel.setText('Tracking completed')
        if self.exportEdges_LT.isChecked():
            vout.release()
            self.msgLabel.setText('Tracking completed and Y channel video created.')

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

        movAvgPt = int(self.movAvgIn_LT.text()) #this number is half of the interval considered for the spread rate (movAvgPt = 2 means I am considering a total of 5 points (my point, 2 before and 2 after))
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

        self.xRight_mm = ft.np.round(self.xRight_mm, 3)
        self.xRight_mm = self.xRight_mm.tolist()
        self.xLeft_mm = ft.np.round(self.xLeft_mm, 3)
        self.xLeft_mm = self.xLeft_mm.tolist()
        self.spreadRateRight = ft.np.round(self.spreadRateRight, 3)
        self.spreadRateRight = self.spreadRateRight.tolist()
        self.spreadRateLeft = ft.np.round(self.spreadRateLeft, 3)
        self.spreadRateLeft = self.spreadRateLeft.tolist()

        # self.lbl1_LT = ft.pg.PlotWidget(self.lumaTrackingBox)
        # self.lbl2_LT = ft.pg.PlotWidget(self.lumaTrackingBox)
        self.lbl1_LT.deleteLater()
        self.lbl2_LT.deleteLater()
        self.lbl1_LT = ft.pg.PlotWidget()
        self.lbl2_LT = ft.pg.PlotWidget()

        # if ft.sys.platform == 'darwin':
        #     # lbl1 = [190, 25, 420, 300]
        #     # lbl2 = [620, 25, 420, 300]
        #     lbl1 = [250, 25, 390, 270]
        #     lbl2 = [650, 25, 390, 270]
        # elif ft.sys.platform == 'win32':
        #     # lbl1 = [190, 15, 420, 300]
        #     # lbl2 = [620, 15, 420, 300]
        #     lbl1 = [250, 15, 390, 270]
        #     lbl2 = [650, 15, 390, 270]
        # elif ft.sys.platform == 'linux':
        #     # lbl1 = [190, 25, 420, 300]
        #     # lbl2 = [620, 25, 420, 300]
        #     lbl1 = [250, 25, 390, 270]
        #     lbl2 = [650, 25, 390, 270]
        #
        # self.lbl1_LT.setGeometry(lbl1[0], lbl1[1], lbl1[2], lbl1[3])
        # self.lbl2_LT.setGeometry(lbl2[0], lbl2[1], lbl2[2], lbl2[3])
        self.box_layout.addWidget(self.lbl1_LT, 0, 3, 8, 4)
        self.box_layout.addWidget(self.lbl2_LT, 0, 8, 8, 4)
        self.lbl1_LT.setBackground('w')
        # self.lbl1_LT.setLabel('left', 'Position [mm]', color='black', size=14)
        self.lbl1_LT.setLabel('left', str(yAxis_lbl1), color='black', size=14)
        self.lbl1_LT.setLabel('bottom', str(xAxis_lbl1), color='black', size=14)
        self.lbl1_LT.getAxis('bottom').setPen(color=(0, 0, 0))
        self.lbl1_LT.getAxis('left').setPen(color=(0, 0, 0))
        self.lbl1_LT.addLegend(offset = [1, 0.1]) # background color modified in line 122 and 123 of Versions/3.7/lib/python3.7/site-packages/pyqtgraph/graphicsItems
        self.lbl2_LT.setBackground('w')
        # self.lbl2_LT.setLabel('left', 'Spread Rate [mm/s]', color='black', size=14)
        # self.lbl2_LT.setLabel('bottom', 'Time [s]', color='black', size=14)
        self.lbl2_LT.setLabel('left', str(yAxis_lbl2), color='black', size=14)
        self.lbl2_LT.setLabel('bottom', str(xAxis_lbl2), color='black', size=14)
        self.lbl2_LT.getAxis('bottom').setPen(color=(0, 0, 0))
        self.lbl2_LT.getAxis('left').setPen(color=(0, 0, 0))
        self.lbl2_LT.addLegend(offset = [1, 0.1]) # background color modified in line 122 and 123 of Versions/3.7/lib/python3.7/site-packages/pyqtgraph/graphicsItems

        xPlot1, yRight1, yLeft1 = selectAxes(self, xAxis_lbl1, yAxis_lbl1)
        xPlot2, yRight2, yLeft2 = selectAxes(self, xAxis_lbl2, yAxis_lbl2)

        if yAxis_lbl1 == 'Flame length [mm]':
            lumaTrackingPlot(self.lbl1_LT, xPlot1, yRight1, 'flame length', 'o', 'b')
        else:
            lumaTrackingPlot(self.lbl1_LT, xPlot1, yRight1, 'right edge', 'o', 'b')
            lumaTrackingPlot(self.lbl1_LT, xPlot1, yLeft1, 'left edge', 't', 'r')

        if yAxis_lbl2 == 'Flame length [mm]':
            lumaTrackingPlot(self.lbl2_LT, xPlot2, yRight2, 'flame length', 'o', 'b')
        else:
            lumaTrackingPlot(self.lbl2_LT, xPlot2, yRight2, 'right edge', 'o', 'b')
            lumaTrackingPlot(self.lbl2_LT, xPlot2, yLeft2, 'left edge', 't', 'r')

        # lumaTrackingPlot(self.lbl1_LT, self.timeCount, self.xRight_mm, 'right edge', 'o', 'b')
        # lumaTrackingPlot(self.lbl1_LT, self.timeCount, self.xLeft_mm, 'left edge', 't', 'r')
        # lumaTrackingPlot(self.lbl2_LT, self.timeCount, self.spreadRateRight, 'right edge', 'o', 'b')
        # lumaTrackingPlot(self.lbl2_LT, self.timeCount, self.spreadRateLeft, 'left edge', 't', 'r')

        self.lbl1_LT.show()
        self.lbl2_LT.show()

def lumaTrackingPlot(label, x, y, name, symbol, color):
    pen = ft.pg.mkPen(color)
    label.plot(x, y, pen = pen, name = name, symbol = symbol, symbolSize = 7, symbolBrush = (color))

# def chooseFlameDirection(self, text):
#     global flameDir
#     selection = self.directionBox.currentText()
#     if selection == 'Left to right':
#         flameDir = 'toRight'
#     elif selection == 'Right to left':
#         flameDir = 'toLeft'

def saveData(self):
    fileName = ft.QFileDialog.getSaveFileName(self, 'Save tracking data')
    fileName = fileName[0]
    if not fileName[-4:] == '.csv':
        fileName = fileName + '.csv'

    fileInfo = ['Name', self.fNameLbl.text(), 'Scale [px/mm]', self.scaleIn.text(), 'Luma Tracking', 'Flame dir.:', self.directionBox.currentText(), 'Luma threshold', self.thresholdIn.text(), 'Min. particle [px]', str(self.filterParticleSldr_LT.value()),'Points LE', self.avgLEIn_LT.text(), 'Moving avg', self.movAvgIn_LT.text()]
    if self.refPoint != []:
        fileInfo = fileInfo + ['Ref. point (abs)', [self.refPoint[0], self.refPoint[1]]]
    fileInfo = fileInfo + ['Code version', str(self.FTversion)]

    lbl = ['File info', 'Frame', 'Time [s]', 'Right edge [mm]', 'Left edge [mm]', 'Length [mm]', 'Spread Rate RE [mm/s]', 'Spread Rate LE [mm/s]', 'Area [mm^2]']
    clms = [fileInfo, self.frameCount, self.timeCount, self.xRight_mm, self.xLeft_mm, self.flameLength_mm, self.spreadRateRight, self.spreadRateLeft, self.flameArea]
    clms_zip = ft.zip_longest(*clms)

    with open(fileName, 'w', newline = '') as csvfile:
        writer = ft.csv.writer(csvfile, delimiter = ',')
        writer.writerow(lbl)
        for row in clms_zip:
            writer.writerow(row)
    self.msgLabel.setText('Data succesfully saved.')

def absValue(self):
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

    self.lbl1_LT.clear()
    self.lbl2_LT.clear()

    xPlot1, yRight1, yLeft1 = selectAxes(self, xAxis_lbl1, yAxis_lbl1)
    xPlot2, yRight2, yLeft2 = selectAxes(self, xAxis_lbl2, yAxis_lbl2)

    if yAxis_lbl1 == 'Flame length [mm]':
        lumaTrackingPlot(self.lbl1_LT, xPlot1, yRight1, 'flame length', 'o', 'b')
    else:
        lumaTrackingPlot(self.lbl1_LT, xPlot1, yRight1, 'right edge', 'o', 'b')
        lumaTrackingPlot(self.lbl1_LT, xPlot1, yLeft1, 'left edge', 't', 'r')
    if yAxis_lbl2 == 'Flame length [mm]':
        lumaTrackingPlot(self.lbl2_LT, xPlot2, yRight2, 'flame length', 'o', 'b')
    else:
        lumaTrackingPlot(self.lbl2_LT, xPlot2, yRight2, 'right edge', 'o', 'b')
        lumaTrackingPlot(self.lbl2_LT, xPlot2, yLeft2, 'left edge', 't', 'r')

    # lumaTrackingPlot(self.lbl1_LT, self.timeCount, self.xRight_mm, '', 'o', 'b')
    # lumaTrackingPlot(self.lbl1_LT, self.timeCount, self.xLeft_mm, '','t', 'r')
    # lumaTrackingPlot(self.lbl2_LT, self.timeCount, self.spreadRateRight, '', 'o', 'b')
    # lumaTrackingPlot(self.lbl2_LT, self.timeCount, self.spreadRateLeft, '', 't', 'r')

def filterParticleSldr(self):
    frame, frameCrop = ft.checkEditing(self, self.frameNumber)
    getFilteredFrame(self, frameCrop)
    self.lbl1_LT.setPixmap(ft.QPixmap.fromImage(self.frameY))
    self.lbl2_LT.setPixmap(ft.QPixmap.fromImage(self.frameBW))
    self.filterParticleSldr_LT.setMaximum(int(self.particleSldrMax.text()))

def showFrameLarge(self):
    ft.cv2.namedWindow(('Frame (luminance): ' + self.frameIn.text()), ft.cv2.WINDOW_AUTOSIZE)
    ft.cv2.imshow(('Frame (luminance): ' + self.frameIn.text()), self.currentFrameY_LT)
    ft.cv2.namedWindow(('Frame (black/white): ' + self.frameIn.text()), ft.cv2.WINDOW_AUTOSIZE)
    ft.cv2.imshow(('Frame (black/white): ' + self.frameIn.text()), self.currentFrameBW_LT)
    while True:
        if ft.cv2.waitKey(1) == 27: #ord('Esc')
            ft.cv2.destroyAllWindows()
            return

def lightROIBtn(self):
    frame, frameCrop = ft.checkEditing(self, self.frameNumber)
    self.lightROI_LT = ft.cv2.selectROI(frame)
    ft.cv2.destroyAllWindows()
    self.lightROI_LT_recorded = True

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
        self.lbl1_LT.clear()
        self.lbl2_LT.clear()
        self.lbl1_LT.addLegend(offset = [1, 0.1])
        self.lbl2_LT.addLegend(offset = [1, 0.1])

        xPlot1, yRight1, yLeft1 = selectAxes(self, xAxis_lbl1, yAxis_lbl1)
        xPlot2, yRight2, yLeft2 = selectAxes(self, xAxis_lbl2, yAxis_lbl2)

        self.lbl1_LT.setLabel('left', str(yAxis_lbl1), color='black', size=14)
        self.lbl1_LT.setLabel('bottom', str(xAxis_lbl1), color='black', size=14)
        self.lbl2_LT.setLabel('left', str(yAxis_lbl2), color='black', size=14)
        self.lbl2_LT.setLabel('bottom', str(xAxis_lbl2), color='black', size=14)

        if yAxis_lbl1 == 'Flame length [mm]':
            lumaTrackingPlot(self.lbl1_LT, xPlot1, yRight1, 'flame length', 'o', 'b')
        else:
            lumaTrackingPlot(self.lbl1_LT, xPlot1, yRight1, 'right edge', 'o', 'b')
            lumaTrackingPlot(self.lbl1_LT, xPlot1, yLeft1, 'left edge', 't', 'r')
        if yAxis_lbl2 == 'Flame length [mm]':
            lumaTrackingPlot(self.lbl2_LT, xPlot2, yRight2, 'flame length', 'o', 'b')
        else:
            lumaTrackingPlot(self.lbl2_LT, xPlot2, yRight2, 'right edge', 'o', 'b')
            lumaTrackingPlot(self.lbl2_LT, xPlot2, yLeft2, 'left edge', 't', 'r')

        self.lbl1_LT.show()
        self.lbl2_LT.show()
    except:
        print('Unexpected error:', ft.sys.exc_info())
        self.msgLabel.setText('Error: the graphs could not be updated.')

def helpBtn(self):
    msg = ft.QMessageBox(self)
    msg.setText("""Luma Tracking allows you to track a flame in an automatic way by considering the luminance intensity of each pixel in the ROI.

    The frames considered are transformed from the RGB to the YCC color space. Only the Y (luma intensity) component is considered, and the flame is isolated from the background by adjusting the 'Luma threshold' value (from 0 to 255).

    The resulting Y channel image is shown on the left window when the slider in the 'Preview box' is used, while the corresponding binary image is shown on the right. The left and right edges of the flame region are calculated as maximum and minimum locations of the binary image. '#px to locate edges' controls the number of pixels considered to calculate these locations.

    Small bright regions can be filtered out with the 'Filter particles' slider. The value of the slider indicates the area (in px^2) of the regions to remove from the image/frame, and you can change the maximum value by typing a number in the text box next to 'Filter particles'.

    If there is a flashing or strobe light in the recorded video, you can click on 'Pick bright region' to choose a rectangular region (in the same way that the ROI is selected) that is illuminated when the light is on and dark when it is off (this region is independent from the ROI specified in the 'Preview box'). The frames where the light is on can be discarded during the analysis by checking the 'Ignore flashing light' box.

    Flame position and spread rates are calculated automatically after clicking on 'Start Tracking' (the Flame Tracker interface will not be responsive during the analysis, but the progress can be monitored in the terminal window). The instantaneous spread rates are averaged with a moving average (with a number of points specified by the 'Moving avg points' text box. Note that this value is doubled for the calculation of the spread rate, i.e. 'Moving avg points' = 2 considers two points before and two points after an instantaneous value). The 'Flame direction' determines the positive increment of the flame location along the horizontal coordinate.

    By clicking on 'Absolute values', the x-axis of the tracked data will be shifted to the origin.

    Click on 'Save data' to export a csv file with all the tracking results (position of left and right edges, their spread rates and their distance variation in time, as well as the area of the flame region).

    If 'Video output' is checked, the frames converted to the Y channel are exported as a new video, which could be used to visually check the tracking accuracy.

    """)
    if self.pyqtVer == '5':
        msg.exec_()
    elif self.pyqtVer == '6':
        msg.exec()
