#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from builtin_interfaces.msg import Duration
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from std_msgs.msg import Float64MultiArray
import random 

class TrajectoryTest(Node):

    def __init__(self):
        super().__init__('trajectory_test')
        topic_name = "/scara_position_controller/commands"
        self.trajectory_publisher = self.create_publisher(Float64MultiArray, topic_name,10)
        self.timer = self.create_timer(5, self.timer_callback)
        self.goal_positions = [1.57/2, 1.57/2, 1.57/2]
        self.get_logger().info('Controller is running and publishing to topic: {}'.format(topic_name))

    def timer_callback(self):
        position_msg = Float64MultiArray()
        self.goal_positions = [(random.random() - 0.5) * 3.14, (random.random() - 0.5) * 3.14, (random.random() - 0.5) * 3.14]
        position_msg.data = self.goal_positions
        self.trajectory_publisher.publish(position_msg)
        self.get_logger().info('Sending position:')
        self.get_logger().info('x: ' + str(self.goal_positions[0] * (180/3.14)))
        self.get_logger().info('x: ' + str(self.goal_positions[1] * (180/3.14)))
        self.get_logger().info('x: ' + str(self.goal_positions[2] * (180/3.14)))

def main(args=None):
    rclpy.init(args=args)
    trajectory_publisher_node = TrajectoryTest()
    rclpy.spin(trajectory_publisher_node)
    trajectory_publisher_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

        



