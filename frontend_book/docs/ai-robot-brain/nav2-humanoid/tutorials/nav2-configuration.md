---
title: Configuring Nav2 for Humanoid Robots
sidebar_position: 1
---

# Configuring Nav2 for Humanoid Robots

This tutorial will guide you through configuring Navigation 2 (Nav2) specifically for humanoid robot navigation. You'll learn how to set up the navigation stack with humanoid-specific parameters, constraints, and behaviors.

## Prerequisites

Before starting this tutorial, you should have:
- A humanoid robot with ROS2 support
- Basic Nav2 installation and understanding
- Knowledge of your robot's kinematic constraints
- Isaac ROS perception system (optional but recommended)

## Step 1: Set Up the Robot Configuration

### Robot Description (URDF/XACRO)
Ensure your robot's description includes:
1. Properly defined base footprint and base link
2. Correct physical dimensions for collision checking
3. Proper joint limits and safety controllers
4. Sensor mounting points for navigation

Example robot configuration:
```xml
<link name="base_link">
  <visual>
    <geometry>
      <box size="0.5 0.4 0.8"/>  <!-- Humanoid torso dimensions -->
    </geometry>
  </visual>
  <collision>
    <geometry>
      <box size="0.5 0.4 0.8"/>
    </geometry>
  </collision>
</link>

<link name="base_footprint">
  <visual>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
      <cylinder radius="0.25" length="0.01"/>
    </geometry>
  </visual>
</link>

<joint name="base_footprint_joint" type="fixed">
  <parent link="base_link"/>
  <child link="base_footprint"/>
  <origin xyz="0 0 -0.4" rpy="0 0 0"/>  <!-- Height of feet from center -->
</joint>
```

### Sensor Configuration
Ensure navigation-relevant sensors are properly configured:
- IMU for balance and orientation
- Cameras for perception (if using visual navigation)
- LIDAR or depth sensors for obstacle detection
- Proper calibration and TF frames

## Step 2: Install and Verify Nav2

### Nav2 Installation
```bash
# Install Nav2 packages
sudo apt update
sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup

# Verify installation
ros2 pkg list | grep nav2
```

### Basic Verification
Test basic Nav2 functionality:
```bash
# Launch Nav2 in simulation first
ros2 launch nav2_bringup navigation_launch.py \
  use_sim_time:=true \
  params_file:=/path/to/your/nav2_params.yaml
```

## Step 3: Configure Humanoid-Specific Parameters

### Create Parameter Files
Create a comprehensive parameter configuration for humanoid navigation:

