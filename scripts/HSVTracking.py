"""
Flame Tracker. This program is designed to track flames or bright objects in videos or images.
Copyright (C) 2021, 2022 Charles Scudiere; 2021, 2022  Luca Carmignani

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

Author: Charles Scudiere, PhD (adapted from colorTracking.py)
Collaborator/Contributor: Luca Carmignani, PhD
Contact: flameTrackerContact@gmail.com

Comments:
Note on implementation of HSL and HSV:
Hue, the angular dimension, starting at the red primary at 0°, passing through the green primary at 120° and the blue primary at 240°, and then wrapping back to red at 360°

OpenCV Implementation: RGB to HSV
In case of 8-bit and 16-bit images, R, G, and B are converted to the floating-point format and scaled to fit the 0 to 1 range.

If H<0 then H <- +360 . On output 0≤V≤1, 0≤S≤1, 0≤H≤360 .

The values are then converted to the destination data type:

    8-bit images: V <- 255V, S <- 255S,H <- H/2(to fit to 0 to 255)
    16-bit images: (currently not supported) V < -65535V, S < 65535S, H <− H
    32-bit images: H, S, and V are left as is
"""

# from PyQt5 import QtGui
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from itertools import zip_longest

import flameTracker as ft
import boxesGUI_OS as gui
# import csv
# import cv2
# import pyqtgraph as pg
# import numpy as np
# import sys

def initVars(self): # define initial variables
    # global flameDir
    # flameDir = 'toRight'
    # Add time/frame plotting toggle - CAS
    # self.isPlotTimevsFrame = False #True
    # self.connectivity_HT = 4
    self.lightROI_HT_recorded = False

def getFilteredFrame(self, frame):
    # Filter here: #CAS Modified for HSV tracking instead of color tracking
    valLow = self.valMinSlider.value()
    valHigh = self.valMaxSlider.value()
    satLow = self.satMinSlider.value()
    satHigh = self.satMaxSlider.value()
    hueLow = self.hueMinSlider.value()
    hueHigh = self.hueMaxSlider.value()
    low = ([hueLow, satLow, valLow])
    high = ([hueHigh, satHigh, valHigh])
    low = ft.np.array(low, dtype = 'uint8') #this conversion is necessary
    high = ft.np.array(high, dtype = 'uint8')
    newMask = ft.cv2.inRange(ft.cv2.cvtColor(frame, ft.cv2.COLOR_BGR2HSV), low, high)
    frame = ft.cv2.bitwise_and(frame, frame, mask = newMask)
    grayFrame = ft.cv2.cvtColor(frame, ft.cv2.COLOR_BGR2GRAY)
    (threshold, frameBW) = ft.cv2.threshold(grayFrame, 0, 255, ft.cv2.THRESH_BINARY)

    # Find all the connected components (8 means in the four directions and diagonals)
    componentNum, componentLbl, stats, centroids = ft.cv2.connectedComponentsWithStats(frameBW, connectivity = int(self.connectivityBox.currentText())) # self.connectivity_HT)
    ### 1 = number of labels; 2 = array; 3 = [[x location (left), y location (top), width, height, area]] for each label; 4 = [centroid of each label, x and y]. Note: the background is the first component

    # minimum area (measured in px) for filtering the components
    minArea = self.filterParticleSldr_HT.value()
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

    self.currentFrameRGB_HT = frame
    # calculate the total number of bytes in the frame for lbl1
    totalBytes = frame.nbytes
    # divide by the number of rows
    bytesPerLine = int(totalBytes/frame.shape[0]) #I had to introduce it to avoid distortion in the opened file for some of the videos
    if self.pyqtVer == '5':
        self.frame = ft.QImage(frame.data, frame.shape[1], frame.shape[0], bytesPerLine, ft.QImage.Format_BGR888)#.rgbSwapped() #shape[0] = height, [1] = width QImage.Format_Indexed8 BGR888
        self.frame = self.frame.scaled(self.lbl1_HT.size(), ft.Qt.KeepAspectRatio, ft.Qt.SmoothTransformation)
    elif self.pyqtVer == '6':
        self.frame = ft.QImage(frame.data, frame.shape[1], frame.shape[0], bytesPerLine, ft.QImage.Format.Format_BGR888)#.rgbSwapped() #shape[0] = height, [1] = width QImage.Format_Indexed8 BGR888
        self.frame = self.frame.scaled(self.lbl1_HT.size(), ft.Qt.AspectRatioMode.KeepAspectRatio, ft.Qt.TransformationMode.SmoothTransformation)

    self.currentFrameBW_HT = frameBW
    # calculate the total number of bytes in the frame for lbl2
    totalBytesBW = frameBW.nbytes
    # divide by the number of rows
    bytesPerLineBW = int(totalBytesBW/frameBW.shape[0]) #I had to introduce it to avoid distortion in the opened file for some of the videos
    if self.pyqtVer == '5':
        self.frameBW = ft.QImage(frameBW.data, frameBW.shape[1], frameBW.shape[0], bytesPerLineBW, ft.QImage.Format_Grayscale8)#.rgbSwapped() #shape[0] = height, [1] = width QImage.Format_Indexed8 or Grayscale8 BGR888
        self.frameBW = self.frameBW.scaled(self.lbl1_HT.size(), ft.Qt.KeepAspectRatio, ft.Qt.SmoothTransformation)
    elif self.pyqtVer == '6':
        self.frameBW = ft.QImage(frameBW.data, frameBW.shape[1], frameBW.shape[0], bytesPerLineBW, ft.QImage.Format.Format_Grayscale8)#.rgbSwapped() #shape[0] = height, [1] = width QImage.Format_Indexed8 or Grayscale8 BGR888
        self.frameBW = self.frameBW.scaled(self.lbl1_HT.size(), ft.Qt.AspectRatioMode.KeepAspectRatio, ft.Qt.TransformationMode.SmoothTransformation)

