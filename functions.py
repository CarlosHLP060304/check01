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
    hsv = convertToHsv(frame)
    low_white = np.array([0, 0, 200]) 
    up_white = np.array([180, 30, 255])  
    mask_white = cv2.inRange(hsv, low_white, up_white)    
    edges_white = cv2.Canny(mask_white, 75, 150)
    lines_white = cv2.HoughLinesP(edges_white, 1, np.pi / 180, 50, maxLineGap=50)
    if lines_white is not None:
        for line in lines_white:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2) 

def displayFrame(frame):
    cv2.imshow("frame", frame)

def returnKey():
    return cv2.waitKey(25)

def destroyAllWindows():
    cv2.destroyAllWindows()