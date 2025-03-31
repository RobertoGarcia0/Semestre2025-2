#!/usr/bin/env python3
import rclpy
import rclpy.action
from rclpy.node import Node
#from rclpy.task import Future
from rclpy.action.client import ClientGoalHandle, Future, ActionClient
from ejemplo_personalizados.action import Contar

class ClienteAccion(Node):
  def __init__(self):
    super().__init__('nodo_accion_cliente')
    self.cliente = ActionClient(self, Contar, 'accion_contar')

  def enviar_solicitud(self, numero_objetivo:int):
    self.get_logger().info(f"Enviando meta: contar hasta {numero_objetivo}")
    solicitud = Contar.Goal()
    solicitud.objetivo = numero_objetivo

    self.cliente.wait_for_server()
    futuro = self.cliente.send_goal_async(solicitud, self.feedback_callback)
    futuro.add_done_callback(self.respuesta_solicitud_callback)

  def respuesta_solicitud_callback(self, futuro):
    respuesta_solicitud:Contar.Impl.SendGoalService.Response = futuro.result()
    if not respuesta_solicitud.accepted:
      self.get_logger().error("Meta rechazada.")
      return
    
    self.get_logger().info("Meta aceptada.")
    futuro_resultado = respuesta_solicitud.get_result_async()
    futuro_resultado.add_done_callback(self.resultado_callback)


  def feedback_callback(self, feedback_msg:Contar.Impl.FeedbackMessage):
    self.get_logger().info(f"Feedback: {feedback_msg.feedback.actual}")

  def resultado_callback(self, futuro:Future):
    resultado:Contar.Impl.GetResultService.Response = futuro.result()
    self.get_logger().info(f"Resultado final: {resultado.result.final}")
    raise SystemExit

def main():
  try:
    rclpy.init()
    node = ClienteAccion()
    node.enviar_solicitud(2)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
  except KeyboardInterrupt as e:
    print("\nPrograma detenido por teclado")
      
if __name__ == '__main__':
    main()
