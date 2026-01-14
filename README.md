# Gesture-Controlled Virtual Mouse 🖱️

This project implements a virtual mouse using hand gestures and computer vision.

## ✋ Gesture Controls

Gesture               | Action
----------------------|------------------------------
Index finger          | Move mouse cursor
Index + Middle        | Left / Double click
Index + Pinky         | Right click
Middle finger         | Scroll (vertical & horizontal)
Thumb + Index (pinch) | Zoom in / Zoom out

## Tech Stack
- Python
- OpenCV
- MediaPipe
- NumPy
- AutoPy
- PyAutoGUI

## Attribution
The hand tracking module (`handmodule2.py`) is adapted from the 
freeCodeCamp.org Computer Vision tutorial.  
The gesture interpretation and virtual mouse logic are custom implemented.

## How to Run
```bash
python virtual_mouse.py
