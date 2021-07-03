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

from flameTracker import *

def createManualTrackingBox(self):
    manualTrackingBox = QGroupBox(' ', self.analysisGroupBox)
    manualTrackingBox.setGeometry(0,0, 1050, 390)
    manualTrackingBox.setStyleSheet('background-color: None')

    #first column
    x_cln1 = 10
    x_cln2 = 120
    h_txt = 30
    h_btn = 30
    h_lbl = 22
    w_cln1 = 80
    w_cln2 = 50
    directionBoxTxt = QLabel('Flame direction:', manualTrackingBox)
    directionBoxTxt.setGeometry(x_cln1, 20, 100, h_txt)
    self.directionBox = QComboBox(manualTrackingBox)
    self.directionBox.setGeometry(x_cln1 - 5, 45, 150, h_btn)
    self.directionBox.addItem('Left to right')
    self.directionBox.addItem('Right to left')
    self.directionBox.activated.connect(self.directionMT_clicked)
    lightTxt = QLabel('Flashing light (optional):', manualTrackingBox)
    lightTxt.setGeometry(x_cln1, 70, 150, h_txt)
    self.filterLight = QComboBox(manualTrackingBox)
    self.filterLight.setGeometry(x_cln1 - 5, 95, 150, h_btn)
    self.filterLight.addItem('Track every frame')
    self.filterLight.addItem('Frames light on')
    self.filterLight.addItem('Frames light off')
    self.filterLight.activated.connect(self.filterLightMT_clicked)
    nClicksTxt = QLabel('Tracking points #:', manualTrackingBox)
    nClicksTxt.setGeometry(x_cln1, 125, 100, h_txt)
    self.nClicksLbl = QLineEdit('1', manualTrackingBox)
    self.nClicksLbl.setGeometry(x_cln2, 129, 30, h_lbl)
    self.showEdges_MT = QCheckBox('Show tracking lines', manualTrackingBox)
    self.showEdges_MT.setGeometry(x_cln1, 150, 140, h_btn)
    self.showEdges_MT.setChecked(True)
    self.manualTrackingBtn = QPushButton('Start Tracking', manualTrackingBox)
    self.manualTrackingBtn.setGeometry(x_cln1 - 5, 180, 150, h_btn)
    self.manualTrackingBtn.clicked.connect(self.manualTrackingBtn_clicked)
    self.absValBtn = QPushButton('Absolute values', manualTrackingBox)
    self.absValBtn.setGeometry(x_cln1 - 5, 210, 150, h_btn)
    self.absValBtn.clicked.connect(self.absValBtnMT_clicked)
    self.save_MT_Btn = QPushButton('Save data', manualTrackingBox)
    self.save_MT_Btn.setGeometry(x_cln1 - 5, 240, 150, h_btn)
    self.save_MT_Btn.clicked.connect(self.saveData_clicked)
    self.helpBtn_MT = QPushButton('Help', manualTrackingBox)
    self.helpBtn_MT.setGeometry(x_cln1 - 5, 270, 150, h_btn)
    self.helpBtn_MT.clicked.connect(self.helpBtn_MT_clicked)

    # first label
    self.label1 = pg.PlotWidget(manualTrackingBox)
    self.label1.setGeometry(190, 25, 420, 300)
    self.label1.setBackground('w')
    self.label1.setLabel('left', 'Position [mm]', color='black', size=14)
    self.label1.setLabel('bottom', 'Time [s]', color='black', size=14)
    self.label1.getAxis('bottom').setPen(color=(0, 0, 0))
    self.label1.getAxis('left').setPen(color=(0, 0, 0))

    # second label
    self.label2 = pg.PlotWidget(manualTrackingBox)
    self.label2.setGeometry(620, 25, 420, 300)
    self.label2.setBackground('w')
    self.label2.setLabel('left', 'Spread Rate [mm/s]', color='black', size=14)
    self.label2.setLabel('bottom', 'Time [s]', color='black', size=14)
    self.label2.getAxis('bottom').setPen(color=(0, 0, 0))
    self.label2.getAxis('left').setPen(color=(0, 0, 0))

    # these are default values for the relative selections
    self.flameDir = 'toRight'
    self.lightStatus = 'None'

    manualTrackingBox.show()

