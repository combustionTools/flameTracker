"""
Flame Tracker. This program is designed to track flames or bright objects in videos or images.
Copyright (C) 2021-2025 Charles Scudiere; 2021-2025  Luca Carmignani

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

Author: Charles Scudiere, PhD (adapted from RGBTracking.py)
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

import flameTracker as ft
import boxesGUI_OS as gui

def initVars(self): # define initial variables
    self.lightROI_HT_recorded = False
    self.connectivity = self.connectivityGroup.checkedAction()
    self.connectivity = self.connectivity.text()

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
    componentNum, componentLbl, stats, centroids = ft.cv2.connectedComponentsWithStats(frameBW, connectivity = int(self.connectivity)) # self.connectivity_HT) Box.currentText()
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

    if self.showEdges_HT.isChecked() == True:
        ft.cv2.line(frame, (self.xMax, 0),(self.xMax, int(self.roiFourIn.text())), (255, 255, 255), 2)
        ft.cv2.line(frame, (self.xMin, 0),(self.xMin, int(self.roiFourIn.text())), (255, 255, 255), 2)
        ft.cv2.line(frameBW, (self.xMax, 0),(self.xMax, int(self.roiFourIn.text())), (255, 255, 255), 2)
        ft.cv2.line(frameBW, (self.xMin, 0),(self.xMin, int(self.roiFourIn.text())), (255, 255, 255), 2)

    self.currentFrameRGB_HT = frame
    # calculate the total number of bytes in the frame for lbl1
    totalBytes = frame.nbytes
    # divide by the number of rows
    bytesPerLine = int(totalBytes/frame.shape[0]) #I had to introduce it to avoid distortion in the opened file for some of the videos
    self.frame = ft.QImage(frame.data, frame.shape[1], frame.shape[0], bytesPerLine, ft.QImage.Format.Format_BGR888)#.rgbSwapped() #shape[0] = height, [1] = width QImage.Format_Indexed8 BGR888
    self.frame = self.frame.scaled(self.lbl1_HT.size(), ft.Qt.AspectRatioMode.KeepAspectRatio, ft.Qt.TransformationMode.SmoothTransformation)

    self.currentFrameBW_HT = frameBW
    # calculate the total number of bytes in the frame for lbl2
    totalBytesBW = frameBW.nbytes
    # divide by the number of rows
    bytesPerLineBW = int(totalBytesBW/frameBW.shape[0]) #I had to introduce it to avoid distortion in the opened file for some of the videos
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
    startTimer = ft.time.perf_counter() # v1.3.0; to measure the execution time of the tracking
    scale = True
    if not self.scaleIn.text():
        scale = False
        msg = ft.QMessageBox(self)
        msg.setText('The scale [px/len] has not been specified')
        # if self.pyqtVer == '5':
        #     msg.exec_()
        # elif self.pyqtVer == '6':
        msg.exec()

    firstFrame = int(self.firstFrameIn.text())
    lastFrame = int(self.lastFrameIn.text())
    self.connectivity = self.connectivityGroup.checkedAction()
    self.connectivity = self.connectivity.text()
    currentFrame = firstFrame
    self.xRight_px = list()
    self.xLeft_px = list()
    self.xRight_unit = list() #v1.3.0; the unit is now a variable selected by the user, check Luma tracking for previous version
    self.xLeft_unit = list()
    flameLength_unit = list()
    self.frameCount = list()
    flameArea = list()

    if self.exportVideo_HT.isChecked() or self.exportTrackOverlay_HT.isChecked():
        fps = (float(self.vFps))/(int(self.skipFrameIn.text()) + 1)
        vName = self.fPath + '-trackedVideo.' + str(self.vFormat) # alternative: 'output.{}'.format(vFormat);   self.fNameLbl.text()
        fourcc = ft.cv2.VideoWriter_fourcc(*self.codec)
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
                    msg.setText('Before the tracking, click on "Pick a bright region" to select a small region visible only when the light is on.')
                    # if self.pyqtVer == '5':
                    #     msg.exec_()
                    # elif self.pyqtVer == '6':
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
            self.xRight_unit.append(self.xRight / float(self.scaleIn.text()))
            self.xLeft_unit.append(self.xLeft / float(self.scaleIn.text()))
            flameArea.append(self.flameArea)
            self.frameCount.append(currentFrame)
            if self.exportVideo_HT.isChecked() and not self.exportTrackOverlay_HT.isChecked():
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


        for i in range(len(self.xRight_unit)):
            flameLength_unit.append(abs(self.xRight_unit[i] - self.xLeft_unit[i]))

        flameLength_unit = ft.np.round(flameLength_unit, 2)
        self.flameLength_unit = flameLength_unit.tolist()
        
        endTimer = ft.time.perf_counter()
        runTime = ft.np.round(endTimer - startTimer, 4)
        txtMessage = 'Progress: 100 %; Run time: ' + str(runTime) + ' s'
        # print('Progress: 100 % - Tracking completed')
        # self.msgLabel.setText('Tracking completed')

        if self.exportVideo_HT.isChecked() or self.exportTrackOverlay_HT.isChecked():
            vout.release()
            # self.msgLabel.setText('Tracking completed and video created.')
            txtMessage = txtMessage + '; HT video created.'

        print(txtMessage)
        self.msgLabel.setText(txtMessage)

        # the following approach to calculate the spread rate is the same one used for lumaTracking
        movAvgPt = int(self.movAvgIn_HT.text()) #this number is half of the interval considered for the spread rate (movAvgPt = 2 means I am considering a total of 5 points (my point, 2 before and 2 after))
        self.spreadRateRight = list()
        self.spreadRateLeft = list()

        if movAvgPt == 0:
            for i in range(len(self.timeCount)-1):
                xCoeffRight = ft.np.polyfit(self.timeCount[(i):(i + 2)], self.xRight_unit[(i):(i + 2)], 1)
                xCoeffLeft = ft.np.polyfit(self.timeCount[(i):(i + 2)], self.xLeft_unit[(i):(i + 2)], 1)
                self.spreadRateRight.append(xCoeffRight[0])
                self.spreadRateLeft.append(xCoeffLeft[0])
            #repeat the last value
            self.spreadRateRight.append(xCoeffRight[0])
            self.spreadRateLeft.append(xCoeffLeft[0])
        else: #here we calculate the instantaneous spread rate based on the moving avg. I also included the initial and final points
            for i in range(len(self.timeCount)):
                if i - movAvgPt < 0:
                    xCoeffRight = ft.np.polyfit(self.timeCount[0:(i + movAvgPt + 1)], self.xRight_unit[0:(i + movAvgPt + 1)], 1)
                    xCoeffLeft = ft.np.polyfit(self.timeCount[0:(i + movAvgPt + 1)], self.xLeft_unit[0:(i + movAvgPt + 1)], 1)
                    self.spreadRateRight.append(xCoeffRight[0])
                    self.spreadRateLeft.append(xCoeffLeft[0])
                elif i >= movAvgPt:
                    xCoeffRight = ft.np.polyfit(self.timeCount[(i - movAvgPt):(i + movAvgPt + 1)], self.xRight_unit[(i - movAvgPt):(i + movAvgPt + 1)], 1)
                    xCoeffLeft = ft.np.polyfit(self.timeCount[(i - movAvgPt):(i + movAvgPt + 1)], self.xLeft_unit[(i - movAvgPt):(i + movAvgPt + 1)], 1)
                    self.spreadRateRight.append(xCoeffRight[0])
                    self.spreadRateLeft.append(xCoeffLeft[0])
                elif i + movAvgPt > len(self.timeCount):
                    xCoeffRight = ft.np.polyfit(self.timeCount[(i - movAvgPt):], self.xRight_unit[(i - movAvgPt):], 1)
                    xCoeffLeft = ft.np.polyfit(self.timeCount[(i - movAvgPt):], self.xLeft_unit[(i - movAvgPt):], 1)
                    self.spreadRateRight.append(xCoeffRight[0])
                    self.spreadRateLeft.append(xCoeffLeft[0])

        self.spreadRateRight = ft.np.round(self.spreadRateRight, 3)
        self.spreadRateRight = self.spreadRateRight.tolist()
        self.spreadRateLeft = ft.np.round(self.spreadRateLeft, 3)
        self.spreadRateLeft = self.spreadRateLeft.tolist()

        xPlot1, yRight1, yLeft1, yUnit1, nPlot1 = selectAxes(self, xAxis_lbl1, yAxis_lbl1) #v1.3.0; added yUnit and nPlot to update axes labels and plots to the units used
        xPlot2, yRight2, yLeft2, yUnit2, nPlot2 = selectAxes(self, xAxis_lbl2, yAxis_lbl2)

        # self.plot1_HT.setLabel('left', str(yAxis_lbl1), color='black', size=14)
        self.plot1_HT.setLabel('bottom', str(xAxis_lbl1), color='black', size=14)
        self.plot1_HT.setLabel('left', f'{yAxis_lbl1} [{yUnit1}]', color='black', size=14) #v1.3.0
        self.plot1_HT.getAxis('bottom').setPen(color=(0, 0, 0))
        self.plot1_HT.getAxis('left').setPen(color=(0, 0, 0))
        self.plot1_HT.addLegend(offset = [1, 0.1]) # background color modified in line 122 and 123 of Versions/3.7/lib/python3.7/site-packages/pyqtgraph/graphicsItems
        # self.plot2_HT.setLabel('left', str(yAxis_lbl2), color='black', size=14)
        self.plot2_HT.setLabel('bottom', str(xAxis_lbl2), color='black', size=14)
        self.plot2_HT.setLabel('left', f'{yAxis_lbl2} [{yUnit2}]', color='black', size=14) #v1.3.0
        self.plot2_HT.getAxis('bottom').setPen(color=(0, 0, 0))
        self.plot2_HT.getAxis('left').setPen(color=(0, 0, 0))
        self.plot2_HT.addLegend(offset = [1, 0.1]) # background color modified in line 122 and 123 of Versions/3.7/lib/python3.7/site-packages/pyqtgraph/graphicsItems

        # xPlot1, yRight1, yLeft1 = selectAxes(self, xAxis_lbl1, yAxis_lbl1)
        # xPlot2, yRight2, yLeft2 = selectAxes(self, xAxis_lbl2, yAxis_lbl2)

        # if yAxis_lbl1 == 'Flame length [mm]':
        #     HSVTrackingPlot(self.plot1_HT, xPlot1, yRight1, 'flame length', 'o', 'b')
        # elif yAxis_lbl1 == 'Flame area [mm2]':
        #     HSVTrackingPlot(self.plot1_HT, xPlot1, yRight1, 'flame area', 'o', 'b')
        if nPlot1 == 1: #added in v1.3.0, replaces code above
            HSVTrackingPlot(self.plot1_HT, xPlot1, yRight1, xAxis_lbl1, 'o', 'b')
        else:
            HSVTrackingPlot(self.plot1_HT, xPlot1, yRight1, 'right edge', 'o', 'b')
            HSVTrackingPlot(self.plot1_HT, xPlot1, yLeft1, 'left edge', 't', 'r')

        # if yAxis_lbl2 == 'Flame length [mm]':
        #     HSVTrackingPlot(self.plot2_HT, xPlot2, yRight2, 'flame length', 'o', 'b')
        # elif yAxis_lbl2 == 'Flame area [mm2]':
        #     HSVTrackingPlot(self.plot2_HT, xPlot2, yRight2, 'flame area', 'o', 'b')
        if nPlot2 == 1:
            HSVTrackingPlot(self.plot2_HT, xPlot2, yRight2, yAxis_lbl2, 'o', 'b')
        else:
            HSVTrackingPlot(self.plot2_HT, xPlot2, yRight2, 'right edge', 'o', 'b')
            HSVTrackingPlot(self.plot2_HT, xPlot2, yLeft2, 'left edge', 't', 'r')

        self.win1_HT.setCurrentIndex(1) #to activate the preview tab in the analysis box
        self.win2_HT.setCurrentIndex(1)


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
                writer.writerow(['Connectivity', self.connectivity]) #Box.currentText()
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
    abs_xRight_unit = list()
    abs_xLeft_unit = list()

    for i in self.frameCount:
        abs_frames.append(i - self.frameCount[0])

    for i in self.timeCount:
        abs_time.append(i - self.timeCount[0])

    for i in self.xRight_px:
        abs_xRight_px.append(i - self.xRight_px[0])

    for i in self.xLeft_px:
        abs_xLeft_px.append(i - self.xRight_px[0])

    for i in self.xRight_unit:
        abs_xRight_unit.append(i - self.xRight_unit[0])

    for i in self.xLeft_unit:
        abs_xLeft_unit.append(i - self.xRight_unit[0])

    self.frameCount = abs_frames
    self.timeCount = abs_time
    self.xRight_px = abs_xRight_px
    self.xLeft_px = abs_xLeft_px
    self.xRight_unit = abs_xRight_unit
    self.xLeft_unit = abs_xLeft_unit

    self.plot1_HT.clear()
    self.plot2_HT.clear()

    # xPlot1, yRight1, yLeft1 = selectAxes(self, xAxis_lbl1, yAxis_lbl1)
    # xPlot2, yRight2, yLeft2 = selectAxes(self, xAxis_lbl2, yAxis_lbl2)
    xPlot1, yRight1, yLeft1, yUnit1, nPlot1 = selectAxes(self, xAxis_lbl1, yAxis_lbl1)
    xPlot2, yRight2, yLeft2, yUnit2, nPlot2 = selectAxes(self, xAxis_lbl2, yAxis_lbl2)

    # if yAxis_lbl1 == 'Flame length [mm]':
    #     HSVTrackingPlot(self.plot1_HT, xPlot1, yRight1, 'flame length', 'o', 'b')
    # elif yAxis_lbl1 == 'Flame area [mm2]':
    #     HSVTrackingPlot(self.plot1_HT, xPlot1, yRight1, 'flame area', 'o', 'b')
    if nPlot1 == 1:
        HSVTrackingPlot(self.plot1_HT, xPlot1, yRight1, xAxis_lbl1, 'o', 'b')
    else:
        HSVTrackingPlot(self.plot1_HT, xPlot1, yRight1, 'right edge', 'o', 'b')
        HSVTrackingPlot(self.plot1_HT, xPlot1, yLeft1, 'left edge', 't', 'r')

    # if yAxis_lbl2 == 'Flame length [mm]':
    #     HSVTrackingPlot(self.plot2_HT, xPlot2, yRight2, 'flame length', 'o', 'b')
    # elif yAxis_lbl2 == 'Flame area [mm2]':
    #     HSVTrackingPlot(self.plot2_HT, xPlot2, yRight2, 'flame area', 'o', 'b')
    if nPlot2 == 1:
        HSVTrackingPlot(self.plot2_HT, xPlot2, yRight2, yAxis_lbl2, 'o', 'b')
    else:
        HSVTrackingPlot(self.plot2_HT, xPlot2, yRight2, 'right edge', 'o', 'b')
        HSVTrackingPlot(self.plot2_HT, xPlot2, yLeft2, 'left edge', 't', 'r')

    self.win1_HT.setCurrentIndex(1)
    self.win2_HT.setCurrentIndex(1)

def saveBtn(self):
    fileName = ft.QFileDialog.getSaveFileName(self, 'Save tracking data')
    fileName = fileName[0]
    if not fileName[-4:] == '.csv':
        fileName = fileName + '.csv'

    # fileInfo = ['Name', self.fNameLbl.text(), 'Scale [px/mm]', self.scaleIn.text(), 'Moving avg', self.movAvgIn_HT.text(), 'Points LE', self.avgLEIn_HT.text(), 'Flame dir.:', self.directionBox.currentText(), 'code version', str(self.version_FT)]
    fileInfo = ['Name', self.fNameLbl.text(), f'Scale [px/{self.unitScale}]', self.scaleIn.text(), 'Moving avg', self.movAvgIn_HT.text(), 'Points LE', self.avgLEIn_HT.text(), 'Flame dir.:', self.directionBox.currentText(), 'code version', str(self.version_FT)]
    # lbl = ['File info', 'Frame', 'Time [s]', 'Right Edge [mm]', 'Left Edge [mm]', 'Length [mm]', 'Spread Rate RE [mm/s]', 'Spread Rate LE [mm/s]', 'Area [mm^2]']
    lbl = ['File info', 'Frame', 'Time [s]', f'Right Edge [{self.unitScale}]', f'Left Edge [{self.unitScale}]', f'Length [{self.unitScale}]', f'Spread Rate RE [{self.unitScale}/s]', f'Spread Rate LE [{self.unitScale}/s]', f'Area [{self.unitScale}^2]']
    # clms = [fileInfo, self.frameCount, self.timeCount, self.xRight_mm, self.xLeft_mm, self.flameLength_mm, self.spreadRateRight, self.spreadRateLeft, self.flameArea]
    clms = [fileInfo, self.frameCount, self.timeCount, self.xRight_unit, self.xLeft_unit, self.flameLength_unit, self.spreadRateRight, self.spreadRateLeft, self.flameArea]
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

    nPlot = 1 #added in v1.3.0

    if xAxis_lbl == 'Time [s]':
        xPlot = self.timeCount
    elif xAxis_lbl == 'Frame #':
        xPlot = self.frameCount
    if yAxis_lbl == 'Position':
        nPlot = 2
        yUnit = f'{self.unitScale}' #added in v1.3.0
        yRight = self.xRight_unit
        yLeft = self.xLeft_unit
    if yAxis_lbl == 'Position [px]':
        nPlot = 2
        yUnit = 'px'
        yRight = self.xRight_px
        yLeft = self.xLeft_px
    elif yAxis_lbl == 'Flame length':
        yUnit = f'{self.unitScale}'
        yRight = self.flameLength_unit
        yLeft = 0
    elif yAxis_lbl == 'Spread rate':
        yUnit = f'{self.unitScale}/s'
        yRight = self.spreadRateRight
        yLeft = self.spreadRateLeft
    elif yAxis_lbl == 'Flame area':
        yUnit = f'{self.unitScale}^2'
        yRight = self.flameArea
        yLeft = 0

    # return(xPlot, yRight, yLeft)
    return(xPlot, yRight, yLeft, yUnit, nPlot) #v1.3.0; added yUnit and nPlot to update axes labels and plots to the units used

def updateGraphsBtn(self):
    try:
        xAxis_lbl1 = self.xAxis_lbl1.currentText()
        yAxis_lbl1 = self.yAxis_lbl1.currentText()
        xAxis_lbl2 = self.xAxis_lbl2.currentText()
        yAxis_lbl2 = self.yAxis_lbl2.currentText()
        self.plot1_HT.clear()
        self.plot2_HT.clear()
        self.plot1_HT.addLegend(offset = [1, 0.1])
        self.plot2_HT.addLegend(offset = [1, 0.1])

        xPlot1, yRight1, yLeft1, yUnit1, nPlot1 = selectAxes(self, xAxis_lbl1, yAxis_lbl1)
        xPlot2, yRight2, yLeft2, yUnit2, nPlot2 = selectAxes(self, xAxis_lbl2, yAxis_lbl2)

        # self.plot1_HT.setLabel('left', str(yAxis_lbl1), color='black', size=14)
        self.plot1_HT.setLabel('bottom', str(xAxis_lbl1), color='black', size=14)
        self.plot1_HT.setLabel('left', f'{yAxis_lbl1} [{yUnit1}]', color='black', size=14) #v1.3.0
        # self.plot2_HT.setLabel('left', str(yAxis_lbl2), color='black', size=14)
        self.plot2_HT.setLabel('bottom', str(xAxis_lbl2), color='black', size=14)
        self.plot2_HT.setLabel('left', f'{yAxis_lbl2} [{yUnit2}]', color='black', size=14) #v1.3.0

        # if yAxis_lbl1 == 'Flame length [mm]':
        #     HSVTrackingPlot(self.plot1_HT, xPlot1, yRight1, 'flame length', 'o', 'b')
        # elif yAxis_lbl1 == 'Flame area [mm2]':
        #     HSVTrackingPlot(self.plot1_HT, xPlot1, yRight1, 'flame area', 'o', 'b')
        if nPlot1 == 1: #added in v1.3.0
            HSVTrackingPlot(self.plot1_HT, xPlot1, yRight1, xAxis_lbl1, 'o', 'b')
        else:
            HSVTrackingPlot(self.plot1_HT, xPlot1, yRight1, 'right edge', 'o', 'b')
            HSVTrackingPlot(self.plot1_HT, xPlot1, yLeft1, 'left edge', 't', 'r')

        # if yAxis_lbl2 == 'Flame length':
        #     HSVTrackingPlot(self.plot2_HT, xPlot2, yRight2, 'flame length', 'o', 'b')
        # elif yAxis_lbl2 == 'Flame area':
        #     HSVTrackingPlot(self.plot2_HT, xPlot2, yRight2, 'flame area', 'o', 'b')
        if nPlot2 == 1:
            HSVTrackingPlot(self.plot2_HT, xPlot2, yRight2, yAxis_lbl2, 'o', 'b')
        else:
            HSVTrackingPlot(self.plot2_HT, xPlot2, yRight2, 'right edge', 'o', 'b')
            HSVTrackingPlot(self.plot2_HT, xPlot2, yLeft2, 'left edge', 't', 'r')

        self.win1_HT.setCurrentIndex(1)
        self.win2_HT.setCurrentIndex(1)

    except:
        print('Unexpected error:', ft.sys.exc_info())
        self.msgLabel.setText('Error: the graphs could not be updated.')
