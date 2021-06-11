import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution, LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.substitutions import FindPackagePrefix


def generate_launch_description():
    pkg_gazebo_ros = get_package_share_directory("gazebo_ros")

    urdf_file = os.path.join(get_package_share_directory("unitree_a1_desc"), "a1.urdf")
    print(urdf_file)

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments=[('--verbose', 'true')]
    )

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-entity', 'unitree_a1', '-file', urdf_file], output='screen')

    robot_pub = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': Command([
            PathJoinSubstitution([FindPackagePrefix('xacro'), "bin", "xacro"]),
            ' ',
            # PathJoinSubstitution([get_package_share_directory('robot_description'), 'my_robot.xacro']),
            PathJoinSubstitution([get_package_share_directory('unitree_a1_desc'), 'robot.xacro']),
        ])
        }],
    )

    return LaunchDescription([
        DeclareLaunchArgument('pause', default_value='true', description='pause the world'),
        gazebo,
		robot_pub,
        spawn_entity
    ])