def findFlameEdges(self, frameBW, flamePx):
    # global flameDir
    self.flameArea = len(flamePx[0])
    self.xMax = 0
    self.xMin = 0
    self.xRight = 0
    self.xLeft = 0
    sortedBWx = sorted(flamePx[1])
    i = 0
    try:
        # average of the flame location based on the n# of points indicated by the user
        for x in range(int(self.avgLEIn_HT.text())):
            i = i + 1
            self.xMax = self.xMax + sortedBWx[-i]
            self.xMin = self.xMin + sortedBWx[i]

        self.xMax = int(self.xMax/int(self.avgLEIn_HT.text()))
        self.xMin = int(self.xMin/int(self.avgLEIn_HT.text()))

        #     if flameDir == 'toRight'::
        if self.directionBox.currentText() == 'Left to right':
            self.xRight = int(self.roiOneIn.text()) + self.xMax
            self.xLeft = int(self.roiOneIn.text()) + self.xMin
        elif self.directionBox.currentText() == 'Right to left':
            # elif flameDir == 'toLeft':
            self.xRight = self.vWidth - int(self.roiOneIn.text()) - self.xMax
            self.xLeft = self.vWidth - int(self.roiOneIn.text()) - self.xMin
    except:
        self.msgLabel.setText('Flame not found in some frames')

