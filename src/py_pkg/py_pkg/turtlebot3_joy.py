#!/usr/bin/env python3

import os
from geometry_msgs.msg import Twist
from geometry_msgs.msg import TwistStamped
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import Joy

BURGER_MAX_LIN_VEL = 0.22
BURGER_MAX_ANG_VEL = 2.84

WAFFLE_MAX_LIN_VEL = 0.26
WAFFLE_MAX_ANG_VEL = 1.82

class TB3JoyTeleop(Node):
    def __init__(self):
        super().__init__('turtlebot3_joy_teleop')
        
        self.tb3_model = os.environ.get('TURTLEBOT3_MODEL', 'burger').lower()
        self.ros_distro = os.environ.get('ROS_DISTRO', 'jazzy').lower()

        # Fator multiplicador de velocidade inicial (1.0 = 100% da velocidade padrão)
        self.speed_multiplier = 1.0
        # Trava para registrar apenas um clique por vez
        self.button_pressed = False
        
        if self.tb3_model == 'burger':
            self.base_max_lin_vel = BURGER_MAX_LIN_VEL
            self.base_max_ang_vel = BURGER_MAX_ANG_VEL
        else:
            self.base_max_lin_vel = WAFFLE_MAX_LIN_VEL
            self.base_max_ang_vel = WAFFLE_MAX_ANG_VEL

        qos = QoSProfile(depth=10)
        if self.ros_distro == 'humble':
            self.pub = self.create_publisher(Twist, 'cmd_vel', qos)
        else:
            self.pub = self.create_publisher(TwistStamped, 'cmd_vel', qos)

        self.sub = self.create_subscription(Joy, 'joy', self.joy_callback, 10)

        self.get_logger().info(f"Nó iniciado para o modelo: {self.tb3_model.upper()}")
        self.get_logger().info("Use L1 para DIMINUIR e R1 para AUMENTAR a velocidade máxima.")

    def constrain(self, input_vel, low_bound, high_bound):
        if input_vel < low_bound:
            return low_bound
        elif input_vel > high_bound:
            return high_bound
        return input_vel

    def joy_callback(self, msg):
        # Precisamos de pelo menos 11 botões para ler L1 (9) e R1 (10)
        if len(msg.axes) < 2 or len(msg.buttons) < 11:
            return

        # --- LÓGICA DE ALTERAÇÃO DE VELOCIDADE (L1 e R1) ---
        button_l1 = msg.buttons[9]
        button_r1 = msg.buttons[10]

        if button_r1 and not self.button_pressed:
            self.speed_multiplier += 0.1  # Aumenta 10%
            self.speed_multiplier = min(self.speed_multiplier, 2.5) # Limite máximo de ganho (250%)
            self.get_logger().info(f"Velocidade aumentada! Multiplicador atual: {self.speed_multiplier:.1f}x")
            self.button_pressed = True
        elif button_l1 and not self.button_pressed:
            self.speed_multiplier -= 0.1  # Diminui 10%
            self.speed_multiplier = max(self.speed_multiplier, 0.2) # Limite mínimo de ganho (20%)
            self.get_logger().info(f"Velocidade diminuída! Multiplicador atual: {self.speed_multiplier:.1f}x")
            self.button_pressed = True
        elif not button_r1 and not button_l1:
            # Libera a trava quando você solta os dois botões
            self.button_pressed = False

        # --- CALCULO DAS VELOCIDADES DINÂMICAS ---
        # Multiplica os limites base pelo fator atualizado pelos botões R1/L1
        current_max_lin = self.base_max_lin_vel * self.speed_multiplier
        current_max_ang = self.base_max_ang_vel * self.speed_multiplier

        # LEFTY (Index 1) e LEFTX (Index 0)
        target_linear = msg.axes[1] * current_max_lin
        target_angular = msg.axes[0] * current_max_ang

        control_linear = self.constrain(target_linear, -current_max_lin, current_max_lin)
        control_angular = self.constrain(target_angular, -current_max_ang, current_max_ang)

        # Envia a mensagem de acordo com a sua distro
        if self.ros_distro == 'humble':
            twist = Twist()
            twist.linear.x = control_linear
            twist.angular.z = control_angular
            self.pub.publish(twist)
        else:
            twist_stamped = TwistStamped()
            twist_stamped.header.stamp = self.get_clock().now().to_msg()
            twist_stamped.header.frame_id = 'base_footprint'
            twist_stamped.twist.linear.x = control_linear
            twist_stamped.twist.angular.z = control_angular
            self.pub.publish(twist_stamped)

def main(args=None):
    rclpy.init(args=args)
    node = TB3JoyTeleop()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node.ros_distro == 'humble':
            stop_msg = Twist()
            node.pub.publish(stop_msg)
        else:
            stop_stamped = TwistStamped()
            stop_stamped.header.stamp = node.get_clock().now().to_msg()
            node.pub.publish(stop_stamped)
            
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()