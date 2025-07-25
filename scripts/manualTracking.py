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

def initVars(self): # define initial variables
    self.lightROI_MT_recorded = False

def startTracking(self):
    global clk, nClicks #, flameDir

    firstFrame = int(self.firstFrameIn.text())
    lastFrame = int(self.lastFrameIn.text())

    # scale = True

    #Set up the first frame for analysis and clk for the mouse event
    currentFrame = firstFrame

    clk = False # False unless the mouse is clicked
    posX = dict()
    # posX_mm = dict()
    posX_unit = dict() #v1.3.0
    posY = dict()
    # posY_mm = dict()
    posY_unit = dict()
    frameCount = dict()
    timeCount = dict()

    # find out how many points to be selected in each frame
    try:
        nClicks = int(self.nClicksLbl.text())
    except:
        nClicks = 1
        self.msgLabel.setText('Clicks not specified (=1)')

    while (currentFrame < lastFrame):
        print('Frame #:', currentFrame, end='\r')

        if not self.scaleIn.text():
            # scale = False
            msg = ft.QMessageBox(self)
            msg.setText('The scale [px/len] has not been specified')
            msg.exec()
            break

        frame, frameCrop = ft.checkEditing(self, currentFrame)

        if self.lightROI_MT_recorded == True:
            # looking for frames with a light on (which would increase the red and green channel values of the background)
            # low and high are the thresholds for each color channel
            low = ([5, 5, 10]) # blueLow, greenLow, redLow
            high = ([255, 255, 255]) # blueHigh, greenHigh, redHigh
            low = ft.np.array(low, dtype = 'uint8') #this conversion is necessary
            high = ft.np.array(high, dtype = 'uint8')

            currentLightROI = frame[self.lightROI_MT[1] : (self.lightROI_MT[1] + self.lightROI_MT[3]), self.lightROI_MT[0] : (self.lightROI_MT[0] + self.lightROI_MT[2])]
            newMask = ft.cv2.inRange(currentLightROI, low, high)
            frame_light = ft.cv2.bitwise_and(currentLightROI, currentLightROI, mask = newMask)
            grayFrame_light = ft.cv2.cvtColor(frame_light, ft.cv2.COLOR_BGR2GRAY)
            (thresh_light, BW_light) = ft.cv2.threshold(grayFrame_light, 0, 255, ft.cv2.THRESH_BINARY)
            flamePx_light = ft.np.where(BW_light == [255])
            area_light = int(self.lightROI_MT[3] * self.lightROI_MT[2])

            # if lightStatus == 'lightOff':
            if self.filterLight_MT.currentText() == 'Frames light off':
                if len(flamePx_light[0]) > 0.5 * area_light: #avoid this frame
                    currentFrame = currentFrame + 1 + int(self.skipFrameIn.text())
                    continue
            # elif lightStatus == 'lightOn':
            elif self.filterLight_MT.currentText() == 'Frames light on':
                if len(flamePx_light[0]) < 0.5 * area_light: #avoid this frame
                    currentFrame = currentFrame + 1 + int(self.skipFrameIn.text())
                    continue

        # create the window and the line over the first point clicked
        ft.cv2.namedWindow('manualTracking', ft.cv2.WINDOW_AUTOSIZE)
        ft.cv2.setWindowTitle('manualTracking', f'MT, frame #: {currentFrame}')
        # ft.cv2.namedWindow(f'ManualTracking; frame #: {currentFrame}', ft.cv2.WINDOW_AUTOSIZE)
        ft.cv2.setMouseCallback('manualTracking', click)
        # ft.cv2.setMouseCallback(f'ManualTracking; frame #: {currentFrame}', click)


        #if currentFrame > firstFrame:
        if len(posY) > 0:
            for n in range(nClicks):
                if self.showLines_MT.isChecked() == True:
                    ft.cv2.line(frameCrop, (0, int(posY[str(n+1)][0])),(int(self.roiThreeIn.text()), int(posY[str(n+1)][0])), (0, 245, 184), 2)

        ft.cv2.imshow('manualTracking', frameCrop)
        # ft.cv2.imshow(f'ManualTracking; frame #: {currentFrame}',frameCrop)

        self.msgLabel.setText('Tracking started, press (Esc) to quit.')
        for n in range(nClicks):
            # wait for the mouse event or 'escape' key
            while (True):
                if clk == True:
                    clk = False
                    # the zero location changes based on the flame direction

                    if self.directionBox.currentText() == 'Left to right':
                        xClick = xPos + int(self.roiOneIn.text())
                    elif self.directionBox.currentText() == 'Right to left':
                        xClick = self.vWidth - int(self.roiOneIn.text()) - xPos
                    break

                if ft.cv2.waitKey(1) == 27: #ord('q')
                    ft.cv2.destroyAllWindows()
                    return

            # update each position and frame list for the current click
            if str(n+1) in posX:
                posX[str(n+1)].append(xClick)
                # posX_mm[str(n+1)].append(xClick / float(self.scaleIn.text()))
                posX_unit[str(n+1)].append(xClick / float(self.scaleIn.text()))
                posY[str(n+1)].append(yPos)
                # posY_mm[str(n+1)].append(yPos / float(self.scaleIn.text()))
                posY_unit[str(n+1)].append(yPos / float(self.scaleIn.text()))
                if n == 0: #frames and time are the same for all the clicks
                    frameCount[str(n+1)].append(currentFrame)
                    timeCount[str(n+1)].append(currentFrame / float(self.vFpsLbl.text()))

            else:
                posX[str(n+1)] = [xClick]
                # posX_mm[str(n+1)] = [xClick / float(self.scaleIn.text())]
                posX_unit[str(n+1)] = [xClick / float(self.scaleIn.text())]
                posY[str(n+1)] = [yPos]
                # posY_mm[str(n+1)] = [yPos / float(self.scaleIn.text())]
                posY_unit[str(n+1)] = [yPos / float(self.scaleIn.text())]
                if n == 0: #frames and time are the same for all the clicks
                    frameCount[str(n+1)] = [currentFrame]
                    timeCount[str(n+1)] = [currentFrame / float(self.vFpsLbl.text())]

        currentFrame = currentFrame + 1 + int(self.skipFrameIn.text())
    print('Tracking completed')
    self.msgLabel.setText('Tracking completed')

    if len(timeCount) == 0:
        msg = ft.QMessageBox(self)
        msg.setText('No frames were detected, please check ROI size and light settings.')
        msg.exec()

    ft.cv2.destroyAllWindows()

    self.posX_px = posX
    # self.posX_plot = posX_mm
    self.posX_plot = posX_unit
    self.posY_px = posY
    # self.posY_plot = posY_mm
    self.posY_plot = posY_unit
    self.frames_plot = frameCount
    self.time_plot = timeCount
    # moving average of the spread rate values
    self.spreadRateX = dict()
    self.spreadRateY = dict()
    # if scale:
    for n in range(nClicks):
        for i in range(len(timeCount['1'])-1):
            # xCoeff = ft.np.polyfit(timeCount['1'][(i):(i + 2)], posX_mm[str(n+1)][(i):(i + 2)], 1)
            xCoeff = ft.np.polyfit(timeCount['1'][(i):(i + 2)], posX_unit[str(n+1)][(i):(i + 2)], 1)
            spreadRate = xCoeff[0]
            # yCoeff = ft.np.polyfit(timeCount['1'][(i):(i + 2)], posY_mm[str(n+1)][(i):(i + 2)], 1)
            yCoeff = ft.np.polyfit(timeCount['1'][(i):(i + 2)], posY_unit[str(n+1)][(i):(i + 2)], 1)
            spreadRateY = yCoeff[0]
            if str(n+1) in self.spreadRateX:
                self.spreadRateX[str(n+1)].append(spreadRate)
                self.spreadRateY[str(n+1)].append(spreadRateY)
            else:
                self.spreadRateX[str(n+1)] = [spreadRate]
                self.spreadRateY[str(n+1)] = [spreadRateY]
        #repeat the last value
        self.spreadRateX[str(n+1)].append(xCoeff[0])
        self.spreadRateY[str(n+1)].append(yCoeff[0])

    self.plot1_MT.clear()
    self.lbl2_MT.clear()
    # select the variables to plot based on user input
    xAxis_lbl1 = self.xAxis_lbl1.currentText()
    yAxis_lbl1 = self.yAxis_lbl1.currentText()
    xAxis_lbl2 = self.xAxis_lbl2.currentText()
    yAxis_lbl2 = self.yAxis_lbl2.currentText()

    self.lbl2_MT.addLegend(offset = [1, 0.1]) # background color modified in line 122 and 123 of python3.7/site-packages/pyqtgraph/graphicsItems (only up to v1.13)
    color = ['b', 'r', 'k', 'g', 'c', 'y']
    for n in range(nClicks):
        name = 'click{}'.format([n+1])
        try:
            clr = color[n]
        except:
            if n > len(color):
                self.msgLabel.setText('Not enough colors for plotting.')

        xPlot1, yPlot1, yUnit1 = selectAxes(self, xAxis_lbl1, yAxis_lbl1, n)
        xPlot2, yPlot2, yUnit2 = selectAxes(self, xAxis_lbl2, yAxis_lbl2, n)
        # manualTrackingPlot(self.lbl1_MT, self.time_plot['1'], self.posX_plot[str(n+1)], name, 'o', clr)
        manualTrackingPlot(self.plot1_MT, xPlot1, yPlot1, name, 'o', clr)
        # manualTrackingPlot(self.lbl2_MT, self.time_plot['1'], self.spreadRate[str(n+1)], name, 'o', clr)
        manualTrackingPlot(self.lbl2_MT, xPlot2, yPlot2, name, 'o', clr)


    # self.plot1_MT.setLabel('left', str(yAxis_lbl1), color='black', size=14)
    self.plot1_MT.setLabel('bottom', str(xAxis_lbl1), color='black', size=14)
    self.plot1_MT.setLabel('left', f'{yAxis_lbl1} [{yUnit1}]', color='black', size=14)
    self.lbl2_MT.setLabel('left', f'{yAxis_lbl2} [{yUnit2}]', color='black', size=14)
    self.plot1_MT.getAxis('bottom').setPen(color=(0, 0, 0))
    self.plot1_MT.getAxis('left').setPen(color=(0, 0, 0))
    self.plot1_MT.addLegend(offset = [1, 0.1])

    self.plot1_MT.show()
    self.win1_MT.setCurrentIndex(1)

