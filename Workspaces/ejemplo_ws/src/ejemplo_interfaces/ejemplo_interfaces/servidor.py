#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import SetBool

class NodoServidor(Node):
  estado = False
  def __init__(self):
    super().__init__("nodo_servidor")
    self.estado = False
    self.get_logger().info("Nodo servidor inicializado. SetBool")
    self.get_logger().info("Estado actual: " + str(self.estado))
    self.servicio = self.create_service(SetBool, "servicio_bool", self.servidor_callback)
    
    
  def servidor_callback(self, solicitud:SetBool.Request, respuesta:SetBool.Response)->SetBool.Response:
    self.get_logger().info("Solicitud recibida: " + str(solicitud.data))
    if solicitud.data != self.estado:
      self.estado = solicitud.data
      respuesta.success = True
      respuesta.message = "Solicitud realizada correctamente"
      self.get_logger().info("Estado actual: " + str(self.estado))
    else:
      respuesta.success = False
      respuesta.message = "No se cambió el estado actual: " + str(self.estado)
      self.get_logger().info("No se cambió el estado actual: " + str(self.estado))
    return respuesta
def main():
  try:
    rclpy.init()
    nodo_servidor = NodoServidor()
    rclpy.spin(nodo_servidor)
    rclpy.shutdown()
  except KeyboardInterrupt as e:
    print("\nPrograma detenido por teclado")

if __name__ == "__main__":
  main()