**nav2_params_humanoid.yaml**:
```yaml
amcl:
  ros__parameters:
    use_sim_time: false
    alpha1: 0.2
    alpha2: 0.2
    alpha3: 0.2
    alpha4: 0.2
    alpha5: 0.2
    base_frame_id: "base_footprint"
    beam_skip_distance: 0.5
    beam_skip_error_threshold: 0.9
    beam_skip_threshold: 0.3
    do_beamskip: false
    global_frame_id: "map"
    lambda_short: 0.1
    laser_likelihood_max_dist: 2.0
    laser_max_range: 10.0
    laser_min_range: -1.0
    laser_model_type: "likelihood_field"
    max_beams: 60
    max_particles: 2000
    min_particles: 500
    odom_frame_id: "odom"
    pf_err: 0.05
    pf_z: 0.99
    recovery_alpha_fast: 0.0
    recovery_alpha_slow: 0.0
    resample_interval: 1
    robot_model_type: "nav2_amcl::DifferentialMotionModel"
    save_pose_rate: 0.5
    sigma_hit: 0.2
    tf_broadcast: true
    transform_tolerance: 1.0
    update_min_a: 0.2
    update_min_d: 0.25
    z_hit: 0.5
    z_max: 0.05
    z_rand: 0.5
    z_short: 0.05

amcl_map_client:
  ros__parameters:
    use_sim_time: false

amcl_rclcpp_node:
  ros__parameters:
    use_sim_time: false

bt_navigator:
  ros__parameters:
    use_sim_time: false
    global_frame: map
    robot_base_frame: base_footprint
    odom_topic: /odom
    bt_loop_duration: 10
    default_server_timeout: 20
    # Humanoid-specific behavior tree
    plugin_lib_names:
    - nav2_compute_path_to_pose_action_bt_node
    - nav2_follow_path_action_bt_node
    - nav2_back_up_action_bt_node
    - nav2_spin_action_bt_node
    - nav2_wait_action_bt_node
    - nav2_clear_costmap_service_bt_node
    - nav2_is_stuck_condition_bt_node
    - nav2_goal_reached_condition_bt_node
    - nav2_goal_updated_condition_bt_node
    - nav2_initial_pose_received_condition_bt_node
    - nav2_reinitialize_global_localization_service_bt_node
    - nav2_rate_controller_bt_node
    - nav2_distance_controller_bt_node
    - nav2_speed_controller_bt_node
    - nav2_truncate_path_action_bt_node
    - nav2_goal_updater_node_bt_node
    - nav2_recovery_node_bt_node
    - nav2_pipeline_sequence_bt_node
    - nav2_round_robin_node_bt_node
    - nav2_transform_available_condition_bt_node
    - nav2_time_expired_condition_bt_node
    - nav2_path_expiring_timer_condition
    - nav2_distance_traveled_condition_bt_node

bt_navigator_rclcpp_node:
  ros__parameters:
    use_sim_time: false

controller_server:
  ros__parameters:
    use_sim_time: false
    controller_frequency: 20.0
    min_x_velocity_threshold: 0.05
    min_y_velocity_threshold: 0.05
    min_theta_velocity_threshold: 0.05
    progress_checker_plugin: "progress_checker"
    goal_checker_plugin: "goal_checker"
    controller_plugins: ["HumanoidFollowPath"]

    # Humanoid-specific controller
    HumanoidFollowPath:
      plugin: "nav2_mppi_controller::MPPIController"

      # Humanoid-specific parameters
      speed_limit_scale: 0.5      # Conservative for balance
      frequency: 20.0
      time_steps: 30
      model_dt: 0.05
      batch_size: 1000
      vx_std: 0.2
      vy_std: 0.1
      wz_std: 0.3
      vx_max: 0.5
      vx_min: 0.05    # Minimum for stable walking
      vy_max: 0.1
      wz_max: 0.3
      acc_lim_x: 0.2
      acc_lim_y: 0.1
      acc_lim_theta: 0.3
      decel_lim_x: -0.3
      decel_lim_y: -0.1
      decel_lim_theta: -0.5
      steering_angle_alpha: 0.8
      progress_checker: "progress_checker"
      goal_checker: "goal_checker"

    progress_checker:
      plugin: "nav2_controller::SimpleProgressChecker"
      required_movement_radius: 0.5
      movement_time_allowance: 10.0

    goal_checker:
      plugin: "nav2_controller::SimpleGoalChecker"
      xy_goal_tolerance: 0.25    # More tolerant for humanoid
      yaw_goal_tolerance: 0.25
      stateful: true

    local_costmap:
      local_costmap:
        ros__parameters:
          update_frequency: 20.0
          publish_frequency: 10.0
          global_frame: odom
          robot_base_frame: base_footprint
          use_rollout_costs: true
          rollout_resolution: 0.05
          rollout_dist: 0.5
          resolution: 0.05
          robot_radius: 0.25    # Humanoid radius
          plugins: ["voxel_layer", "inflation_layer"]
          inflation_layer:
            plugin: "nav2_costmap_2d::InflationLayer"
            cost_scaling_factor: 3.0
            inflation_radius: 0.5
          voxel_layer:
            plugin: "nav2_costmap_2d::VoxelLayer"
            enabled: true
            voxel_size: 0.05
            observation_sources: pointcloud
            pointcloud:
              topic: "/pointcloud_topic"
              max_obstacle_height: 2.0
              min_obstacle_height: 0.0
              obstacle_range: 2.5
              raytrace_range: 3.0
              clearing: true
              marking: true
              data_type: "PointCloud2"
          static_layer:
            map_subscribe_transient_local: true
          always_send_full_costmap: true

    global_costmap:
      global_costmap:
        ros__parameters:
          update_frequency: 5.0
          publish_frequency: 2.0
          global_frame: map
          robot_base_frame: base_footprint
          robot_radius: 0.25    # Humanoid radius
          resolution: 0.1
          track_unknown_space: true
          plugins: ["static_layer", "obstacle_layer", "inflation_layer"]
          obstacle_layer:
            plugin: "nav2_costmap_2d::ObstacleLayer"
            enabled: true
            observation_sources: scan
            scan:
              topic: "/scan"
              max_obstacle_height: 2.0
              clearing: true
              marking: true
              data_type: "LaserScan"
          static_layer:
            plugin: "nav2_costmap_2d::StaticLayer"
            map_subscribe_transient_local: true
          inflation_layer:
            plugin: "nav2_costmap_2d::InflationLayer"
            cost_scaling_factor: 3.0
            inflation_radius: 0.5

planner_server:
  ros__parameters:
    expected_planner_frequency: 10.0    # Lower for complex humanoid planning
    use_sim_time: false
    planner_plugins: ["GridBased"]

    GridBased:
      plugin: "nav2_navfn_planner/NavfnPlanner"
      tolerance: 0.5
      use_astar: false
      allow_unknown: true

      # Humanoid-specific parameters
      step_height_limit: 0.15    # Maximum step height
      step_width_limit: 0.30     # Maximum step width
      slope_limit: 0.3          # Maximum slope in radians
      min_distance_from_obstacles: 0.3  # Extra safety margin

smoother_server:
  ros__parameters:
    use_sim_time: false
    smoother_plugins: ["simple_smoother"]
    simple_smoother:
      plugin: "nav2_smoother::SimpleSmoother"
      tolerance: 1.0e-10
      max_its: 1000
      do_refinement: true

behavior_server:
  ros__parameters:
    costmap_topic: local_costmap/costmap_raw
    footprint_topic: local_costmap/published_footprint
    cycle_frequency: 10.0
    behavior_plugins: ["spin", "backup", "wait"]
    spin:
      plugin: "nav2_behaviors/Spin"
      spin_dist: 1.57    # 90 degrees for humanoid turning
    backup:
      plugin: "nav2_behaviors/BackUp"
      backup_dist: 0.2   # Conservative backup distance
      backup_speed: 0.05
    wait:
      plugin: "nav2_behaviors/Wait"
      wait_duration: 5s

waypoint_follower:
  ros__parameters:
    loop_rate: 20
    stop_on_failure: false
    waypoint_task_executor_plugin: "wait_at_waypoint"
    wait_at_waypoint:
      plugin: "nav2_waypoint_follower::WaitAtWaypoint"
      enabled: true
      wait_time: 2s
```

