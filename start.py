import cv2
import easyocr
import numpy as np
import re
import warnings

warnings.filterwarnings('ignore')

reader = easyocr.Reader(['en'])
cap = cv2.VideoCapture(0)
frame_count = 0

def is_license_plate(text):
   
    text_clean = text.replace(" ", "").strip()
    
  
    pattern = r'^[A-Z]{2}\d{2}[A-Z]\d{4}$'
    
    if re.match(pattern, text_clean):
        return True
    

    pattern_with_space = r'^[A-Z]{2}\d{2}\s[A-Z]\d{4}$'
    if re.match(pattern_with_space, text):
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
    
    
    if frame_count % 5 == 0:

        results = reader.readtext(enhanced, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        for (bbox, text, confidence) in results:
            
            if confidence > 0.6 and is_license_plate(text):
                print(f"License Plate Detected: {text} (Confidence: {confidence:.2f})")
               
                pts = [(int(p[0]), int(p[1]) + h//2) for p in bbox]
                cv2.polylines(frame, [np.array(pts)], True, (0, 255, 0), 2)
               
                cv2.putText(frame, text, (int(pts[0][0]), int(pts[0][1]) - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    cv2.imshow('Number Plate Detector', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()