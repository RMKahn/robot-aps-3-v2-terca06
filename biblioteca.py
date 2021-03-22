#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import math

def morpho_limpa(mask):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(13,13))
    mask = cv2.morphologyEx( mask, cv2.MORPH_OPEN, kernel )
    mask = cv2.morphologyEx( mask, cv2.MORPH_CLOSE, kernel )
    return mask


def segmenta_linha_amarela(bgr):
    """Não mude ou renomeie esta função
        deve receber uma imagem bgr e retornar os segmentos amarelos do centro da pista em branco.
        Utiliza a função cv2.morphologyEx() para limpar ruidos na imagem
    """
    img = bgr.copy()
    bgr1 = (0,210,90)
    bgr2 = (150,255,255)
    mask = cv2.inRange(img, bgr1, bgr2)   
    mask = morpho_limpa(mask)
    return mask


def encontrar_contornos(mask):
    """Não mude ou renomeie esta função
        deve receber uma imagem preta e branca os contornos encontrados
    """

    #Thresh
    ret, thresh = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)

    #Finding the contours in the image
    
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return contours

def crosshair(img, point, size, color):
    """ Desenha um crosshair centrado no point.
        point deve ser uma tupla (x,y)
        color é uma tupla R,G,B uint8
    """
    x,y = point
    cv2.line(img,(x - size,y),(x + size,y),color,2)
    cv2.line(img,(x,y - size),(x, y + size),color,2)

def encontrar_centro_dos_contornos(img, contornos):
    """Não mude ou renomeie esta função
        deve receber um contorno e retornar, respectivamente, a imagem com uma cruz no centro de cada segmento e o centro dele. formato: img, x, y
    """
    list_x = []
    list_y = []
    for c in contornos:

        M = cv2.moments(c)

        try:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            crosshair(img, (cX,cY), size=5, color=(0, 255, 0))
            list_x.append(cX)
            list_y.append(cY)
        except:pass
    return img, list_x, list_y
    

def desenhar_linha_entre_pontos(img, X, Y, color):
    """Não mude ou renomeie esta função
        deve receber uma lista de coordenadas XY, e retornar uma imagem com uma linha entre os centros EM SEQUENCIA do mais proximo.
    """
    img_copy = img.copy()
    for i in range(len(X)-1):
        x = cv2.line(img_copy, (X[i+1], Y[i+1]), (X[i], Y[i]), (0, 255, 0), thickness=3, lineType=8)

    return img_copy

def regressao_por_centro(img, x,y):
    """Não mude ou renomeie esta função
        deve receber uma lista de coordenadas XY, e estimar a melhor reta, utilizando o metodo preferir, que passa pelos centros. Retorne a imagem com a reta e os parametros da reta
        
        Dica: cv2.line(img,ponto1,ponto2,color,2) desenha uma linha que passe entre os pontos, mesmo que ponto1 e ponto2 não pertençam a imagem.
    """
    img_copy = img.copy()
    
    linear_regressor = LinearRegression()  # create object for the class

    x = np.array(x)
    x = x.reshape(-1,1)
    y = np.array(y)
    y = y.reshape(-1,1)
    
    linear_regressor.fit(x, y)  # perform linear regression
        
    X = np.array([-1000, 1000]).reshape(-1, 1)
    Y_pred = linear_regressor.predict(X)  # make predictions

    img_regres = cv2.line(img_copy, (int(X[0]),int(Y_pred[0])), (int(X[1]),int(Y_pred[1])), (0, 255, 0), thickness=3, lineType=8)
    
    return img_regres, linear_regressor

def calcular_angulo_com_vertical(img, lm):
    """Não mude ou renomeie esta função
        deve receber uma lista de coordenadas XY, e estimar a melhor reta, utilizando o metodo preferir, que passa pelos centros. Retorne a imagem com a reta.
        
        Dica: cv2.line(img,ponto1,ponto2,color,2) desenha uma linha que passe entre os pontos, mesmo que ponto1 e ponto2 não pertençam a imagem.
    """
    x1 = 250
    x2 = 550
    x = np.array([x1,x2])
    x= x.reshape(-1,1)
    y = lm.predict(x)
    y1,y2 = y
    delta_y = y1-y2
    delta_x = x2-x1
    
    angulo = math.degrees( math.atan2(delta_x, delta_y))
    
    return abs(angulo)