# this function waits for the next mouse click
def click(event, x, y, flags, param):
    global xPos, yPos, clk

    if event == ft.cv2.EVENT_LBUTTONUP:
        xPos = x
        yPos = y
        clk = True

def manualTrackingPlot(label, x, y, lineName, symbol, color):
    pen = ft.pg.mkPen(color)
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
          abs_posY_px = list()
          for i in self.posX_px[str(n+1)]:
              abs_posX_px.append(i - self.posX_px[str(n+1)][0])
              abs_posY_px.append(i - self.posY_px[str(n+1)][0])
          self.posX_px.update({str(n+1): abs_posX_px})
          self.posY_px.update({str(n+1): abs_posY_px})

          abs_posX = list()
          abs_posY = list()
          for i in self.posX_plot[str(n+1)]:
              abs_posX.append(i - self.posX_plot[str(n+1)][0])
              abs_posY.append(i - self.posY_plot[str(n+1)][0])
          self.posX_plot.update({str(n+1): abs_posX})
          self.posY_plot.update({str(n+1): abs_posY})

      self.frames_plot.update({'1': abs_frame})
      self.time_plot.update({'1': abs_time})

      self.plot1_MT.clear()
      self.lbl2_MT.clear()
      color = ['b', 'r', 'k', 'g', 'c', 'y']
      for n in range(nClicks):
          name = 'click{}'.format([n+1])
          try:
              clr = color[n]
          except:
              if n > len(color):
                  self.msgLabel.setText('Not enough colors for plotting.')
          xAxis_lbl1 = self.xAxis_lbl1.currentText()
          yAxis_lbl1 = self.yAxis_lbl1.currentText()
          xAxis_lbl2 = self.xAxis_lbl2.currentText()
          yAxis_lbl2 = self.yAxis_lbl2.currentText()
          xPlot1, yPlot1, yUnit1 = selectAxes(self, xAxis_lbl1, yAxis_lbl1, n)
          xPlot2, yPlot2, yUnit2 = selectAxes(self, xAxis_lbl2, yAxis_lbl2, n)
          # manualTrackingPlot(self.lbl1_MT, self.time_plot['1'], self.posX_plot[str(n+1)], '', 'o', clr)
          # manualTrackingPlot(self.lbl2_MT, self.time_plot['1'], self.spreadRate[str(n+1)], '', 'o', clr)
          manualTrackingPlot(self.plot1_MT, xPlot1, yPlot1, '', 'o', clr)
          manualTrackingPlot(self.lbl2_MT, xPlot2, yPlot2, '', 'o', clr)

