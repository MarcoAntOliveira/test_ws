#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <sensor_msgs/msg/joy.hpp>

class TeleopTurtle : public rclcpp::Node
{
public:
  TeleopTurtle();

private:
  // Callback que processa os dados do controle sempre que um botão ou analógico se move
  void joyCallback(const sensor_msgs::msg::Joy::SharedPtr msg);

  rclcpp::Subscription<sensor_msgs::msg::Joy>::SharedPtr joy_sub_;
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr twist_pub_;

  double l_scale_, a_scale_;
};

TeleopTurtle::TeleopTurtle()
: Node("teleop_turtle"),
  l_scale_(2.0),
  a_scale_(2.0)
{
  // Declara e recupera os parâmetros de escala (assim como no nó de teclado original)
  this->declare_parameter("scale_angular", 3.0);
  this->declare_parameter("scale_linear", 3.0);
  this->get_parameter("scale_angular", a_scale_);
  this->get_parameter("scale_linear", l_scale_);

  // Cria o publisher para mover a tartaruga
  twist_pub_ = this->create_publisher<geometry_msgs::msg::Twist>("turtle1/cmd_vel", 1);

  // Cria o subscriber para escutar o controle
  joy_sub_ = this->create_subscription<sensor_msgs::msg::Joy>(
    "joy", 
    10, 
    std::bind(&TeleopTurtle::joyCallback, this, std::placeholders::_1)
  );

  RCLCPP_INFO(this->get_logger(), "Nó Teleop iniciado com suporte a Joystick.");
}

void TeleopTurtle::joyCallback(const sensor_msgs::msg::Joy::SharedPtr msg)
{
  geometry_msgs::msg::Twist twist;

  // Evita falha de segmentação se o vetor de eixos estiver vazio ou incompleto
  if (msg->axes.size() >= 2)
  {
    // LEFTY (Index 1) controla a velocidade linear (frente/trás)
    twist.linear.x = l_scale_ * msg->axes[1];

    // LEFTX (Index 0) controla a velocidade angular (esquerda/direita)
    twist.angular.z = a_scale_ * msg->axes[0];
  }

  // Publica o comando de velocidade gerado pelo analógico
  twist_pub_->publish(twist);
}

int main(int argc, char** argv)
{
  rclcpp::init(argc, argv);
  
  // Instancia e mantém o nó rodando de forma assíncrona (spin)
  auto node = std::make_shared<TeleopTurtle>();
  rclcpp::spin(node);
  
  rclcpp::shutdown();
  return 0;
}