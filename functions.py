import cv2
import numpy as np
import math

def readVideo(name):
    return cv2.VideoCapture(name)

def applyGaussianBlur(frame):
    return cv2.GaussianBlur(frame, (5, 5), 0)

def convertToHsv(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

def calculate_slope(x1, y1, x2, y2):
    """Calcula a inclinação de uma linha."""
    if x2 - x1 == 0:
        return 999  # Evita divisão por zero (reta vertical)
    return (y2 - y1) / (x2 - x1)

def draw_average_line(image, lines, color):
    """Desenha a linha média com base nas linhas detectadas."""
    if len(lines) < 2:
        return None
    x_coords = []
    y_coords = []
    for x1, y1, x2, y2 in lines:
        x_coords += [x1, x2]
        y_coords += [y1, y2]
    try:
        poly = np.polyfit(y_coords, x_coords, 1)
        y1 = image.shape[0]
        y2 = int(y1 * 0.7)
        x1 = int(np.polyval(poly, y1))
        x2 = int(np.polyval(poly, y2))
        cv2.line(image, (x1, y1), (x2, y2), color, 10)
        return (x1, y1, x2, y2)
    except np.RankWarning:
        return None

def process_frame(frame):
    """Processa cada frame para calcular a direção, exibir o texto correspondente e desenhar o ponto médio."""
    imshape = frame.shape

    # 1. Escala de cinza e suavização
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)

    # 2. Detecção de bordas
    edges = cv2.Canny(blur, 60, 150)

    # 3. Máscara da região de interesse
    vertices = np.array([[ 
        (0, imshape[0]),
        (450, 320),
        (490, 320),
        (imshape[1], imshape[0])
    ]], dtype=np.int32)
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, vertices, 255)
    masked_edges = cv2.bitwise_and(edges, mask)

    # 4. Transformada de Hough para encontrar linhas
    lines = cv2.HoughLinesP(masked_edges, 2, np.pi / 180, 45, np.array([]), 40, 100)

    left_lines, right_lines = [], []
    left_slopes, right_slopes = [], []

    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                slope = calculate_slope(x1, y1, x2, y2)
                if 0.5 < slope < 2:
                    right_lines.append((x1, y1, x2, y2))
                    right_slopes.append(slope)
                elif -2 < slope < -0.5:
                    left_lines.append((x1, y1, x2, y2))
                    left_slopes.append(slope)

    # Calcular direção, ângulo e ponto médio
    direction = "Reto"
    curve_intensity = "Leve"
    angle = 0
    mid_x, mid_y = None, None
    if left_lines and right_lines:
        # Calcular ângulo médio
        left_slope = np.mean(left_slopes)
        right_slope = np.mean(right_slopes)
        avg_slope = (left_slope + right_slope) / 2
        angle_rad = math.atan(avg_slope)
        angle = math.degrees(angle_rad)

        # Determinar direção com base no ângulo
        if angle <= -7 and angle > -6:
            direction = "Reto"
        elif angle < -8:
            direction = "Esquerda"
        elif -4 < angle <= 3:
            direction = "Direita"

        if abs(angle) < 15:
            curve_intensity = "Leve"    
        else:
            curve_intensity = "Acentuada"

        # Calcular ponto médio entre as linhas
        left_line = draw_average_line(frame, left_lines, (255, 0, 0))  # Vermelho
        right_line = draw_average_line(frame, right_lines, (0, 0, 255))  # Azul
        if left_line and right_line:
            mid_x = (left_line[2] + right_line[2]) // 2
            mid_y = (left_line[3] + right_line[3]) // 2

    # Exibir direção no canto esquerdo da imagem
    cv2.putText(frame, f"Direcao: {direction}({curve_intensity})", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


    # Desenhar ponto médio no centro da pista
    if mid_x is not None and mid_y is not None:
        cv2.circle(frame, (mid_x, mid_y), 10, (0, 255, 0), -1)  # Verde

    return frame

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
    low_black = np.array([0, 0, 0])
    up_black = np.array([180, 255, 50])
    mask_black = cv2.inRange(hsv, low_black, up_black)
    contours_black, _ = cv2.findContours(mask_black, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours_black:
        x, y, w, h = cv2.boundingRect(cnt)
        if w * h > 3000 and h > 50:
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 0, 0), 2)
            cv2.putText(roi, "Vehicle Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

def captureWhiteVehicles(frame):
    h, w, c = frame.shape
    roi = frame[h // 2 :h//2+h//4, w//2+w//7:w]
    hsv = convertToHsv(roi)
    low_white = np.array([0, 0, 200])
    up_white = np.array([180, 30, 255])
    mask_white = cv2.inRange(hsv, low_white, up_white)
    contours_white, _ = cv2.findContours(mask_white, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours_white:
        x, y, w, h = cv2.boundingRect(cnt)
        if w * h > 3000 and h > 40:
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