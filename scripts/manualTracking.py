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

from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from itertools import zip_longest
# from flameTracker import *
# from boxesGUI_OS import *
import csv
import cv2
import flameTracker as ft
import boxesGUI_OS as gui
import pyqtgraph as pg
import numpy as np


def initVars(self):
    # default variables
    global flameDir, lightStatus
    flameDir = 'toRight'
    lightStatus = 'None'
    self.lightROI_MT_recorded = False

# def createTrackingBox(self):

    # gui.manualTrackingBox(self)
    # # if self.OStype == 'mac' or self.OStype == 'lin':
    # #     gui.manualTrackingBox_Mac(self)
    # # elif self.OStype == 'win':
    # #     gui.manualTrackingBox_Win(self)
    #
    # initVars(self)
    # # default variables
    # self.flameDir = 'toRight'
    # self.lightStatus = 'None'
    # self.lightROI_MT_recorded = False

    # self.manualTrackingBox.show()

# def checkEditing(self, frameNumber):
#     roiOne = int(self.roiOneIn.text())
#     roiTwo = int(self.roiTwoIn.text())
#     roiThree = int(self.roiThreeIn.text())
#     roiFour = int(self.roiFourIn.text())
#
#     if self.openSelection == 'video':
#         self.fVideo.set(1, int(frameNumber))
#         ret, frame = self.fVideo.read()
#     elif self.openSelection == 'image(s)':
#         imageNumber = self.imagesList[int(frameNumber)]
#         frame = cv2.imread(imageNumber)
#
#     try:
#         if self.perspectiveValue == True:
#             if self.rotationValue == True:
#                 frame = rotationCorrection(self, frame, self.anglePerspective)
#             frame = perspectiveCorrection(self, frame)
#             #the rotation has already been included in the perspective correction, but it could happen that a further rotation is needed after the correction (e.g. for the analysis)
#             if self.anglePerspective != float(self.rotationAngleIn.text()):
#                 angle = float(self.rotationAngleIn.text()) - self.anglePerspective
#                 frame = rotationCorrection(self, frame, angle)
#         elif float(self.rotationAngleIn.text()) != 0: #in case there is no perspective correction
#                 angle = float(self.rotationAngleIn.text())
#                 frame = rotationCorrection(self, frame, angle)
#         if self.brightnessLbl.text() != '0' or self.contrastLbl.text() != '0':
#             frameContainer = np.zeros(frame.shape, frame.dtype)
#             alpha = (int(self.contrastSlider.value()) + 100) * 2 / 200
#             beta = int(self.brightnessSlider.value())    # Simple brightness control [0-100]. Instead, we have [-50-50]
#             frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
#         if self.grayscale.isChecked() == True:
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     except:
#         pass
#
#     # crop image
#     frameCrop = frame[roiTwo : (roiTwo + roiFour), roiOne : (roiOne + roiThree)]
#
#     return(frame, frameCrop)