def lightROIBtn(self):
    frame, frameCrop = ft.checkEditing(self, self.frameNumber)
    self.lightROI_MT = ft.cv2.selectROI(frame)
    ft.cv2.destroyAllWindows()
    self.lightROI_MT_recorded = True

def saveData(self):
    fileName = ft.QFileDialog.getSaveFileName(self, 'Save tracking data')
    fileName = fileName[0]
    if not fileName[-4:] == '.csv':
        fileName = fileName + '.csv'

    try:
        # fileInfo = ['Name', self.fNameLbl.text(), 'Scale [px/mm]', self.scaleIn.text(), 'Manual Tracking', 'Flame dir.:', self.directionBox.currentText(), 'code version', str(self.version_FT)]
        fileInfo = ['Name', self.fNameLbl.text(), f'Scale [px/{self.unitScale}]', self.scaleIn.text(), 'Manual Tracking', 'Flame dir.:', self.directionBox.currentText(), 'code version', str(self.version_FT)]
        lbl = ['File info', 'Frame', 'Time [s]']
        clmns = [fileInfo, self.frames_plot['1'], self.time_plot['1']]
        for n in range(int(self.nClicksLbl.text())):
            # lbl.append('x_click{} [px]'.format([n+1]))
            lbl.append(f'x_click{n+1} [px]')
            clmns.append(self.posX_px[str(n+1)])
            # lbl.append('x_click{} [mm]'.format([n+1]))
            lbl.append(f'x_click{n+1} [{self.unitScale}]')
            clmns.append(ft.np.round((self.posX_plot[str(n+1)]), 2))
            # lbl.append('y_click{} [px]'.format([n+1]))
            lbl.append(f'y_click{n+1} [px]')
            clmns.append(self.posY_px[str(n+1)])
            # lbl.append('y_click{} [mm]'.format([n+1]))
            lbl.append(f'y_click{n+1} [{self.unitScale}]')
            clmns.append(ft.np.round((self.posY_plot[str(n+1)]), 2))
            # lbl.append('Vf,x_click{}'.format([n+1]))
            lbl.append(f'Vf,x_click{n+1} [{self.unitScale}/s]')
            clmns.append(self.spreadRateX[str(n+1)])
            # lbl.append('Vf,y_click{}'.format([n+1]))
            lbl.append(f'Vf,y_click{n+1} [{self.unitScale}/s]')
            clmns.append(self.spreadRateY[str(n+1)])

        clmns_zip = ft.zip_longest(*clmns)
    except:
        self.msgLabel.setText('Ops! Something went wrong while saving the data.')
        print('Unexpected error:', ft.sys.exc_info())

    if fileName == '.csv': #this prevents name issues when the user closes the dialog without saving
        self.msgLabel.setText('Ops! The file name was not valid and the data was not saved.')
    else:
        try:
            with open(fileName, 'w', newline = '') as csvfile:
                writer = ft.csv.writer(csvfile, delimiter = ',')
                writer.writerow(lbl)
                for row in clmns_zip:
                    writer.writerow(row)
            self.msgLabel.setText('Data successfully saved.')
        except:
            notParameters_dlg = ft.QErrorMessage(self)
            notParameters_dlg.showMessage('Ops! Something went wrong, the values were not saved.')
            self.msgLabel.setText('Data not saved.')
            print('Unexpected error:', ft.sys.exc_info())

