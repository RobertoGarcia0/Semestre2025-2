#!/usr/bin/env python3 
import rclpy
import rclpy.duration
from rclpy.node import Node
from turtlesim.srv import Spawn 

class SpawnerTortuga(Node):
  count = 0
  def __init__(self):
    super().__init__("spawner_tortuga")
    self.get_logger().info("Inicializado nodo para spawnear tortuga")
    #Parámetros
    self.declare_parameter("nombre", "turtle2")
    self.declare_parameter("pos_x", 0.5)
    self.declare_parameter("pos_y", 0.5)
    self.declare_parameter("pos_th", 0.5)
    self.nombre = self.get_parameter("nombre").get_parameter_value().string_value
    self.pos_x = self.get_parameter("pos_x").get_parameter_value().double_value
    self.pos_y = self.get_parameter("pos_y").get_parameter_value().double_value
    self.pos_th = self.get_parameter("pos_th").get_parameter_value().double_value
    self.get_logger().info("Leyendo parámetros:\n" + 
                           "Nombre: " + self.nombre + 
                           "\nPosición" + 
                           "\nx: " + str(self.pos_x) + 
                           "\nx: " + str(self.pos_y) + 
                           "\nth: " + str(self.pos_th))
    #Cliente
    self.cliente = self.create_client(Spawn, 'spawn') 

  def spawnear_tortuga(self):
    # Esperar a que el servicio esté disponible
    while not self.cliente.wait_for_service(1):
      self.get_logger().warn("Servidor no disponible. Esperando")
    
    # Solicitud
    solicitud = Spawn.Request()
    solicitud.x = self.pos_x 
    solicitud.y = self.pos_y
    solicitud.theta = self.pos_th
    solicitud.name = self.nombre
    # Llamada asincrona al servicio
    futuro = self.cliente.call_async(solicitud) 
    futuro.add_done_callback(self.respuesta_callback)

  def respuesta_callback(self, futuro):
    try:
      respuesta:Spawn.Response = futuro.result()
      if respuesta.name:
        self.get_logger().info("Tortuga " + respuesta.name + " creada")
      else:
        self.get_logger().error("No se pudo crear la tortuga")
    except Exception as e:
      self.get_logger().error(f'Error al llamar al servicio Spawn: {str(e)}')
    finally:
      raise SystemExit

def main():
  try:
    rclpy.init()
    spawner = SpawnerTortuga() 
    spawner.spawnear_tortuga()
    rclpy.spin(spawner)
    rclpy.shutdown()
  except KeyboardInterrupt as ex: 
    print("\nPrograma interrumpido")

if __name__ == "__main__":
  main()