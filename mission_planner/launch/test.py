import os.path

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.conditions import IfCondition
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():
    package_path = get_package_share_directory('perfect_drone_sim')

    default_rviz_fpv_config_path = os.path.join(
        package_path, 'rviz2', 'test.rviz')

    default_config_path = 'waypoint.yaml'
    default_data_path =  'benchmark.txt'

    perfect_drone_sim_config_name = 'click.yaml'
    super_config_name = 'test.yaml'


    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time', default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )
    declare_config_path_cmd = DeclareLaunchArgument(
        'config_name', default_value=default_config_path,
        description='Yaml config file path'
    )
    declare_data_path_cmd = DeclareLaunchArgument(
        'data_name', default_value=default_data_path,
        description='Yaml config file path'
    )

    # perfect_drone_sim_config_name_cmd = DeclareLaunchArgument(
    #     'config_name', default_value=perfect_drone_sim_config_name,
    #     description='Yaml config file path'
    # )

    super_config_name_cmd = DeclareLaunchArgument(
        'config_name', default_value=super_config_name,
        description='Yaml config file path'
    )



    ld = LaunchDescription()
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_config_path_cmd)
    ld.add_action(declare_data_path_cmd)

    ldlidar = IncludeLaunchDescription(
        launch_description_source=PythonLaunchDescriptionSource([
            get_package_share_directory('ldlidar_node'),
            '/launch/ldlidar_rviz2.launch.py'
        ])
    )
    ld.add_action(ldlidar)

    ldlidar_tool = IncludeLaunchDescription(
        launch_description_source=PythonLaunchDescriptionSource([
            get_package_share_directory('points_cloud_tool'),
            '/launch/pc2_launch.py'
        ])
    )
    ld.add_action(ldlidar_tool)

    rviz_node2 = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', default_rviz_fpv_config_path],
        output='screen'
    )
    ld.add_action(rviz_node2)

    # perfect_drone_sim = Node(
    #     package='perfect_drone_sim',
    #     executable='perfect_drone_node',
    #     output='log',
    #     parameters=[{
    #         'config_name': perfect_drone_sim_config_name,
    #     }]
    # )
    # ld.add_action(perfect_drone_sim)

    SUPER = Node(
        package='super_planner',
        executable='fsm_node',
        output='screen',
        parameters=[{
            'config_name': super_config_name,
        }]
    )

    ld.add_action(SUPER)

    return ld
