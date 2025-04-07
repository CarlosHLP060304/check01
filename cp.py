from functions import *

cap = readVideo("project_video.mp4")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = applyGaussianBlur(frame)
    frame = process_frame(frame)
    drawYellowLines(frame)

    drawWhiteLines(frame)

    captureVehicles(frame)

    displayFrame(frame)

    key = returnKey()

    if key == 27:
        break

cap.release()
destroyAllWindows()