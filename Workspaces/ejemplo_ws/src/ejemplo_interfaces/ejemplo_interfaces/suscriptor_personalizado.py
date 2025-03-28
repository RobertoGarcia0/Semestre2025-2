#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from ejemplo_personalizados.msg import MensajeNuevo

class NodoSuscriptor(Node):
  def __init__(self):
    super().__init__("nodo_suscriptor_personalizado")
    self.get_logger().info("Nodo suscriptor inicializado")
    self.create_subscription(MensajeNuevo,"/topico_personalizado",self.recibir_mensaje_callback,10)

  def recibir_mensaje_callback(self, msg:MensajeNuevo):
    self.get_logger().info("Mensaje recibido:" 
    + "\nID: " + str(msg.id) 
    + "\nValor: "+ str(msg.valor)
    + "\nMensaje: "+ str(msg.mensaje))

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