def HSVTracking(self):
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

    if self.exportEdges_HT.isChecked() or self.exportTrackOverlay_HT.isChecked():
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

            if self.filterLight_HT.isChecked() == True:
                if self.lightROI_HT_recorded == True:
                    # looking for frames with a light on (which would increase the red and green channel values of the background)
                    low = ([5, 5, 10]) # blueLow, greenLow, redLow (see color tracking)
                    high = ([255, 255, 255]) # blueHigh, greenHigh, redHigh
                    low = ft.np.array(low, dtype = 'uint8') #this conversion is necessary
                    high = ft.np.array(high, dtype = 'uint8')
                    currentLightROI = frame[self.lightROI_HT[1] : (self.lightROI_HT[1] + self.lightROI_HT[3]), self.lightROI_HT[0] : (self.lightROI_HT[0] + self.lightROI_HT[2])]
                    newMask = ft.cv2.inRange(currentLightROI, low, high)
                    frame_light = ft.cv2.bitwise_and(currentLightROI, currentLightROI, mask = newMask)
                    grayFrame_light = ft.cv2.cvtColor(frame_light, ft.cv2.COLOR_BGR2GRAY)
                    (thresh_light, frameBW_light) = ft.cv2.threshold(grayFrame_light, 0, 255, ft.cv2.THRESH_BINARY)
                    flamePx_light = ft.np.where(frameBW_light == [255]) #beta
                    area_lightROI = int(self.lightROI_HT[3] * self.lightROI_HT[2])
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
                    print('frame counted')
                else:
                    currentFrame = currentFrame + 1 + int(self.skipFrameIn.text())
                    print('frame not counted')
                    continue
            else:
                getFilteredFrame(self, frameCrop)

            self.xRight_px.append(self.xRight)
            self.xLeft_px.append(self.xLeft)
            self.xRight_mm.append(self.xRight / float(self.scaleIn.text()))
            self.xLeft_mm.append(self.xLeft / float(self.scaleIn.text()))
            flameArea.append(self.flameArea)
            self.frameCount.append(currentFrame)
            if self.exportEdges_HT.isChecked() and not self.exportTrackOverlay_HT.isChecked():
                vout.write(self.currentFrameRGB_HT)
            elif self.exportTrackOverlay_HT.isChecked():
                #CAS Add Track lines over cropped video
                trackframe = ft.np.copy(frameCrop) # frame is 1080 x 1920
                trackframe[:, min(self.xRight-1 - int(self.roiOneIn.text()), ft.np.size(trackframe,1))] = 255 # white out line to mark where tracked flame, using relative distance
                vout.write(trackframe)

            # print('Progress: ', round((currentFrame - firstFrame)/(lastFrame - firstFrame) * 10000)/100, '%')
            print('Progress: ', round((currentFrame - firstFrame)/(lastFrame - firstFrame) * 10000)/100, '%', '(Frame #: ', currentFrame, ')', end='\r')
            currentFrame = currentFrame + 1 + int(self.skipFrameIn.text())

        try:
            self.flameArea = [areaN / (float(self.scaleIn.text())**2) for areaN in flameArea]
            self.flameArea = ft.np.round(self.flameArea, 3)
            self.flameArea = self.flameArea.tolist()
            self.timeCount = [frameN / float(self.vFpsLbl.text()) for frameN in self.frameCount]
        except:
            pass

            # CAS Add tracking line from flameTracker.py
            #if self.HSVTrackingValue == True:
            #    # Start tracking for export
            #    #HSVTracking(self)
            #    # #findFlameEdges_HT(self, frameBW, flamePx)
            #    getHSVFilteredFrame(self, currentFrame)
            #    trackframe = frameCrop # frame is 1080 x 1920
            #    import numpy
            #    #print(type(frame), numpy.size(frame, 0), 'x', numpy.size(frame, 1))
            #    #print(type(frameCrop), numpy.size(frameCrop, 0), 'x', numpy.size(frameCrop, 1))
            #    trackframe[:, min(self.xRight-1 - int(self.roiOneIn.text()), numpy.size(trackframe,1))] = 255 # white out line to mark where tracked flame, using relative distance
            #    #if self.xRight-1 > numpy.size(trackframe,1):
            #    #    print('xRight would have errored here with value:', self.xRight)
            #    #cv2.imshow('Frame_With_255_TrackLine', trackframe)


        for i in range(len(self.xRight_mm)):
            flameLength_mm.append(abs(self.xRight_mm[i] - self.xLeft_mm[i]))

        flameLength_mm = ft.np.round(flameLength_mm, 2)
        self.flameLength_mm = flameLength_mm.tolist()
        print('Progress: 100 % - Tracking completed')
        self.msgLabel.setText('Tracking completed')

        if self.exportEdges_HT.isChecked() or self.exportTrackOverlay_HT.isChecked():
            vout.release()
            self.msgLabel.setText('Tracking completed and video created.')

        # the following approach to calculate the spread rate is the same one used for lumaTracking
        movAvgPt = int(self.movAvgIn_HT.text()) #this number is half of the interval considered for the spread rate (movAvgPt = 2 means I am considering a total of 5 points (my point, 2 before and 2 after))
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

        self.lbl1_HT = ft.pg.PlotWidget(self.HSVTrackingBox)
        if ft.sys.platform == 'darwin' or ft.sys.platform == 'linux':
            lbl1 = [370,  25, 670, 125]
            lbl2 = [370, 150, 670, 125]
        elif ft.sys.platform == 'win32':
            lbl1 = [370,  15, 670, 125]
            lbl2 = [370, 150, 670, 125]

        self.lbl1_HT.setGeometry(lbl1[0], lbl1[1], lbl1[2], lbl1[3]) # Changed geometry as removed BW image display
        self.lbl1_HT.setBackground('w')
        # self.lbl1_HT.setLabel('left', 'Position [mm]', color='black', size=14)
        self.lbl1_HT.setLabel('left', str(yAxis_lbl1), color='black', size=14)
        self.lbl1_HT.setLabel('bottom', str(xAxis_lbl1), color='black', size=14)
        # if self.isPlotTimevsFrame:
        #     ## Plot in terms of time
        #     self.lbl1_HT.setLabel('bottom', 'Time [s]', color='black', size=14)
        # else:
        #     ## CAS Plot in terms of frame:
        #     self.lbl1_HT.setLabel('bottom', 'Frame', color='black', size=14)

        self.lbl1_HT.getAxis('bottom').setPen(color=(0, 0, 0))
        self.lbl1_HT.getAxis('left').setPen(color=(0, 0, 0))
        self.lbl1_HT.addLegend(offset = [1, 0.1]) # background color modified in line 122 and 123 of Versions/3.7/lib/python3.7/site-packages/pyqtgraph/graphicsItems
        self.lbl2_HT = ft.pg.PlotWidget(self.HSVTrackingBox)
        self.lbl2_HT.setGeometry(lbl2[0], lbl2[1], lbl2[2], lbl2[3])
        #print('\nView rect=', self.lbl2_HT.viewRect() )
        #print('\nGeometry set to', self.lbl2_HT.viewGeometry())
        self.lbl2_HT.setBackground('w')
        # self.lbl2_HT.setLabel('left', 'Spread Rate [mm/s]', color='black', size=14)
        self.lbl2_HT.setLabel('left', str(yAxis_lbl2), color='black', size=14)
        self.lbl2_HT.setLabel('bottom', str(xAxis_lbl2), color='black', size=14)
        # if self.isPlotTimevsFrame:
        #     ## Plot in terms of time
        #     self.lbl2_HT.setLabel('bottom', 'Time [s]', color='black', size=14)
        # else:
        #     ## CAS Plot in terms of frame:
        #     self.lbl2_HT.setLabel('bottom', 'Frame', color='black', size=14)

        self.lbl2_HT.getAxis('bottom').setPen(color=(0, 0, 0))
        self.lbl2_HT.getAxis('left').setPen(color=(0, 0, 0))
        self.lbl2_HT.addLegend(offset = [1, 0.1]) # background color modified in line 122 and 123 of Versions/3.7/lib/python3.7/site-packages/pyqtgraph/graphicsItems

        # if self.isPlotTimevsFrame:
        #     ## Plot in terms of time
        #     HSVTrackingPlot(self.lbl1_HT, self.timeCount, self.xRight_mm, 'right edge', 'o', 'b')
        #     HSVTrackingPlot(self.lbl1_HT, self.timeCount, self.xLeft_mm, 'left edge', 't', 'r')
        #     HSVTrackingPlot(self.lbl2_HT, self.timeCount, self.spreadRateRight, 'right edge', 'o', 'b')
        #     HSVTrackingPlot(self.lbl2_HT, self.timeCount, self.spreadRateLeft, 'left edge', 't', 'r')
        # else:
        #     ## CAS Plot in terms of frame:
        #     HSVTrackingPlot(self.lbl1_HT, self.frameCount, self.xRight_mm, 'right edge', 'o', 'b')
        #     HSVTrackingPlot(self.lbl1_HT, self.frameCount, self.xLeft_mm, 'left edge', 't', 'r')
        #     HSVTrackingPlot(self.lbl2_HT, self.frameCount, self.spreadRateRight, 'right edge', 'o', 'b')
        #     HSVTrackingPlot(self.lbl2_HT, self.frameCount, self.spreadRateLeft, 'left edge', 't', 'r')
        xPlot1, yRight1, yLeft1 = selectAxes(self, xAxis_lbl1, yAxis_lbl1)
        xPlot2, yRight2, yLeft2 = selectAxes(self, xAxis_lbl2, yAxis_lbl2)

        if yAxis_lbl1 == 'Flame length [mm]':
            HSVTrackingPlot(self.lbl1_HT, xPlot1, yRight1, 'flame length', 'o', 'b')
        else:
            HSVTrackingPlot(self.lbl1_HT, xPlot1, yRight1, 'right edge', 'o', 'b')
            HSVTrackingPlot(self.lbl1_HT, xPlot1, yLeft1, 'left edge', 't', 'r')

        if yAxis_lbl2 == 'Flame length [mm]':
            HSVTrackingPlot(self.lbl2_HT, xPlot2, yRight2, 'flame length', 'o', 'b')
        else:
            HSVTrackingPlot(self.lbl2_HT, xPlot2, yRight2, 'right edge', 'o', 'b')
            HSVTrackingPlot(self.lbl2_HT, xPlot2, yLeft2, 'left edge', 't', 'r')

        # print('Showing!')
        self.lbl1_HT.show()
        self.lbl2_HT.show()

