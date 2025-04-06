import cv2
import numpy as np

def readVideo(name):
    return cv2.VideoCapture(name)

def applyGaussianBlur(frame):
    return cv2.GaussianBlur(frame, (5, 5), 0)

def convertToHsv(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

def drawYellowLines(frame):
    hsv = convertToHsv(frame)
    low_yellow = np.array([18, 94, 140])
    up_yellow = np.array([48, 255, 255])
    mask_yellow = cv2.inRange(hsv, low_yellow, up_yellow)
    edges_yellow = cv2.Canny(mask_yellow, 75, 150)
    lines_yellow = cv2.HoughLinesP(edges_yellow, 1, np.pi / 180, 50, maxLineGap=50)
    if lines_yellow is not None:
        for line in lines_yellow:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

def drawWhiteLines(frame):
    h, w, c = frame.shape
    roi = frame[h//2:h, :w//2+w//4] 
    cv2.imshow("ROI", roi)  # Exibir a região de interesse
    hsv = convertToHsv(roi)
    low_white = np.array([0, 0, 200]) 
    up_white = np.array([180, 30, 255])  
    mask_white = cv2.inRange(hsv, low_white, up_white)    
    edges_white = cv2.Canny(mask_white, 75, 150)
    lines_white = cv2.HoughLinesP(edges_white, 1, np.pi / 180, 50, maxLineGap=50)
    if lines_white is not None:
        for line in lines_white:
            x1, y1, x2, y2 = line[0]                 
            cv2.line(roi, (x1, y1), (x2, y2), (255, 0, 0), 2) 

def captureBlackVehicles(frame):
    h, w, c = frame.shape
    roi = frame[h // 2 + h//14 : h , w//2 : w//2+w//4+w//4]
    hsv = convertToHsv(roi)
    low_black = np.array([0, 0, 0])  # Limite inferior para preto
    up_black = np.array([180, 255, 50])  # Limite superior para preto
    mask_black = cv2.inRange(hsv, low_black, up_black)
    contours_black, _ = cv2.findContours(mask_black, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours_black:
        x, y, w, h = cv2.boundingRect(cnt)
        if w * h > 3000:  # Filtrar pequenos ruídos
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 0, 0), 2)
            cv2.putText(roi, "Vehicle Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

def captureWhiteVehicles(frame):
    h, w, c = frame.shape
    roi = frame[h // 2 :h//2+h//4, w//2+w//7:w] 
    cv2.imshow("RI", roi)  # Exibir a região de interesse
    # Detectar veículos brancos
    hsv = convertToHsv(roi)
    low_white = np.array([0, 0, 200])  # Limite inferior para branco
    up_white = np.array([180, 30, 255])  # Limite superior para branco
    mask_white = cv2.inRange(hsv, low_white, up_white)
    contours_white, _ = cv2.findContours(mask_white, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours_white:
        x, y, w, h = cv2.boundingRect(cnt)
        if w * h > 3000 and h>40 :  # Filtrar pequenos ruídos
            cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 255, 255), 2)
            cv2.putText(roi, "Vehicle Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

def captureVehicles(frame):
    captureBlackVehicles(frame)
    captureWhiteVehicles(frame)

def displayFrame(frame):
    cv2.imshow("frame", frame)

def returnKey():
    return cv2.waitKey(25)

def destroyAllWindows():
    cv2.destroyAllWindows()