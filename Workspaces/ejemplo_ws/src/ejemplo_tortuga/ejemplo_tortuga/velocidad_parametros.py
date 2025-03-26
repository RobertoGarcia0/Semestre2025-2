#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import turtlesim

class ROSTwistPublisher(Node):
  def __init__(self):
    super().__init__("nodo_tortuga_velocidad")
    self.get_logger().info("Inicializando nodo publicador de velocidad")
    
    self.declare_parameter("nombre", "turtle1")
    self.declare_parameter("vel_lineal", 1.0)
    self.declare_parameter("vel_angular", 0.5)
    self.declare_parameter("tiempo", 1.0)
    self.nombre = self.get_parameter("nombre").get_parameter_value().string_value
    self.vel_lineal = self.get_parameter("vel_lineal").get_parameter_value().double_value
    self.vel_angular = self.get_parameter("vel_angular").get_parameter_value().double_value
    self.tiempo = self.get_parameter("tiempo").get_parameter_value().double_value
    self.get_logger().info("Leyendo parámetros:\n" + 
                           "Nombre: " + self.nombre + 
                           "\nVelocidad lineal: " + str(self.vel_lineal) + 
                           "\nVelocidad angular: " + str(self.vel_angular) + 
                           "\nTiempo entre mensajes: " + str(self.tiempo))

    self.publisher = self.create_publisher(Twist, "/" + self.nombre + "/cmd_vel", 10)
    self.create_timer(self.tiempo, self.timer_callback)
    

  def timer_callback(self):
    msg = Twist()
    msg.linear.x = self.vel_lineal
    msg.angular.z = self.vel_angular
    self.publisher.publish(msg)
    self.get_logger().info("Enviada velocidad \nlineal: " + str(self.vel_lineal) + "\nangular: " + str(self.vel_angular))
def main(args = None):
  try:
    rclpy.init(args = args)
    node = ROSTwistPublisher()
    rclpy.spin(node)
    rclpy.shutdown()
  except KeyboardInterrupt as e:
    print("\nPrograma interrumpido por teclado")
if __name__ == "__main__":
  main()