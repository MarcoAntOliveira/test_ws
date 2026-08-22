from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    """Launch Rviz with the MR-3 Mini model and joint sliders."""

    pkg_path = get_package_share_directory('mr3_mini_description')
    urdf_file = os.path.join(pkg_path, 'urdf', 'mr3_mini.urdf')

    # GUI view configuration
    rviz_gui_config = os.path.join(pkg_path, 'rviz', 'mr3_mini_view.rviz')
    
    with open(urdf_file, 'r') as f:
        robot_desc = f.read()    

    return LaunchDescription([        
        
        # Publishes the robot state (required for Rviz)
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{'robot_description': robot_desc}]
        ),
        
        # Joint sliders GUI for playing with the model
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui'
        ),        
        
        # Rviz with pre-configured view        
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_gui_config]
        )        
    ])