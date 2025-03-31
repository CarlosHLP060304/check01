#!/usr/bin/python
# -*- coding: utf-8 -*-

# Programa simples com camera webcam e opencv
import cv2
import numpy as np



def image_da_webcam(img):
    """
    ->>> função que processa a imagem e retorna.
    """  
    #exemplo de processamento de imagem
    img_cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
      


    return img_cinza

cv2.namedWindow("preview")

# define a entrada de video para webcam
# vc = cv2.VideoCapture(0)
vc = cv2.VideoCapture("project_video.mp4") # para ler um video mp4 

#configura o tamanho da janela 
vc.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    
    img = image_da_webcam(frame) # passa o frame para a função imagem_da_webcam e recebe em img imagem tratada

    cv2.imshow("preview", img)
    cv2.imshow("original", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

cv2.destroyWindow("preview")
vc.release()