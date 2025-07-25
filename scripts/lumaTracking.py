"""
Flame Tracker. This program is designed to track flames or bright objects in videos or images.
Copyright (C) 2020-2025  Luca Carmignani

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

import flameTracker as ft
import boxesGUI_OS as gui

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
        ft.cv2.line(frameBW, (self.xMax, 0),(self.xMax, int(self.roiFourIn.text())), (255, 255, 255), 2)
        ft.cv2.line(frameBW, (self.xMin, 0),(self.xMin, int(self.roiFourIn.text())), (255, 255, 255), 2)

    self.currentFrameY_LT = Y
    # calculate the total number of bytes in the frame
    totalBytes = Y.nbytes
    # divide by the number of rows
    bytesPerLine = int(totalBytes/Y.shape[0]) #I had to introduce it to avoid distortion in the opened file for some of the videos
    self.frameY = ft.QImage(Y.data, Y.shape[1], Y.shape[0], bytesPerLine, ft.QImage.Format.Format_Grayscale8) #shape[0] = height, [1] = width
    self.frameY = self.frameY.scaled(self.lbl1_LT.size(), ft.Qt.AspectRatioMode.KeepAspectRatio, ft.Qt.TransformationMode.SmoothTransformation)

    self.currentFrameBW_LT = frameBW
    totalBytes = frameBW.nbytes
    bytesPerLine = int(totalBytes/frameBW.shape[0])
    self.frameBW = ft.QImage(frameBW.data, frameBW.shape[1], frameBW.shape[0], bytesPerLine, ft.QImage.Format.Format_Grayscale8)
    self.frameBW = self.frameBW.scaled(self.lbl2_LT.size(), ft.Qt.AspectRatioMode.KeepAspectRatio, ft.Qt.TransformationMode.SmoothTransformation)


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

        self.xMax = int(self.xMax/int(self.avgLEIn_LT.text()))
        self.xMin = int(self.xMin/int(self.avgLEIn_LT.text()))

        if self.directionBox.currentText() == 'Left to right':
            self.xRight = int(self.roiOneIn.text()) + self.xMax
            self.xLeft = int(self.roiOneIn.text()) + self.xMin
        elif self.directionBox.currentText() == 'Right to left':
            self.xRight = self.vWidth - int(self.roiOneIn.text()) - self.xMax
            self.xLeft = self.vWidth - int(self.roiOneIn.text()) - self.xMin
    except:
        self.msgLabel.setText('Flame not found in some frames')
        #pass

    # moved in getFilteredFlame function in v1.2.2
    # if self.showEdges_LT.isChecked() == True:
    #     ft.cv2.line(frameBW, (self.xMax, 0),(self.xMax, int(self.roiFourIn.text())), (255, 255, 255), 2)
    #     ft.cv2.line(frameBW, (self.xMin, 0),(self.xMin, int(self.roiFourIn.text())), (255, 255, 255), 2)

    # self.currentFrameBW_LT = frameBW
    # totalBytes = frameBW.nbytes
    # bytesPerLine = int(totalBytes/frameBW.shape[0])
    # self.frameBW = ft.QImage(frameBW.data, frameBW.shape[1], frameBW.shape[0], bytesPerLine, ft.QImage.Format.Format_Grayscale8)
    # self.frameBW = self.frameBW.scaled(self.lbl2_LT.size(), ft.Qt.AspectRatioMode.KeepAspectRatio, ft.Qt.TransformationMode.SmoothTransformation)

def lumaTracking(self):
    startTimer = ft.time.perf_counter() # v1.3.0; to measure the execution time of the tracking
    scale = True
    if not self.scaleIn.text():
        scale = False
        msg = ft.QMessageBox(self)
        msg.setText('The scale [px/len] has not been specified')
        msg.exec()

    firstFrame = int(self.firstFrameIn.text())
    lastFrame = int(self.lastFrameIn.text())
    currentFrame = firstFrame
    self.xRight_px = list()
    self.xLeft_px = list()
    # self.xRight_mm = list()
    # self.xLeft_mm = list()
    self.xRight_unit = list() #v1.3.0; the unit is now a variable selected by the user
    self.xLeft_unit = list()
    # flameLength_mm = list()
    flameLength_unit = list()
    self.frameCount = list()
    # iCount = 0
    flameArea = list()
    self.plot1_LT.clear()
    self.plot2_LT.clear()

    if self.exportVideoBW_LT.isChecked(): # added in v1.2.2
        fps = (float(self.vFps))/(int(self.skipFrameIn.text()) + 1)
        vNameBW = self.fPath + '-videoBW.' + str(self.vFormat)
        fourccBW = ft.cv2.VideoWriter_fourcc(*self.codec)
        size = (int(self.roiThreeIn.text()), int(self.roiFourIn.text()))
        # open and set properties
        voutBW = ft.cv2.VideoWriter()
        voutBW.open(vNameBW, fourccBW, fps, size, 0)

    if self.exportVideo_LT.isChecked():
        fps = (float(self.vFps))/(int(self.skipFrameIn.text()) + 1)
        vName = self.fPath + '-videoLuma.' + str(self.vFormat)
        fourcc = ft.cv2.VideoWriter_fourcc(*self.codec)
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
            if self.filterLight_LT.isChecked() == True:
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
                    msg.setText('Before the tracking, click on "Pick a bright region" to select a small region visible only when the light is on.')
                    msg.exec()
                    break

                if len(flamePx_light[0]) < 0.5 * area_light:
                    getFilteredFrame(self, frameCrop)
                else:
                    currentFrame = currentFrame + 1 + int(self.skipFrameIn.text())
                    continue
            else:
                getFilteredFrame(self, frameCrop)

            self.xRight_px.append(self.xRight)
            self.xLeft_px.append(self.xLeft)
            # self.xRight_mm.append(self.xRight / float(self.scaleIn.text()))
            # self.xLeft_mm.append(self.xLeft / float(self.scaleIn.text()))
            self.xRight_unit.append(self.xRight / float(self.scaleIn.text())) #v1.3.0; the unit is now a variable selected by the user
            self.xLeft_unit.append(self.xLeft / float(self.scaleIn.text()))
            flameArea.append(self.flameArea)
            self.frameCount.append(currentFrame)
            if self.exportVideoBW_LT.isChecked():
                voutBW.write(self.currentFrameBW_LT)
            if self.exportVideo_LT.isChecked():
                vout.write(self.currentFrameY_LT)
            # print('Frame #:', currentFrame,  end='\r')
            print('Progress: ', round((currentFrame - firstFrame)/(lastFrame - firstFrame) * 10000)/100, '%', '(Frame #: ', currentFrame, ')', end='\r')
            currentFrame = currentFrame + 1 + int(self.skipFrameIn.text())

        endTimer = ft.time.perf_counter() #v1.3.0; added to measure the execution time of the tracking
        runTime = ft.np.round(endTimer - startTimer, 4)
        txtMessage = 'Progress: 100 %; Run time: ' + str(runTime) + ' s'
        
        if self.exportVideoBW_LT.isChecked():
            voutBW.release()
            # self.msgLabel.setText('Tracking completed and BW video created.')
            txtMessage = txtMessage + '; BW video created.'
        if self.exportVideo_LT.isChecked():
            vout.release()
            # self.msgLabel.setText('Tracking completed and Luma video created.')
            txtMessage = txtMessage + '; Luma video created.'

        print(txtMessage)
        self.msgLabel.setText(txtMessage) 
        
        try:
            self.flameArea = [areaN / (float(self.scaleIn.text())**2) for areaN in flameArea]
            self.flameArea = ft.np.round(self.flameArea, 3)
            self.flameArea = self.flameArea.tolist()
            self.timeCount = [frameN / float(self.vFpsLbl.text()) for frameN in self.frameCount]
        except:
            pass

        # for i in range(len(self.xRight_mm)):
        for i in range(len(self.xRight_unit)): #v1.3.0
            # flameLength_mm.append(abs(self.xRight_mm[i] - self.xLeft_mm[i]))
            flameLength_unit.append(abs(self.xRight_unit[i] - self.xLeft_unit[i]))

        # flameLength_mm = ft.np.round(flameLength_mm, 2)
        # self.flameLength_mm = flameLength_mm.tolist()
        flameLength_unit = ft.np.round(flameLength_unit, 2)
        self.flameLength_unit = flameLength_unit.tolist()

        movAvgPt = int(self.movAvgIn_LT.text()) #this number is half of the interval considered for the spread rate (movAvgPt = 2 means I am considering a total of 5 points (my point, 2 before and 2 after))
        self.spreadRateRight = list()
        self.spreadRateLeft = list()

        if movAvgPt == 0:
            for i in range(len(self.timeCount)-1):
                # xCoeffRight = ft.np.polyfit(self.timeCount[(i):(i + 2)], self.xRight_mm[(i):(i + 2)], 1)
                # xCoeffLeft = ft.np.polyfit(self.timeCount[(i):(i + 2)], self.xLeft_mm[(i):(i + 2)], 1)
                xCoeffRight = ft.np.polyfit(self.timeCount[(i):(i + 2)], self.xRight_unit[(i):(i + 2)], 1) #v1.3.0
                xCoeffLeft = ft.np.polyfit(self.timeCount[(i):(i + 2)], self.xLeft_unit[(i):(i + 2)], 1)
                self.spreadRateRight.append(xCoeffRight[0])
                self.spreadRateLeft.append(xCoeffLeft[0])
            #repeat the last value
            self.spreadRateRight.append(xCoeffRight[0])
            self.spreadRateLeft.append(xCoeffLeft[0])
        else: #here we calculate the instantaneous spread rate based on the moving avg. I also included the initial and final points
            for i in range(len(self.timeCount)):
                if i - movAvgPt < 0:
                    # xCoeffRight = ft.np.polyfit(self.timeCount[0:(i + movAvgPt + 1)], self.xRight_mm[0:(i + movAvgPt + 1)], 1)
                    # xCoeffLeft = ft.np.polyfit(self.timeCount[0:(i + movAvgPt + 1)], self.xLeft_mm[0:(i + movAvgPt + 1)], 1)
                    xCoeffRight = ft.np.polyfit(self.timeCount[0:(i + movAvgPt + 1)], self.xRight_unit[0:(i + movAvgPt + 1)], 1) #v1.3.0
                    xCoeffLeft = ft.np.polyfit(self.timeCount[0:(i + movAvgPt + 1)], self.xLeft_unit[0:(i + movAvgPt + 1)], 1)
                    self.spreadRateRight.append(xCoeffRight[0])
                    self.spreadRateLeft.append(xCoeffLeft[0])
                elif i >= movAvgPt:
                    # xCoeffRight = ft.np.polyfit(self.timeCount[(i - movAvgPt):(i + movAvgPt + 1)], self.xRight_mm[(i - movAvgPt):(i + movAvgPt + 1)], 1)
                    # xCoeffLeft = ft.np.polyfit(self.timeCount[(i - movAvgPt):(i + movAvgPt + 1)], self.xLeft_mm[(i - movAvgPt):(i + movAvgPt + 1)], 1)
                    xCoeffRight = ft.np.polyfit(self.timeCount[(i - movAvgPt):(i + movAvgPt + 1)], self.xRight_unit[(i - movAvgPt):(i + movAvgPt + 1)], 1) #v1.3.0
                    xCoeffLeft = ft.np.polyfit(self.timeCount[(i - movAvgPt):(i + movAvgPt + 1)], self.xLeft_unit[(i - movAvgPt):(i + movAvgPt + 1)], 1)
                    self.spreadRateRight.append(xCoeffRight[0])
                    self.spreadRateLeft.append(xCoeffLeft[0])
                elif i + movAvgPt > len(self.timeCount):
                    # xCoeffRight = ft.np.polyfit(self.timeCount[(i - movAvgPt):], self.xRight_mm[(i - movAvgPt):], 1)
                    # xCoeffLeft = ft.np.polyfit(self.timeCount[(i - movAvgPt):], self.xLeft_mm[(i - movAvgPt):], 1)
                    xCoeffRight = ft.np.polyfit(self.timeCount[(i - movAvgPt):], self.xRight_unit[(i - movAvgPt):], 1) #v1.3.0
                    xCoeffLeft = ft.np.polyfit(self.timeCount[(i - movAvgPt):], self.xLeft_unit[(i - movAvgPt):], 1)
                    self.spreadRateRight.append(xCoeffRight[0])
                    self.spreadRateLeft.append(xCoeffLeft[0])

        # self.xRight_mm = ft.np.round(self.xRight_mm, 3)
        # self.xRight_mm = self.xRight_mm.tolist()
        # self.xLeft_mm = ft.np.round(self.xLeft_mm, 3)
        # self.xLeft_mm = self.xLeft_mm.tolist()
        self.xRight_unit = ft.np.round(self.xRight_unit, 3) #v1.3.0
        self.xRight_unit = self.xRight_unit.tolist()
        self.xLeft_unit = ft.np.round(self.xLeft_unit, 3)
        self.xLeft_unit = self.xLeft_unit.tolist()
        self.spreadRateRight = ft.np.round(self.spreadRateRight, 3)
        self.spreadRateRight = self.spreadRateRight.tolist()
        self.spreadRateLeft = ft.np.round(self.spreadRateLeft, 3)
        self.spreadRateLeft = self.spreadRateLeft.tolist()

        xPlot1, yRight1, yLeft1, yUnit1, nPlot1 = selectAxes(self, xAxis_lbl1, yAxis_lbl1) #v1.3.0; added yUnit and nPlot to update axes labels and plots to the units used
        xPlot2, yRight2, yLeft2, yUnit2, nPlot2 = selectAxes(self, xAxis_lbl2, yAxis_lbl2)

        # self.plot1_LT.setLabel('left', str(yAxis_lbl1), color='black', size=14)
        self.plot1_LT.setLabel('bottom', str(xAxis_lbl1), color='black', size=14)
        self.plot1_LT.setLabel('left', f'{yAxis_lbl1} [{yUnit1}]', color='black', size=14) #v1.3.0
        self.plot1_LT.getAxis('bottom').setPen(color=(0, 0, 0))
        self.plot1_LT.getAxis('left').setPen(color=(0, 0, 0))
        self.plot1_LT.addLegend(offset = [1, 0.1]) # background color modified in line 122 and 123 of Versions/3.7/lib/python3.7/site-packages/pyqtgraph/graphicsItems
        # self.plot2_LT.setLabel('left', str(yAxis_lbl2), color='black', size=14)
        self.plot2_LT.setLabel('bottom', str(xAxis_lbl2), color='black', size=14)
        self.plot2_LT.setLabel('left', f'{yAxis_lbl2} [{yUnit2}]', color='black', size=14) #v1.3.0
        self.plot2_LT.getAxis('bottom').setPen(color=(0, 0, 0))
        self.plot2_LT.getAxis('left').setPen(color=(0, 0, 0))
        self.plot2_LT.addLegend(offset = [1, 0.1]) # background color modified in line 122 and 123 of Versions/3.7/lib/python3.7/site-packages/pyqtgraph/graphicsItems

        # xPlot1, yRight1, yLeft1 = selectAxes(self, xAxis_lbl1, yAxis_lbl1)
        # xPlot2, yRight2, yLeft2 = selectAxes(self, xAxis_lbl2, yAxis_lbl2)
       
        if nPlot1 == 1: #added in v1.3.0, replaces code below
            lumaTrackingPlot(self.plot1_LT, xPlot1, yRight1, xAxis_lbl1, 'o', 'b')
        else:
            lumaTrackingPlot(self.plot1_LT, xPlot1, yRight1, 'right edge', 'o', 'b')
            lumaTrackingPlot(self.plot1_LT, xPlot1, yLeft1, 'left edge', 't', 'r')
        if nPlot2 == 1:
            lumaTrackingPlot(self.plot2_LT, xPlot2, yRight2, yAxis_lbl2, 'o', 'b')
        else:
            lumaTrackingPlot(self.plot2_LT, xPlot2, yRight2, 'right edge', 'o', 'b')
            lumaTrackingPlot(self.plot2_LT, xPlot2, yLeft2, 'left edge', 't', 'r')

        # if yAxis_lbl1 == 'Flame length [mm]':
        #     lumaTrackingPlot(self.plot1_LT, xPlot1, yRight1, 'flame length', 'o', 'b')
        # elif yAxis_lbl1 == 'Flame area [mm2]':
        #     lumaTrackingPlot(self.plot1_LT, xPlot1, yRight1, 'flame area', 'o', 'b')
        # else:
        #     lumaTrackingPlot(self.plot1_LT, xPlot1, yRight1, 'right edge', 'o', 'b')
        #     lumaTrackingPlot(self.plot1_LT, xPlot1, yLeft1, 'left edge', 't', 'r')

        # if yAxis_lbl2 == 'Flame length [mm]':
        #     lumaTrackingPlot(self.plot2_LT, xPlot2, yRight2, 'flame length', 'o', 'b')
        # elif yAxis_lbl2 == 'Flame area [mm2]':
        #     lumaTrackingPlot(self.plot2_LT, xPlot2, yRight2, 'flame area', 'o', 'b')
        # else:
        #     lumaTrackingPlot(self.plot2_LT, xPlot2, yRight2, 'right edge', 'o', 'b')
        #     lumaTrackingPlot(self.plot2_LT, xPlot2, yLeft2, 'left edge', 't', 'r')

        self.win1_LT.setCurrentIndex(1) #to activate the preview tab in the analysis box
        self.win2_LT.setCurrentIndex(1) #to activate the preview tab in the analysis box


def lumaTrackingPlot(label, x, y, name, symbol, color):
    pen = ft.pg.mkPen(color)
    label.plot(x, y, pen = pen, name = name, symbol = symbol, symbolSize = 7, symbolBrush = (color))

def saveData(self):
    fileName = ft.QFileDialog.getSaveFileName(self, 'Save tracking data')
    fileName = fileName[0]
    if not fileName[-4:] == '.csv':
        fileName = fileName + '.csv'

    # fileInfo = ['Name', self.fNameLbl.text(), 'Scale [px/mm]', self.scaleIn.text(), 'Luma Tracking', 'Flame dir.:', self.directionBox.currentText(), 'Luma threshold', self.thresholdIn.text(), 'Min. particle [px]', str(self.filterParticleSldr_LT.value()),'Points LE', self.avgLEIn_LT.text(), 'Moving avg', self.movAvgIn_LT.text()]
    fileInfo = ['Name', self.fNameLbl.text(), f'Scale [px/{self.unitScale}]', self.scaleIn.text(), 'Luma Tracking', 'Flame dir.:', self.directionBox.currentText(), 'Luma threshold', self.thresholdIn.text(), 'Min. particle [px]', str(self.filterParticleSldr_LT.value()),'Points LE', self.avgLEIn_LT.text(), 'Moving avg', self.movAvgIn_LT.text()]
    if self.refPoint != []:
        fileInfo = fileInfo + ['Ref. point (abs)', [self.refPoint[0], self.refPoint[1]]]
    fileInfo = fileInfo + ['Code version', str(self.version_FT)]

    # lbl = ['File info', 'Frame', 'Time [s]', 'Right edge [mm]', 'Left edge [mm]', 'Length [mm]', 'Spread Rate RE [mm/s]', 'Spread Rate LE [mm/s]', 'Area [mm^2]']
    lbl = ['File info', 'Frame', 'Time [s]', f'Right edge [{self.unitScale}]', f'Left edge [{self.unitScale}]', f'Length [{self.unitScale}]', f'Spread Rate RE [{self.unitScale}/s]', f'Spread Rate LE [{self.unitScale}/s]', f'Area [{self.unitScale}^2]'] #v1.3.0; updated labels to the unit selected by the user
    # clms = [fileInfo, self.frameCount, self.timeCount, self.xRight_mm, self.xLeft_mm, self.flameLength_mm, self.spreadRateRight, self.spreadRateLeft, self.flameArea]
    clms = [fileInfo, self.frameCount, self.timeCount, self.xRight_unit, self.xLeft_unit, self.flameLength_unit, self.spreadRateRight, self.spreadRateLeft, self.flameArea] #v1.3.0; updated labels to the unit selected by the user
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
    # abs_xRight_mm = list()
    # abs_xLeft_mm = list()
    abs_xRight_unit = list() #v1.3.0; updated to the unit selected by the user
    abs_xLeft_unit = list()

    for i in self.frameCount:
        abs_frames.append(i - self.frameCount[0])

    for i in self.timeCount:
        abs_time.append(i - self.timeCount[0])

    for i in self.xRight_px:
        abs_xRight_px.append(i - self.xRight_px[0])

    for i in self.xLeft_px:
        abs_xLeft_px.append(i - self.xRight_px[0])

    # for i in self.xRight_mm:
    for i in self.xRight_unit: #v1.3.0; updated to the unit selected by the user
        # abs_xRight_mm.append(i - self.xRight_mm[0])
        abs_xRight_unit.append(i - self.xRight_unit[0])

    # for i in self.xLeft_mm:
    for i in self.xLeft_unit: #v1.3.0; updated to the unit selected by the user
        # abs_xLeft_mm.append(i - self.xRight_mm[0])
        abs_xLeft_unit.append(i - self.xRight_unit[0])

    self.frameCount = abs_frames
    self.timeCount = abs_time
    self.xRight_px = abs_xRight_px
    self.xLeft_px = abs_xLeft_px
    # self.xRight_mm = abs_xRight_mm
    # self.xLeft_mm = abs_xLeft_mm
    self.xRight_unit = abs_xRight_unit #v1.3.0; updated to the unit selected by the user
    self.xLeft_unit = abs_xLeft_unit

    self.plot1_LT.clear()
    self.plot2_LT.clear()

    # xPlot1, yRight1, yLeft1 = selectAxes(self, xAxis_lbl1, yAxis_lbl1)
    # xPlot2, yRight2, yLeft2 = selectAxes(self, xAxis_lbl2, yAxis_lbl2)
    xPlot1, yRight1, yLeft1, yUnit1, nPlot1 = selectAxes(self, xAxis_lbl1, yAxis_lbl1)
    xPlot2, yRight2, yLeft2, yUnit2, nPlot2 = selectAxes(self, xAxis_lbl2, yAxis_lbl2)
 
    if nPlot1 == 1:
        lumaTrackingPlot(self.plot1_LT, xPlot1, yRight1, xAxis_lbl1, 'o', 'b')
        # if yAxis_lbl1 == 'Flame length [mm]':
    #     lumaTrackingPlot(self.plot1_LT, xPlot1, yRight1, 'flame length', 'o', 'b')
    # elif yAxis_lbl1 == 'Flame area [mm2]':
    #     lumaTrackingPlot(self.plot1_LT, xPlot1, yRight1, 'flame area', 'o', 'b')
    else:
        lumaTrackingPlot(self.plot1_LT, xPlot1, yRight1, 'right edge', 'o', 'b')
        lumaTrackingPlot(self.plot1_LT, xPlot1, yLeft1, 'left edge', 't', 'r')
    
    if nPlot2 == 1:
        lumaTrackingPlot(self.plot2_LT, xPlot2, yRight2, yAxis_lbl2, 'o', 'b')
    # if yAxis_lbl2 == 'Flame length [mm]':
    #     lumaTrackingPlot(self.plot2_LT, xPlot2, yRight2, 'flame length', 'o', 'b')
    # elif yAxis_lbl2 == 'Flame area [mm2]':
    #     lumaTrackingPlot(self.plot2_LT, xPlot2, yRight2, 'flame area', 'o', 'b')
    else:
        lumaTrackingPlot(self.plot2_LT, xPlot2, yRight2, 'right edge', 'o', 'b')
        lumaTrackingPlot(self.plot2_LT, xPlot2, yLeft2, 'left edge', 't', 'r')


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
    
    nPlot = 1 #added in v1.3.0
    
    if xAxis_lbl == 'Time [s]':
        xPlot = self.timeCount
    elif xAxis_lbl == 'Frame #':
        xPlot = self.frameCount
    # if yAxis_lbl == 'Position [mm]':
    #     yRight = self.xRight_mm
    #     yLeft = self.xLeft_mm
    if yAxis_lbl == 'Position': #v1.3.0; updated to the unit selected by the user
        nPlot = 2
        yUnit = f'{self.unitScale}' #added in v1.3.0
        yRight = self.xRight_unit
        yLeft = self.xLeft_unit
    if yAxis_lbl == 'Position [px]':
        nPlot = 2
        yUnit = 'px'
        yRight = self.xRight_px
        yLeft = self.xLeft_px
    # elif yAxis_lbl == 'Flame length [mm]':
    #     yRight = self.flameLength_mm
    elif yAxis_lbl == 'Flame length':
        # yAxis_lbl == f'Flame length [{self.unitScale}]'
        yUnit = f'{self.unitScale}'
        yRight = self.flameLength_unit
        yLeft = 0
    # elif yAxis_lbl == 'Spread rate [mm/s]':
    elif yAxis_lbl == 'Spread rate':
        yUnit = f'{self.unitScale}/s'
        yRight = self.spreadRateRight
        yLeft = self.spreadRateLeft
    elif yAxis_lbl == 'Flame area':
        yUnit = f'{self.unitScale}^2'
        yRight = self.flameArea
        yLeft = 0

    # return(xPlot, yRight, yLeft)
    return(xPlot, yRight, yLeft, yUnit, nPlot)

def updateGraphsBtn(self):
    try:
        xAxis_lbl1 = self.xAxis_lbl1.currentText()
        yAxis_lbl1 = self.yAxis_lbl1.currentText()
        xAxis_lbl2 = self.xAxis_lbl2.currentText()
        yAxis_lbl2 = self.yAxis_lbl2.currentText()
        self.plot1_LT.clear()
        self.plot2_LT.clear()
        self.plot1_LT.addLegend(offset = [1, 0.1])
        self.plot2_LT.addLegend(offset = [1, 0.1])

        # xPlot1, yRight1, yLeft1 = selectAxes(self, xAxis_lbl1, yAxis_lbl1)
        # xPlot2, yRight2, yLeft2 = selectAxes(self, xAxis_lbl2, yAxis_lbl2)
        xPlot1, yRight1, yLeft1, yUnit1, nPlot1 = selectAxes(self, xAxis_lbl1, yAxis_lbl1)
        xPlot2, yRight2, yLeft2, yUnit2, nPlot2 = selectAxes(self, xAxis_lbl2, yAxis_lbl2)

        # self.plot1_LT.setLabel('left', str(yAxis_lbl1), color='black', size=14)
        self.plot1_LT.setLabel('bottom', str(xAxis_lbl1), color='black', size=14)
        self.plot1_LT.setLabel('left', f'{yAxis_lbl1} [{yUnit1}]', color='black', size=14) #v1.3.0
        # self.plot2_LT.setLabel('left', str(yAxis_lbl2), color='black', size=14)
        self.plot2_LT.setLabel('bottom', str(xAxis_lbl2), color='black', size=14)
        self.plot2_LT.setLabel('left', f'{yAxis_lbl2} [{yUnit2}]', color='black', size=14) #v1.3.0

        # if yAxis_lbl1 == 'Flame length [mm]':
        #     lumaTrackingPlot(self.plot1_LT, xPlot1, yRight1, 'flame length', 'o', 'b')
        # elif yAxis_lbl1 == 'Flame area [mm2]':
        #     lumaTrackingPlot(self.plot1_LT, xPlot1, yRight1, 'flame area', 'o', 'b')
        if nPlot1 == 1: #added in v1.3.0
            lumaTrackingPlot(self.plot1_LT, xPlot1, yRight1, xAxis_lbl1, 'o', 'b')
        else:
            lumaTrackingPlot(self.plot1_LT, xPlot1, yRight1, 'right edge', 'o', 'b')
            lumaTrackingPlot(self.plot1_LT, xPlot1, yLeft1, 'left edge', 't', 'r')
        # if yAxis_lbl2 == 'Flame length [mm]':
            # lumaTrackingPlot(self.plot2_LT, xPlot2, yRight2, 'flame length', 'o', 'b')
        # elif yAxis_lbl2 == 'Flame area [mm2]':
            # lumaTrackingPlot(self.plot2_LT, xPlot2, yRight2, 'flame area', 'o', 'b')
        if nPlot2 == 1:
            lumaTrackingPlot(self.plot2_LT, xPlot2, yRight2, yAxis_lbl2, 'o', 'b')
        else:
            lumaTrackingPlot(self.plot2_LT, xPlot2, yRight2, 'right edge', 'o', 'b')
            lumaTrackingPlot(self.plot2_LT, xPlot2, yLeft2, 'left edge', 't', 'r')

        self.win1_LT.setCurrentIndex(1) #to activate the preview tab in the analysis box
        self.win2_LT.setCurrentIndex(2) #to activate the preview tab in the analysis box

    except:
        print('Unexpected error:', ft.sys.exc_info())
        self.msgLabel.setText('Error: the graphs could not be updated.')