def updateGraphsBtn(self):
    try:
        xAxis_lbl1 = self.xAxis_lbl1.currentText()
        yAxis_lbl1 = self.yAxis_lbl1.currentText()
        xAxis_lbl2 = self.xAxis_lbl2.currentText()
        yAxis_lbl2 = self.yAxis_lbl2.currentText()
        self.plot1_MT.clear()
        self.lbl2_MT.clear()
        self.plot1_MT.addLegend(offset = [1, 0.1])
        self.lbl2_MT.addLegend(offset = [1, 0.1])
        color = ['b', 'r', 'k', 'g', 'c', 'y']

        for n in range(nClicks):
            name = 'click{}'.format([n+1])
            try:
                clr = color[n]
            except:
                if n > len(color):
                    self.msgLabel.setText('Not enough colors for plotting.')

            xPlot1, yPlot1, yUnit1 = selectAxes(self, xAxis_lbl1, yAxis_lbl1, n)
            xPlot2, yPlot2, yUnit2 = selectAxes(self, xAxis_lbl2, yAxis_lbl2, n)

            # self.plot1_MT.setLabel('left', str(yAxis_lbl1), color='black', size=14)
            self.plot1_MT.setLabel('bottom', str(xAxis_lbl1), color='black', size=14)
            self.plot1_MT.setLabel('left', f'{yAxis_lbl1} [{yUnit1}]', color='black', size=14)
            # self.lbl2_MT.setLabel('left', str(yAxis_lbl2), color='black', size=14)
            self.lbl2_MT.setLabel('bottom', str(xAxis_lbl2), color='black', size=14)
            self.lbl2_MT.setLabel('left', f'{yAxis_lbl2} [{yUnit2}]', color='black', size=14)
            manualTrackingPlot(self.plot1_MT, xPlot1, yPlot1, name, 'o', clr)
            manualTrackingPlot(self.lbl2_MT, xPlot2, yPlot2, name, 'o', clr)

        self.plot1_MT.show()
        self.lbl2_MT.show()
    except:
        print('Unexpected error:', ft.sys.exc_info())
        self.msgLabel.setText('Error: the graphs could not be updated.')

