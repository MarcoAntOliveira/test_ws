from launch import LaunchDescription
from launch_ros.actions import Node 

def generate_launch_description():
    pub_cmd=Node (
        package="py_pkg",
        executable= "turtle3",
        output = "screen"
    )
    joy_cmd=Node (
        package="joy",
        executable= "joy_node",
        output = "screen"
    )

    ld = LaunchDescription()
    ld.add_action(pub_cmd)
    ld.add_action(joy_cmd)

    return ld