def HSVTrackingPlot(label, x, y, name, symbol, color):
    pen = ft.pg.mkPen(color)
    label.plot(x, y, pen = pen, name = name, symbol = symbol, symbolSize = 7, symbolBrush = (color))

def HSVSlider_released(self):
    frame, frameCrop = ft.checkEditing(self, self.frameNumber)
    getFilteredFrame(self, frameCrop)
    self.lbl1_HT.setPixmap(ft.QPixmap.fromImage(self.frame))
    self.lbl2_HT.setPixmap(ft.QPixmap.fromImage(self.frameBW))

def filterParticleSldr(self):
    frame, frameCrop = ft.checkEditing(self, self.frameNumber)
    getFilteredFrame(self, frameCrop)
    self.lbl1_HT.setPixmap(ft.QPixmap.fromImage(self.frame))
    self.lbl2_HT.setPixmap(ft.QPixmap.fromImage(self.frameBW))

# def chooseFlameDirection(self, text):
#     global flameDir
#     selection = self.directionBox.currentText()
#     if selection == 'Left to right':
#         flameDir = 'toRight'
#     elif selection == 'Right to left':
#         flameDir = 'toLeft'

# def connectivityBox(self, text):
#     selection = self.connectivityBox.currentText()
#     if selection == '4':
#         self.connectivity_HT = 4
#     elif selection == '8':
#         self.connectivity_HT = 8

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
                # CAS slider setting:
                writer.writerow(['H', str(self.hueMinSlider.value()), str(self.hueMaxSlider.value())])
                writer.writerow(['S', str(self.satMinSlider.value()), str(self.satMaxSlider.value())])
                writer.writerow(['V', str(self.valMinSlider.value()), str(self.valMaxSlider.value())])
                writer.writerow([''])
                writer.writerow(['Particle size', str(self.filterParticleSldr_HT.value())])
                writer.writerow(['Moving average', str(self.movAvgIn_HT.text())])
                writer.writerow(['Points LE', str(self.avgLEIn_HT.text())])
                # writer.writerow(['Connectivity', str(self.connectivity_HT)])
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
                # CAS slider setting:
                if 'H' in row:
                    self.hueMinSlider.setValue(int(row[1]))
                    self.hueMaxSlider.setValue(int(row[2]))
                elif 'S' in row:
                    self.satMinSlider.setValue(int(row[1]))
                    self.satMaxSlider.setValue(int(row[2]))
                elif 'V' in row:
                    self.valMinSlider.setValue(int(row[1]))
                    self.valMaxSlider.setValue(int(row[2]))
                elif 'Particle size' in row:
                    self.filterParticleSldr_HT.setMaximum(int(row[1]))
                    self.filterParticleSldr_HT.setValue(int(row[1]))
                    self.particleSldrMax.setText(row[1])
                elif 'Moving average' in row:
                    self.movAvgIn_HT.setText(row[1])
                elif 'Points LE' in row:
                    self.avgLEIn_HT.setText(row[1])

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

    self.lbl1_HT.clear()
    self.lbl2_HT.clear()

    ## Plot in terms of time:
    #HSVTrackingPlot(self.lbl1_HT, self.timeCount, self.xRight_mm, '', 'o', 'b')
    #HSVTrackingPlot(self.lbl1_HT, self.timeCount, self.xLeft_mm, '','t', 'r')
    #HSVTrackingPlot(self.lbl2_HT, self.timeCount, self.spreadRateRight, '', 'o', 'b')
    #HSVTrackingPlot(self.lbl2_HT, self.timeCount, self.spreadRateLeft, '','t', 'r')

    ## CAS Plot in terms of frame:
    # HSVTrackingPlot(self.lbl1_HT, self.frameCount, self.xRight_mm, '', 'o', 'b')
    # HSVTrackingPlot(self.lbl1_HT, self.frameCount, self.xLeft_mm, '','t', 'r')
    # HSVTrackingPlot(self.lbl2_HT, self.frameCount, self.spreadRateRight, '', 'o', 'b')
    # HSVTrackingPlot(self.lbl2_HT, self.frameCount, self.spreadRateLeft, '','t', 'r')

    xPlot1, yRight1, yLeft1 = selectAxes(self, xAxis_lbl1, yAxis_lbl1)
    xPlot2, yRight2, yLeft2 = selectAxes(self, xAxis_lbl2, yAxis_lbl2)

    if yAxis_lbl1 == 'Flame length [mm]':
        HSVTrackingPlot(self.lbl1_HT, xPlot1, yRight1, 'flame length', 'o', 'b')
    else:
        HSVTrackingPlot(self.lbl1_HT, xPlot1, yRight1, 'right edge', 'o', 'b')
        HSVTrackingPlot(self.lbl1_HT, xPlot1, yLeft1, 'left edge', 't', 'r')

    if yAxis_lbl2 == 'Flame length [mm]':
        HSVTrackingPlot(self.lbl2_HT, xPlot2, yRight2, 'flame length', 'o', 'b')
    else:
        HSVTrackingPlot(self.lbl2_HT, xPlot2, yRight2, 'right edge', 'o', 'b')
        HSVTrackingPlot(self.lbl2_HT, xPlot2, yLeft2, 'left edge', 't', 'r')

