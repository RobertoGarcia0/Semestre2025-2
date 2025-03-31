#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from ejemplo_personalizados.action import Contar
from rclpy.action.server import GoalResponse, CancelResponse, ServerGoalHandle
import time

class ServidorAccion(Node):
  def __init__(self):
    super().__init__('nodo_accion_contar')
    self.accion_server = ActionServer(self, Contar, "accion_contar", self.ejecucion_callback)
    self.get_logger().info("Servidor de acción 'accion_contar' iniciado.")
    self.accion_server.register_goal_callback(self.solicitud_recibida_callback)
    self.accion_server.register_cancel_callback(self.solicitud_cancelada__callback)

  def solicitud_recibida_callback(self, solicitud:Contar.Goal):
    if solicitud.objetivo <= 0:
      self.get_logger().warn("Solicitud de meta inválida: " + str(solicitud.objetivo) + ". Rechazada.")
      return GoalResponse.REJECT
    self.get_logger().info("Recibida una meta: contar hasta " + str(solicitud.objetivo))
    return GoalResponse.ACCEPT

  def solicitud_cancelada__callback(self, solicitud_cancelar:ServerGoalHandle):
    self.get_logger().info("Solicitud de cancelación recibida.")
    return CancelResponse.ACCEPT

  def ejecucion_callback(self, accion_servidor_objetivo:ServerGoalHandle):
    pausa = self.create_rate(1.0)
    solicitud:Contar.Goal = accion_servidor_objetivo.request
    valor_objetivo = solicitud.objetivo
    feedback_msg = Contar.Feedback()
    result_msg = Contar.Result()

    for i in range(1, valor_objetivo + 1):
      if accion_servidor_objetivo.is_cancel_requested:
        self.get_logger().info("Meta cancelada.")
        accion_servidor_objetivo.canceled()
        result_msg.result = i
        return result_msg

      feedback_msg.actual = i
      accion_servidor_objetivo.publish_feedback(feedback_msg)
      self.get_logger().info("Contando: " + str(i))
      time.sleep(1)
      
    result_msg.final = valor_objetivo
    self.get_logger().info("Solicitud terminada.")
    accion_servidor_objetivo.succeed()
    return result_msg

def main():
  try:
    rclpy.init()
    node = ServidorAccion()
    rclpy.spin(node)
    rclpy.shutdown()
  except KeyboardInterrupt as e:
    print("\nPrograma detenido por teclado")
    
if __name__ == '__main__':
    main()
