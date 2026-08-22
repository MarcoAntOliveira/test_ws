import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import serial
import time

class MagnetometroNode(Node):
    def __init__(self):
        super().__init__('magnetometro_node')
        
        # Criando os 3 publicadores
        self.pub_x = self.create_publisher(Int32, 'magnetometro/x', 10)
        self.pub_y = self.create_publisher(Int32, 'magnetometro/y', 10)
        self.pub_z = self.create_publisher(Int32, 'magnetometro/z', 10)
        
        # Parâmetros
        self.declare_parameter('port', '/dev/ttyACM0')
        self.declare_parameter('baudrate', 115200)
        
        porta = self.get_parameter('port').get_parameter_value().string_value
        baud = self.get_parameter('baudrate').get_parameter_value().integer_value
        
        self.get_logger().info(f'Conectando ao Arduino em {porta} a {baud} baud...')
        
        try:
            # timeout=0.1 evita que o readline() trave o nó do ROS caso não chegue dado
            self.ser = serial.Serial(porta, baud, timeout=0.1)
            time.sleep(2) # Espera o Arduino resetar
            self.ser.reset_input_buffer() # Limpa lixos iniciais do buffer
            self.get_logger().info('Conectado com sucesso! Aguardando dados...')
        except Exception as e:
            self.get_logger().error(f'Erro ao abrir porta serial: {e}')
            # No ROS 2, não use 'return' no __init__. Se der erro, levantamos uma exceção.
            raise e

        # Timer para rodar a função de leitura (10Hz)
        self.timer = self.create_timer(0.1, self.ler_e_publicar)

    def ler_e_publicar(self):
        try:
            # Lemos a linha direto. Se não houver dado, ela retorna vazia por causa do timeout
            linha_bytes = self.ser.readline()
            
            if not linha_bytes:
                return # Se estiver vazio, sai da função e tenta de novo no próximo ciclo

            linha = linha_bytes.decode('utf-8').strip()
            
            # Log visual para debugar se algo está vindo da serial
            self.get_logger().debug(f'Dados brutos recebidos: {linha}')
            
            valores = linha.split(',')
            
            if len(valores) == 3:
                val_x = int(valores[0])
                val_y = int(valores[1])
                val_z = int(valores[2])
                
                # Publica
                self.pub_x.publish(Int32(data=val_x))
                self.pub_y.publish(Int32(data=val_y))
                self.pub_z.publish(Int32(data=val_z))
                
                # Mudado para INFO para você ver os prints no terminal por padrão
                self.get_logger().info(f'Publicado -> X: {val_x} | Y: {val_y} | Z: {val_z}')
                
        except ValueError:
            # Captura erros caso venha uma string corrompida (ex: "123,,45")
            self.get_logger().warn(f'Dados corrompidos recebidos na serial: {linha_bytes}')
        except Exception as e:
            self.get_logger().error(f'Erro no loop de leitura: {e}')

def main(args=None):
    rclpy.init(args=args)
    try:
        node = MagnetometroNode()
        rclpy.spin(node)
    except Exception as e:
        print(f"Nó finalizado devido a um erro: {e}")
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()