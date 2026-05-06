from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription

from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():

    world_file = os.path.join(
        get_package_share_directory('tb3_custom_world'),
        'worlds',
        'green_sphere_world.world'
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            )
        ),
        launch_arguments={'world': world_file}.items(),
    )

    robot_description_path = os.path.join(
        get_package_share_directory('turtlebot3_gazebo'),
        'models',
        'turtlebot3_waffle_pi',
        'model.sdf'
    )

    spawn_turtlebot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'turtlebot3',
            '-file', robot_description_path,
            '-x', '0',
            '-y', '0',
            '-z', '0.01'
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        spawn_turtlebot
    ])