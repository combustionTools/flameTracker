"""
Flame Tracker. This program is designed to track flames or bright objects in videos or images.
Copyright (C) 2020-2026  Luca Carmignani
Contributor: Charles Scudiere, PhD (HSV tracking addition)

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

Contact: flameTrackerContact@gmail.com
"""

import flameTracker as ft
import boxesGUI_OS as gui # for the objects in the user interface

import trackpy as tp
import pandas as pd


def detectEmbers(self, frame):
    """
    Detect ember(s) on the current frame with TrackPy and show the result in the preview label,
    with added OpenCV preprocessing.
    """

    # 1) Get current edited frame
    frame, frameCrop = ft.checkEditing(self, self.frameNumber)
    if frameCrop is None or frameCrop.size == 0:
        self.msgLabel.setText('Ember preview: empty frame/ROI.')
        return

    # 2) Read parameters from GUI
    try:
        diameter = int(float(self.emberSizeIn.text())*float(self.scaleIn.text()))
        if diameter % 2 == 0: # TrackPy requires odd diameter
            diameter += 1
    except Exception:
        self.msgLabel.setText('Ember preview: invalid diameter.')
        return
    

    try:
        minmass = float(self.emberMinTotIntensity.text()) # minMass = ember area * intensity (Total intensity)
    except Exception:
        minmass = 10.0  # fallback if left empty

    try:
        brightnessThreshold = int(self.brightnessThresholdIn.text())
        if not (0 <= brightnessThreshold <= 255):
            raise ValueError("Threshold must be between 0 and 255.")
    except Exception:
        self.msgLabel.setText('Ember preview: invalid threshold (0-255).')
        return
    
    # 3) Convert to grayscale for TrackPy
    gray = ft.cv2.cvtColor(frameCrop, ft.cv2.COLOR_BGR2GRAY)

    # Apply a binary threshold to isolate the bright ember cores.
    # Pixels brighter than 'brightnessThreshold' become white (255), others become black (0).
    _, thresh = ft.cv2.threshold(
        gray, 
        brightnessThreshold, 
        255, 
        ft.cv2.THRESH_BINARY
    )

    # 4) Detect features (embers) with TrackPy
    # Original 'gray' frame for accurate sub-pixel center finding, 'thresh' image is used later for contour finding

    try:
        features = tp.locate(
            gray,
            diameter=diameter,
            minmass=minmass,
            separation=diameter,   # reasonable default
            preprocess=True # Use TrackPy's internal bandpass filter for robust center finding
        )
    except Exception as e:
        print('TrackPy locate error:', e)
        self.msgLabel.setText('Ember preview: TrackPy failed (see console).')
        return

    if features is None or len(features) == 0:
        self.msgLabel.setText('Ember preview: no embers detected.')
        # Still show the original frame
        vis = frameCrop.copy()
    else:
        self.msgLabel.setText(f'Ember preview: detected {len(features)} ember(s).')

        ### Histogram
        try:
            # 1. Get the mass data
            masses = features['mass'].to_numpy() 
            
            # 1. Generate the histogram (counts and bin edges)
            hist_counts, hist_bins = ft.np.histogram(
                masses, 
                bins=50, 
                range=(0, masses.max()) 
            )

            # 2. Prepare the PlotWidget
            self.plot2_ET.clear() # Clear any previous plot data
 
            # Get the center of each bin for the X-coordinates
            # This results in a (50,) array, matching hist_counts (50,)
            bin_centers = (hist_bins[:-1] + hist_bins[1:]) / 2.0
            
            # Calculate the bin width for correct visual spacing
            bin_width = hist_bins[1] - hist_bins[0] 

            # 3. Plot the histogram using a BarGraphItem (clearest way to plot histograms in pyqtgraph)
            bar_graph = ft.pg.BarGraphItem(
                x=bin_centers, 
                height=hist_counts, 
                width=bin_width * 0.9, # Use 90% of the bin width for spacing
                brush=(50, 50, 200, 150)
            )
            self.plot2_ET.addItem(bar_graph)
           
            if minmass > masses.max():
                self.plot2_ET.setXRange(0, minmass * 1.05) # Extend 5% past minmass
            else:
                self.plot2_ET.setXRange(0, masses.max() * 1.05)

            # 5. Set titles and labels for clarity
            self.plot2_ET.setTitle("Total Intensity Distribution")
            self.plot2_ET.setLabel('bottom', "Tot Intensity (Area * px intensity)")
            self.plot2_ET.setLabel('left', "Number of embers")
           
        except Exception as e:
            self.plot2_ET.clear()
            print(f"ERROR: Could not render pyqtgraph histogram. {e}")
            self.msgLabel.setText(f'Plot Error: {e}')
            
        

        # 4.1 Find contours in the binary image
        # RETR_EXTERNAL is used to find only the outermost contours
        # CHAIN_APPROX_SIMPLE saves memory by only storing key points
        contours, _ = ft.cv2.findContours(
            thresh, 
            ft.cv2.RETR_EXTERNAL, 
            ft.cv2.CHAIN_APPROX_SIMPLE
        )

        # 4.2 Prepare to store shape data
        area_list = []
       
        # Iterate over every feature found by TrackPy
        for index, p in features.iterrows():
            px, py = p['x'], p['y'] # TrackPy center coordinates
            min_dist_sq = float('inf')
            best_contour_area = 0.0

            # Iterate over all found contours to find the one closest to the feature center
            for contour in contours:
                # Calculate the centroid (center of mass) of the contour
                M = ft.cv2.moments(contour)
                if M['m00'] > 0: # Ensure contour has area
                    cx = M['m10'] / M['m00']
                    cy = M['m01'] / M['m00']
                    
                    # Calculate squared distance between TrackPy center and contour centroid
                    dist_sq = (px - cx)**2 + (py - cy)**2
                    
                    # If this contour is closer than the current best match AND it contains the point (for robustness)
                    # Note: We prioritize finding the closest contour
                    if dist_sq < min_dist_sq:
                        # Ensure the TrackPy center is reasonably close to the contour
                        if dist_sq < (diameter * diameter * 4): # If center is within 2 diameters
                            min_dist_sq = dist_sq
                            best_contour_area = ft.cv2.contourArea(contour)

            area_list.append(best_contour_area)
            
        # 4.3 Add the shape data back to the TrackPy features DataFrame
        features['area_px'] = area_list
   
        # 5) Draw markers on a copy of the cropped frame and also visualize the binary threshold
        vis = frameCrop.copy()

        # Overlay the thresholded image onto the visualization frame for tuning feedback
        # This shows the user what their chosen 'emberThreshold' is detecting.
        thresh_colored = ft.cv2.cvtColor(thresh, ft.cv2.COLOR_GRAY2BGR)
        vis = ft.cv2.addWeighted(vis, 0.7, thresh_colored, 0.3, 0)

        for _, p in features.iterrows():
            x, y = float(p['x']), float(p['y'])
            center = (int(round(x)), int(round(y)))
            radius = max(2, diameter // 2)

            # Red circle around the detected ember
            ft.cv2.circle(vis, center, radius, (0, 0, 255), 2)
            # Small center dot
            ft.cv2.circle(vis, center, 2, (0, 255, 0), -1)
   
    # 6) Convert vis (BGR numpy array) → QImage → show in your preview label
    totalBytes = vis.nbytes
    bytesPerLine = int(totalBytes / vis.shape[0]) 
    qimg = ft.QImage(
    vis.data,
    vis.shape[1],
    vis.shape[0],
    bytesPerLine,
    ft.QImage.Format.Format_BGR888
    )
    qimg = qimg.scaled(
        self.lbl1_ET.size(),
        ft.Qt.AspectRatioMode.KeepAspectRatio,
        ft.Qt.TransformationMode.SmoothTransformation
    )

    self.frame = qimg
    self.lbl1_ET.setPixmap(ft.QPixmap.fromImage(self.frame))

def detectEmberFeatures(self, frame, currentFrame):
    """
    Detects features, finds contours, and calculates shape metrics for a single frame.
    Returns the features DataFrame.
    """
    frame, frameCrop = ft.checkEditing(self, currentFrame)

    diameter = int(float(self.emberSizeIn.text())*float(self.scaleIn.text()))
    if diameter % 2 == 0: # TrackPy requires odd diameter
        diameter += 1    
  
    try:
        minmass = float(self.emberMinTotIntensity.text())
    except Exception:
        minmass = 10.0
        
    try:
        brightnessThreshold = int(self.brightnessThresholdIn.text())
    except Exception:
        brightnessThreshold = 130
        self.msgLabel.setText('Ember preview: invalid threshold (0-255).')
        return
    # --------------------------------------------------------------------------

    # 2. Preprocessing
    gray = ft.cv2.cvtColor(frameCrop, ft.cv2.COLOR_BGR2GRAY)
    _, thresh = ft.cv2.threshold(gray, brightnessThreshold, 255, ft.cv2.THRESH_BINARY)
    
    # 3. TrackPy Location
    features = tp.locate(
        gray,
        diameter=diameter,
        minmass=minmass,
        separation=diameter, # reasonable default
        preprocess=True # Use TrackPy's internal bandpass filter for robust center finding
    )

    if features is None or len(features) == 0:
        self.msgLabel.setText('Ember preview: no embers detected.')
        return pd.DataFrame() # Return empty DataFrame if nothing is found

    # 4. Contour and Shape Analysis (Matching TrackPy centers to OpenCV contours)
    contours, _ = ft.cv2.findContours(thresh, ft.cv2.RETR_EXTERNAL, ft.cv2.CHAIN_APPROX_SIMPLE)
    area_list = []
        
    for index, p in features.iterrows():
        px, py = p['x'], p['y']
        min_dist_sq = float('inf')
        best_contour_area = 0.0

        for contour in contours:
            M = ft.cv2.moments(contour)
            if M['m00'] > 0:
                cx, cy = M['m10'] / M['m00'], M['m01'] / M['m00']
                dist_sq = (px - cx)**2 + (py - cy)**2
                    
                if dist_sq < min_dist_sq:
                    # Match only if reasonably close
                    if dist_sq < (diameter * diameter * 4): 
                        min_dist_sq = dist_sq
                        best_contour_area = ft.cv2.contourArea(contour)

        area_list.append(best_contour_area)
            
    # Add frame number and shape data
    features['frame'] = currentFrame
    features['area_px'] = area_list

    # 1. Get the image with vectors drawn
    img_with_vectors = drawVelocityVectors(self, currentFrame)
    
    if img_with_vectors is not None:
        # 2. Convert the OpenCV image BGR to RGB (required for QImage)
        rgb_img = ft.cv2.cvtColor(img_with_vectors, ft.cv2.COLOR_BGR2RGB)
        H, W, C = rgb_img.shape
        
        # Create QImage and QPixmap
        q_img = ft.QtGui.QImage(rgb_img.data, W, H, 3 * W, ft.QtGui.QImage.Format.Format_RGB888)
        pixmap = ft.QtGui.QPixmap.fromImage(q_img)
        
    return features


def showTrajectory(self):
    """
    Displays the trajectory snapshot and waits for 'Esc' to close.
    """
    if not hasattr(self, 'tracks_filtered') or self.tracks_filtered is None:
        self.msgLabel.setText("Run tracking first!")
        return

    try:
        current_frame = self.frameNumber 
        traj_img = drawCumulativeTrajectories(self, current_frame)
        
        if traj_img is not None:
            start_f = self.firstFrameIn.text()
            window_title = f"Paths: {start_f} to {current_frame} (Esc to close)"
            
            # 1. Create the window
            ft.cv2.imshow(window_title, traj_img)
            ft.cv2.waitKey(100)
            
            # 2. This keeps the window responsive without freezing your main GUI
            while True:
                # Wait for 10ms for a keypress
                key = ft.cv2.waitKey(10) & 0xFF
                
                # Check if 'Esc' (ASCII 27) was pressed
                if key == 27:
                    break
                
                # OPTIONAL: Check if the user clicked the 'X' button
                # This prevents the app from hanging if you close via mouse
                if ft.cv2.getWindowProperty(window_title, ft.cv2.WND_PROP_VISIBLE) < 1:
                    break
            
            # 3. Clean up: Close ONLY this specific window
            ft.cv2.destroyWindow(window_title)
            
        else:
            self.msgLabel.setText("No tracks found.")

    except Exception as e:
        print(f"Window Error: {e}")
        
        
    
def emberTracking(self):
    """
    Master function to loop through frames, detect features, and link trajectories.
    """
    startTimer = ft.time.perf_counter()
    
    # 1. Parameter and Safety Checks
    if not hasattr(self, "unitScale") or not self.unitScale:
        ft.QMessageBox.warning(self, "Missing unit scale", "Please select a unit scale before starting tracking.")
        return

    firstFrame = int(self.firstFrameIn.text())
    lastFrame = int(self.lastFrameIn.text())
    # maximum distance (in pixels) an ember is allowed to travel between two consecutive frames to still be considered the same particle.
    search_range = int(float(self.searchRangeIn.text())*float(self.scaleIn.text()))
    # how many consecutive frames an ember is allowed to disappear from the video and still be remembered and linked back to its original track when it reappears.
    memory = int(self.frameMemoryIn.text())  
   

    currentFrame = firstFrame
    all_features = [] # List to collect DataFrames from all frames
    
    # 2. Feature Collection Loop (Similar to your lumaTracking while loop)
    while (currentFrame < lastFrame):
                
        try:
            # Get the features for the current frame
            frame, _ = ft.checkEditing(self, currentFrame)
            features = detectEmberFeatures(self, frame, currentFrame) 
            
            if not features.empty:
                all_features.append(features)
        
        except Exception as e:
            print(f"Error processing frame {currentFrame}: {e}")
            self.msgLabel.setText(f"Error at frame {currentFrame}. Check console.")
            break
            
        print('Progress: ', round((currentFrame - firstFrame)/(lastFrame - firstFrame) * 10000)/100, '%', '(Frame #: ', currentFrame, ')', end='\r')
        currentFrame = currentFrame + 1 + int(self.skipFrameIn.text())


    # 3. Combine and Link Features
    if not all_features:
        self.msgLabel.setText('Tracking completed. No features found in any frame.')
        return
        
    feats_all = pd.concat(all_features).reset_index(drop=True)
    
    # Ensure the dataframe is sorted by frame for linking
    feats_all.sort_values(by='frame', inplace=True) 

    # Link the features into trajectories
    tracks = tp.link_df(
        feats_all,
        search_range=search_range,
        memory=memory,
        t_column='frame', 
        adaptive_stop=0.5, # Shrink range until subnetwork is manageable
        adaptive_step=0.95, # Decrease range by 5% each attempt (Shrinks range gradually)
        neighbor_strategy='KDTree' # Fastest math for linking many points   
        # predict=True
    )
    

    # Filter out "stub" (short) trajectories, keeping only those longer than 'memory'
    self.tracks_filtered = tp.filter_stubs(tracks, threshold=memory + 1)

    # Integrate the calculation helper here
    if not self.tracks_filtered.empty:
        self.tracks_filtered = calculateMetrics(self, self.tracks_filtered)
        print('Calculated velocity and speed metrics for tracked embers.')
    
    endTimer = ft.time.perf_counter()
    runTime = ft.np.round(endTimer - startTimer, 4)
    
    num_tracks = self.tracks_filtered['particle'].nunique()
    
    txtMessage = f'Tracking complete. Found {num_tracks} trajectories. Run time: {runTime} s.'
    print(txtMessage)
    self.msgLabel.setText(txtMessage)

    return self.tracks_filtered

def ETTrackingPlot(label, x, y, name, symbol, color):
    pen = ft.pg.mkPen(color)
    label.plot(x, y, pen = pen, name = name, symbol = symbol, symbolSize = 7, symbolBrush = (color))

def calculateMetrics(self, tracks_df):
    """Calculates instantaneous velocity and speed and adds them to the DataFrame."""
    
    # 1. Get the time interval (Delta t) in frames
    skip_count = int(self.skipFrameIn.text()) if self.skipFrameIn.text() else 0
    frame_interval = 1 + skip_count

    # 2. Calculate difference in position between consecutive frames for each particle
    # The calculation is grouped by 'particle' so diff() only compares points belonging 
    # to the same ember, setting NaNs at the start of each track.
    
    # Velocity components (vx and vy) in [px/frame]
    tracks_df['vx_px'] = tracks_df.groupby('particle')['x'].diff() / frame_interval
    tracks_df['vy_px'] = tracks_df.groupby('particle')['y'].diff() / frame_interval
    
    # 3. Calculate Instantaneous Speed (magnitude of velocity) in [px/frame]
    tracks_df['speed_px'] = ft.np.sqrt(tracks_df['vx_px']**2 + tracks_df['vy_px']**2)

    return tracks_df


def showVelocity(self):
    """
    Displays the velocity history and waits for 'Esc' to close.
    """
    if not hasattr(self, 'tracks_filtered') or self.tracks_filtered is None:
        self.msgLabel.setText("Run tracking first!")
        return

    try:
        current_frame = self.frameNumber 
        # Generate the cumulative image from your logic file
        vector_img = drawVelocityVectors(self, current_frame)
        
        if vector_img is not None:
            start_frame = self.firstFrameIn.text()
            window_title = f"Velocity Field at frame {current_frame} (Esc to close)"
            
            # 1. Create the window
            ft.cv2.imshow(window_title, vector_img)
            ft.cv2.waitKey(100)
            
            # 2. This keeps the window responsive without freezing main GUI
            while True:
                # Wait for 10ms for a keypress
                key = ft.cv2.waitKey(10) & 0xFF
                
                # Check if 'Esc' (ASCII 27) was pressed
                if key == 27:
                    break
                
                # OPTIONAL: Check if the user clicked the 'X' button
                if ft.cv2.getWindowProperty(window_title, ft.cv2.WND_PROP_VISIBLE) < 1:
                    break
            
            # 3. Clean up: Close ONLY this specific window
            ft.cv2.destroyWindow(window_title)
            
        else:
            self.msgLabel.setText("No tracks found.")

    except Exception as e:
        print(f"Window Error: {e}")


def animateVelocityVectors(self):
    if not hasattr(self, 'tracks_filtered') or self.tracks_filtered.empty:
        return

    # 1. Timing Setup
    fps = (float(self.vFps))/(int(self.skipFrameIn.text()) + 1)
    speed_text = self.animationSpeed.currentText().replace('x', '')
    multiplier = float(speed_text)
    preview_delay = int(1000 / (fps * multiplier))
    output_fps = fps * multiplier

    # 2. Video Saving Setup
    video_writer = None
    # save_active = self.saveAnimation_box.isChecked()
    
    if self.saveAnimation_box.isChecked():
        # base_name = self.fNameLbl.text().split('.')[0]
        animation_name = self.fPath[0] + '-embers-{speed_text}x.mp4'
        # save_name = f"{base_name}-embers-{speed_text}x.mp4"
        test_img = drawEmberAnalysis(self, int(self.firstFrameIn.text()), mode='tail')
        h, w, _ = test_img.shape
        video_writer = ft.cv2.VideoWriter(animation_name, ft.cv2.VideoWriter_fourcc(*'mp4v'), output_fps, (w, h))

    # 3. Main Playback Loop
    frames = self.tracks_filtered['frame'].unique()
    start_frame, end_frame = frames.min(), frames.max()
    window_title = f"Ember Tracking from {start_frame} to {end_frame} (Esc to close)"
    
    first_pass = True
    keep_running = True

    while keep_running:
        for f in range(start_frame, end_frame + 1):
            img = drawEmberAnalysis(self, f, mode='tail')
            if img is not None:
                ft.cv2.imshow(window_title, img)
                # Only write to video file during the FIRST loop iteration
                if video_writer and first_pass:
                    video_writer.write(img)

            key = ft.cv2.waitKey(preview_delay) & 0xFF
            if key == 27: # Esc
                keep_running = False
                break
            

        # Close video writer after first pass completes
        if first_pass and video_writer:
            video_writer.release()
            video_writer = None
            self.msgLabel.setText(f"File saved. Continuing playback loop...")
        
        first_pass = False # Subsequent loops won't attempt to save

    ft.cv2.destroyWindow(window_title)

def drawVelocityVectors(self, frame_num):
    """
    Draws thin velocity vectors for a single frame. 
    Returns the processed BGR image.
    """
    if not hasattr(self, 'tracks_filtered') or self.tracks_filtered is None:
        return None

    # Fix the 'frame' column ambiguity
    df = self.tracks_filtered.reset_index(drop=True)
    
    # Filter for the current frame and drop NaNs
    frame_data = df[df['frame'] == frame_num].copy()
    critical_cols = ['x', 'y', 'vx_px', 'vy_px']
    frame_data = frame_data.dropna(subset=critical_cols)

    # Get background image
    _, frameCrop = ft.checkEditing(self, frame_num)
    img = frameCrop.copy()
    if len(img.shape) == 2:
        img = ft.cv2.cvtColor(img, ft.cv2.COLOR_GRAY2BGR)

    # Drawing settings: Smaller and thinner for the "Snapshot"
    scale_factor = 2
    
    for _, row in frame_data.iterrows():
        try:
            x1, y1 = int(row['x']), int(row['y'])
            vx, vy = row['vx_px'], row['vy_px']
            
            x2 = int(x1 + vx * scale_factor)
            y2 = int(y1 + vy * scale_factor)

            # Draw thin blue arrow (thickness=1)
            ft.cv2.arrowedLine(img, (x1, y1), (x2, y2), (255, 0, 0), 2, tipLength=0.2)
            
        except (ValueError, OverflowError):
            continue

    return img

def drawCumulativeTrajectories(self, current_frame):
    if not hasattr(self, 'tracks_filtered') or self.tracks_filtered is None:
        return None

    df = self.tracks_filtered.reset_index(drop=True)
    
    # Check if there's a weird duplicate 'level_0' column and drop it if so
    if 'level_0' in df.columns:
        df = df.drop(columns=['level_0'])

    # Get start frame from the GUI input box
    try:
        start_frame = int(self.firstFrameIn.text()) 
    except:
        start_frame = df['frame'].min()

    # Get the image
    _, frameCrop = ft.checkEditing(self, current_frame)
    img = frameCrop.copy()
    if len(img.shape) == 2: 
        img = ft.cv2.cvtColor(img, ft.cv2.COLOR_GRAY2BGR)

    # Filter data: Start -> Current
    mask = (df['frame'] >= start_frame) & (df['frame'] <= current_frame)
    history = df[mask]

    for p_id in history['particle'].unique():
        p_path = history[history['particle'] == p_id].sort_values('frame')
        
        if len(p_path) > 1:
            # Draw the green path
            pts = p_path[['x', 'y']].values.astype(ft.np.int32)
            ft.cv2.polylines(img, [pts], False, (0, 255, 0), 1)
            
            # Draw the current position (the 'head')
            current_pos = pts[-1]
            ft.cv2.circle(img, (int(current_pos[0]), int(current_pos[1])), 3, (0, 255, 0), -1)

    return img


def showCombined(self):
    """
    Displays green historical trajectories with current velocity arrows.
    Waits for 'Esc' to close.
    """
    if not hasattr(self, 'tracks_filtered') or self.tracks_filtered is None:
        self.msgLabel.setText("Run tracking first!")
        return

    try:
        current_frame = self.frameNumber
        
        # Call the logic that combines paths + current vectors
        combined_img = drawCombinedAnalysis(self, current_frame)
        
        if combined_img is not None:
            start_f = self.firstFrameIn.text()
            window_title = f"Analysis: {start_f} to {current_frame} (Esc to close)"
            
            # 1. Create and show window
            ft.cv2.imshow(window_title, combined_img)
            ft.cv2.waitKey(100) # Mac safety delay
            
            # 2. Event loop
            while True:
                key = ft.cv2.waitKey(10) & 0xFF
                if key == 27: # Esc
                    break
                
                # Check if window was closed via 'X'
                if ft.cv2.getWindowProperty(window_title, ft.cv2.WND_PROP_VISIBLE) < 1:
                    break
            
            # 3. Clean up
            ft.cv2.destroyWindow(window_title)
            
        else:
            self.msgLabel.setText("No tracks found for this frame.")

    except Exception as e:
        print(f"Window Error: {e}")



def drawCombinedAnalysis(self, current_frame):
    """
    Draws full historical paths (Green) and current velocity (Red).
    """
    # 1. Start with the historical green paths
    img = drawCumulativeTrajectories(self, current_frame)
    if img is None:
        return None

    # 2. Get ONLY the current frame's data for the arrows
    df = self.tracks_filtered.reset_index(drop=True)
    current_data = df[df['frame'] == current_frame].dropna(subset=['x', 'y', 'vx_px', 'vy_px'])
    
    # 3. Draw the blue arrows at the tips of the green lines
    scale_factor = 2.0 # Smaller size as requested
    for _, row in current_data.iterrows():
        x1, y1 = int(row['x']), int(row['y'])
        vx, vy = row['vx_px'], row['vy_px']
        
        x2 = int(x1 + vx * scale_factor)
        y2 = int(y1 + vy * scale_factor)

        # Draw current vector
        ft.cv2.arrowedLine(img, (x1, y1), (x2, y2), (255, 0, 0), 2, tipLength=0.2)

    return img


def showCharactSelection(self):
    # get value box:
    selected_text = self.showCharact_Box.currentText()
    if selected_text == 'Trajectories':
        showTrajectory(self)
    elif selected_text == 'Velocities':
        showVelocity(self)
    elif selected_text == 'Combined':
        showCombined(self)


def saveEmberPar(self):
    name, _ = ft.QFileDialog.getSaveFileName(self, 'Save Ember Parameters', '', 'CSV Files (*.csv)')
    if not name: return
    if not name.endswith('.csv'): name += '.csv'

    try:
        with open(name, 'w', newline='') as f:
            writer = ft.csv.writer(f)
            writer.writerow(['Parameter', 'Value'])
            writer.writerow(['Threshold', self.brightnessThresholdIn.text()])
            writer.writerow(['Diameter', self.emberSizeIn.text()])
            writer.writerow(['Min Tot Intensity', self.emberMinTotIntensity.text()])
            writer.writerow(['Search Range', self.searchRangeIn.text()])
            writer.writerow(['Memory', self.frameMemoryIn.text()])
            
        self.msgLabel.setText('Ember parameters saved.')
    except Exception as e:
        self.msgLabel.setText(f'Error saving params: {e}')

def loadEmberPar(self):
    name, _ = ft.QFileDialog.getOpenFileName(self, 'Load Ember Parameters', '', 'CSV Files (*.csv)')
    if not name: return

    try:
        with open(name, 'r') as f:
            reader = ft.csv.reader(f)
            next(reader) # Skip header
            for row in reader:
                if row[0] == 'Threshold': self.brightnessThresholdIn.setText(row[1])
                elif row[0] == 'Diameter': self.emberSizeIn.setText(row[1])
                elif row[0] == 'Min Tot Intensity': self.emberMinTotIntensity.setText(row[1])
                elif row[0] == 'Search Range': self.searchRangeIn.setText(row[1])
                elif row[0] == 'Memory': self.frameMemoryIn.setText(row[1])

        self.msgLabel.setText('Ember parameters loaded.')
    except Exception as e:
        self.msgLabel.setText(f'Error loading params: {e}')


def saveEmberResults(self):
    if not hasattr(self, 'tracks_filtered') or self.tracks_filtered is None:
        self.msgLabel.setText("No data to save. Run tracking first.")
        return

    fileName, _ = ft.QFileDialog.getSaveFileName(self, 'Save Tracking Data', '', 'CSV Files (*.csv)')
    if not fileName: return
    if not fileName.endswith('.csv'): fileName += '.csv'

    try:
        # 1. Prepare a copy of the data
        export_df = self.tracks_filtered.copy().reset_index(drop=True)
        
        # 2. Convert to physical units (Assuming self.scale is px/unit)
        scale = float(self.scaleIn.text()) if self.scaleIn.text() else 1.0
        unit = self.unitScale 
        
        export_df[f'x_{unit}'] = export_df['x'] / scale
        export_df[f'y_{unit}'] = export_df['y'] / scale
        export_df[f'vx_{unit}_per_frame'] = export_df['vx_px'] / scale
        export_df[f'vy_{unit}_per_frame'] = export_df['vy_px'] / scale
        export_df[f'speed_{unit}_per_frame'] = export_df['speed_px'] / scale

        # 3. Save to CSV (Pandas handles headers and rows automatically)
        export_df.to_csv(fileName, index=False)
        
        self.msgLabel.setText(f'Data saved successfully in {fileName}.')
        
    except Exception as e:
        print(f"Save Error: {e}")
        self.msgLabel.setText(f'Error saving results: {e}')


def drawEmberAnalysis(caller, current_frame, mode='tail'):
    if not hasattr(caller, 'tracks_filtered') or caller.tracks_filtered is None:
        return None

    df = caller.tracks_filtered.reset_index(drop=True)
    
    # 1. Setup Frame Range
    start_limit = int(caller.firstFrameIn.text())
    display_start = max(start_limit, current_frame - 9) if mode == 'tail' else start_limit

    # 2. Get Background
    _, frameCrop = ft.checkEditing(caller, current_frame)
    img = frameCrop.copy()
    if len(img.shape) == 2:
        img = ft.cv2.cvtColor(img, ft.cv2.COLOR_GRAY2BGR)

    # 3. Filter Data
    mask = (df['frame'] >= display_start) & (df['frame'] <= current_frame)
    history = df[mask]

    scale_factor = 2  # Adjust this to control arrow length
    
    for p_id in history['particle'].unique():
        p_path = history[history['particle'] == p_id].sort_values('frame')
        
        # Draw Tail (Green)
        if mode != 'snap' and len(p_path) > 1:
            pts = p_path[['x', 'y']].values.astype(ft.np.int32)
            ft.cv2.polylines(img, [pts], False, (0, 255, 0), 1, lineType=ft.cv2.LINE_AA)

        # Draw "Quiver-style" Arrow (Blue)
        curr_row = p_path[p_path['frame'] == current_frame]
        if not curr_row.empty:
            row = curr_row.iloc[0]
            if not ft.np.isnan(row['vx_px']):
                x1, y1 = int(row['x']), int(row['y'])
                x2 = int(x1 + row['vx_px'] * scale_factor)
                y2 = int(y1 + row['vy_px'] * scale_factor)
                
                # tipLength is a fraction of the line length. 
                # 0.3 on a short line makes a tiny, sharp point.
                ft.cv2.arrowedLine(img, (x1, y1), (x2, y2), (255, 0, 0), 2, 
                                   tipLength=0.2, line_type=ft.cv2.LINE_AA)
    return img