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

def createLumaTrackingBox(self):
    self.lumaTrackingValue = True
    self.lumaTrackingBox = QGroupBox(' ', self.analysisGroupBox)
    self.lumaTrackingBox.setGeometry(0, 0, 1050, 390)

    #first column
    x_cln1 = 10
    x_cln2 = 120
    w_btn = 150
    h_btn = 30
    h_txt = 30
    h_lbl = 22
    directionBoxTxt = QLabel('Flame direction:', self.lumaTrackingBox)
    directionBoxTxt.setGeometry(x_cln1, 20, 100, h_txt)
    self.directionBox = QComboBox(self.lumaTrackingBox)
    self.directionBox.setGeometry(x_cln1 - 5, 45, 150, h_btn)
    self.directionBox.addItem('Left to right')
    self.directionBox.addItem('Right to left')
    self.directionBox.activated.connect(self.directionLT_clicked)
    thresholdTxt = QLabel('Luma threshold:', self.lumaTrackingBox)
    thresholdTxt.setGeometry(x_cln1, 75, 100, h_txt)
    self.thresholdIn = QLineEdit('30', self.lumaTrackingBox)
    self.thresholdIn.setGeometry(x_cln2, 79, 30, h_lbl)
    filterParticleTxt = QLabel('Filter particles size:', self.lumaTrackingBox)
    filterParticleTxt.setGeometry(x_cln1, 100, 150, h_txt)
    self.filterParticleSldr_LT = QSlider(Qt.Horizontal, self.lumaTrackingBox)
    self.filterParticleSldr_LT.setGeometry(x_cln1 - 5, 125, 140, 25)
    self.filterParticleSldr_LT.setMinimum(1)
    try:
        self.filterParticleSldr_LT.setMaximum((int(self.roiThreeIn.text()) * int(self.roiFourIn.text())) / 20)
    except:
        self.filterParticleSldr_LT.setMaximum(2000)
    self.filterParticleSldr_LT.setValue(10)
    self.filterParticleSldr_LT.sliderReleased.connect(self.filterParticleSldr_LT_released)
    avgLE_txt = QLabel('#px to locate edges:', self.lumaTrackingBox)
    avgLE_txt.setGeometry(x_cln1, 150, 140, h_txt)
    self.avgLEIn_LT = QLineEdit('5', self.lumaTrackingBox)
    self.avgLEIn_LT.setGeometry(x_cln2, 154, 30, h_lbl)
    trackingTxt = QLabel('Flame tracking:', self.lumaTrackingBox)
    trackingTxt.setGeometry(x_cln1, 180, 120, h_txt)
    self.filterLight = QCheckBox('Ignore flashing light', self.lumaTrackingBox)
    self.filterLight.setGeometry(x_cln1, 205, 140, h_btn)
    movAvgTxt = QLabel('Moving avg points:', self.lumaTrackingBox)
    movAvgTxt.setGeometry(x_cln1, 230, 100, h_txt)
    self.movAvgIn_LT = QLineEdit('2', self.lumaTrackingBox)
    self.movAvgIn_LT.setGeometry(x_cln2, 234, 30, h_lbl)
    self.lumaTrackingBtn = QPushButton('Start Tracking', self.lumaTrackingBox)
    self.lumaTrackingBtn.setGeometry(x_cln1 - 5, 260, w_btn, h_txt)
    self.lumaTrackingBtn.clicked.connect(self.lumaTrackingBtn_clicked)
    self.absValBtn = QPushButton('Absolute values', self.lumaTrackingBox)
    self.absValBtn.setGeometry(x_cln1 - 5, 290, w_btn, h_btn)
    self.absValBtn.clicked.connect(self.absValBtnLT_clicked)
    self.saveBtn_LT = QPushButton('Save data', self.lumaTrackingBox)
    self.saveBtn_LT.setGeometry(x_cln1 - 5, 320, w_btn, h_btn)
    self.saveBtn_LT.clicked.connect(self.lumaSaveData_clicked)
    self.helpBtn_LT = QPushButton('Help', self.lumaTrackingBox)
    self.helpBtn_LT.setGeometry(x_cln1 - 5, 350, w_btn, h_btn)
    self.helpBtn_LT.clicked.connect(self.helpBtn_LT_clicked)

    self.showEdges = QCheckBox('Show edges location', self.lumaTrackingBox)
    self.showEdges.setGeometry(780, 325, 135, h_btn)
    self.showEdges.setChecked(True)
    self.exportEdges_LT = QCheckBox('Output video analysis', self.lumaTrackingBox)
    self.exportEdges_LT.setGeometry(780, 350, 135, h_btn)
    self.showFrameLargeBtn_LT = QPushButton('Show frames', self.lumaTrackingBox)
    self.showFrameLargeBtn_LT.setGeometry(930, 325, 115, h_btn)
    self.showFrameLargeBtn_LT.clicked.connect(self.showFrameLargeBtn_LT_clicked)

    # first label
    self.lbl1_LT = QLabel(self.lumaTrackingBox)
    self.lbl1_LT.setGeometry(190, 25, 420, 300)
    self.lbl1_LT.setStyleSheet('background-color: white')

    # second label
    self.lbl2_LT = QLabel(self.lumaTrackingBox)
    self.lbl2_LT.setGeometry(620, 25, 420, 300)
    self.lbl2_LT.setStyleSheet('background-color: white')

    self.flameDir = 'toRight' #default value
    self.lumaTrackingBox.show()

