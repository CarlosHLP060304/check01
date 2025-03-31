import cv2
import numpy as np

cap = cv2.VideoCapture("./project_video.mp4")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Apply GaussianBlur to reduce noise
    frame = cv2.GaussianBlur(frame, (5, 5), 0)

    # Convert to HSV for better color segmentation
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the yellow color range in HSV
    low_yellow = np.array([18, 94, 140])
    up_yellow = np.array([48, 255, 255])

    # Define the white color range in HSV
    low_white = np.array([0, 0, 200])  # Low threshold for white color
    up_white = np.array([180, 30, 255])  # High threshold for white color
    
    # Create masks for yellow and white colors
    mask_yellow = cv2.inRange(hsv, low_yellow, up_yellow)
    mask_white = cv2.inRange(hsv, low_white, up_white)

    # Detect edges using Canny on the yellow and white masks
    edges_yellow = cv2.Canny(mask_yellow, 75, 150)
    edges_white = cv2.Canny(mask_white, 75, 150)

    # Use Hough Transform to detect yellow lines
    lines_yellow = cv2.HoughLinesP(edges_yellow, 1, np.pi / 180, 50, maxLineGap=50)

    # Use Hough Transform to detect white lines
    lines_white = cv2.HoughLinesP(edges_white, 1, np.pi / 180, 50, maxLineGap=50)

    # Draw detected yellow lines
    if lines_yellow is not None:
        for line in lines_yellow:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green for yellow lines

    # Draw detected white lines
    if lines_white is not None:
        for line in lines_white:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blue for white lines

    # Display the frames
    cv2.imshow("frame", frame)
    cv2.imshow("edges_yellow", edges_yellow)
    cv2.imshow("edges_white", edges_white)

    key = cv2.waitKey(25)

    if key == 27:
        break

# Release the video capture and close the windows after the loop ends
cap.release()
cv2.destroyAllWindows()
