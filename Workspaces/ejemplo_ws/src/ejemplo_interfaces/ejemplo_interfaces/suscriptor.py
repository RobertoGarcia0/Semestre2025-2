#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class NodoSuscriptor(Node):
  def __init__(self):
    super().__init__("nodo_suscriptor")
    self.get_logger().info("Nodo suscriptor inicializado")
    self.create_subscription(String,"/topico",self.recibir_mensaje_callback,10)

  def recibir_mensaje_callback(self, msg:String):
    self.get_logger().info("Mensaje recibido: " + msg.data)

def main():
  try:
    rclpy.init()
    nodo_suscriptor = NodoSuscriptor()
    rclpy.spin(nodo_suscriptor)
    rclpy.shutdown()
  except KeyboardInterrupt as e:
    print("\nPrograma detenido por teclado")

if __name__ == "__main__":
  main()