def saveBtn(self):
    fileName = ft.QFileDialog.getSaveFileName(self, 'Save tracking data')
    fileName = fileName[0]
    if not fileName[-4:] == '.csv':
        fileName = fileName + '.csv'

    fileInfo = ['Name', self.fNameLbl.text(), 'Scale [px/mm]', self.scaleIn.text(), 'Moving avg', self.movAvgIn_HT.text(), 'Points LE', self.avgLEIn_HT.text(), 'Flame dir.:', self.directionBox.currentText(), 'code version', str(self.FTversion)]
    lbl = ['File info', 'Frame', 'Time [s]', 'Right Edge [mm]', 'Left Edge [mm]', 'Length [mm]', 'Spread Rate RE [mm/s]', 'Spread Rate LE [mm/s]', 'Area [mm^2]']
    clms = [fileInfo, self.frameCount, self.timeCount, self.xRight_mm, self.xLeft_mm, self.flameLength_mm, self.spreadRateRight, self.spreadRateLeft, self.flameArea]
    clms_zip = ft.zip_longest(*clms)

    if fileName == '.csv': #this prevents name issues when the user closes the dialog without saving
        self.msgLabel.setText('Ops! The values were not saved.')
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
    ft.cv2.imshow(('Frame (RGB): ' + self.frameIn.text()), self.currentFrameRGB_HT)
    #cv2.namedWindow(('Frame (black/white): ' + self.frameIn.text()), cv2.WINDOW_AUTOSIZE)
    #cv2.imshow(('Frame (black/white): ' + self.frameIn.text()), self.currentFrameBW_HT)
    while True:
        if ft.cv2.waitKey(1) == 27: #ord('Esc')
            ft.cv2.destroyAllWindows()
            return

