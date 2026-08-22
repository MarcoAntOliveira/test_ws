from launch import LaunchDescription
from launch_ros.actions import Node 

def generate_launch_description():
    pub_cmd=Node (
        package="my_package",
        executable= "pub",
        output = "screen"
    )
    sub_cmd=Node (
        package="my_package",
        executable= "sub",
        output = "screen"
    )

    ld = LaunchDescription()
    ld.add_action(pub_cmd)
    ld.add_action(sub_cmd)

    return ld

