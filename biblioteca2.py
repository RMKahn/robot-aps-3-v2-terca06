#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import math

def segmenta_linha_branca(bgr):
    """Não mude ou renomeie esta função
        deve receber uma imagem e segmentar as faixas brancas
    """
    bgr = bgr.copy()
    bgr = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    bgr[bgr > 235] = 255
    bgr[bgr < 235] = 0

    return bgr

def estimar_linha_nas_faixas(img, mask):
    """Não mude ou renomeie esta função
        deve receber uma imagem preta e branca e retorna dois pontos que formen APENAS uma linha em cada faixa. Desenhe cada uma dessas linhas na iamgem.
         formato: [[(x1,y1),(x2,y2)], [(x1,y1),(x2,y2)]]
    """
    x1 = 0
    x2 = 0
    x3 = 0
    x4 = 0
    y1 = 0
    y2 = 0
    y3 = 0
    y4 = 0
    m = []
    linhas = cv2.HoughLinesP(mask,1,np.pi/180, 100, 50, 1000)
    for l in linhas:
        a1, b1, a2, b2 = l[0]
        m.append((b2-b1) / (a2-a1))
    d = m.index(min(m))
    e = m.index(max(m))
    
    x3, y3, x4, y4 = linhas[d][0][0], linhas[d][0][1], linhas[d][0][2], linhas[d][0][3]
    x1, y1, x2, y2 = linhas[e][0][0], linhas[e][0][1], linhas[e][0][2], linhas[e][0][3]
    lines = [[(x3,y3),(x4,y4)], [(x1,y1),(x2,y2)]]
    i1 = (x3, y3)
    f1 = (x4, y4)
    i2 = (x1, y1)
    f2 = (x2, y2)
    
    cv2.line(img, i1, f1, (255, 0, 255), thickness = 3, lineType = 8)
    cv2.line(img, i2, f2, (255, 0, 255), thickness = 3, lineType = 8)
   
    return lines, img

def calcular_equacao_das_retas(linhas):
    """Não mude ou renomeie esta função
        deve receber dois pontos que estejam em cada uma das faixas e retornar a equacao das duas retas. Onde y = h + m * x. Formato: [(m1,h1), (m2,h2)]
    """
    c_a = []
    for l in linhas:
        x1, x2 = l[0][0], l[1][0]
        y1, y2 = l[0][1], l[1][1]
        ca = (y1-y2) / (x1-x2)
        altura = y2 - (ca*x2)
        c_a.append([ca, altura])
        
    
    return c_a

def calcular_ponto_de_fuga(img, equacoes):
    """Não mude ou renomeie esta função
        deve receber duas equacoes de retas e retornar o ponto de encontro entre elas. Desenhe esse ponto na imagem.
    """
    return None, (None,None)

        