def selectAxes(self, xAxis_lbl, yAxis_lbl, n):

    if xAxis_lbl == 'Time [s]':
        xPlot = self.time_plot['1']
    elif xAxis_lbl == 'Frame #':
        xPlot = self.frames_plot['1']
    if yAxis_lbl == 'x coord.':
        yUnit = f'{self.unitScale}'
        yPlot = self.posX_plot[str(n+1)]
    elif yAxis_lbl == 'x coord. [px]':
        yUnit = 'px'
        yPlot = self.posX_px[str(n+1)]
    elif yAxis_lbl == 'y coord.':
        yUnit = f'{self.unitScale}'
        yPlot = self.posY_plot[str(n+1)]
    elif yAxis_lbl == 'y coord. [px]':
        yUnit = 'px'
        yPlot = self.posY_px[str(n+1)]
    elif yAxis_lbl == 'Spread rate, x':
        yUnit = f'{self.unitScale}/s'
        yPlot = self.spreadRateX[str(n+1)]
    elif yAxis_lbl == 'Spread rate, y':
        yUnit = f'{self.unitScale}/s'
        yPlot = self.spreadRateY[str(n+1)]

    return(xPlot, yPlot, yUnit)


def helpBtn(self):
    msg = ft.QMessageBox(self)
    msg.setText("""Manual Tracking allows you to track a flame with a point-and-click method.

    'Tracking points #' defines the number of mouse clicks to record for each frame before moving to the next one (the default is one click per frame). By clicking on 'Start tracking', a pop-up window will show the first frame (press 'Esc' to exit at any time, but note that the progress will be lost). The following frames will show the horizontal lines corresponding to the points clicked. These lines can be hidden by unchecking 'Show tracking lines' before starting the analysis. After the tracking, the position vs time and spread rate vs time values will be shown in the windows in the 'Analysis box' when the slider in the 'Preview box' is used. The 'Flame direction' determines the positive increment of the flame location along the horizontal coordinate.

    If there is a flashing or strobe light in the recorded video, you can click on 'Pick bright region' to choose a rectangular region (in the same way that the ROI is selected) that is illuminated when the light is on and dark when it is off. Note that this region is independent from the ROI specified in the 'Preview box', and will show up of the left window in the 'Analysis box'. From the dropdown menu, select the option 'Frames light on' to consider only the frames where the light is on, or 'Frames light off' to consider only the frames without the light. By default all the frames are considered.

    By clicking on 'Absolute values', the first point/frame will be used as the origin in the plots.

    Click on 'Save data' to export a csv file with all the tracking results (position in pixel and mm for each point tracked, and their corresponding spread rate).
    """)
    msg.exec()
