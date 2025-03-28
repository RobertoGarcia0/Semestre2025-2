#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from ejemplo_personalizados.msg import MensajeNuevo

class NodoPublicador(Node):
  def __init__(self):
    super().__init__("nodo_publicador_personalizado")
    self.get_logger().info("Nodo publicador inicializado")
    self.publicador = self.create_publisher(MensajeNuevo, "/topico_personalizado", 10)
    self.create_timer(1,self.mandar_mensaje_callback)

  def mandar_mensaje_callback(self):
    msg = MensajeNuevo()
    msg.mensaje = "Hola"
    msg.valor = 1.83
    msg.id = 1
    self.publicador.publish(msg)
    self.get_logger().info("Mensaje publicado:" 
    + "\nID: " + str(msg.id) 
    + "\nValor: "+ str(msg.valor)
    + "\nMensaje: "+ str(msg.mensaje))
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