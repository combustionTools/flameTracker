"""
Flame Tracker. This program is designed to track flames or bright objects in videos or images.
Copyright (C) 2021 Charles Scudiere; 2021  Luca Carmignani

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

from flameTracker import *

def createHSVTrackingBox(self):
    self.HSVTrackingValue = True
    self.HSVTrackingBox = QGroupBox(' ', self.analysisGroupBox)
    self.HSVTrackingBox.setGeometry(0, 0, 1050, 390)
    self.HSVTrackingBox.setStyleSheet('background-color: None')

    h_btn = 30
    h_txt = 30
    h_lbl = 22
    w_btn2 = 30
    #first column
    x_cln1 = 10
    directionBoxTxt = QLabel('Flame direction:', self.HSVTrackingBox)
    directionBoxTxt.setGeometry(x_cln1, 20, 100, h_txt)
    self.directionBox = QComboBox(self.HSVTrackingBox)
    self.directionBox.setGeometry(x_cln1 - 5, 45, 150, h_btn)
    self.directionBox.addItem('Left to right')
    self.directionBox.addItem('Right to left')
    self.directionBox.activated.connect(self.directionHT_clicked)
    hueChannelTxt = QLabel('Hue:', self.HSVTrackingBox)
    hueChannelTxt.setGeometry(x_cln1, 70, 100, h_txt)
    hueMinTxt = QLabel('Min:', self.HSVTrackingBox)
    hueMinTxt.setGeometry(x_cln1, 92, 80, h_txt)
    self.hueMinLeftBtn_HT = QPushButton('<', self.HSVTrackingBox)
    self.hueMinLeftBtn_HT.setGeometry(35, 90, w_btn2, h_btn)
    self.hueMinLeftBtn_HT.clicked.connect(self.hueMinLeftBtn_HT_clicked)
    self.hueMinRightBtn_HT = QPushButton('>', self.HSVTrackingBox)
    self.hueMinRightBtn_HT.setGeometry(175, 90, w_btn2, h_btn)
    self.hueMinRightBtn_HT.clicked.connect(self.hueMinRightBtn_HT_clicked)
    # CAS slider setting:
    self.hueMinSlider = QSlider(Qt.Horizontal, self.HSVTrackingBox)
    self.hueMinSlider.setGeometry(60, 95, 120, 25)
    self.hueMinSlider.setMinimum(0)
    #self.hueMinSlider.setMaximum(255)
    self.hueMinSlider.setMaximum(180) # since stored as H/2 for 8-bit (normally 0-360)
    #self.hueMinSlider.setValue(10)
    self.hueMinSlider.setValue(80) # Default to include blue values - 92=~185 deg Min Hue
    self.hueMinSlider.sliderReleased.connect(self.singleHSVSlider_released)
    self.hueMinSlider.valueChanged.connect(self.singleHSVSlider_released) #LC We need to check this. I had to remove one from the other files (changed or released) because on Mac it counts twice
    hueMaxTxt = QLabel('Max:', self.HSVTrackingBox)
    hueMaxTxt.setGeometry(x_cln1, 114, 100, h_txt)
    self.hueMaxLeftBtn_HT = QPushButton('<', self.HSVTrackingBox)
    self.hueMaxLeftBtn_HT.setGeometry(35, 112, w_btn2, h_btn)
    self.hueMaxLeftBtn_HT.clicked.connect(self.hueMaxLeftBtn_HT_clicked)
    self.hueMaxRightBtn_HT = QPushButton('>', self.HSVTrackingBox)
    self.hueMaxRightBtn_HT.setGeometry(175, 112, w_btn2, h_btn)
    self.hueMaxRightBtn_HT.clicked.connect(self.hueMaxRightBtn_HT_clicked)
    # CAS slider setting:
    self.hueMaxSlider = QSlider(Qt.Horizontal, self.HSVTrackingBox)
    self.hueMaxSlider.setGeometry(60, 117, 120, 25)
    self.hueMaxSlider.setMinimum(0)
    #self.hueMaxSlider.setMaximum(255)
    self.hueMaxSlider.setMaximum(180) # since stored as H/2 for 8-bit (normally 0-360)
    #self.hueMaxSlider.setValue(255)
    self.hueMaxSlider.setValue(163) # Default to include blue values - 130=~260 deg Max Hue
    self.hueMaxSlider.sliderReleased.connect(self.singleHSVSlider_released)
    self.hueMaxSlider.valueChanged.connect(self.singleHSVSlider_released)
    satChannelTxt = QLabel('Saturation:', self.HSVTrackingBox)
    satChannelTxt.setGeometry(x_cln1, 140, 100, h_txt)
    satMinTxt = QLabel('Min:', self.HSVTrackingBox)
    satMinTxt.setGeometry(x_cln1, 162, 100, h_txt)
    self.satMinLeftBtn_HT = QPushButton('<', self.HSVTrackingBox)
    self.satMinLeftBtn_HT.setGeometry(35, 160, w_btn2, h_btn)
    self.satMinLeftBtn_HT.clicked.connect(self.satMinLeftBtn_HT_clicked)
    self.satMinRightBtn_HT = QPushButton('>', self.HSVTrackingBox)
    self.satMinRightBtn_HT.setGeometry(175, 160, w_btn2, h_btn)
    self.satMinRightBtn_HT.clicked.connect(self.satMinRightBtn_HT_clicked)
    # CAS slider setting:
    self.satMinSlider = QSlider(Qt.Horizontal, self.HSVTrackingBox)
    self.satMinSlider.setGeometry(60, 165, 120, 25)
    self.satMinSlider.setMinimum(0)
    self.satMinSlider.setMaximum(255)
    #self.satMinSlider.setValue(10)
    self.satMinSlider.setValue(30) # Default to include blue values - 100=~40% min Saturation
    self.satMinSlider.sliderReleased.connect(self.singleHSVSlider_released)
    self.satMinSlider.valueChanged.connect(self.singleHSVSlider_released)
    satMaxTxt = QLabel('Max:', self.HSVTrackingBox)
    satMaxTxt.setGeometry(x_cln1, 184, 100, h_txt)
    self.satMaxLeftBtn_HT = QPushButton('<', self.HSVTrackingBox)
    self.satMaxLeftBtn_HT.setGeometry(35, 182, w_btn2, h_btn)
    self.satMaxLeftBtn_HT.clicked.connect(self.satMaxLeftBtn_HT_clicked)
    self.satMaxRightBtn_HT = QPushButton('>', self.HSVTrackingBox)
    self.satMaxRightBtn_HT.setGeometry(175, 182, w_btn2, h_btn)
    self.satMaxRightBtn_HT.clicked.connect(self.satMaxRightBtn_HT_clicked)
    # CAS slider setting:
    self.satMaxSlider = QSlider(Qt.Horizontal, self.HSVTrackingBox)
    self.satMaxSlider.setGeometry(60, 187, 120, 25)
    self.satMaxSlider.setMinimum(0)
    self.satMaxSlider.setMaximum(255)
    #self.satMaxSlider.setValue(255)
    self.satMaxSlider.setValue(255) # Default to some blue value - 255=~100% max Saturation
    self.satMaxSlider.sliderReleased.connect(self.singleHSVSlider_released)
    self.satMaxSlider.valueChanged.connect(self.singleHSVSlider_released)
    valChannelTxt = QLabel('Value:', self.HSVTrackingBox)
    valChannelTxt.setGeometry(x_cln1, 210, 100, h_txt)
    valMinTxt = QLabel('Min:', self.HSVTrackingBox)
    valMinTxt.setGeometry(x_cln1, 232, 100, h_txt)
    self.valMinLeftBtn_HT = QPushButton('<', self.HSVTrackingBox)
    self.valMinLeftBtn_HT.setGeometry(35, 230, w_btn2, h_btn)
    self.valMinLeftBtn_HT.clicked.connect(self.valMinLeftBtn_HT_clicked)
    self.valMinRightBtn_HT = QPushButton('>', self.HSVTrackingBox)
    self.valMinRightBtn_HT.setGeometry(175, 230, w_btn2, h_btn)
    self.valMinRightBtn_HT.clicked.connect(self.valMinRightBtn_HT_clicked)
    # CAS slider setting:
    self.valMinSlider = QSlider(Qt.Horizontal, self.HSVTrackingBox)
    self.valMinSlider.setGeometry(60, 235, 120, 25)
    self.valMinSlider.setMinimum(0)
    self.valMinSlider.setMaximum(255)
    self.valMinSlider.setValue(20) # Default to some blue value - 63=~25% min Value
    self.valMinSlider.sliderReleased.connect(self.singleHSVSlider_released)
    self.valMinSlider.valueChanged.connect(self.singleHSVSlider_released)
    valMaxTxt = QLabel('Max:', self.HSVTrackingBox)
    valMaxTxt.setGeometry(x_cln1, 254, 100, h_txt)
    self.valMaxLeftBtn_HT = QPushButton('<', self.HSVTrackingBox)
    self.valMaxLeftBtn_HT.setGeometry(35, 252, w_btn2, h_btn)
    self.valMaxLeftBtn_HT.clicked.connect(self.valMaxLeftBtn_HT_clicked)
    self.valMaxRightBtn_HT = QPushButton('>', self.HSVTrackingBox)
    self.valMaxRightBtn_HT.setGeometry(175, 252, w_btn2, h_btn)
    self.valMaxRightBtn_HT.clicked.connect(self.valMaxRightBtn_HT_clicked)
    # CAS slider setting:
    self.valMaxSlider = QSlider(Qt.Horizontal, self.HSVTrackingBox)
    self.valMaxSlider.setGeometry(60, 257, 120, 25)
    self.valMaxSlider.setMinimum(0)
    self.valMaxSlider.setMaximum(255)
    #self.valMaxSlider.setValue(255)
    self.valMaxSlider.setValue(255) # Default to some blue value - 255=~100% max Value
    self.valMaxSlider.sliderReleased.connect(self.singleHSVSlider_released)
    self.valMaxSlider.valueChanged.connect(self.singleHSVSlider_released)

    # May Move to xxxTrackingBox_OS
    filterParticleTxt = QLabel('Filter particles size:', self.HSVTrackingBox)
    filterParticleTxt.setGeometry(x_cln1, 280, 150, h_txt)
    self.filterParticleSldr_HT = QSlider(Qt.Horizontal, self.HSVTrackingBox)
    self.filterParticleSldr_HT.setGeometry(10, 305, 170, 25)
    self.filterParticleSldr_HT.setMinimum(1)
    self.filterParticleSldr_HT.setMaximum(1000)
    self.filterParticleSldr_HT.setValue(20) #	was defulted to 10, but experience says around ~1228 or ~350 to not filter too much
    self.filterParticleSldr_HT.sliderReleased.connect(self.filterParticleSldr_HT_released)

    avgLE_txt = QLabel('#px to locate edges:', self.HSVTrackingBox)
    avgLE_txt.setGeometry(x_cln1, 330, 140, h_txt)
    self.avgLEIn_HT = QLineEdit('10', self.HSVTrackingBox) #was defaulted to 1, but experience says around 5-10
    self.avgLEIn_HT.setGeometry(x_cln1 + 135, 334, 30, h_lbl)
    connectivityTxt = QLabel('Connectivity (px):', self.HSVTrackingBox)
    connectivityTxt.setGeometry(x_cln1, 360, 100, h_txt)
    self.connectivityBox = QComboBox(self.HSVTrackingBox)
    self.connectivityBox.setGeometry(x_cln1 + 110, 360, 60, h_btn)
    self.connectivityBox.addItem('4')
    self.connectivityBox.addItem('8')
    self.connectivityBox.activated.connect(self.connectivityBoxHT_clicked)

    #second column
    x_cln1 = 220
    self.saveChannelsBtn_HT = QPushButton('Save filter values', self.HSVTrackingBox)
    self.saveChannelsBtn_HT.setGeometry(x_cln1 - 10, 30, 150, h_btn)
    self.saveChannelsBtn_HT.clicked.connect(self.saveChannelsBtn_HT_clicked)
    self.loadChannelsBtn_HT = QPushButton('Load filter values', self.HSVTrackingBox)
    self.loadChannelsBtn_HT.setGeometry(x_cln1 - 10, 60, 150, h_btn)
    self.loadChannelsBtn_HT.clicked.connect(self.loadChannelsBtn_HT_clicked)
    self.helpBtn_HT = QPushButton('Help', self.HSVTrackingBox)
    self.helpBtn_HT.setGeometry(x_cln1 - 10, 90, 150, h_btn)
    self.helpBtn_HT.clicked.connect(self.helpBtn_HT_clicked)
    trackingTxt = QLabel('Flame tracking:', self.HSVTrackingBox)
    trackingTxt.setGeometry(x_cln1, 120, 120, h_txt)
    self.filterLight_HT = QCheckBox('Ignore flashing light', self.HSVTrackingBox)
    self.filterLight_HT.setGeometry(x_cln1, 145, 135, h_btn)
    movAvgTxt = QLabel('Moving avg points:', self.HSVTrackingBox)
    movAvgTxt.setGeometry(x_cln1, 170, 130, h_txt)
    self.movAvgIn_HT = QLineEdit('5', self.HSVTrackingBox) #was defaulted to 2, experience says around 5 better
    self.movAvgIn_HT.setGeometry(x_cln1 + 105, 174, 30, h_lbl)
    self.HSVTrackingBtn = QPushButton('Start tracking', self.HSVTrackingBox)
    self.HSVTrackingBtn.setGeometry(x_cln1 - 10, 200, 150, h_btn)
    self.HSVTrackingBtn.clicked.connect(self.HSVTrackingBtn_clicked)
    self.absValBtn_HT = QPushButton('Absolute values', self.HSVTrackingBox)
    self.absValBtn_HT.setGeometry(x_cln1 - 10, 230, 150, h_btn)
    self.absValBtn_HT.clicked.connect(self.absValBtn_HT_clicked)
    self.saveBtn_HT = QPushButton('Save data', self.HSVTrackingBox)
    self.saveBtn_HT.setGeometry(x_cln1 - 10, 260, 150, h_btn)
    self.saveBtn_HT.clicked.connect(self.saveBtn_HT_clicked)

    # Add time/frame plotting toggle - CAS
    self.isPlotTimevsFrame = False #True

    # first label
    self.lbl1_HT = QLabel(self.HSVTrackingBox)
    #self.lbl1_HT.setGeometry(370, 25, 330, 250)
    self.lbl1_HT.setGeometry(370, 25, 670, 125) # Changed geometry as removed BW image display
    self.lbl1_HT.setStyleSheet('background-color: white')
    self.showEdges = QCheckBox('Show edges location', self.HSVTrackingBox)
    self.showEdges.setGeometry(780, 275, 135, h_btn)
    self.showEdges.setChecked(True)
    self.exportEdges_HT = QCheckBox('Output video analysis', self.HSVTrackingBox)
    self.exportEdges_HT.setGeometry(780, 300, 135, h_btn)
    #CAS Export with tracking line
    self.exportTrackOverlay_HT = QCheckBox('Video Tracking Overlay', self.HSVTrackingBox)
    self.exportTrackOverlay_HT.setGeometry(780, 325, 200, h_btn)



    # second label
    self.lbl2_HT = QLabel(self.HSVTrackingBox)
    #self.lbl2_HT.setGeometry(710, 25, 330, 250)
    self.lbl2_HT.setGeometry(370, 150, 670, 125)
    self.lbl2_HT.setStyleSheet('background-color: white')
    self.showFrameLargeBtn_HT = QPushButton('Show frames', self.HSVTrackingBox)
    self.showFrameLargeBtn_HT.setGeometry(930, 275, 115, h_btn)
    self.showFrameLargeBtn_HT.clicked.connect(self.showFrameLargeBtn_HT_clicked)

    self.flameDir = 'toRight'
    self.connectivity_HT = 4
    self.HSVTrackingValue = True

    self.HSVTrackingBox.show()

def getHSVFilteredFrame(self, frameNumber):
    if self.openSelection == 'video':
        self.fVideo.set(1, frameNumber)
        ret, frame = self.fVideo.read()
    elif self.openSelection == 'image(s)':
        frame = self.imagesList[int(frameNumber)]
        frame = cv2.imread(frame)

    if self.perspectiveValue == True:
        if self.rotationValue == True:
            frame = rotationCorrection_HT(self, frame, self.anglePerspective)
        frame = perspectiveCorrectionHT(self, frame)
        #the rotation has already been included in the perspective correction, but it could happen that a further rotation is needed after the correction (e.g. for the analysis)
        if self.anglePerspective != float(self.rotationAngleIn.text()):
            angle = float(self.rotationAngleIn.text()) - self.anglePerspective
            frame = rotationCorrection_HT(self, frame, angle)
    elif float(self.rotationAngleIn.text()) != 0: #in case there is no perspective correction
            angle = float(self.rotationAngleIn.text())
            frame = rotationCorrection_HT(self, frame, angle)
    if int(self.brightnessSlider.value()) != 0 or int(self.contrastSlider.value()) != 0:
        frameContainer = np.zeros(frame.shape, frame.dtype)
        alpha = (int(self.contrastSlider.value()) + 100) * 2 / 200
        beta = int(self.brightnessSlider.value())    # Simple brightness control [0-100]. Instead, we have [-50-50]
        frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    # crop frame (after rotation)
    #frameCrop = frame[int(self.roiTwoIn.text()) : (int(self.roiTwoIn.text()) + int(self.roiFourIn.text())), int(self.roiOneIn.text()) : (int(self.roiOneIn.text()) + int(self.roiThreeIn.text()))]
    self.frameCrop = frame[int(self.roiTwoIn.text()) : (int(self.roiTwoIn.text()) + int(self.roiFourIn.text())), int(self.roiOneIn.text()) : (int(self.roiOneIn.text()) + int(self.roiThreeIn.text()))]

    # Filter here: #CAS Modified for HSV tracking instead of color tracking
    valLow = self.valMinSlider.value()
    valHigh = self.valMaxSlider.value()
    satLow = self.satMinSlider.value()
    satHigh = self.satMaxSlider.value()
    hueLow = self.hueMinSlider.value()
    hueHigh = self.hueMaxSlider.value()
    low = ([hueLow, satLow, valLow])
    high = ([hueHigh, satHigh, valHigh])
    low = np.array(low, dtype = 'uint8') #this conversion is necessary
    high = np.array(high, dtype = 'uint8')
    #newMask = cv2.inRange(frameCrop, low, high)
    newMask = cv2.inRange(cv2.cvtColor(self.frameCrop, cv2.COLOR_BGR2HSV), low, high)
    frame = cv2.bitwise_and(self.frameCrop, self.frameCrop, mask = newMask)
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    (threshold, frameBW) = cv2.threshold(grayFrame, 0, 255, cv2.THRESH_BINARY)

    # Find all the connected components (8 means in the four directions and diagonals)
    componentNum, componentLbl, stats, centroids = cv2.connectedComponentsWithStats(frameBW, connectivity = self.connectivity_HT)
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

    flamePx = np.where(frameBW == [255]) # total area in px

    if self.filterLight_HT.isChecked() == True:
        if len(flamePx[0]) < 0.5 * (int(self.roiThreeIn.text()) * int(self.roiFourIn.text())): #flamePx[0] = x; flamePx[1] = y
            findFlameEdges_HT(self, frameBW, flamePx)
    else:
        findFlameEdges_HT(self, frameBW, flamePx)

    if self.showEdges.isChecked() == True:
        cv2.line(frame, (self.xMax, 0),(self.xMax, int(self.roiFourIn.text())), (255, 255, 255), 2)
        cv2.line(frame, (self.xMin, 0),(self.xMin, int(self.roiFourIn.text())), (255, 255, 255), 2)
        cv2.line(frameBW, (self.xMax, 0),(self.xMax, int(self.roiFourIn.text())), (255, 255, 255), 2)
        cv2.line(frameBW, (self.xMin, 0),(self.xMin, int(self.roiFourIn.text())), (255, 255, 255), 2)

    self.currentFrameRGB_HT = frame
    # calculate the total number of bytes in the frame for lbl1
    totalBytes = frame.nbytes
    # divide by the number of rows
    bytesPerLine = int(totalBytes/frame.shape[0]) #I had to introduce it to avoid distortion in the opened file for some of the videos
    self.frame = QImage(frame.data, frame.shape[1], frame.shape[0], bytesPerLine, QImage.Format_BGR888)#.rgbSwapped() #shape[0] = height, [1] = width QImage.Format_Indexed8 BGR888
    self.frame = self.frame.scaled(self.lbl1_HT.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

    self.currentFrameBW_HT = frameBW
    # calculate the total number of bytes in the frame for lbl2
    totalBytesBW = frameBW.nbytes
    # divide by the number of rows
    bytesPerLineBW = int(totalBytesBW/frameBW.shape[0]) #I had to introduce it to avoid distortion in the opened file for some of the videos
    self.frameBW = QImage(frameBW.data, frameBW.shape[1], frameBW.shape[0], bytesPerLineBW, QImage.Format_Grayscale8)#.rgbSwapped() #shape[0] = height, [1] = width QImage.Format_Indexed8 or Grayscale8 BGR888
    self.frameBW = self.frameBW.scaled(self.lbl1_HT.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

def findFlameEdges_HT(self, frameBW, flamePx):
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
        if self.flameDir == 'toRight':
            self.xRight = int(self.roiOneIn.text()) + self.xMax
            self.xLeft = int(self.roiOneIn.text()) + self.xMin
        elif self.flameDir == 'toLeft':
            self.xRight = self.vWidth - int(self.roiOneIn.text()) - self.xMax
            self.xLeft = self.vWidth - int(self.roiOneIn.text()) - self.xMin
    except:
        self.msgLabel.setText('Flame not found in some frames')

def HSVTracking(self):
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

    if self.exportEdges_HT.isChecked() or self.exportTrackOverlay_HT.isChecked():
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
        import numpy #CAS Added for tracking line
        while (currentFrame < lastFrame):
            getHSVFilteredFrame(self, currentFrame)
            self.xRight_mm.append(self.xRight / float(self.scaleIn.text()))
            self.xLeft_mm.append(self.xLeft / float(self.scaleIn.text()))
            flameArea.append(self.flameArea)
            self.frameCount.append(currentFrame)
            if self.exportEdges_HT.isChecked() and not self.exportTrackOverlay_HT.isChecked():
                vout.write(self.currentFrameRGB_HT)
            elif self.exportTrackOverlay_HT.isChecked():
                #CAS Add Track lines over cropped video
                trackframe = numpy.copy(self.frameCrop) # frame is 1080 x 1920
                trackframe[:, min(self.xRight-1 - int(self.roiOneIn.text()), numpy.size(trackframe,1))] = 255 # white out line to mark where tracked flame, using relative distance
                vout.write(trackframe)

            print('Progress: ', round((currentFrame - firstFrame)/(lastFrame - firstFrame) * 10000)/100, '%')
            currentFrame = currentFrame + 1 + int(self.skipFrameIn.text())

        try:
            self.flameArea = [areaN / (float(self.scaleIn.text())**2) for areaN in flameArea]
            self.flameArea = np.round(self.flameArea, 3)
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

        flameLength_mm = np.round(flameLength_mm, 2)
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

        self.lbl1_HT = pg.PlotWidget(self.HSVTrackingBox)
        #self.lbl1_HT.setGeometry(370, 25, 330, 250)
        self.lbl1_HT.setGeometry(370, 25, 670, 125) # Changed geometry as removed BW image display
        self.lbl1_HT.setBackground('w')
        self.lbl1_HT.setLabel('left', 'Position [mm]', color='black', size=14)
        if self.isPlotTimevsFrame:
            ## Plot in terms of time
            self.lbl1_HT.setLabel('bottom', 'Time [s]', color='black', size=14)
        else:
            ## CAS Plot in terms of frame:
            self.lbl1_HT.setLabel('bottom', 'Frame', color='black', size=14)

        self.lbl1_HT.getAxis('bottom').setPen(color=(0, 0, 0))
        self.lbl1_HT.getAxis('left').setPen(color=(0, 0, 0))
        self.lbl1_HT.addLegend(offset = [1, 0.1]) # background color modified in line 122 and 123 of Versions/3.7/lib/python3.7/site-packages/pyqtgraph/graphicsItems
        self.lbl2_HT = pg.PlotWidget(self.HSVTrackingBox)
        #self.lbl2_HT.setGeometry(710, 25, 330, 250)
        self.lbl2_HT.setGeometry(370, 150, 670, 125) #(370, 25, 670, 250)
        #print('\nView rect=', self.lbl2_HT.viewRect() )
        #print('\nGeometry set to', self.lbl2_HT.viewGeometry())
        self.lbl2_HT.setBackground('w')
        self.lbl2_HT.setLabel('left', 'Spread Rate [mm/s]', color='black', size=14)
        if self.isPlotTimevsFrame:
            ## Plot in terms of time
            self.lbl2_HT.setLabel('bottom', 'Time [s]', color='black', size=14)
        else:
            ## CAS Plot in terms of frame:
            self.lbl2_HT.setLabel('bottom', 'Frame', color='black', size=14)

        self.lbl2_HT.getAxis('bottom').setPen(color=(0, 0, 0))
        self.lbl2_HT.getAxis('left').setPen(color=(0, 0, 0))
        self.lbl2_HT.addLegend(offset = [1, 0.1]) # background color modified in line 122 and 123 of Versions/3.7/lib/python3.7/site-packages/pyqtgraph/graphicsItems

        if self.isPlotTimevsFrame:
            ## Plot in terms of time
            HSVTrackingPlot(self.lbl1_HT, self.timeCount, self.xRight_mm, 'right edge', 'o', 'b')
            HSVTrackingPlot(self.lbl1_HT, self.timeCount, self.xLeft_mm, 'left edge', 't', 'r')
            HSVTrackingPlot(self.lbl2_HT, self.timeCount, self.spreadRateRight, 'right edge', 'o', 'b')
            HSVTrackingPlot(self.lbl2_HT, self.timeCount, self.spreadRateLeft, 'left edge', 't', 'r')
        else:
            ## CAS Plot in terms of frame:
            HSVTrackingPlot(self.lbl1_HT, self.frameCount, self.xRight_mm, 'right edge', 'o', 'b')
            HSVTrackingPlot(self.lbl1_HT, self.frameCount, self.xLeft_mm, 'left edge', 't', 'r')
            HSVTrackingPlot(self.lbl2_HT, self.frameCount, self.spreadRateRight, 'right edge', 'o', 'b')
            HSVTrackingPlot(self.lbl2_HT, self.frameCount, self.spreadRateLeft, 'left edge', 't', 'r')

        print('Showing!')
        self.lbl1_HT.show()
        self.lbl2_HT.show()

def HSVTrackingPlot(label, x, y, name, symbol, color):
    pen = pg.mkPen(color)
    label.plot(x, y, pen = pen, name = name, symbol = symbol, symbolSize = 7, symbolBrush = (color))

def HSVSlider_released(self):
    frame = self.previewSlider.value()
    getHSVFilteredFrame(self, frame)
    self.lbl1_HT.setPixmap(QPixmap.fromImage(self.frame))
    self.lbl2_HT.setPixmap(QPixmap.fromImage(self.frameBW))

def filterParticleSldr_HT(self):
    frame = self.previewSlider.value()
    getHSVFilteredFrame(self, frame)
    self.lbl1_HT.setPixmap(QPixmap.fromImage(self.frame))
    self.lbl2_HT.setPixmap(QPixmap.fromImage(self.frameBW))

def perspectiveCorrectionHT(self, frame):
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

def rotationCorrection_HT(self, frame, angle):
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

def chooseFlameDirection_HT(self, text):
    selection = self.directionBox.currentText()
    if selection == 'Left to right':
        self.flameDir = 'toRight'
    elif selection == 'Right to left':
        self.flameDir = 'toLeft'

def connectivityBox_HT(self, text):
    selection = self.connectivityBox.currentText()
    if selection == '4':
        self.connectivity_HT = 4
    elif selection == '8':
        self.connectivity_HT = 8

def saveChannelsBtn_HT(self):
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
                # CAS slider setting:
                writer.writerow(['H', str(self.hueMinSlider.value()), str(self.hueMaxSlider.value())])
                writer.writerow(['S', str(self.satMinSlider.value()), str(self.satMaxSlider.value())])
                writer.writerow(['V', str(self.valMinSlider.value()), str(self.valMaxSlider.value())])
                writer.writerow([''])
                writer.writerow(['Particle size', str(self.filterParticleSldr_HT.value())])
                writer.writerow(['Moving average', str(self.movAvgIn_HT.text())])
                writer.writerow(['Points LE', str(self.avgLEIn_HT.text())])
                writer.writerow(['Connectivity', str(self.connectivity_HT)])
            self.msgLabel.setText('Channel values saved.')
        except:
            self.msgLabel.setText('Ops! The values were not saved.')

def loadChannelsBtn_HT(self):
    name = QFileDialog.getOpenFileName(self, 'Load channel values')
    try:
        with open(name[0], 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
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
                    self.filterParticleSldr_HT.setValue(int(row[1]))
                elif 'Moving average' in row:
                    self.movAvgIn_HT.setText(row[1])
                elif 'Points LE' in row:
                    self.avgLEIn_HT.setText(row[1])

        self.msgLabel.setText('Channel values loaded.')
    except:
        notParameters_dlg = QErrorMessage(self)
        notParameters_dlg.showMessage('Ops! There was a problem loading the parameters.')
        self.msgLabel.setText('Ops! Parameters were not loaded.')

def absValBtn_HT(self):
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

    self.lbl1_HT.clear()
    self.lbl2_HT.clear()

    ## Plot in terms of time:
    #HSVTrackingPlot(self.lbl1_HT, self.timeCount, self.xRight_mm, '', 'o', 'b')
    #HSVTrackingPlot(self.lbl1_HT, self.timeCount, self.xLeft_mm, '','t', 'r')
    #HSVTrackingPlot(self.lbl2_HT, self.timeCount, self.spreadRateRight, '', 'o', 'b')
    #HSVTrackingPlot(self.lbl2_HT, self.timeCount, self.spreadRateLeft, '','t', 'r')

    ## CAS Plot in terms of frame:
    HSVTrackingPlot(self.lbl1_HT, self.frameCount, self.xRight_mm, '', 'o', 'b')
    HSVTrackingPlot(self.lbl1_HT, self.frameCount, self.xLeft_mm, '','t', 'r')
    HSVTrackingPlot(self.lbl2_HT, self.frameCount, self.spreadRateRight, '', 'o', 'b')
    HSVTrackingPlot(self.lbl2_HT, self.frameCount, self.spreadRateLeft, '','t', 'r')

def saveBtn_HT(self):
    fileName = QFileDialog.getSaveFileName(self, 'Save tracking data')
    fileName = fileName[0]
    if not fileName[-4:] == '.csv':
        fileName = fileName + '.csv'

    fileInfo = ['Name', self.fNameLbl.text(), 'Scale [px/mm]', self.scaleIn.text(), 'Moving avg', self.movAvgIn_HT.text(), 'Points LE', self.avgLEIn_HT.text(), 'Flame dir.:', self.flameDir]
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

def showFrameLarge_HT(self):
    cv2.namedWindow(('Frame (RGB): ' + self.frameIn.text()), cv2.WINDOW_AUTOSIZE)
    cv2.imshow(('Frame (RGB): ' + self.frameIn.text()), self.currentFrameRGB_HT)
    #cv2.namedWindow(('Frame (black/white): ' + self.frameIn.text()), cv2.WINDOW_AUTOSIZE)
    #cv2.imshow(('Frame (black/white): ' + self.frameIn.text()), self.currentFrameBW_HT)
    while True:
        if cv2.waitKey(1) == 27: #ord('Esc')
            cv2.destroyAllWindows()
            return

def helpBtn_HT(self):
    msg = QMessageBox(self)
    msg.setText("""In this analysis the flame is tracked based on the image HSV colors. After specifying the video parameters and the flame direction, the flame region can be identified by choosing appropriate values of the HSV parameters (and particle size filtering). The HSV values vary depending on the colorspace of the frame/image - current implemntation uses a hue from 0-180 (since 0-360 deg hue is stored as H/2 for 8-bit), value and saturation are set from 0 to 255.
    The code will consider the range between minimum and maximum of each of the HSV as adjusted with the sliders. Small particles can be filtered out; the maximum value of the 'Filter particles size' slider corresponds to 25% of the size of the Region Of Interest (ROI).

    The preview box on the left shows the RGB image resulting from the filtering, while the preview box on the right shows the binary image with the particle filtering applied. The edges of the flame region are calculated as maximum and minimum locations.

    If there is a flashing light in the video, it can be filtered out by checking 'Ignore flashing light'.

    Flame position and spread rates are calculated automatically once 'Start tracking' is clicked. The instantaneous spread rates are averaged according to the number of points specified by the user ('Moving Avg'). Note that the 'Moving Avg points' value is doubled for the calculation of the spread rate (i.e. 'Moving Avg points' = 2 considers two points before and two points after the instantaneous value).

    'Absolute values' can be used to make the counts of flame position and time starting from zero.

    By clicking on 'Save data' a csv file containing all the information is generated. The channel values and particle size are saved separately with 'Save filter values'.

    By checking 'Video output' all the considered frames in the analysis (filtered images) will be exported as a video.

    """)
    msg.exec_()

def hueMinLeftBtn_HT(self):
    currentValue = self.hueMinSlider.value()
    self.hueMinSlider.setValue(currentValue - 1)
    HSVSlider_released(self)
def hueMinRightBtn_HT(self):
    currentValue = self.hueMinSlider.value()
    self.hueMinSlider.setValue(currentValue + 1)
    HSVSlider_released(self)
def hueMaxLeftBtn_HT(self):
    currentValue = self.hueMaxSlider.value()
    self.hueMaxSlider.setValue(currentValue - 1)
    HSVSlider_released(self)
def hueMaxRightBtn_HT(self):
    currentValue = self.hueMaxSlider.value()
    self.hueMaxSlider.setValue(currentValue + 1)
    HSVSlider_released(self)
def satMinLeftBtn_HT(self):
    currentValue = self.satMinSlider.value()
    self.satMinSlider.setValue(currentValue - 1)
    HSVSlider_released(self)
def satMinRightBtn_HT(self):
    currentValue = self.satMinSlider.value()
    self.satMinSlider.setValue(currentValue + 1)
    HSVSlider_released(self)
def satMaxLeftBtn_HT(self):
    currentValue = self.satMaxSlider.value()
    self.satMaxSlider.setValue(currentValue - 1)
    HSVSlider_released(self)
def satMaxRightBtn_HT(self):
    currentValue = self.satMaxSlider.value()
    self.satMaxSlider.setValue(currentValue + 1)
    HSVSlider_released(self)
def valMinLeftBtn_HT(self):
    currentValue = self.valMinSlider.value()
    self.valMinSlider.setValue(currentValue - 1)
    HSVSlider_released(self)
def valMinRightBtn_HT(self):
    currentValue = self.valMinSlider.value()
    self.valMinSlider.setValue(currentValue + 1)
    HSVSlider_released(self)
def valMaxLeftBtn_HT(self):
    currentValue = self.valMaxSlider.value()
    self.valMaxSlider.setValue(currentValue - 1)
    HSVSlider_released(self)
def valMaxRightBtn_HT(self):
    currentValue = self.valMaxSlider.value()
    self.valMaxSlider.setValue(currentValue + 1)
    HSVSlider_released(self)
