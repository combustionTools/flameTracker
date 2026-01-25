"""
Flame Tracker. This program is designed to track flames or bright objects in videos or images.
Copyright (C) 2020,2026  Luca Carmignani

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

### This connects this specific file to the main code (flameTracker.py)
import flameTracker as ft
import boxesGUI_OS as gui # for the objects in the user interface
import glob
import os
import re

def initVars(self): # define initial variables
    global a, b
    var = 0

def videoStitching(self, par):
    # The video editing is covered by the Flame Tracker code, here only the independent analysis should be included
    print('hi world')  # Placeholder for actual video stitching logic



### here you can write the text for the help button
def helpBtn_clicked(self):
    msg = QMessageBox(self)
    msg.setText('This Flame Tracker option is designed to stitch together multiple image files into a single video.')
    msg.exec_()


def folder1Btn_clicked(self):
    # Open a file dialog to select the folder containing the first set of images
    # Pick the folder
    folder1 = ft.QFileDialog.getExistingDirectory(self, "Select Folder 1")
    if not folder1:
        print("No folder selected for Folder 1")
        return

    self.folder1Txt.setText(folder1)
    print(f"Folder 1 selected: {folder1}")

    # Get image files in natural order
    self.frames1 = list_frames(folder1, exts=("*.png", "*.jpg", "*.jpeg", "*.JPEG", "*.tif", "*.tiff"))
    print(f"Found {len(self.frames1)} frames in folder 1")

def folder2Btn_clicked(self):
    ## Open a file dialog to select the folder containing the first set of images
    # Pick the folder
    folder2 = ft.QFileDialog.getExistingDirectory(self, "Select Folder 2")
    if not folder2:
        print("No folder selected for Folder 1")
        return

    self.folder2Txt.setText(folder2)
    print(f"Folder 2 selected: {folder2}")

    # Get image files in natural order
    self.frames2 = list_frames(folder2, exts=("*.png", "*.jpg", "*.jpeg", "*.JPEG", "*.tif", "*.tiff"))
    print(f"Found {len(self.frames2)} frames in folder 1")

def calibrationFrameBtn_clicked(self):
    if not getattr(self, "frames1", None):
        ft.QMessageBox.warning(self, "Calibration frame", "Pick a folder first.")
        return

    start_dir = self.folder1Txt.text() if hasattr(self, "folder1Txt") else os.path.dirname(self.frames1[0])
    fname, _ = ft.QFileDialog.getOpenFileName(
        self,
        "Select calibration frame",
        start_dir,
        "Images (*.png *.jpg *.jpeg *.tif *.tiff)"
    )
    if not fname:
        return

    # Normalize paths to avoid mismatch (symlinks/relative vs absolute)
    norm = os.path.abspath
    frames_norm = [norm(p) for p in self.frames1]
    fname_norm = norm(fname)

    try:
        self.ref_index = frames_norm.index(fname_norm)
    except ValueError:
        ft.QMessageBox.warning(self, "Calibration", "Selected file is not in the chosen folder’s image list.")
        return

    # # (Optional) show a preview thumbnail in a QLabel called self.previewLbl
    # if hasattr(self, "previewLbl"):
    #     pix = QPixmap(fname_norm)
    #     if not pix.isNull():
    #         self.previewLbl.setPixmap(pix.scaled(
    #             self.previewLbl.size(),
    #             Qt.AspectRatioMode.KeepAspectRatio,
    #             Qt.TransformationMode.SmoothTransformation
    #         ))
    # Update any UI elements
    if hasattr(self, "refSpinBox"):
        self.refSpinBox.setMaximum(len(self.frames1)-1)
        self.refSpinBox.setValue(self.ref_index)

    # Enable Calibrate button now that we have a ref frame
    if hasattr(self, "calibrateButton"):
        self.calibrateButton.setEnabled(True)

    print(f"Calibration frame selected: index {self.ref_index} -> {self.frames1[self.ref_index]}")
        
def calibrationFrame2Btn_clicked(self):
    if not getattr(self, "frames2", None):
        ft.QMessageBox.warning(self, "Calibration frame", "Pick a folder first.")
        return

    start_dir = self.folder2Txt.text() if hasattr(self, "folder2Txt") else os.path.dirname(self.frames2[0])
    fname, _ = ft.QFileDialog.getOpenFileName(
        self,
        "Select calibration frame",
        start_dir,
        "Images (*.png *.jpg *.jpeg *.tif *.tiff)"
    )
    if not fname:
        return

    # Normalize paths to avoid mismatch (symlinks/relative vs absolute)
    norm = os.path.abspath
    frames_norm = [norm(p) for p in self.frames2]
    fname_norm = norm(fname)

    try:
        self.ref_index = frames_norm.index(fname_norm)
    except ValueError:
        ft.QMessageBox.warning(self, "Calibration", "Selected file is not in the chosen folder’s image list.")
        return

    # # (Optional) show a preview thumbnail in a QLabel called self.previewLbl
    # if hasattr(self, "previewLbl"):
    #     pix = QPixmap(fname_norm)
    #     if not pix.isNull():
    #         self.previewLbl.setPixmap(pix.scaled(
    #             self.previewLbl.size(),
    #             Qt.AspectRatioMode.KeepAspectRatio,
    #             Qt.TransformationMode.SmoothTransformation
    #         ))
    # Update any UI elements
    if hasattr(self, "refSpinBox"):
        self.refSpinBox.setMaximum(len(self.frames2)-1)
        self.refSpinBox.setValue(self.ref_index)

    # Enable Calibrate button now that we have a ref frame
    if hasattr(self, "calibrateButton"):
        self.calibrateButton.setEnabled(True)

    print(f"Calibration frame selected: index {self.ref_index} -> {self.frames2[self.ref_index]}")

def natural_sort_key(path):
    # Sort ... 1, 2, 10 (not 1,10,2)
    name = os.path.basename(path)
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', name)]

def list_frames(folder, exts=("*.png", "*.jpg", "*.jpeg", "*.tif", "*.tiff")):
    paths = []
    for ext in exts:
        paths.extend(glob.glob(os.path.join(folder, ext)))
    paths.sort(key=natural_sort_key)
    return paths


def calibrationBtn_clicked(self):
    # Basic checks
    if not getattr(self, "frames1", None) or not getattr(self, "frames2", None):
        print("Pick both folders first.")
        return
    n = min(len(self.frames1), len(self.frames2))
    if n == 0:
        print("No frames to calibrate.")
        return

    idx = getattr(self, "ref_index", 0)
    idx = max(0, min(idx, n-1))

    img1_path = self.frames1[idx]  # Cam1 reference frame
    img2_path = self.frames2[idx]  # Cam2 frame at same index

    try:
        if hasattr(self, "statusbar"): self.statusbar.showMessage("Calibrating…")
        calib = calibrate_from_pair(img1_path, img2_path)
        self.calib = calib  # store for stitching
        (W, H) = calib["out_size"]
        print(f"Calibration OK. Canvas: {W}x{H}")
        if hasattr(self, "statusbar"): self.statusbar.showMessage(f"Calibration OK. Canvas: {W}x{H}", 5000)

        # (Optional) enable your “Run/Export” button now:
        if hasattr(self, "runButton"): self.runButton.setEnabled(True)

    except Exception as e:
        print(f"Calibration failed: {e}")
        if hasattr(self, "statusbar"): self.statusbar.showMessage("Calibration failed.")

def _detect_and_match(imgA, imgB):
    """Return homography H: B→A using SIFT (if available) or ORB + RANSAC."""
    gA = ft.cv2.cvtColor(imgA, ft.cv2.COLOR_BGR2GRAY)
    gB = ft.cv2.cvtColor(imgB, ft.cv2.COLOR_BGR2GRAY)

    if hasattr(ft.cv2, 'SIFT_create'):
        det, norm, ratio = ft.cv2.SIFT_create(), ft.cv2.NORM_L2, 0.75
    else:
        det, norm, ratio = ft.cv2.ORB_create(nfeatures=5000), ft.cv2.NORM_HAMMING, 0.8

    kA, dA = det.detectAndCompute(gA, None)
    kB, dB = det.detectAndCompute(gB, None)
    if dA is None or dB is None:
        raise RuntimeError("No keypoints/descriptors found.")

    bf = ft.cv2.BFMatcher(norm, crossCheck=False)
    knn = bf.knnMatch(dB, dA, k=2)  # want H: B→A
    good = [m for m, n in knn if m.distance < ratio * n.distance]
    if len(good) < 12:
        raise RuntimeError(f"Not enough good matches ({len(good)}).")

    ptsB = ft.np.float32([kB[m.queryIdx].pt for m in good])
    ptsA = ft.np.float32([kA[m.trainIdx].pt for m in good])

    H, inliers = ft.cv2.findHomography(ptsB, ptsA, ft.cv2.RANSAC, 3.0)
    if H is None:
        raise RuntimeError("findHomography failed.")
    return H.astype(ft.np.float32)

def _warp_corners(w, h, H):
    c = ft.np.float32([[0,0],[w,0],[w,h],[0,h]]).reshape(-1,1,2)
    return ft.cv2.perspectiveTransform(c, H).reshape(-1,2)

def calibrate_from_pair(img1_path, img2_path):
    """Calibrate Cam2→Cam1 on a single reference pair. Returns dict with H21_t, T, out_size."""
    img1 = ft.cv2.imread(img1_path, ft.cv2.IMREAD_COLOR)  # Cam1 (reference plane)
    img2 = ft.cv2.imread(img2_path, ft.cv2.IMREAD_COLOR)  # Cam2 (to be warped into Cam1)
    if img1 is None or img2 is None:
        raise FileNotFoundError("Reference images failed to load.")

    H21 = _detect_and_match(img1, img2)  # Cam2 → Cam1

    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    c1 = ft.np.float32([[0,0],[w1,0],[w1,h1],[0,h1]])        # Cam1 corners in Cam1 coords
    c2 = _warp_corners(w2, h2, H21)                        # Cam2 corners mapped into Cam1 coords

    allp = ft.np.vstack([c1, c2])
    min_xy = ft.np.floor(allp.min(axis=0)).astype(int)
    max_xy = ft.np.ceil(allp.max(axis=0)).astype(int)

    tx = -min(0, min_xy[0])
    ty = -min(0, min_xy[1])
    T = ft.np.array([[1,0,tx],[0,1,ty],[0,0,1]], dtype=np.float32)  # translate so everything is >= 0

    out_w = int(max_xy[0] + tx)
    out_h = int(max_xy[1] + ty)

    H21_t = (T @ H21).astype(ft.np.float32)  # translated homography, ready to use in warpPerspective
    return {"H21_t": H21_t, "T": T, "out_size": (out_w, out_h)}