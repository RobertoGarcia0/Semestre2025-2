#!/usr/bin/env python
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
    if self.refImg == [] or self.newImg == []:
      return [], 0
    refImgGray = cv2.cvtColor(self.refImg, cv2.COLOR_BGR2GRAY)
    refImgGray = cv2.GaussianBlur(refImgGray,(5,5),0)
    newImgGray = cv2.cvtColor(self.newImg, cv2.COLOR_BGR2GRAY)
    newImgGray = cv2.GaussianBlur(newImgGray,(5,5),0)
    #Diferencia entre imagen anterior y reciente
    diffImg = cv2.absdiff(refImgGray, newImgGray)
    # La imagen se pasa a blanco y negro con un umbral
    thresImg = cv2.threshold(diffImg, 4, 255, cv2.THRESH_BINARY)[1]
    #umbral = cv2.adaptiveThreshold(resta,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    #Erosionamos el umbral para quitar ruido
    thresImg = cv2.erode(thresImg, None, iterations=2)
    # Dilatamos el umbral para tapar agujeros
    thresImg = cv2.dilate(thresImg, None, iterations=20)
    #Se buscan los contornos de los elementos encontrados
    contours, hier = cv2.findContours(thresImg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
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
    cv2.imshow('Frame', drawnImg)
    if cv2.waitKey(25) & 0xFF == ord('q'):
      pass
    return drawnImg, totalContours
  
  def image_update(self, newImg):
    self.refImg = self.newImg
    self.newImg = newImg

class MotionDetectionNode(Node):
  rate = 15 #fps
  def __init__(self):
    super().__init__("motion_detection_node")
    self.get_logger().info("Motion Detection Node Init")

  def detector_init(self):
    self.imgMsg = Image()
    self.motionDetection = MotionDetection()
    self.image_pub = self.create_publisher(Image, "/motion_detection", 10)
    self.image_subs = self.create_subscription(Image, '/image_raw', self.image_callback, 1)
    self.create_timer(float(1.0 / self.rate),self.send_image)

  def image_callback(self, img):
    self.motionDetection.image_update(bridge.imgmsg_to_cv2(img, "bgr8"))

  def send_image(self):
    img, obj = self.motionDetection.motion_detection()
    if img == []:
      self.get_logger().warn("No camera input")
      return
    self.image_pub.publish(bridge.cv2_to_imgmsg(img, encoding="bgr8"))
    self.get_logger().info("Objects detected: " + str(len(obj)))

if __name__ == '__main__':
  try:
    rclpy.init()
    motionDetectionNode = MotionDetectionNode()
    motionDetectionNode.detector_init()
    rclpy.spin(motionDetectionNode)
    rclpy.shutdown()
  except KeyboardInterrupt as ex:
    print("Programa interrumpido")

