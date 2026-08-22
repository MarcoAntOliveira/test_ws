#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class TurtlesimCirculo(Node):
    def __init__(self):
        super().__init__("turtlesim_circulo")

        # 1. Cria o Publicador de comandos de velocidade (cmd_vel)
        self.publisher_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

        # 2. Cria o Assinante (Subscriber) para monitorar a posição/pose atual da tartaruga
        self.subscription = self.create_subscription(
            Pose, "/turtle1/pose", self.pose_callback, 10
        )

        # 3. Define um timer para publicar comandos a uma taxa de 10Hz (0.1 segundos)
        # Isso garante o envio síncrono e contínuo para evitar timeouts do simulador
        self.timer = self.create_timer(0.1, self.mover_em_circulo)

        self.get_logger().info("Nó do Turtlesim em Círculo foi iniciado!")

    def pose_callback(self, msg):
        """
        Esta função é chamada automaticamente toda vez que o Turtlesim atualiza a posição.
        O ROS 2 gerencia a recepção desses dados em segundo plano.
        """
        # Aqui você lê onde a tartaruga está.
        # Útil se você quiser parar o círculo após completar uma volta, por exemplo.
        self.get_logger().info(
            f"Posição atual: x={msg.x:.2f}, y={msg.y:.2f}, theta={msg.theta:.2f}",
            once=True,
        )

    def mover_em_circulo(self):
        """
        Publica constantemente a velocidade necessária para gerar o círculo.
        """
        msg = Twist()

        # Velocidade para frente (m/s)
        msg.linear.x = 2.0
        msg.linear.y = 0.0
        msg.linear.z = 0.0

        # Velocidade de rotação (rad/s)
        # Se linear.x = 2.0 e angular.z = 1.0, o raio da circunferência será de 2 metros.
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 1.0

        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    no = TurtlesimCirculo()
    try:
        rclpy.spin(no)
    except KeyboardInterrupt:
        pass
    finally:
        # Envia comando de parada antes de desligar o nó
        parar_msg = Twist()
        no.publisher_.publish(parar_msg)
        no.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