def filterParticleSldr(self):
    frame, frameCrop = ft.checkEditing(self, self.frameNumber)
    getFilteredFrame(self, frameCrop)
    self.lbl1_HT.setPixmap(ft.QPixmap.fromImage(self.frame))
    self.lbl2_HT.setPixmap(ft.QPixmap.fromImage(self.frameBW))
    self.filterParticleSldr_HT.setMaximum(int(self.particleSldrMax.text()))

def lightROIBtn(self):
    frame, frameCrop = ft.checkEditing(self, self.frameNumber)
    self.lightROI_HT = ft.cv2.selectROI(frame)
    ft.cv2.destroyAllWindows()
    self.lightROI_HT_recorded = True

def helpBtn(self):
    msg = ft.QMessageBox(self)
    msg.setText("""HSV Tracking allows you to track a flame in an automatic way by considering the intensity in the HSV space of each pixel in the ROI.

    The flame region can be identified by choosing appropriate values of the HSV parameters (and particle size filtering). The HSV values vary depending on the colorspace of the frame/image - current implementation uses a hue from 0-180 (since 0-360 deg hue is stored as H/2 for 8-bit), value and saturation are set from 0 to 255.
    The code will consider the range between minimum and maximum of each of the HSV channels as adjusted with the sliders. Small particles can be filtered out. The value of the slider indicates the area (in px^2) of the regions to remove from the image/frame, and you can change the maximum value by typing a number in the text box next to 'Filter particles'.

    The preview box on the left shows the RGB image resulting from the filtering, while the preview box on the right shows the binary image with the particle filtering applied. The edges of the flame region are calculated as maximum and minimum locations.

    If there is a flashing or strobe light in the recorded video, you can click on 'Pick bright region' to choose a rectangular region (in the same way that the ROI is selected) that is illuminated when the light is on and dark when it is off (this region is independent from the ROI specified in the 'Preview box'). The frames where the light is on can be discarded during the analysis by checking the 'Ignore flashing light' box.

    Flame position and spread rates are calculated automatically once 'Start tracking' is clicked. The instantaneous spread rates are averaged according to the number of points specified by the user ('Moving Avg'). Note that the 'Moving Avg points' value is doubled for the calculation of the spread rate (i.e. 'Moving Avg points' = 2 considers two points before and two points after the instantaneous value).

    By clicking on 'Absolute values', the x-axis of the tracked data will be shifted to the origin.

    Click on 'Save data' to export a csv file with all the tracking results (position of left and right edges, their spread rates and their distance variation in time, as well as the area of the flame region).

    If 'Video output' is checked, the filtered frames are exported as a new video, which could be used to visually check the tracking accuracy.
    """)
    if self.pyqtVer == '5':
        msg.exec_()
    elif self.pyqtVer == '6':
        msg.exec()