def getLumaFrame(self, frameNumber):
    if self.openSelection == 'video':
        self.fVideo.set(1, frameNumber)
        ret, frame = self.fVideo.read()
    elif self.openSelection == 'image(s)':
        frame = self.imagesList[int(frameNumber)]
        frame = cv2.imread(frame)

    if self.perspectiveValue == True:
        if self.rotationValue == True:
            frame = rotationCorrection_LT(self, frame, self.anglePerspective)
        frame = perspectiveCorrectionLT(self, frame)
        #the rotation has already been included in the perspective correction, but it could happen that a further rotation is needed after the correction (e.g. for the analysis)
        if self.anglePerspective != float(self.rotationAngleIn.text()):
            angle = float(self.rotationAngleIn.text()) - self.anglePerspective
            frame = rotationCorrection_LT(self, frame, angle)
    elif float(self.rotationAngleIn.text()) != 0: #in case there is no perspective correction
            angle = float(self.rotationAngleIn.text())
            frame = rotationCorrection_LT(self, frame, angle)
    if int(self.brightnessSlider.value()) != 0 or int(self.contrastSlider.value()) != 0:
        frameContainer = np.zeros(frame.shape, frame.dtype)
        alpha = (int(self.contrastSlider.value()) + 100) * 2 / 200
        beta = int(self.brightnessSlider.value())    # Simple brightness control [0-100]. We have [-50-50]
        frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    # crop frame
    frameCrop = frame[int(self.roiTwoIn.text()) : (int(self.roiTwoIn.text()) + int(self.roiFourIn.text())), int(self.roiOneIn.text()) : (int(self.roiOneIn.text()) + int(self.roiThreeIn.text()))]
    # Transform the frame into the YCC space
    frameYCC = cv2.cvtColor(frameCrop, cv2.COLOR_BGR2YCR_CB)
    Y, C, C = cv2.split(frameYCC)

    # Isolate flame region with user specified threshold
    (thresh, frameBW) = cv2.threshold(Y, int(self.thresholdIn.text()), 255, cv2.THRESH_BINARY)

    # Find all the connected components (8 means in the four directions and diagonals)
    componentNum, componentLbl, stats, centroids = cv2.connectedComponentsWithStats(frameBW, connectivity=8)
    ### 1 = number of labels; 2 = array; 3 = [[x location (left), y location (top), width, height, area]] for each label; 4 = [centroid of each label, x and y]. Note: the background is the first component

    # minimum area (measured in px) for filtering the components
    minArea = self.filterParticleSldr_LT.value()
    componentAreas = stats[:, 4] # stats is a list of list, here we start from 0 (the background), and we consider the last elements (area)

    # keep only the components with area larger than minArea, starting from 1 to avoid the background
    for i in range(1, componentNum):
        if componentAreas[i] >= minArea:
            frameBW[componentLbl == i] = 255
        else:
            frameBW[componentLbl == i] = 0

    flamePx = np.where(frameBW == [255])

    roiArea = Y.shape[0] * Y.shape[1]
    if self.filterLight.isChecked() == True:
        if len(flamePx[0]) < 0.5 * roiArea: #flamePx[0] = x; flamePx[1] = y
            findFlameEdges(self, frameBW, flamePx)
    else:
        findFlameEdges(self, frameBW, flamePx)

    if self.showEdges.isChecked() == True:
        cv2.line(Y, (self.xMax, 0),(self.xMax, int(self.roiFourIn.text())), (255, 255, 255), 2)
        cv2.line(Y, (self.xMin, 0),(self.xMin, int(self.roiFourIn.text())), (255, 255, 255), 2)

    self.currentFrameY_LT = Y
    # calculate the total number of bytes in the frame
    totalBytes = Y.nbytes
    # divide by the number of rows
    bytesPerLine = int(totalBytes/Y.shape[0]) #I had to introduce it to avoid distortion in the opened file for some of the videos
    self.frameY = QImage(Y.data, Y.shape[1], Y.shape[0], bytesPerLine, QImage.Format_Grayscale8) #shape[0] = height, [1] = width
    self.frameY = self.frameY.scaled(self.lbl1_LT.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

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

    if self.flameDir == 'toRight':
        self.xRight = int(self.roiOneIn.text()) + self.xMax
        self.xLeft = int(self.roiOneIn.text()) + self.xMin
    elif self.flameDir == 'toLeft':
        self.xRight = self.vWidth - int(self.roiOneIn.text()) - self.xMax
        self.xLeft = self.vWidth - int(self.roiOneIn.text()) - self.xMin

    if self.showEdges.isChecked() == True:
        cv2.line(frameBW, (self.xMax, 0),(self.xMax, int(self.roiFourIn.text())), (255, 255, 255), 2)
        cv2.line(frameBW, (self.xMin, 0),(self.xMin, int(self.roiFourIn.text())), (255, 255, 255), 2)

    self.currentFrameBW_LT = frameBW
    totalBytes = frameBW.nbytes
    bytesPerLine = int(totalBytes/frameBW.shape[0])
    self.frameBW = QImage(frameBW.data, frameBW.shape[1], frameBW.shape[0], bytesPerLine, QImage.Format_Grayscale8)
    self.frameBW = self.frameBW.scaled(self.lbl2_LT.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

def lumaTracking(self):
    scale = True
    if not self.scaleIn.text():
        scale = False
        msg = QMessageBox(self)
        msg.setText('The scale [px/mm] has not been specified')
        msg.exec_()
    self.lbl2_LT = QLabel(self.lumaTrackingBox)
    firstFrame = int(self.firstFrameIn.text())
    lastFrame = int(self.lastFrameIn.text())
    currentFrame = firstFrame
    self.xRight_mm = list()
    self.xLeft_mm = list()
    flameLength_mm = list()
    self.frameCount = list()
    iCount = 0
    flameArea = list()

    if self.exportEdges_LT.isChecked():
        fps = (float(self.vFpsLbl.text()))/(int(self.skipFrameIn.text()) + 1) #fps(new) = fps(original)/(skipframes + 1)
        codec = str(self.codecIn.text())
        vFormat = str(self.formatIn.text())
        vName = self.fPath + '-YVideo.' + str(vFormat) # alternative: 'output.{}'.format(vFormat); self.fNameLbl.text() +
        fourcc = cv2.VideoWriter_fourcc(*codec)
        size = (int(self.roiThreeIn.text()), int(self.roiFourIn.text()))
        # open and set properties
        vout = cv2.VideoWriter()
        vout.open(vName, fourcc, fps, size, 0)

    if scale: #this condition prevents crashes in case the scale is not specified
        while (currentFrame < lastFrame):
            getLumaFrame(self, currentFrame)
            iCount = iCount + 1
            self.xRight_mm.append(self.xRight / float(self.scaleIn.text()))
            self.xLeft_mm.append(self.xLeft / float(self.scaleIn.text()))
            flameArea.append(self.flameArea)
            self.frameCount.append(currentFrame)
            if self.exportEdges_LT.isChecked():
                vout.write(self.currentFrameY_LT)
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
            flameLength_mm.append(self.xRight_mm[i] - self.xLeft_mm[i])

        flameLength_mm = np.round(flameLength_mm, 2)
        self.flameLength_mm = flameLength_mm.tolist()
        print('Progress: 100 % - Tracking completed')
        self.msgLabel.setText('Tracking completed')

        if self.exportEdges_LT.isChecked():
            vout.release()
            self.msgLabel.setText('Tracking completed and Y channel video created.')

        movAvgPt = int(self.movAvgIn_LT.text()) #this number is half of the interval considered for the spread rate (movAvgPt = 2 means I am considering a total of 5 points (my point, 2 before and 2 after))
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

        self.xRight_mm = np.round(self.xRight_mm, 3)
        self.xRight_mm = self.xRight_mm.tolist()
        self.xLeft_mm = np.round(self.xLeft_mm, 3)
        self.xLeft_mm = self.xLeft_mm.tolist()
        self.spreadRateRight = np.round(self.spreadRateRight, 3)
        self.spreadRateRight = self.spreadRateRight.tolist()
        self.spreadRateLeft = np.round(self.spreadRateLeft, 3)
        self.spreadRateLeft = self.spreadRateLeft.tolist()

        self.lbl1_LT = pg.PlotWidget(self.lumaTrackingBox)
        self.lbl1_LT.setGeometry(190, 25, 420, 300)
        self.lbl1_LT.setBackground('w')
        self.lbl1_LT.setLabel('left', 'Position [mm]', color='black', size=14)
        self.lbl1_LT.setLabel('bottom', 'Time [s]', color='black', size=14)
        self.lbl1_LT.getAxis('bottom').setPen(color=(0, 0, 0))
        self.lbl1_LT.getAxis('left').setPen(color=(0, 0, 0))
        self.lbl1_LT.addLegend(offset = [1, 0.1]) # background color modified in line 122 and 123 of Versions/3.7/lib/python3.7/site-packages/pyqtgraph/graphicsItems
        self.lbl2_LT = pg.PlotWidget(self.lumaTrackingBox)
        self.lbl2_LT.setGeometry(620, 25, 420, 300)
        self.lbl2_LT.setBackground('w')
        self.lbl2_LT.setLabel('left', 'Spread Rate [mm/s]', color='black', size=14)
        self.lbl2_LT.setLabel('bottom', 'Time [s]', color='black', size=14)
        self.lbl2_LT.getAxis('bottom').setPen(color=(0, 0, 0))
        self.lbl2_LT.getAxis('left').setPen(color=(0, 0, 0))
        self.lbl2_LT.addLegend(offset = [1, 0.1]) # background color modified in line 122 and 123 of Versions/3.7/lib/python3.7/site-packages/pyqtgraph/graphicsItems

        lumaTrackingPlot(self.lbl1_LT, self.timeCount, self.xRight_mm, 'right edge', 'o', 'b')
        lumaTrackingPlot(self.lbl1_LT, self.timeCount, self.xLeft_mm, 'left edge', 't', 'r')
        lumaTrackingPlot(self.lbl2_LT, self.timeCount, self.spreadRateRight, 'right edge', 'o', 'b')
        lumaTrackingPlot(self.lbl2_LT, self.timeCount, self.spreadRateLeft, 'left edge', 't', 'r')

        self.lbl1_LT.show()
        self.lbl2_LT.show()

def lumaTrackingPlot(label, x, y, name, symbol, color):
    pen = pg.mkPen(color)
    label.plot(x, y, pen = pen, name = name, symbol = symbol, symbolSize = 7, symbolBrush = (color))

def chooseFlameDirection_LT(self, text):
    selection = self.directionBox.currentText()
    if selection == 'Left to right':
        self.flameDir = 'toRight'
    elif selection == 'Right to left':
        self.flameDir = 'toLeft'

def lumaSaveData(self):
    fileName = QFileDialog.getSaveFileName(self, 'Save tracking data')
    fileName = fileName[0]
    if not fileName[-4:] == '.csv':
        fileName = fileName + '.csv'

    fileInfo = ['Name', self.fNameLbl.text(), 'Scale [px/mm]', self.scaleIn.text(), 'Moving avg', self.movAvgIn_LT.text(), 'Points LE', self.avgLEIn_LT.text(), 'Luma threshold', self.thresholdIn.text(), 'Flame dir.:', self.flameDir]
    lbl = ['File info', 'Frame', 'Time [s]', 'Right edge [mm]', 'Left edge [mm]', 'Length [mm]', 'Spread Rate RE [mm/s]', 'Spread Rate LE [mm/s]', 'Area [mm^2]']
    rows = [fileInfo, self.frameCount, self.timeCount, self.xRight_mm, self.xLeft_mm, self.flameLength_mm, self.spreadRateRight, self.spreadRateLeft, self.flameArea]
    rows_zip = zip_longest(*rows)

    with open(fileName, 'w', newline = '') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')
        writer.writerow(lbl)
        for row in rows_zip:
            writer.writerow(row)
    self.msgLabel.setText('Data succesfully saved.')

def absValueLT(self):
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

    self.lbl1_LT.clear()
    self.lbl2_LT.clear()

    lumaTrackingPlot(self.lbl1_LT, self.timeCount, self.xRight_mm, '', 'o', 'b')
    lumaTrackingPlot(self.lbl1_LT, self.timeCount, self.xLeft_mm, '','t', 'r')
    lumaTrackingPlot(self.lbl2_LT, self.timeCount, self.spreadRateRight, '', 'o', 'b')
    lumaTrackingPlot(self.lbl2_LT, self.timeCount, self.spreadRateLeft, '', 't', 'r')

def perspectiveCorrectionLT(self, frame):
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

def filterParticleSldr_LT(self):
    frame = self.previewSlider.value()
    getLumaFrame(self, frame)
    self.lbl1_LT.setPixmap(QPixmap.fromImage(self.frameY))
    self.lbl2_LT.setPixmap(QPixmap.fromImage(self.frameBW))

def rotationCorrection_LT(self, frame, angle):
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

def showFrameLarge_LT(self):
    cv2.namedWindow(('Frame (luminance): ' + self.frameIn.text()), cv2.WINDOW_AUTOSIZE)
    cv2.imshow(('Frame (luminance): ' + self.frameIn.text()), self.currentFrameY_LT)
    cv2.namedWindow(('Frame (black/white): ' + self.frameIn.text()), cv2.WINDOW_AUTOSIZE)
    cv2.imshow(('Frame (black/white): ' + self.frameIn.text()), self.currentFrameBW_LT)
    while True:
        if cv2.waitKey(1) == 27: #ord('Esc')
            cv2.destroyAllWindows()
            return

def helpBtn_LT(self):
    msg = QMessageBox(self)
    msg.setText("""In this analysis the luminance intensity of each pixel is used to isolate the flame. After specifying the video parameters and the flame direction, the frames are transformed from the RGB to the YCC color space. Only the Y (luma intensity) component is considered, and the threshold to filter the flame from the background can be adjusted by the user (from 0 to 255).
    The Y channel of the image is shown in the preview box on the left, while the corresponding binary image is shown on the right. Small bright points can be filtered out with 'Filter particle size'. The maximum value of the 'Filter particles size' slider corresponds to 25% of the size of the Region Of Interest (ROI).

    The edges of the flame region are calculated as maximum and minimum locations, which can be adjusted by increasing the number of points considered ('#px to locate edges:').

    If there is a flashing light in the video, the bright frames can be discarded in the analysis by checking the 'Ignore flashing light' box.

    Flame position and spread rates are calculated automatically by clicking on 'Start Tracking'. The instantaneous spread rates are averaged according to the number of points specified by the user ('Moving avg points'). Note that the 'Moving avg points' value is doubled for the calculation of the spread rate (i.e. 'Moving avg points' = 2 considers two points before and two points after the instantaneous value).

    'Absolute values' can be used to make the counts of flame position and time starting from zero.

    By clicking on 'Save data' a csv file containing all the information is generated.

    By checking 'Video output' all the considered frames in the analysis (Y channel) will be exported as a video for further analysis.

    """)
    msg.exec_()
