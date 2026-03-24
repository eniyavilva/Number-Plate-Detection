# Number Plate Detection System

## About
A real-time number plate detection system built using Python and OpenCV. The system uses a camera feed to detect and read vehicle number plates using OCR (Optical Character Recognition).

## Problem it solves
In traffic enforcement, police often fail to stop overspeeding vehicles or two-wheeler riders not wearing helmets in time. This system helps by automatically detecting and reading the number plate of the vehicle, making it easier to identify the owner and take action even after the vehicle has passed.

## How it works
- Opens a live camera feed
- Captures video frames continuously
- Uses EasyOCR to read text from each frame
- Filters detections by confidence score
- Displays detected number plates on screen in real time

## Technologies used
- Python
- OpenCV — for camera capture and image processing
- EasyOCR — for optical character recognition

## How to run
```
pip install opencv-python easyocr
python start.py
```

## Author
Eniyavilva Thirumurugan  
