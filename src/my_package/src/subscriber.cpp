#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/int32.hpp"


using namespace std::chrono_literals;
using namespace std::placeholders;

class SubscriberNode: public rclcpp::Node{
    public:
    SubscriberNode():Node("Subscriber_node"){
        Subscriber_= create_subscription<std_msgs::msg::Int32>("int_topic", 10, std::bind(&SubscriberNode::callback, this, _1));
    
    }
    void callback(const std_msgs::msg::Int32::SharedPtr msg){
       RCLCPP_INFO(get_logger(), "hello %d", msg->data);
    }
    private:
        rclcpp::TimerBase::SharedPtr timer_;
        rclcpp::Subscription<std_msgs::msg::Int32>::SharedPtr Subscriber_;
        std_msgs::msg::Int32 message_;


};



int main(int argc, char * argv[]){
    rclcpp::init(argc, argv);

    auto node = std::make_shared<SubscriberNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
