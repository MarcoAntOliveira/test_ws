import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import numpy as np

class SignalNode(Node):

    def __init__(self):
        super().__init__('signal_node')

        # Publishers
        self.pub1 = self.create_publisher(Float32, 'signal1', 10)
        self.pub2 = self.create_publisher(Float32, 'signal2', 10)

        # Parâmetros do sinal
        self.n = 3
        self.omega = 2 * np.pi  # 1 Hz base
        self.phi = np.pi / 4

        # Frequência de amostragem (Hz)
        self.fs = 200.0
        self.dt = 1.0 / self.fs

        # Tempo discreto
        self.t = 0.0

        # Timer baseado em fs
        self.timer = self.create_timer(self.dt, self.timer_callback)

    def timer_callback(self):
        msg1 = Float32()
        msg2 = Float32()

        # Sinais
        y1 = np.sin(self.n * self.omega * self.t - self.phi)
        y2 = np.sin(self.n * self.omega * self.t - self.n * self.phi)

        msg1.data = float(y1)
        msg2.data = float(y2)

        self.pub1.publish(msg1)
        self.pub2.publish(msg2)

        # Incremento discreto de tempo
        self.t += self.dt


def main(args=None):
    rclpy.init(args=args)
    node = SignalNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()