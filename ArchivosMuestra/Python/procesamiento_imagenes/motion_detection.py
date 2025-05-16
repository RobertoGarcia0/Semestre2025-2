#!/usr/bin/env python
import time
import rclpy
from rclpy.node import Node
import cv2
import numpy as np
import sys
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import Bool
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
bridge = CvBridge()


class MotionDetection():
  refImg = []
  newImg = []
  #Area minima del area que se considera movimiento
  contourMinArea = 4500
  def motion_detection(self): 
    refImgGray = cv2.cvtColor(self.refImg, cv2.COLOR_BGR2GRAY)
    refImgGray = cv2.GaussianBlur(refImgGray,(5,5),0)
    newImgGray = cv2.cvtColor(self.newImg, cv2.COLOR_BGR2GRAY)
    newImgGray = cv2.GaussianBlur(newImgGray,(5,5),0)
    #Diferencia entre imagen anterior y reciente
    diffImg = cv2.absdiff(refImgGray, newImgGray)
    # La imagen se pasa a blanco y negro con un umbral
    thresImg = cv2.threshold(diffImg, 4, 255, cv2.THRESH_BINARY)[1]
    #Erosionamos el umbral para quitar ruido (Reducir las imágenes)
    erodeImg = cv2.erode(thresImg, None, iterations=2)
    # Dilatamos el umbral para tapar agujeros
    dilImg = cv2.dilate(erodeImg, None, iterations=4)
    #Se buscan los contornos de los elementos encontrados
    contours, hier = cv2.findContours(dilImg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #Verificar los contornos más grandes
    totalContours = []
    #Imagen donde se dibujarán los objetos
    drawnImg = self.newImg.copy()
    for c in contours:
      # Eliminamos los contornos mas pequenos
      if cv2.contourArea(c) < self.contourMinArea:
        continue
      # Obtenemos el recángulo delimitador del contorno
      (x, y, we, hi) = cv2.boundingRect(c)
      totalContours.append([x, y, we, hi])
      # Dibujamos el recángulo delimitador
      drawnImg = cv2.rectangle(drawnImg, (x, y), (x + we, y + hi), (255, 0, 0), 2)
      #Contamos el numero de objetivos
    cv2.imshow('Imagen', self.refImg)
    cv2.imshow('Movimiento', diffImg)
    cv2.imshow('BN', thresImg)
    cv2.imshow('Erosion', erodeImg)
    cv2.imshow('Dilatacion', dilImg)
    cv2.imshow('Deteccion', drawnImg)
    #cv2.waitKey(0)
    if cv2.waitKey(25) & 0xFF == ord('q'):
      pass
    #return cv2.cvtColor(thresImg, cv2.COLOR_GRAY2BGR), targetsNo
    return 
  
  def image_update(self, newImg):
    self.refImg = self.newImg
    self.newImg = newImg

if __name__ == '__main__':
  delay = 1.0/15.0
  try:
    videoStream = cv2.VideoCapture("/dev/video0")
    print("Abriendo cámara")
    while not videoStream.isOpened():
      pass
    motionDetection = MotionDetection()
    motionDetection.image_update(videoStream.read()[1])
    time.sleep(delay)
    while(True):
      motionDetection.image_update(videoStream.read()[1])
      motionDetection.motion_detection()
      time.sleep(delay)      
  except KeyboardInterrupt as ex:
    print("Programa interrumpido")

