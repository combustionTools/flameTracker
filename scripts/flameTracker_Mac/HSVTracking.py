"""
CAS:	HSL and HSV
Hue, the angular dimension, starting at the red primary at 0°, passing through the green primary at 120° and the blue primary at 240°, and then wrapping back to red at 360°

Central vertical axis comprises the neutral, achromatic, or gray colors ranging, from top to bottom, white at lightness 1 (value 1) to black at lightness 0 (value 0). 

In both geometries, the additive primary and secondary colors—red, yellow, green, cyan, blue and magenta—and linear mixtures between adjacent pairs of them, sometimes called pure colors, are arranged around the outside edge of the cylinder with saturation 1. These saturated colors have lightness 0.5 in HSL, while in HSV they have value 1.

OpenCV Implementation: RGB to HSV
In case of 8-bit and 16-bit images, R, G, and B are converted to the floating-point format and scaled to fit the 0 to 1 range.

If H<0 then H <- +360 . On output 0≤V≤1, 0≤S≤1, 0≤H≤360 .

The values are then converted to the destination data type:

    8-bit images: V <- 255V, S <- 255S,H <- H/2(to fit to 0 to 255)
    16-bit images: (currently not supported) V < -65535V, S < 65535S, H < −H
    32-bit images: H, S, and V are left as is


Switching to HSV from color 
H - Red
S - Green
V - Blue

:CAS


Flame Tracker. This program is designed to track flames or bright objects in videos or images.
Copyright (C) 2021  Luca Carmignani and Charles Scudiere

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

Author: Luca Carmignani, PhD, Charles Scudiere, PhD
Contact: flameTrackerContact@gmail.com
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
    self.directionBox.activated.connect(self.directionCT_clicked)
    redChannelTxt = QLabel('H channel:', self.HSVTrackingBox)
    redChannelTxt.setGeometry(x_cln1, 70, 100, h_txt)
    redMinTxt = QLabel('Min:', self.HSVTrackingBox)
    redMinTxt.setGeometry(x_cln1, 92, 80, h_txt)
    self.redMinLeftBtn_CT = QPushButton('<', self.HSVTrackingBox)
    self.redMinLeftBtn_CT.setGeometry(35, 90, w_btn2, h_btn)
    self.redMinLeftBtn_CT.clicked.connect(self.redMinLeftBtn_CT_clicked)
    self.redMinRightBtn_CT = QPushButton('>', self.HSVTrackingBox)
    self.redMinRightBtn_CT.setGeometry(175, 90, w_btn2, h_btn)
    self.redMinRightBtn_CT.clicked.connect(self.redMinRightBtn_CT_clicked)
    # CAS slider setting: H - Red, S - Green, V - Blue
    self.redMinSlider = QSlider(Qt.Horizontal, self.HSVTrackingBox)
    self.redMinSlider.setGeometry(60, 95, 120, 25)
    self.redMinSlider.setMinimum(0)
    #self.redMinSlider.setMaximum(255)
    self.redMinSlider.setMaximum(180) # since stored as H/2 for 8-bit (normally 0-360)
    #self.redMinSlider.setValue(10)
    self.redMinSlider.setValue(80) # Default to include blue values - 92=~185 deg Min Hue
    self.redMinSlider.sliderReleased.connect(self.singleHSVSlider_released)
    self.redMinSlider.valueChanged.connect(self.singleHSVSlider_released)
    redMaxTxt = QLabel('Max:', self.HSVTrackingBox)
    redMaxTxt.setGeometry(x_cln1, 114, 100, h_txt)
    self.redMaxLeftBtn_CT = QPushButton('<', self.HSVTrackingBox)
    self.redMaxLeftBtn_CT.setGeometry(35, 112, w_btn2, h_btn)
    self.redMaxLeftBtn_CT.clicked.connect(self.redMaxLeftBtn_CT_clicked)
    self.redMaxRightBtn_CT = QPushButton('>', self.HSVTrackingBox)
    self.redMaxRightBtn_CT.setGeometry(175, 112, w_btn2, h_btn)
    self.redMaxRightBtn_CT.clicked.connect(self.redMaxRightBtn_CT_clicked)
    # CAS slider setting: H - Red, S - Green, V - Blue
    self.redMaxSlider = QSlider(Qt.Horizontal, self.HSVTrackingBox)
    self.redMaxSlider.setGeometry(60, 117, 120, 25)
    self.redMaxSlider.setMinimum(0)
    #self.redMaxSlider.setMaximum(255)
    self.redMaxSlider.setMaximum(180) # since stored as H/2 for 8-bit (normally 0-360)
    #self.redMaxSlider.setValue(255)
    self.redMaxSlider.setValue(163) # Default to include blue values - 130=~260 deg Max Hue
    self.redMaxSlider.sliderReleased.connect(self.singleHSVSlider_released)
    self.redMaxSlider.valueChanged.connect(self.singleHSVSlider_released)
    greenChannelTxt = QLabel('S channel:', self.HSVTrackingBox)
    greenChannelTxt.setGeometry(x_cln1, 140, 100, h_txt)
    greenMinTxt = QLabel('Min:', self.HSVTrackingBox)
    greenMinTxt.setGeometry(x_cln1, 162, 100, h_txt)
    self.greenMinLeftBtn_CT = QPushButton('<', self.HSVTrackingBox)
    self.greenMinLeftBtn_CT.setGeometry(35, 160, w_btn2, h_btn)
    self.greenMinLeftBtn_CT.clicked.connect(self.greenMinLeftBtn_CT_clicked)
    self.greenMinRightBtn_CT = QPushButton('>', self.HSVTrackingBox)
    self.greenMinRightBtn_CT.setGeometry(175, 160, w_btn2, h_btn)
    self.greenMinRightBtn_CT.clicked.connect(self.greenMinRightBtn_CT_clicked)
    # CAS slider setting: H - Red, S - Green, V - Blue
    self.greenMinSlider = QSlider(Qt.Horizontal, self.HSVTrackingBox)
    self.greenMinSlider.setGeometry(60, 165, 120, 25)
    self.greenMinSlider.setMinimum(0)
    self.greenMinSlider.setMaximum(255)
    #self.greenMinSlider.setValue(10)
    self.greenMinSlider.setValue(30) # Default to include blue values - 100=~40% min Saturation
    self.greenMinSlider.sliderReleased.connect(self.singleHSVSlider_released)
    self.greenMinSlider.valueChanged.connect(self.singleHSVSlider_released)
    greenMaxTxt = QLabel('Max:', self.HSVTrackingBox)
    greenMaxTxt.setGeometry(x_cln1, 184, 100, h_txt)
    self.greenMaxLeftBtn_CT = QPushButton('<', self.HSVTrackingBox)
    self.greenMaxLeftBtn_CT.setGeometry(35, 182, w_btn2, h_btn)
    self.greenMaxLeftBtn_CT.clicked.connect(self.greenMaxLeftBtn_CT_clicked)
    self.greenMaxRightBtn_CT = QPushButton('>', self.HSVTrackingBox)
    self.greenMaxRightBtn_CT.setGeometry(175, 182, w_btn2, h_btn)
    self.greenMaxRightBtn_CT.clicked.connect(self.greenMaxRightBtn_CT_clicked)
    # CAS slider setting: H - Red, S - Green, V - Blue
    self.greenMaxSlider = QSlider(Qt.Horizontal, self.HSVTrackingBox)
    self.greenMaxSlider.setGeometry(60, 187, 120, 25)
    self.greenMaxSlider.setMinimum(0)
    self.greenMaxSlider.setMaximum(255)
    #self.greenMaxSlider.setValue(255)
    self.greenMaxSlider.setValue(255) # Default to some blue value - 255=~100% max Saturation
    self.greenMaxSlider.sliderReleased.connect(self.singleHSVSlider_released)
    self.greenMaxSlider.valueChanged.connect(self.singleHSVSlider_released)
    blueChannelTxt = QLabel('V channel:', self.HSVTrackingBox)
    blueChannelTxt.setGeometry(x_cln1, 210, 100, h_txt)
    blueMinTxt = QLabel('Min:', self.HSVTrackingBox)
    blueMinTxt.setGeometry(x_cln1, 232, 100, h_txt)
    self.blueMinLeftBtn_CT = QPushButton('<', self.HSVTrackingBox)
    self.blueMinLeftBtn_CT.setGeometry(35, 230, w_btn2, h_btn)
    self.blueMinLeftBtn_CT.clicked.connect(self.blueMinLeftBtn_CT_clicked)
    self.blueMinRightBtn_CT = QPushButton('>', self.HSVTrackingBox)
    self.blueMinRightBtn_CT.setGeometry(175, 230, w_btn2, h_btn)
    self.blueMinRightBtn_CT.clicked.connect(self.blueMinRightBtn_CT_clicked)
    # CAS slider setting: H - Red, S - Green, V - Blue
    self.blueMinSlider = QSlider(Qt.Horizontal, self.HSVTrackingBox)
    self.blueMinSlider.setGeometry(60, 235, 120, 25)
    self.blueMinSlider.setMinimum(0)
    self.blueMinSlider.setMaximum(255)
    self.blueMinSlider.setValue(20) # Default to some blue value - 63=~25% min Value
    self.blueMinSlider.sliderReleased.connect(self.singleHSVSlider_released)
    self.blueMinSlider.valueChanged.connect(self.singleHSVSlider_released)
    blueMaxTxt = QLabel('Max:', self.HSVTrackingBox)
    blueMaxTxt.setGeometry(x_cln1, 254, 100, h_txt)
    self.blueMaxLeftBtn_CT = QPushButton('<', self.HSVTrackingBox)
    self.blueMaxLeftBtn_CT.setGeometry(35, 252, w_btn2, h_btn)
    self.blueMaxLeftBtn_CT.clicked.connect(self.blueMaxLeftBtn_CT_clicked)
    self.blueMaxRightBtn_CT = QPushButton('>', self.HSVTrackingBox)
    self.blueMaxRightBtn_CT.setGeometry(175, 252, w_btn2, h_btn)
    self.blueMaxRightBtn_CT.clicked.connect(self.blueMaxRightBtn_CT_clicked)
    # CAS slider setting: H - Red, S - Green, V - Blue
    self.blueMaxSlider = QSlider(Qt.Horizontal, self.HSVTrackingBox)
    self.blueMaxSlider.setGeometry(60, 257, 120, 25)
    self.blueMaxSlider.setMinimum(0)
    self.blueMaxSlider.setMaximum(255)
    #self.blueMaxSlider.setValue(255)
    self.blueMaxSlider.setValue(255) # Default to some blue value - 255=~100% max Value
    self.blueMaxSlider.sliderReleased.connect(self.singleHSVSlider_released)
    self.blueMaxSlider.valueChanged.connect(self.singleHSVSlider_released)
    filterParticleTxt = QLabel('Filter particles size:', self.HSVTrackingBox)
    filterParticleTxt.setGeometry(x_cln1, 280, 150, h_txt)
    self.filterParticleSldr_CT = QSlider(Qt.Horizontal, self.HSVTrackingBox)
    self.filterParticleSldr_CT.setGeometry(10, 305, 170, 25)
    self.filterParticleSldr_CT.setMinimum(1)
    try:
        self.filterParticleSldr_CT.setMaximum((int(self.roiThreeIn.text()) * int(self.roiFourIn.text())) / 20)
    except:
        self.filterParticleSldr_CT.setMaximum(2000)
    self.filterParticleSldr_CT.setValue(350) #	was defulted to 10, but experience says around ~1228 or ~350 to not filter too much
    self.filterParticleSldr_CT.sliderReleased.connect(self.filterParticleSldr_CT_released)
    avgLE_txt = QLabel('#px to locate edges:', self.HSVTrackingBox)
    avgLE_txt.setGeometry(x_cln1, 330, 140, h_txt)
    self.avgLEIn_CT = QLineEdit('10', self.HSVTrackingBox) #was defaulted to 1, but experience says around 5-10
    self.avgLEIn_CT.setGeometry(x_cln1 + 135, 334, 30, h_lbl)
    connectivityTxt = QLabel('Connectivity (px):', self.HSVTrackingBox)
    connectivityTxt.setGeometry(x_cln1, 360, 100, h_txt)
    self.connectivityBox = QComboBox(self.HSVTrackingBox)
    self.connectivityBox.setGeometry(x_cln1 + 110, 360, 60, h_btn)
    self.connectivityBox.addItem('4')
    self.connectivityBox.addItem('8')
    self.connectivityBox.activated.connect(self.connectivityBoxCT_clicked)

    #second column
    x_cln1 = 220
    self.saveChannelsBtn_CT = QPushButton('Save filter values', self.HSVTrackingBox)
    self.saveChannelsBtn_CT.setGeometry(x_cln1 - 10, 30, 150, h_btn)
    self.saveChannelsBtn_CT.clicked.connect(self.saveChannelsBtn_CT_clicked)
    self.loadChannelsBtn_CT = QPushButton('Load filter values', self.HSVTrackingBox)
    self.loadChannelsBtn_CT.setGeometry(x_cln1 - 10, 60, 150, h_btn)
    self.loadChannelsBtn_CT.clicked.connect(self.loadChannelsBtn_CT_clicked)
    self.helpBtn_CT = QPushButton('Help', self.HSVTrackingBox)
    self.helpBtn_CT.setGeometry(x_cln1 - 10, 90, 150, h_btn)
    self.helpBtn_CT.clicked.connect(self.helpBtn_CT_clicked)
    trackingTxt = QLabel('Flame tracking:', self.HSVTrackingBox)
    trackingTxt.setGeometry(x_cln1, 120, 120, h_txt)
    self.filterLight_CT = QCheckBox('Ignore flashing light', self.HSVTrackingBox)
    self.filterLight_CT.setGeometry(x_cln1, 145, 135, h_btn)
    movAvgTxt = QLabel('Moving avg points:', self.HSVTrackingBox)
    movAvgTxt.setGeometry(x_cln1, 170, 130, h_txt)
    self.movAvgIn_CT = QLineEdit('5', self.HSVTrackingBox) #was defaulted to 2, experience says around 5 better
    self.movAvgIn_CT.setGeometry(x_cln1 + 105, 174, 30, h_lbl)
    self.HSVTrackingBtn = QPushButton('Start tracking', self.HSVTrackingBox)
    self.HSVTrackingBtn.setGeometry(x_cln1 - 10, 200, 150, h_btn)
    self.HSVTrackingBtn.clicked.connect(self.HSVTrackingBtn_clicked)
    self.absValBtn_CT = QPushButton('Absolute values', self.HSVTrackingBox)
    self.absValBtn_CT.setGeometry(x_cln1 - 10, 230, 150, h_btn)
    self.absValBtn_CT.clicked.connect(self.absValBtn_CT_clicked)
    self.saveBtn_CT = QPushButton('Save data', self.HSVTrackingBox)
    self.saveBtn_CT.setGeometry(x_cln1 - 10, 260, 150, h_btn)
    self.saveBtn_CT.clicked.connect(self.saveBtn_CT_clicked)

    # first label
    self.lbl1_CT = QLabel(self.HSVTrackingBox)
    self.lbl1_CT.setGeometry(370, 25, 330, 250)
    self.lbl1_CT.setStyleSheet('background-color: white')
    self.showEdges = QCheckBox('Show edges location', self.HSVTrackingBox)
    self.showEdges.setGeometry(780, 275, 135, h_btn)
    self.showEdges.setChecked(True)
    self.exportEdges_CT = QCheckBox('Output video analysis', self.HSVTrackingBox)
    self.exportEdges_CT.setGeometry(780, 300, 135, h_btn)

    # second label
    self.lbl2_CT = QLabel(self.HSVTrackingBox)
    self.lbl2_CT.setGeometry(710, 25, 330, 250)
    self.lbl2_CT.setStyleSheet('background-color: white')
    self.showFrameLargeBtn_CT = QPushButton('Show frames', self.HSVTrackingBox)
    self.showFrameLargeBtn_CT.setGeometry(930, 275, 115, h_btn)
    self.showFrameLargeBtn_CT.clicked.connect(self.showFrameLargeBtn_CT_clicked)

    self.flameDir = 'toRight'
    self.connectivity_CT = 4
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
            frame = rotationCorrection_CT(self, frame, self.anglePerspective)
        frame = perspectiveCorrectionCT(self, frame)
        #the rotation has already been included in the perspective correction, but it could happen that a further rotation is needed after the correction (e.g. for the analysis)
        if self.anglePerspective != float(self.rotationAngleIn.text()):
            angle = float(self.rotationAngleIn.text()) - self.anglePerspective
            frame = rotationCorrection_CT(self, frame, angle)
    elif float(self.rotationAngleIn.text()) != 0: #in case there is no perspective correction
            angle = float(self.rotationAngleIn.text())
            frame = rotationCorrection_CT(self, frame, angle)
    if int(self.brightnessSlider.value()) != 0 or int(self.contrastSlider.value()) != 0:
        frameContainer = np.zeros(frame.shape, frame.dtype)
        alpha = (int(self.contrastSlider.value()) + 100) * 2 / 200
        beta = int(self.brightnessSlider.value())    # Simple brightness control [0-100]. Instead, we have [-50-50]
        frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    # crop frame (after rotation)
    frameCrop = frame[int(self.roiTwoIn.text()) : (int(self.roiTwoIn.text()) + int(self.roiFourIn.text())), int(self.roiOneIn.text()) : (int(self.roiOneIn.text()) + int(self.roiThreeIn.text()))]

    # Filter here: #CAS Modified for HSV tracking instead of color tracking
    blueLow = self.blueMinSlider.value()
    blueHigh = self.blueMaxSlider.value()
    greenLow = self.greenMinSlider.value()
    greenHigh = self.greenMaxSlider.value()
    redLow = self.redMinSlider.value()
    redHigh = self.redMaxSlider.value()
    # H - Red
    # S - Green
    # V - Blue
    #low = ([blueLow, greenLow, redLow])
    #high = ([blueHigh, greenHigh, redHigh])
    low = ([redLow, greenLow, blueLow])
    high = ([redHigh, greenHigh, blueHigh])
    low = np.array(low, dtype = 'uint8') #this conversion is necessary
    high = np.array(high, dtype = 'uint8')
    #newMask = cv2.inRange(frameCrop, low, high)
    newMask = cv2.inRange(cv2.cvtColor(frameCrop, cv2.COLOR_BGR2HSV), low, high)
    frame = cv2.bitwise_and(frameCrop, frameCrop, mask = newMask)
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    (threshold, frameBW) = cv2.threshold(grayFrame, 0, 255, cv2.THRESH_BINARY)

    # Find all the connected components (8 means in the four directions and diagonals)
    componentNum, componentLbl, stats, centroids = cv2.connectedComponentsWithStats(frameBW, connectivity = self.connectivity_CT)
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

    if self.filterLight_CT.isChecked() == True:
        if len(flamePx[0]) < 0.5 * (int(self.roiThreeIn.text()) * int(self.roiFourIn.text())): #flamePx[0] = x; flamePx[1] = y
            findFlameEdges_CT(self, frameBW, flamePx)
    else:
        findFlameEdges_CT(self, frameBW, flamePx)

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

def findFlameEdges_CT(self, frameBW, flamePx):
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
            getHSVFilteredFrame(self, currentFrame)
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

        self.lbl1_CT = pg.PlotWidget(self.HSVTrackingBox)
        self.lbl1_CT.setGeometry(370, 25, 330, 250)
        self.lbl1_CT.setBackground('w')
        self.lbl1_CT.setLabel('left', 'Position [mm]', color='black', size=14)
        self.lbl1_CT.setLabel('bottom', 'Time [s]', color='black', size=14)
        self.lbl1_CT.getAxis('bottom').setPen(color=(0, 0, 0))
        self.lbl1_CT.getAxis('left').setPen(color=(0, 0, 0))
        self.lbl1_CT.addLegend(offset = [1, 0.1]) # background color modified in line 122 and 123 of Versions/3.7/lib/python3.7/site-packages/pyqtgraph/graphicsItems
        self.lbl2_CT = pg.PlotWidget(self.HSVTrackingBox)
        self.lbl2_CT.setGeometry(710, 25, 330, 250)
        self.lbl2_CT.setBackground('w')
        self.lbl2_CT.setLabel('left', 'Spread Rate [mm/s]', color='black', size=14)
        self.lbl2_CT.setLabel('bottom', 'Time [s]', color='black', size=14)
        self.lbl2_CT.getAxis('bottom').setPen(color=(0, 0, 0))
        self.lbl2_CT.getAxis('left').setPen(color=(0, 0, 0))
        self.lbl2_CT.addLegend(offset = [1, 0.1]) # background color modified in line 122 and 123 of Versions/3.7/lib/python3.7/site-packages/pyqtgraph/graphicsItems

        HSVTrackingPlot(self.lbl1_CT, self.timeCount, self.xRight_mm, 'right edge', 'o', 'b')
        HSVTrackingPlot(self.lbl1_CT, self.timeCount, self.xLeft_mm, 'left edge', 't', 'r')
        HSVTrackingPlot(self.lbl2_CT, self.timeCount, self.spreadRateRight, 'right edge', 'o', 'b')
        HSVTrackingPlot(self.lbl2_CT, self.timeCount, self.spreadRateLeft, 'left edge', 't', 'r')

        self.lbl1_CT.show()
        self.lbl2_CT.show()

def HSVTrackingPlot(label, x, y, name, symbol, color):
    pen = pg.mkPen(color)
    label.plot(x, y, pen = pen, name = name, symbol = symbol, symbolSize = 7, symbolBrush = (color))

def HSVSlider_released(self):
    frame = self.previewSlider.value()
    getHSVFilteredFrame(self, frame)
    self.lbl1_CT.setPixmap(QPixmap.fromImage(self.frame))
    self.lbl2_CT.setPixmap(QPixmap.fromImage(self.frameBW))

def filterParticleSldr_CT(self):
    frame = self.previewSlider.value()
    getHSVFilteredFrame(self, frame)
    self.lbl1_CT.setPixmap(QPixmap.fromImage(self.frame))
    self.lbl2_CT.setPixmap(QPixmap.fromImage(self.frameBW))

def perspectiveCorrectionCT(self, frame):
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

def rotationCorrection_CT(self, frame, angle):
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

def chooseFlameDirection_CT(self, text):
    selection = self.directionBox.currentText()
    if selection == 'Left to right':
        self.flameDir = 'toRight'
    elif selection == 'Right to left':
        self.flameDir = 'toLeft'

def connectivityBox_CT(self, text):
    selection = self.connectivityBox.currentText()
    if selection == '4':
        self.connectivity_CT = 4
    elif selection == '8':
        self.connectivity_CT = 8

def saveChannelsBtn_CT(self):
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
                # CAS slider setting: H - Red, S - Green, V - Blue
                writer.writerow(['H', str(self.redMinSlider.value()), str(self.redMaxSlider.value())])
                writer.writerow(['S', str(self.greenMinSlider.value()), str(self.greenMaxSlider.value())])
                writer.writerow(['V', str(self.blueMinSlider.value()), str(self.blueMaxSlider.value())])
                writer.writerow([''])
                writer.writerow(['Particle size', str(self.filterParticleSldr_CT.value())])
                writer.writerow(['Moving average', str(self.movAvgIn_CT.text())])
                writer.writerow(['Points LE', str(self.avgLEIn_CT.text())])
                writer.writerow(['Connectivity', str(self.connectivity_CT)])
            self.msgLabel.setText('Channel values saved.')
        except:
            self.msgLabel.setText('Ops! The values were not saved.')

def loadChannelsBtn_CT(self):
    name = QFileDialog.getOpenFileName(self, 'Load channel values')
    try:
        with open(name[0], 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for row in reader:
                # CAS slider setting: H - Red, S - Green, V - Blue
                if 'H' in row:
                    self.redMinSlider.setValue(int(row[1]))
                    self.redMaxSlider.setValue(int(row[2]))
                elif 'S' in row:
                    self.greenMinSlider.setValue(int(row[1]))
                    self.greenMaxSlider.setValue(int(row[2]))
                elif 'V' in row:
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

def absValBtn_CT(self):
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

    HSVTrackingPlot(self.lbl1_CT, self.timeCount, self.xRight_mm, '', 'o', 'b')
    HSVTrackingPlot(self.lbl1_CT, self.timeCount, self.xLeft_mm, '','t', 'r')
    HSVTrackingPlot(self.lbl2_CT, self.timeCount, self.spreadRateRight, '', 'o', 'b')
    HSVTrackingPlot(self.lbl2_CT, self.timeCount, self.spreadRateLeft, '','t', 'r')

def saveBtn_CT(self):
    fileName = QFileDialog.getSaveFileName(self, 'Save tracking data')
    fileName = fileName[0]
    if not fileName[-4:] == '.csv':
        fileName = fileName + '.csv'

    fileInfo = ['Name', self.fNameLbl.text(), 'Scale [px/mm]', self.scaleIn.text(), 'Moving avg', self.movAvgIn_CT.text(), 'Points LE', self.avgLEIn_CT.text(), 'Flame dir.:', self.flameDir]
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

def showFrameLarge_CT(self):
    cv2.namedWindow(('Frame (RGB): ' + self.frameIn.text()), cv2.WINDOW_AUTOSIZE)
    cv2.imshow(('Frame (RGB): ' + self.frameIn.text()), self.currentFrameRGB_CT)
    cv2.namedWindow(('Frame (black/white): ' + self.frameIn.text()), cv2.WINDOW_AUTOSIZE)
    cv2.imshow(('Frame (black/white): ' + self.frameIn.text()), self.currentFrameBW_CT)
    while True:
        if cv2.waitKey(1) == 27: #ord('Esc')
            cv2.destroyAllWindows()
            return

def helpBtn_CT(self):
    msg = QMessageBox(self)
    msg.setText("""In this analysis the flame is tracked based on the image HSV colors. After specifying the video parameters and the flame direction, the flame region can be identified by choosing appropriate values of the RGB channels (and particle size filtering). The channel values vary between 0 and 255, and the code will consider the range between minimum and maximum of each channel adjusted with the sliders. Small particles can be filtered out; the maximum value of the 'Filter particles size' slider corresponds to 25% of the size of the Region Of Interest (ROI).

    The preview box on the left shows the RGB image resulting from the filtering, while the preview box on the right shows the binary image with the particle filtering applied. The edges of the flame region are calculated as maximum and minimum locations.

    If there is a flashing light in the video, it can be filtered out by checking 'Ignore flashing light'.

    Flame position and spread rates are calculated automatically once 'Start tracking' is clicked. The instantaneous spread rates are averaged according to the number of points specified by the user ('Moving Avg'). Note that the 'Moving Avg points' value is doubled for the calculation of the spread rate (i.e. 'Moving Avg points' = 2 considers two points before and two points after the instantaneous value).

    'Absolute values' can be used to make the counts of flame position and time starting from zero.

    By clicking on 'Save data' a csv file containing all the information is generated. The channel values and particle size are saved separately with 'Save filter values'.

    By checking 'Video output' all the considered frames in the analysis (filtered images) will be exported as a video.

    """)
    msg.exec_()

def redMinLeftBtn_CT(self):
    currentValue = self.redMinSlider.value()
    self.redMinSlider.setValue(currentValue - 1)
    HSVSlider_released(self)
def redMinRightBtn_CT(self):
    currentValue = self.redMinSlider.value()
    self.redMinSlider.setValue(currentValue + 1)
    HSVSlider_released(self)
def redMaxLeftBtn_CT(self):
    currentValue = self.redMaxSlider.value()
    self.redMaxSlider.setValue(currentValue - 1)
    HSVSlider_released(self)
def redMaxRightBtn_CT(self):
    currentValue = self.redMaxSlider.value()
    self.redMaxSlider.setValue(currentValue + 1)
    HSVSlider_released(self)
def greenMinLeftBtn_CT(self):
    currentValue = self.greenMinSlider.value()
    self.greenMinSlider.setValue(currentValue - 1)
    HSVSlider_released(self)
def greenMinRightBtn_CT(self):
    currentValue = self.greenMinSlider.value()
    self.greenMinSlider.setValue(currentValue + 1)
    HSVSlider_released(self)
def greenMaxLeftBtn_CT(self):
    currentValue = self.greenMaxSlider.value()
    self.greenMaxSlider.setValue(currentValue - 1)
    HSVSlider_released(self)
def greenMaxRightBtn_CT(self):
    currentValue = self.greenMaxSlider.value()
    self.greenMaxSlider.setValue(currentValue + 1)
    HSVSlider_released(self)
def blueMinLeftBtn_CT(self):
    currentValue = self.blueMinSlider.value()
    self.blueMinSlider.setValue(currentValue - 1)
    HSVSlider_released(self)
def blueMinRightBtn_CT(self):
    currentValue = self.blueMinSlider.value()
    self.blueMinSlider.setValue(currentValue + 1)
    HSVSlider_released(self)
def blueMaxLeftBtn_CT(self):
    currentValue = self.blueMaxSlider.value()
    self.blueMaxSlider.setValue(currentValue - 1)
    HSVSlider_released(self)
def blueMaxRightBtn_CT(self):
    currentValue = self.blueMaxSlider.value()
    self.blueMaxSlider.setValue(currentValue + 1)
    HSVSlider_released(self)
