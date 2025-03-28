#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool

class NodoCliente(Node):
  estado_solicitado = True
  def __init__(self):
    super().__init__("nodo_cliente")
    self.get_logger().info("Nodo cliente inicializado. SetBool")
    self.cliente = self.create_client(SetBool, "servicio_bool")
    self.create_timer(1,self.mandar_solicitud_callback)
    
  def mandar_solicitud_callback(self):
    while not self.cliente.wait_for_service(1):
      self.get_logger().warn("Servidor no disponible. Esperando")
    
    solicitud = SetBool.Request()
    solicitud.data = self.estado_solicitado

    futuro = self.cliente.call_async(solicitud)
    futuro.add_done_callback(self.recibir_respuesta_callback)

    self.get_logger().info("Solicitud enviada: " + str(solicitud.data))
    
  def recibir_respuesta_callback(self, futuro):
    respuesta:SetBool.Response = futuro.result()
    if respuesta.success:
      self.get_logger().info(respuesta.message)
    else:
      self.get_logger().warn(respuesta.message)
def main():
  try:
    rclpy.init()
    nodo_cliente = NodoCliente()
    nodo_cliente.mandar_solicitud_callback()
    rclpy.spin(nodo_cliente)
    rclpy.shutdown()
  except KeyboardInterrupt as e:
    print("\nPrograma detenido por teclado")

if __name__ == "__main__":
  main()