def startTracking(self):
    global clk, nClicks
    # transforming the first label into a plot
    self.lbl1_MT = pg.PlotWidget(self.manualTrackingBox)
    self.lbl1_MT.setGeometry(190, 25, 420, 300)
    self.lbl1_MT.setBackground('w')
    self.lbl1_MT.setLabel('left', 'Position [mm]', color='black', size=14)
    self.lbl1_MT.setLabel('bottom', 'Time [s]', color='black', size=14)
    self.lbl1_MT.getAxis('bottom').setPen(color=(0, 0, 0))
    self.lbl1_MT.getAxis('left').setPen(color=(0, 0, 0))
    self.lbl1_MT.addLegend(offset = [1, 0.1]) # background color modified in line 122 and 123 of Versions/3.7/lib/python3.7/site-packages/pyqtgraph/graphicsItems

    firstFrame = int(self.firstFrameIn.text())
    lastFrame = int(self.lastFrameIn.text())

    scale = True

    #Set up the first frame for analysis and clk for the mouse event
    currentFrame = firstFrame

    clk = False # False unless the mouse is clicked
    posX = dict()
    posX_mm = dict()
    posY = dict()
    posY_mm = dict()
    frameCount = dict()
    timeCount = dict()

    # find out how many points to be selected in each frame
    try:
        nClicks = int(self.nClicksLbl.text())
    except:
        nClicks = 1
        self.msgLabel.setText('Clicks not specified (=1)')

    while (currentFrame < lastFrame):
        print('Frame #:', currentFrame)
        if not self.scaleIn.text():
            scale = False
            msg = QMessageBox(self)
            msg.setText('The scale [px/mm] has not been specified')
            msg.exec_()
            break

        frame, frameCrop = ft.checkEditing(self, currentFrame)

        if self.lightROI_MT_recorded == True:
            # looking for frames with a light on (which would increase the red and green channel values of the background)
            # low and high are the thresholds for each color channel
            low = ([5, 5, 10]) # blueLow, greenLow, redLow
            high = ([255, 255, 255]) # blueHigh, greenHigh, redHigh
            low = np.array(low, dtype = 'uint8') #this conversion is necessary
            high = np.array(high, dtype = 'uint8')

            currentLightROI = frame[self.lightROI_MT[1] : (self.lightROI_MT[1] + self.lightROI_MT[3]), self.lightROI_MT[0] : (self.lightROI_MT[0] + self.lightROI_MT[2])]
            newMask = cv2.inRange(currentLightROI, low, high)
            frame_light = cv2.bitwise_and(currentLightROI, currentLightROI, mask = newMask)
            grayFrame_light = cv2.cvtColor(frame_light, cv2.COLOR_BGR2GRAY)
            (thresh_light, BW_light) = cv2.threshold(grayFrame_light, 0, 255, cv2.THRESH_BINARY)
            flamePx_light = np.where(BW_light == [255])
            area_light = int(self.lightROI_MT[3] * self.lightROI_MT[2])

            print('area_light', area_light)
            print('flamePx_light', len(flamePx_light[0]))
            if lightStatus == 'lightOff':
                if len(flamePx_light[0]) > 0.5 * area_light: #avoid this frame
                    currentFrame = currentFrame + 1 + int(self.skipFrameIn.text())
                    continue
            elif lightStatus == 'lightOn':
                if len(flamePx_light[0]) < 0.5 * area_light: #avoid this frame
                    currentFrame = currentFrame + 1 + int(self.skipFrameIn.text())
                    continue

        # create the window and the line over the first point clicked
        cv2.namedWindow('manualTracking', cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback('manualTracking', click)

        #if currentFrame > firstFrame:
        if len(posY) > 0:
            for n in range(nClicks):
                if self.showEdges_MT.isChecked() == True:
                    cv2.line(frameCrop, (0, int(posY[str(n+1)][0])),(int(self.roiThreeIn.text()), int(posY[str(n+1)][0])), (0, 245, 184), 2)

        cv2.imshow('manualTracking',frameCrop)

        self.msgLabel.setText('Tracking started, press (Esc) to quit.')
        for n in range(nClicks):
            # wait for the mouse event or 'escape' key
            while (True):
                if clk == True:
                    clk = False
                    # the zero location changes based on the flame direction
                    if flameDir == 'toRight':
                        xClick = xPos + int(self.roiOneIn.text())
                    elif flameDir == 'toLeft':
                        xClick = self.vWidth - int(self.roiOneIn.text()) - xPos
                    break

                if cv2.waitKey(1) == 27: #ord('q')
                    cv2.destroyAllWindows()
                    return

            # update each position and frame list for the current click
            if str(n+1) in posX:
                posX[str(n+1)].append(xClick)
                posX_mm[str(n+1)].append(xClick / float(self.scaleIn.text()))
                posY[str(n+1)].append(yPos)
                posY_mm[str(n+1)].append(yPos / float(self.scaleIn.text()))
                if n == 0: #frames and time are the same for all the clicks
                    frameCount[str(n+1)].append(currentFrame)
                    timeCount[str(n+1)].append(currentFrame / float(self.vFpsLbl.text()))

            else:
                posX[str(n+1)] = [xClick]
                posX_mm[str(n+1)] = [xClick / float(self.scaleIn.text())]
                posY[str(n+1)] = [yPos]
                posY_mm[str(n+1)] = [yPos / float(self.scaleIn.text())]
                if n == 0: #frames and time are the same for all the clicks
                    frameCount[str(n+1)] = [currentFrame]
                    timeCount[str(n+1)] = [currentFrame / float(self.vFpsLbl.text())]

        currentFrame = currentFrame + 1 + int(self.skipFrameIn.text())

    if len(timeCount) == 0:
        msg = QMessageBox(self)
        msg.setText('No frames were detected, please check ROI size and light settings.')
        msg.exec_()

    cv2.destroyAllWindows()

    self.posX_px = posX
    self.posX_plot = posX_mm
    self.frames_plot = frameCount
    self.time_plot = timeCount
    # moving average of the spread rate values
    self.spreadRate = dict()
    if scale:
        for n in range(nClicks):
            for i in range(len(timeCount['1'])-1):
                xCoeff = np.polyfit(timeCount['1'][(i):(i + 2)], posX_mm[str(n+1)][(i):(i + 2)], 1)
                spreadRate = xCoeff[0]
                if str(n+1) in self.spreadRate:
                    self.spreadRate[str(n+1)].append(spreadRate)
                else:
                    self.spreadRate[str(n+1)] = [spreadRate]
            #repeat the last value
            self.spreadRate[str(n+1)].append(xCoeff[0])

        self.lbl2_MT.clear()
        self.lbl2_MT.addLegend(offset = [1, 0.1]) # background color modified in line 122 and 123 of python3.7/site-packages/pyqtgraph/graphicsItems
        color = ['b', 'r', 'k', 'g', 'c', 'y']
        for n in range(nClicks):
            name = 'click{}'.format([n+1])
            try:
                clr = color[n]
            except:
                if n > len(color):
                    self.msgLabel.setText('Not enough colors for plotting.')
            manualTrackingPlot(self.lbl1_MT, self.time_plot['1'], self.posX_plot[str(n+1)], name, 'o', clr)
            manualTrackingPlot(self.lbl2_MT, self.time_plot['1'], self.spreadRate[str(n+1)], name, 'o', clr)

        self.lbl1_MT.show()

# this function waits for the next mouse click
def click(event, x, y, flags, param):
    global xPos, yPos, clk

    if event == cv2.EVENT_LBUTTONUP:
        xPos = x
        yPos = y
        clk = True

def manualTrackingPlot(label, x, y, lineName, symbol, color):
    pen = pg.mkPen(color)
    label.plot(x, y, pen = pen, name = lineName, symbol = symbol, symbolSize = 7, symbolBrush = (color))

def absValue(self):
      abs_frame = list()
      abs_time = list()

      for i in self.frames_plot['1']:
          abs_frame.append(i - self.frames_plot['1'][0])

      for i in self.time_plot['1']:
          abs_time.append(i - self.time_plot['1'][0])

      for n in range(int(self.nClicksLbl.text())):
          abs_posX_px = list()
          for i in self.posX_px[str(n+1)]:
              abs_posX_px.append(i - self.posX_px[str(n+1)][0])
          self.posX_px.update({str(n+1): abs_posX_px})

          abs_posX = list()
          for i in self.posX_plot[str(n+1)]:
              abs_posX.append(i - self.posX_plot[str(n+1)][0])
          self.posX_plot.update({str(n+1): abs_posX})

      self.frames_plot.update({'1': abs_frame})
      self.time_plot.update({'1': abs_time})

      self.lbl1_MT.clear()
      self.lbl2_MT.clear()
      color = ['b', 'r', 'k', 'g', 'c', 'y']
      for n in range(nClicks):
          name = 'click{}'.format([n+1])
          try:
              clr = color[n]
          except:
              if n > len(color):
                  self.msgLabel.setText('Not enough colors for plotting.')
          manualTrackingPlot(self.lbl1_MT, self.time_plot['1'], self.posX_plot[str(n+1)], '', 'o', clr)
          manualTrackingPlot(self.lbl2_MT, self.time_plot['1'], self.spreadRate[str(n+1)], '', 'o', clr)

def chooseFlameDirection(self):
    global flameDir
    selection = self.directionBox.currentText()
    if selection == 'Left to right':
        flameDir = 'toRight'
    elif selection == 'Right to left':
        flameDir = 'toLeft'


def chooseLightFilter(self):
    global lightStatus
    selection = self.filterLight_MT.currentText()
    if selection == 'Track every frame':
        lightStatus = 'None'
    elif selection == 'Frames light on':
        lightStatus = 'lightOn'
    elif selection == 'Frames light off':
        lightStatus = 'lightOff'

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

def lightROIBtn(self):
    frame, frameCrop = ft.checkEditing(self, self.frameNumber)
    self.lightROI_MT = cv2.selectROI(frame)
    cv2.destroyAllWindows()
    self.lightROI_MT_recorded = True

def saveData(self):
    fileName = QFileDialog.getSaveFileName(self, 'Save tracking data')
    fileName = fileName[0]
    if not fileName[-4:] == '.csv':
        fileName = fileName + '.csv'

    #try:
    fileInfo = ['Name', self.fNameLbl.text(), 'Scale [px/mm]', self.scaleIn.text(), 'Flame dir.:', flameDir]
    lbl = ['File info', 'Frame', 'Time [s]']
    clmns = [fileInfo, self.frames_plot['1'], self.time_plot['1']]

    for n in range(int(self.nClicksLbl.text())):
        lbl.append('xPos_click{} [px]'.format([n+1]))
        clmns.append(self.posX_px[str(n+1)])
        lbl.append('xPos_click{} [mm]'.format([n+1]))
        clmns.append(np.round((self.posX_plot[str(n+1)]), 2))
        lbl.append('Vf_click{}'.format([n+1]))
        clmns.append(self.spreadRate[str(n+1)])

    clmns_zip = zip_longest(*clmns)
#    except:
#        self.msgLabel.setText('Ops! Something went wrong with the click recordings.')

    if fileName == '.csv': #this prevents name issues when the user closes the dialog without saving
        self.msgLabel.setText('Ops! The values were not saved.')
    else:
        #try:
        with open(fileName, 'w', newline = '') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            writer.writerow(lbl)
            for row in clmns_zip:
                writer.writerow(row)
        self.msgLabel.setText('Data successfully saved.')
#        except:
#            notParameters_dlg = QErrorMessage(self)
#            notParameters_dlg.showMessage('Ops! Something went wrong, the values were not saved.')
#            self.msgLabel.setText('Data not saved.')

def helpBtn(self):
    msg = QMessageBox(self)
    msg.setText("""Manual Tracking allows you to click on the desired location(s) in the frames considered. You can select more than one click per frame by changing the 'Tracking points #:'.

    If there is a flashing or strobe light in the recorded video, the option 'Frames light on' will consider only the frames where it is on, whereas 'Frames light off' will consider only frames without the light. If nothing is selected, all the frames are considered. To determine which frames have the light on, click on 'Pick bright region' to select a (small) Region of Interest (ROI) where the effect of the light is visible. Note that this ROI is independent from the ROI specified in the 'Preview box', and it will be shown as a blue rectangle in the left window of the 'Analysis box' when it is used.

    With 'Start Tracking' the frames will show up in a new window (press 'Esc' to exit at any time), and horizontal lines corresponding to the points clicked on the first frame will show up in the following frames (they can be hidden by unchecking 'Show tracking lines'). After the tracking, the position vs time and spread rate values will be shown in the windows in the 'Analysis box'.

    By clicking on 'Absolute values', the x-axis of the tracked data will be shifted to the origin.

    Click on 'Save data' to export a csv file with all the tracked information.
    """)
    msg.exec_()