def hueMinLeftBtn(self):
    currentValue = self.hueMinSlider.value()
    self.hueMinSlider.setValue(currentValue - 1)
    HSVSlider_released(self)
def hueMinRightBtn(self):
    currentValue = self.hueMinSlider.value()
    self.hueMinSlider.setValue(currentValue + 1)
    HSVSlider_released(self)
def hueMaxLeftBtn(self):
    currentValue = self.hueMaxSlider.value()
    self.hueMaxSlider.setValue(currentValue - 1)
    HSVSlider_released(self)
def hueMaxRightBtn(self):
    currentValue = self.hueMaxSlider.value()
    self.hueMaxSlider.setValue(currentValue + 1)
    HSVSlider_released(self)
def satMinLeftBtn(self):
    currentValue = self.satMinSlider.value()
    self.satMinSlider.setValue(currentValue - 1)
    HSVSlider_released(self)
def satMinRightBtn(self):
    currentValue = self.satMinSlider.value()
    self.satMinSlider.setValue(currentValue + 1)
    HSVSlider_released(self)
def satMaxLeftBtn(self):
    currentValue = self.satMaxSlider.value()
    self.satMaxSlider.setValue(currentValue - 1)
    HSVSlider_released(self)
def satMaxRightBtn(self):
    currentValue = self.satMaxSlider.value()
    self.satMaxSlider.setValue(currentValue + 1)
    HSVSlider_released(self)
