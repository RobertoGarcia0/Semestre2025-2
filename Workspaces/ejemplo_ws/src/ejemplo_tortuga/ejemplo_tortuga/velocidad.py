#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class ROSTwistPublisher(Node):
  def __init__(self):
    super().__init__("publisher_turtle_node")
    self.get_logger().info("Inicializando nodo publicador de posición")
    self.publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
    self.create_timer(1, self.timer_callback)

  def timer_callback(self):
    msg = Twist()
    msg.linear.x = 1.0
    msg.angular.z = 1.5
    self.publisher.publish(msg)
    self.get_logger().info("Enviada velocidad \nx: " + str(msg.linear.x) + "\nang: " + str(msg.angular.z))
def main():
  rclpy.init()
  node = ROSTwistPublisher()
  rclpy.spin(node)
  rclpy.shutdown()

if __name__ == "__main__":
  main()