## Step 4: Configure Humanoid-Specific Costmap Layers

### Create Custom Costmap Plugins
For advanced humanoid navigation, you may need custom costmap layers:

**Humanoid Step Costmap Layer**:
```yaml
# Custom step-aware costmap layer
global_costmap:
  plugins:
    - {name: static_layer, type: "nav2_costmap_2d::StaticLayer"}
    - {name: step_layer, type: "nav2_humanoid_layers::StepLayer"}
    - {name: balance_layer, type: "nav2_humanoid_layers::BalanceLayer"}
    - {name: inflation_layer, type: "nav2_costmap_2d::InflationLayer"}

  step_layer:
    enabled: true
    max_step_height: 0.15
    min_traversable_height: 0.05
    step_cost_multiplier: 2.0

  balance_layer:
    enabled: true
    balance_threshold: 0.8
    balance_cost_radius: 0.5
```

## Step 5: Set Up the Launch File

### Create a Humanoid-Specific Launch File
**nav2_humanoid_launch.py**:
```python
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from nav2_common.launch import RewrittenYaml


def generate_launch_description():
    # Launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')
    params_file = LaunchConfiguration('params_file')
    default_bt_xml_filename = LaunchConfiguration('default_bt_xml_filename')
    map_sub = LaunchConfiguration('map_subscribe_transient_local')

    # Launch configuration
    bringup_dir = get_package_share_directory('nav2_bringup')
    bt_dir = get_package_share_directory('nav2_bt_navigator')

    # Create the node
    navigation_node = Node(
        package='nav2_controller',
        executable='controller_server',
        output='screen',
        parameters=[params_file, {'use_sim_time': use_sim_time}],
        remappings=[('cmd_vel', 'cmd_vel_out'),
                   ('odom', 'odom'),
                   ('global_costmap', 'global_costmap'),
                   ('local_costmap', 'local_costmap'),
                   ('robot_base_frame', 'base_footprint')]
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation time if true'),
        DeclareLaunchArgument(
            'autostart',
            default_value='true',
            description='Automatically startup the nav2 stack'),
        DeclareLaunchArgument(
            'params_file',
            default_value=os.path.join(bringup_dir, 'params', 'nav2_params_humanoid.yaml'),
            description='Full path to the ROS2 parameters file to use for all launched nodes'),
        DeclareLaunchArgument(
            'default_bt_xml_filename',
            default_value=os.path.join(bt_dir, 'behavior_trees', 'navigate_w_replanning_and_recovery.xml'),
            description='Full path to the behavior tree xml file to use'),
        DeclareLaunchArgument(
            'map_subscribe_transient_local',
            default_value='false',
            description='Whether to set the map subscriber QoS to transient local'),

        navigation_node,
        # Add other Nav2 nodes here...
    ])
```