def valMinLeftBtn(self):
    currentValue = self.valMinSlider.value()
    self.valMinSlider.setValue(currentValue - 1)
    HSVSlider_released(self)
def valMinRightBtn(self):
    currentValue = self.valMinSlider.value()
    self.valMinSlider.setValue(currentValue + 1)
    HSVSlider_released(self)
def valMaxLeftBtn(self):
    currentValue = self.valMaxSlider.value()
    self.valMaxSlider.setValue(currentValue - 1)
    HSVSlider_released(self)
def valMaxRightBtn(self):
    currentValue = self.valMaxSlider.value()
    self.valMaxSlider.setValue(currentValue + 1)
    HSVSlider_released(self)

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
        self.lbl1_HT.clear()
        self.lbl2_HT.clear()
        self.lbl1_HT.addLegend(offset = [1, 0.1])
        self.lbl2_HT.addLegend(offset = [1, 0.1])

        xPlot1, yRight1, yLeft1 = selectAxes(self, xAxis_lbl1, yAxis_lbl1)
        xPlot2, yRight2, yLeft2 = selectAxes(self, xAxis_lbl2, yAxis_lbl2)

        self.lbl1_HT.setLabel('left', str(yAxis_lbl1), color='black', size=14)
        self.lbl1_HT.setLabel('bottom', str(xAxis_lbl1), color='black', size=14)
        self.lbl2_HT.setLabel('left', str(yAxis_lbl2), color='black', size=14)
        self.lbl2_HT.setLabel('bottom', str(xAxis_lbl2), color='black', size=14)

        if yAxis_lbl1 == 'Flame length [mm]':
            HSVTrackingPlot(self.lbl1_HT, xPlot1, yRight1, 'flame length', 'o', 'b')
        else:
            HSVTrackingPlot(self.lbl1_HT, xPlot1, yRight1, 'right edge', 'o', 'b')
            HSVTrackingPlot(self.lbl1_HT, xPlot1, yLeft1, 'left edge', 't', 'r')

        if yAxis_lbl2 == 'Flame length [mm]':
            HSVTrackingPlot(self.lbl2_HT, xPlot2, yRight2, 'flame length', 'o', 'b')
        else:
            HSVTrackingPlot(self.lbl2_HT, xPlot2, yRight2, 'right edge', 'o', 'b')
            HSVTrackingPlot(self.lbl2_HT, xPlot2, yLeft2, 'left edge', 't', 'r')

        self.lbl1_HT.show()
        self.lbl2_HT.show()
    except:
        print('Unexpected error:', ft.sys.exc_info())
        self.msgLabel.setText('Error: the graphs could not be updated.')