def manualTracking(self):
    firstFrame = int(self.firstFrameIn.text())
    lastFrame = int(self.lastFrameIn.text())
    roiOne = int(self.roiOneIn.text())
    roiTwo = int(self.roiTwoIn.text())
    roiThree = int(self.roiThreeIn.text())
    roiFour = int(self.roiFourIn.text())
    scale = True

    #Set up the first frame for analysis and clk for the mouse event
    currentFrame = firstFrame
    global clk

    clk = False # False unless the mouse is clicked
    posX = dict()
    posX_mm = dict()
    posY = dict()
    posY_mm = dict()
    frameCount = dict()
    timeCount = dict()

    # find out how many points to be selected in each frame
    try:
        self.nClicks = int(self.nClicksLbl.text())
    except:
        self.nClicks = 1
        self.msgLabel.setText('Clicks not specified (=1)')

    while (currentFrame < lastFrame):
        if not self.scaleIn.text():
            scale = False
            msg = QMessageBox(self)
            msg.setText('The scale [px/mm] has not been specified')
            msg.exec_()
            break

        if self.openSelection == 'video':
            self.fVideo.set(1, int(currentFrame))
            ret, frame = self.fVideo.read()
        elif self.openSelection == 'image(s)':
            frame = self.imagesList[int(currentFrame)]
            frame = cv2.imread(frame)

        try:
            if self.perspectiveValue == True:
                if self.rotationValue == True:
                    frame = rotationCorrection_LT(self, frame, self.anglePerspective)
                frame = perspectiveCorrectionMT(self, frame)
                #the rotation has already been included in the perspective correction, but it could happen that a further rotation is needed after the correction (e.g. for the analysis)
                if self.anglePerspective != float(self.rotationAngleIn.text()):
                    angle = float(self.rotationAngleIn.text()) - self.anglePerspective
                    frame = rotationCorrection_MT(self, frame, angle)
            elif float(self.rotationAngleIn.text()) != 0: #in case there is no perspective correction
                    angle = float(self.rotationAngleIn.text())
                    frame = rotationCorrection_MT(self, frame, angle)
            if self.brightnessLbl.text() != '0' or self.contrastLbl.text() != '0':
                frameContainer = np.zeros(frame.shape, frame.dtype)
                alpha = (int(self.contrastSlider.value()) + 100) * 2 / 200
                beta = int(self.brightnessSlider.value())    # Simple brightness control [0-100]. Instead, we have [-50-50]
                frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
            if self.grayscale.isChecked() == True: #the YCC lines below cannot execute in the Gray single channel
                frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except:
            pass

        # crop image
        frameCrop = frame[roiTwo : (roiTwo + roiFour), roiOne : (roiOne + roiThree)]

        #filtering the frames with the light on by considering the luma image (full code and comments in lumaTracking)
        frameYCC = cv2.cvtColor(frameCrop, cv2.COLOR_BGR2YCR_CB)
        Y, C, C = cv2.split(frameYCC)
        (thresh, frameBW) = cv2.threshold(Y, 40, 255, cv2.THRESH_BINARY) #40 = threshold
        noise_px = np.ones((3,3), np.uint8)
        frameBW = cv2.morphologyEx(frameBW, cv2.MORPH_OPEN, noise_px)
        flamePx = np.where(frameBW == [255])
        roiArea = Y.shape[0] * Y.shape[1] # roiThree * roiFour #
        # this condition skips frames if more than half area is illuminated by the light
        if self.lightStatus == 'lightOff':
            if len(flamePx[0]) > 0.5 * roiArea:
                currentFrame = currentFrame + 1 + int(self.skipFrameIn.text())
                continue
        elif self.lightStatus == 'lightOn':
            if len(flamePx[0]) < 0.5 * roiArea:
                currentFrame = currentFrame + 1 + int(self.skipFrameIn.text())
                continue

        if self.grayscale.isChecked() == True:
            frameCrop = frameGray[roiTwo : (roiTwo + roiFour), roiOne : (roiOne + roiThree)]

        # create the window and the line over the first point clicked
        cv2.namedWindow('manualTracking', cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback('manualTracking', click)

        if currentFrame > firstFrame:
            for n in range(self.nClicks):
                if self.showEdges_MT.isChecked() == True:
                    try:
                        cv2.line(frameCrop, (0, int(posY[str(n+1)][0])),(roiThree, int(posY[str(n+1)][0])), (0, 245, 184), 2)
                    except:
                        pass

        cv2.imshow('manualTracking',frameCrop)

        self.msgLabel.setText('Start tracking, press (Esc) to quit.')
        for n in range(self.nClicks):
            # wait for the mouse event or 'escape' key
            while (True):
                if clk == True:
                    clk = False
                    # the zero location changes based on the flame direction
                    if self.flameDir == 'toRight':
                        xClick = xPos + roiOne
                    elif self.flameDir == 'toLeft':
                        xClick = self.vWidth - roiOne - xPos
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
    # smoothing of the spread rate values
    self.spreadRate = dict()
    if scale:
        for n in range(self.nClicks):
            for i in range(len(timeCount['1'])-1):
                xCoeff = np.polyfit(timeCount['1'][(i):(i + 2)], posX_mm[str(n+1)][(i):(i + 2)], 1)
                spreadRate = xCoeff[0]
                if str(n+1) in self.spreadRate:
                    self.spreadRate[str(n+1)].append(spreadRate)
                else:
                    self.spreadRate[str(n+1)] = [spreadRate]
            #repeat the last value
            self.spreadRate[str(n+1)].append(xCoeff[0])

        # plotting code adjusted from lumaTracking
        self.label1.clear()
        self.label2.clear()
        self.label1.addLegend(offset = [1, 0.1]) # background color modified in line 122 and 123 of python3.7/site-packages/pyqtgraph/graphicsItems
        self.label2.addLegend(offset = [1, 0.1])
        color = ['b', 'r', 'k', 'g', 'c', 'y']
        for n in range(self.nClicks):
            name = 'click{}'.format([n+1])
            try:
                clr = color[n]
            except:
                if n > len(color):
                    self.msgLabel.setText('Not enough colors for plotting.')
            manualTrackingPlot(self.label1, self.time_plot['1'], self.posX_plot[str(n+1)], name, 'o', clr)
            manualTrackingPlot(self.label2, self.time_plot['1'], self.spreadRate[str(n+1)], name, 'o', clr)

def absValueMT(self):
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

      self.label1.clear()
      self.label2.clear()
      color = ['b', 'r', 'k', 'g', 'c', 'y']
      for n in range(self.nClicks):
          name = 'click{}'.format([n+1])
          try:
              clr = color[n]
          except:
              if n > len(color):
                  self.msgLabel.setText('Not enough colors for plotting.')
          manualTrackingPlot(self.label1, self.time_plot['1'], self.posX_plot[str(n+1)], '', 'o', clr)
          manualTrackingPlot(self.label2, self.time_plot['1'], self.spreadRate[str(n+1)], '', 'o', clr)

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

def chooseFlameDirection_MT(self, text):
    selection = self.directionBox.currentText()
    if selection == 'Left to right':
        self.flameDir = 'toRight'
    elif selection == 'Right to left':
        self.flameDir = 'toLeft'

def chooseLightFilterMT(self, text):
    selection = self.filterLight.currentText()
    if selection == 'Track every frame':
        self.lightStatus = 'None'
    elif selection == 'Frames light on':
        self.lightStatus = 'lightOn'
    elif selection == 'Frames light off':
        self.lightStatus = 'lightOff'

def perspectiveCorrectionMT(self, frame):
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

def rotationCorrection_MT(self, frame, angle):
    # rotation matrix:
    width = int(self.vWidth)
    height = int(self.vHeight)
    center = (width/2, height/2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1) #center of rotation, angle, zoom In/zoom Out
    # rotation calculates the cos and sin, taking absolutes of those (these extra steps are used to avoid cropping )
    abs_cos = abs(matrix[0,0])
    abs_sin = abs(matrix[0,1])
    # find the new width and height bounds
    region_w = int(height * abs_sin + width * abs_cos)
    region_h = int(height * abs_cos + width * abs_sin)
    # subtract old image center (bringing image back to origo) and adding the new image center coordinates
    matrix[0, 2] += region_w/2 - center[0]
    matrix[1, 2] += region_h/2 - center[1]
    frame = cv2. warpAffine(frame, matrix, (region_w, region_h)) #resolution is specified
    return(frame)

def saveData_ManualTracking(self):
    fileName = QFileDialog.getSaveFileName(self, 'Save tracking data')
    fileName = fileName[0]
    if not fileName[-4:] == '.csv':
        fileName = fileName + '.csv'

    try:
        lbl = ['Frame', 'Time [s]']
        rows = [self.frames_plot['1'], self.time_plot['1']]

        for n in range(int(self.nClicksLbl.text())):
            lbl.append('xPos_click{} [px]'.format([n+1]))
            rows.append(self.posX_px[str(n+1)])
            lbl.append('xPos_click{} [mm]'.format([n+1]))
            rows.append(np.round((self.posX_plot[str(n+1)]), 2))
            lbl.append('Vf_click{}'.format([n+1]))
            rows.append(self.spreadRate[str(n+1)])

        rows_zip = zip(*rows)
    except:
        self.msgLabel.setText('Ops! Something went wrong with the click recordings.')

    if fileName == '.csv': #this prevents name issues when the user closes the dialog without saving
        self.msgLabel.setText('Ops! The values were not saved.')
    else:
        try:
            with open(fileName, 'w', newline = '') as csvfile:
                writer = csv.writer(csvfile, delimiter = ',')
                writer.writerow(['File', self.fNameLbl.text()])
                writer.writerow(['Scale [px/mm]', self.scaleIn.text()])
                writer.writerow(['Flame direction:', self.flameDir])
                writer.writerow(lbl)
                for row in rows_zip:
                    writer.writerow(row)
            self.msgLabel.setText('Data successfully saved.')
        except:
            notParameters_dlg = QErrorMessage(self)
            notParameters_dlg.showMessage('Ops! Something went wrong, the values were not saved.')
            self.msgLabel.setText('Data not saved.')

def helpBtn_MT(self):
    msg = QMessageBox(self)
    msg.setText("""In Manual Tracking you can specify the number of points you want to track (the default is 1), and the spreading direction of the flame. If there is a flashing light in the video, the option 'Frames light on' allows to consider only the frames where it is on, whereas 'Frames light off' will consider only frames without the light. If nothing is selected, all frames are considered. Note: when the light option is used, the program discards frames based on the luminance intensity of the pixels in the ROI, therefore the ROI area should be selected accordingly.

    With 'Start Tracking' the frames will show up in a new window (press 'Esc' to exit at any time), and horizontal lines corresponding to the points clicked on the first frame will show up in the following frames (they can be hidden by unchecking 'Show tracking lines'). After the tracking, the position vs time and spread rate values will be shown in the labels.

    By clicking on 'Absolute values', the same data will be shifted in order to start from zero.

    'Save data' will create a csv file with all the tracked information.
    """)
    msg.exec_()
