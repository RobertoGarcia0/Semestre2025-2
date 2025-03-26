#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class NodoPublicador(Node):
  def __init__(self):
    super().__init__("nodo_publicador")
    self.get_logger().info("Nodo publicador inicializado")
    self.get_logger().warn("Ejemplo mensaje de alerta")
    self.get_logger().error("Ejemplo mensaje de error")
    self.get_logger().fatal("Ejemplo mensaje de error fatal")
    self.publicador = self.create_publisher(String, "/topico", 10)
    self.create_timer(1,self.mandar_mensaje_callback)

  def mandar_mensaje_callback(self):
    msg = String()
    msg.data = "Hola"
    self.publicador.publish(msg)
    self.get_logger().info("Mensaje: " + msg.data)
def main():
  try:
    rclpy.init()
    nodo_publicador = NodoPublicador()
    rclpy.spin(nodo_publicador)
    rclpy.shutdown()
  except KeyboardInterrupt as e:
    print("\nPrograma detenido por teclado")

if __name__ == "__main__":
  main()