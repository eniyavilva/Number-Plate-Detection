import cv2
import easyocr
import numpy as np
import re
import warnings
import datetime

warnings.filterwarnings('ignore')

reader = easyocr.Reader(['en'])
cap = cv2.VideoCapture(0)
frame_count = 0


ignored_words = [
    "menu", "home", "you", "exit", "back", "next", "ok", "cancel", "settings", "help", "about", "close", "open", "save", "load",
    "file", "edit", "view", "tools", "window", "search", "find", "replace", "copy", "paste", "cut", "delete", "select", "all",
    "none", "yes", "no", "true", "false", "on", "off", "start", "stop", "pause", "play", "record", "rewind", "forward",
    "volume", "mute", "full", "screen", "zoom", "in", "out", "reset", "clear", "undo", "redo", "new", "print", "export",
    "import", "share", "download", "upload", "login", "logout", "sign", "up", "register", "forgot", "password", "username",
    "email", "phone", "address", "name", "first", "last", "middle", "title", "company", "city", "state", "zip", "country",
    "date", "time", "year", "month", "day", "hour", "minute", "second", "am", "pm", "monday", "tuesday", "wednesday",
    "thursday", "friday", "saturday", "sunday", "january", "february", "march", "april", "may", "june", "july", "august",
    "september", "october", "november", "december"
]

def is_license_plate(text):
    text_clean = text.replace(" ", "").strip()
    
   
    if text_clean.lower() in ignored_words:
        return False
    
   
    pattern = r'^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$'
    
    if re.match(pattern, text_clean):
        return True
    
    
    pattern_with_space = r'^[A-Z]{2}\d{2}\s[A-Z]{2}\d{4}$'
    if re.match(pattern_with_space, text):
        return True
    
    
    pattern_with_hyphen = r'^[A-Z]{2}\d{2}-[A-Z]{2}\d{4}$'
    if re.match(pattern_with_hyphen, text):
        return True
    
    return False
cap = cv2.VideoCapture(0)
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_count += 1
    

    h, w = frame.shape[:2]
    roi = frame[int(h*0.4):, :] 
 
    
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    
    
    plate_detected = False
    if frame_count % 5 == 0:

        results = reader.readtext(enhanced, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        for (bbox, text, confidence) in results:
            
            if confidence > 0.6 and is_license_plate(text):
                print(f"License Plate Detected: {text} (Confidence: {confidence:.2f})")
                
               
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open("detected_plates.txt", "a") as log_file:
                    log_file.write(f"{timestamp} - License Plate Detected: {text} (Confidence: {confidence:.2f})\n")
               
                pts = [(int(p[0]), int(p[1]) + h//2) for p in bbox]
                cv2.polylines(frame, [np.array(pts)], True, (0, 255, 0), 2)
               
                cv2.putText(frame, f"{text} ({confidence:.2f})", (int(pts[0][0]), int(pts[0][1]) - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                plate_detected = True
    
    # Add title/label on the camera window
    cv2.putText(frame, "Number Plate Detector", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Show message when no plate is detected
    if not plate_detected:
        cv2.putText(frame, "No license plate detected", (10, h - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()