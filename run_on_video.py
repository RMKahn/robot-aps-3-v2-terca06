#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import biblioteca as lb

print("Baixe o arquivo a seguir para funcionar: ")
print("https://github.com/Insper/robot202/raw/master/projeto/centro_massa/video.mp4")

cap = cv2.VideoCapture('line_following.mp4')

font = cv2.FONT_HERSHEY_SIMPLEX
def texto(img, a, p, color=(0,255,255), font=font, width=2, size=1 ):
    """Escreve na img RGB dada a string a na posição definida pela tupla p"""
    cv2.putText(img, str(a), p, font,size,color,width,cv2.LINE_AA)

while(True):
    # Capture frame-by-frame
    ret, img = cap.read()
    # frame = cv2.imread("frame0000.jpg")
    # ret = True
    
    if ret == False:
        print("Codigo de retorno FALSO - problema para capturar o frame")
        break
    else:
        mask = img.copy()
        segmenta_amarelo = lb.segmenta_linha_amarela(mask)
        
        if segmenta_amarelo is not None:
            contorno = lb.encontrar_contornos(segmenta_amarelo)
            cv2.drawContours(mask, contorno, -1, [0,0,255],2)
            mask, x1, y1 = lb.encontrar_centro_dos_contornos(mask, contorno)
            
            mask = lb.desenhar_linha_entre_pontos(mask, x1, y1, (255,0,0))
            
            mask, lm = lb.regressao_por_centro(mask, x1,y1)
                      
            angulo = lb.calcular_angulo_com_vertical(mask,lm)
            
        else:
            pass
    texto(mask, "Angulo: " + str(angulo), (50,80))
    
            

    # Imagem original
    cv2.imshow('img',img)
    # Mascara
    cv2.imshow('mask',mask)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