## Step 6: Configure the Behavior Tree

### Humanoid-Specific Behavior Tree
Create a behavior tree that accounts for humanoid navigation characteristics:

**humanoid_navigate_w_replanning_and_recovery.xml**:
```xml
<root main_tree_to_execute="MainTree">
  <BehaviorTree ID="MainTree">
    <RecoveryNode number_of_retries="6" name="NavigateRecovery">
      <PipelineSequence name="NavigateWithReplanning">
        <RateController hz="1.0">
          <RecoveryNode number_of_retries="1" name="ComputePathToPose">
            <ComputePathToPose goal="{goal}" path="{path}" planner_id="GridBased"/>
            <ReactiveFallback name="SmoothPathOrPass">
              <Condition name="IsStartInKeepoutFilter" filter_id="keepout_filter"/>
              <SmoothPath path="{path}" smoothed_path="{path}" smoother_id="SimpleSmoother"/>
            </ReactiveFallback>
          </RecoveryNode>
        </RateController>
        <ReactiveSequence name="FollowPathSequence">
          <GoalUpdated name="GoalUpdated"/>
          <FollowPath path="{path}" controller_id="HumanoidFollowPath"/>
        </ReactiveSequence>
      </PipelineSequence>
      <ReactiveFallback name="RecoveryFallback">
        <GoalUpdated name="GoalUpdated"/>
        <RecoveryNode number_of_retries="1" name="BackUp">
          <BackUp distance="0.2" speed="0.05"/>  <!-- Conservative for humanoid -->
        </RecoveryNode>
        <RecoveryNode number_of_retries="1" name="Spin">
          <Spin angle="1.57"/>  <!-- 90-degree spins for humanoid -->
        </RecoveryNode>
        <RecoveryNode number_of_retries="1" name="Wait">
          <Wait wait_duration="5"/>
        </RecoveryNode>
      </ReactiveFallback>
    </RecoveryNode>
  </BehaviorTree>
</root>
```

## Step 7: Integrate with Isaac ROS Perception (Optional)

### Perception Integration Configuration
If using Isaac ROS perception:

```yaml
# Integrate Isaac ROS perception with Nav2
perception_integration:
  ros__parameters:
    # Human detection for social navigation
    human_detection_topic: "/isaac_ros/detections_3d"
    human_tracking_enabled: true
    human_safety_distance: 0.8  # meters

    # Obstacle detection from Isaac ROS
    obstacle_detection_topic: "/isaac_ros/obstacles"
    obstacle_processing_enabled: true
    dynamic_obstacle_tracking: true
```

## Step 8: Test the Configuration

### Simulation Testing
1. **Start Navigation Stack**:
   ```bash
   ros2 launch nav2_bringup navigation_launch.py \
     params_file:=/path/to/nav2_params_humanoid.yaml
   ```

2. **Send Navigation Goals**:
   ```bash
   ros2 run nav2_test_launch navigation2_goal.py
   ```

3. **Monitor Navigation**:
   ```bash
   # Monitor navigation topics
   ros2 topic echo /nav_through_poses/_action/status
   ros2 topic echo /local_costmap/costmap_updates
   ros2 topic echo /global_costmap/costmap_updates
   ```

### Real Robot Testing (with Safety)
1. **Start with Safety Personnel Present**
2. **Begin with Simple, Safe Environments**
3. **Monitor Balance and Stability Metrics**
4. **Gradually Increase Complexity**

## Step 9: Fine-tune Parameters

### Performance Tuning
1. **Monitor Navigation Performance**:
   ```bash
   # Check navigation metrics
   ros2 run nav2_util navigation_metrics
   ```

2. **Adjust Speed Parameters**:
   - Start conservative (0.2 m/s)
   - Gradually increase while maintaining stability
   - Monitor balance metrics

3. **Tune Costmap Parameters**:
   - Adjust inflation radius for safety
   - Modify resolution for precision vs. performance
   - Tune obstacle detection thresholds

### Constraint Validation
1. **Verify Kinematic Constraints**:
   - Check step height limits
   - Validate turning capabilities
   - Confirm balance preservation

2. **Test Edge Cases**:
   - Narrow passages
   - Steep slopes
   - Dynamic obstacles
   - Human interaction scenarios

## Step 10: Advanced Configuration (Optional)

### Social Navigation Configuration
```yaml
# Social navigation parameters
social_navigation:
  ros__parameters:
    personal_space_radius: 0.8
    social_space_radius: 1.2
    approach_angle_preference: 45.0
    interaction_readiness: true
    gaze_control_integration: true
```

### Multi-Modal Navigation
Configure for different navigation modes:
- **Walking Mode**: Standard bipedal navigation
- **Crawling Mode**: For low-clearance situations
- **Climbing Mode**: For step climbing (if capable)

## Troubleshooting Common Issues

### Navigation Instability
- **Symptoms**: Robot sways or loses balance during navigation
- **Solutions**:
  - Reduce navigation speeds
  - Increase safety margins
  - Improve balance controller integration

### Path Planning Failures
- **Symptoms**: Planner cannot find valid paths
- **Solutions**:
  - Adjust costmap inflation parameters
  - Verify kinematic constraint parameters
  - Check map quality and resolution

### Localization Drift
- **Symptoms**: Robot position estimate becomes inaccurate
- **Solutions**:
  - Improve sensor integration
  - Tune AMCL parameters
  - Verify odometry quality

## Best Practices

### Safety First
- Always test with safety personnel present
- Implement emergency stop procedures
- Start with conservative parameters
- Monitor balance metrics continuously

### Progressive Testing
- Begin with simple environments
- Gradually increase complexity
- Test edge cases thoroughly
- Validate in multiple scenarios

### Parameter Management
- Document all parameter changes
- Maintain backup configurations
- Use version control for configurations
- Test parameter changes systematically

## Next Steps

Continue to the movement execution tutorial to learn how to implement and test actual navigation commands with your configured Nav2 system for humanoid robots.