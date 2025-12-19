---
title: Nav2 for Humanoid Robots Troubleshooting Guide
sidebar_position: 3
---

# Nav2 for Humanoid Robots Troubleshooting Guide

This guide provides solutions to common issues encountered when running Navigation 2 (Nav2) with humanoid robots. Humanoid navigation presents unique challenges due to balance requirements, kinematic constraints, and complex dynamics that differ from traditional wheeled robots.

## Installation and Setup Issues

### Nav2 Packages Not Found
**Symptoms**: ROS2 cannot find Nav2 packages or nodes.

**Solutions**:
1. **Verify Installation**:
   ```bash
   # Check if Nav2 packages are installed
   ros2 pkg list | grep nav2
   ```

2. **Install Missing Packages**:
   ```bash
   sudo apt update
   sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup
   sudo apt install ros-humble-nav2-rviz-plugins
   ```

3. **Source Environment**:
   ```bash
   source /opt/ros/humble/setup.bash
   source /install/setup.bash  # If built from source
   ```

### Parameter File Issues
**Symptoms**: Navigation stack fails to start due to parameter configuration errors.

**Solutions**:
1. **Validate Parameter File**:
   ```bash
   # Check YAML syntax
   python3 -c "import yaml; print(yaml.safe_load(open('nav2_params.yaml')))"
   ```

2. **Verify Parameter Paths**:
   - Ensure all file paths exist and are accessible
   - Check for typos in parameter names
   - Verify parameter structure matches Nav2 expectations

3. **Use Default Parameters for Testing**:
   ```bash
   ros2 launch nav2_bringup navigation_launch.py \
     params_file:=/opt/ros/humble/share/nav2_bringup/params/nav2_params.yaml
   ```

## Localization Issues

### AMCL Fails to Initialize
**Symptoms**: AMCL reports errors or cannot establish initial pose.

**Solutions**:
1. **Check TF Tree**:
   ```bash
   ros2 run tf2_tools view_frames
   # Verify: map -> odom -> base_link chain exists
   ```

2. **Verify Initial Pose**:
   - Ensure initial pose is set with reasonable covariance
   - Check that initial pose is within map boundaries
   - Verify map file is accessible and properly formatted

3. **AMCL Parameter Tuning**:
   ```yaml
   amcl:
     ros__parameters:
       alpha1: 0.2      # Increase for noisy odometry
       alpha2: 0.2      # Increase for noisy odometry
       alpha3: 0.2      # Increase for noisy odometry
       alpha4: 0.2      # Increase for noisy odometry
       alpha5: 0.2      # Increase for noisy odometry
       max_particles: 2000  # Increase for complex environments
       min_particles: 500   # Decrease for simpler environments
   ```

### Localization Drift
**Symptoms**: Robot position estimate becomes increasingly inaccurate over time.

**Solutions**:
1. **Improve Odometry Quality**:
   - Verify wheel encoder calibration
   - Check for wheel slippage
   - Ensure proper IMU integration

2. **Enhance Particle Filter**:
   ```yaml
   amcl:
     ros__parameters:
       resample_interval: 1    # Adjust resampling frequency
       recovery_alpha_fast: 0.0  # Disable fast recovery if causing issues
       recovery_alpha_slow: 0.0  # Disable slow recovery if causing issues
   ```

3. **Use Better Maps**: Create higher quality maps with more distinctive features

## Path Planning Issues

### Global Planner Cannot Find Path
**Symptoms**: Navigation fails with "Failed to create a plan" error.

**Solutions**:
1. **Check Costmap Configuration**:
   ```yaml
   global_costmap:
     ros__parameters:
       inflation_radius: 1.0    # Increase for humanoid safety
       resolution: 0.1          # Adjust for precision needs
       robot_radius: 0.25       # Set to actual robot radius
   ```

2. **Verify Start and Goal Validity**:
   - Ensure start position is not in obstacle
   - Ensure goal position is reachable
   - Check that both positions are within map bounds

3. **Adjust Inflation Parameters**:
   ```yaml
   inflation_layer:
     ros__parameters:
       cost_scaling_factor: 3.0  # Higher for humanoid safety
       inflation_radius: 0.8     # Larger for humanoid size
   ```

### Path Planning Too Conservative
**Symptoms**: Planner creates unnecessarily long or wide paths.

**Solutions**:
1. **Tune Global Planner**:
   ```yaml
   planner_server:
     ros__parameters:
       GridBased:
         tolerance: 0.5      # Increase to allow approximate paths
         use_astar: true     # Use A* for more direct paths
   ```

2. **Adjust Costmap Resolution**:
   - Lower resolution for less conservative planning
   - Balance precision vs. computation time

## Local Planning and Control Issues

### Robot Gets Stuck Frequently
**Symptoms**: Robot stops moving during navigation, unable to progress.

**Solutions**:
1. **Check Local Planner Configuration**:
   ```yaml
   controller_server:
     ros__parameters:
       HumanoidFollowPath:
         speed_limit_scale: 0.7    # Increase for more aggressive behavior
         acc_lim_x: 0.5           # Increase acceleration limits
         decel_lim_x: -0.7        # Increase deceleration limits
   ```

2. **Verify Sensor Data**:
   - Check that sensor topics are publishing
   - Ensure sensor range is adequate
   - Verify sensor mounting position

3. **Tune Progress Checker**:
   ```yaml
   progress_checker:
     ros__parameters:
       required_movement_radius: 0.8   # Decrease to detect being stuck sooner
       movement_time_allowance: 15.0   # Increase time allowance
   ```

### Oscillating Behavior
**Symptoms**: Robot oscillates back and forth instead of following path.

**Solutions**:
1. **Adjust Controller Parameters**:
   ```yaml
   controller_server:
     ros__parameters:
       HumanoidFollowPath:
         vx_max: 0.3        # Reduce maximum speed
         vx_min: 0.15       # Ensure minimum for stability
         acc_lim_x: 0.1     # Reduce acceleration
         decel_lim_x: -0.2  # Reduce deceleration
   ```

2. **Improve Path Smoothing**:
   - Use path smoother plugins
   - Increase path resolution
   - Apply additional smoothing in post-processing

## Humanoid-Specific Issues

### Balance-Related Navigation Failures
**Symptoms**: Navigation stops due to balance system interventions.

**Solutions**:
1. **Adjust Navigation Speeds**:
   ```yaml
   controller_server:
     ros__parameters:
       HumanoidFollowPath:
         max_linear_speed: 0.3    # Reduce for better balance
         min_linear_speed: 0.08   # Maintain minimum for stability
   ```

2. **Tune for Balance System**:
   - Coordinate with balance controller
   - Implement velocity ramping
   - Use smoother acceleration profiles

3. **Verify Step Constraints**:
   ```yaml
   planner_server:
     ros__parameters:
       GridBased:
         step_height_limit: 0.12    # Adjust to actual robot capability
         step_width_limit: 0.25     # Adjust to actual robot capability
   ```

### Kinematic Constraint Violations
**Symptoms**: Planned paths violate robot's physical constraints.

**Solutions**:
1. **Update Kinematic Parameters**:
   ```yaml
   global_costmap:
     ros__parameters:
       robot_radius: 0.3    # Accurate robot dimensions
       footprint: [[-0.3, -0.25], [-0.3, 0.25], [0.3, 0.25], [0.3, -0.25]]  # Custom footprint
   ```

2. **Implement Custom Costmap Layers**:
   - Create step-aware costmap layer
   - Add balance constraint checking
   - Implement terrain analysis

### Gait-Related Navigation Issues
**Symptoms**: Navigation conflicts with walking gait patterns.

**Solutions**:
1. **Coordinate with Gait Controller**:
   - Implement proper velocity command timing
   - Synchronize with step planning
   - Use appropriate transition states

2. **Adjust for Bipedal Dynamics**:
   - Lower acceleration/deceleration limits
   - Implement velocity smoothing
   - Use appropriate turning strategies

## Sensor Integration Issues

### Laser Scan Problems
**Symptoms**: Obstacle detection fails or provides inconsistent data.

**Solutions**:
1. **Verify Laser Topic**:
   ```bash
   ros2 topic echo /scan
   ros2 topic info /scan
   ```

2. **Check TF Chain**:
   - Ensure laser frame connects to robot base
   - Verify transform timing
   - Check transform accuracy

3. **Costmap Configuration**:
   ```yaml
   local_costmap:
     ros__parameters:
       obstacle_layer:
         scan:
           topic: "/scan"
           max_obstacle_height: 2.0
           obstacle_range: 3.0    # Adjust to sensor range
           raytrace_range: 3.5    # Slightly beyond obstacle range
   ```

### 3D Sensor Issues
**Symptoms**: Depth camera or 3D sensor data not processed correctly.

**Solutions**:
1. **Verify Point Cloud Topic**:
   ```bash
   ros2 topic echo /pointcloud_topic
   ros2 run rqt_plot rqt_plot /pointcloud_topic
   ```

2. **Check Voxel Layer Configuration**:
   ```yaml
   local_costmap:
     ros__parameters:
       voxel_layer:
         enabled: true
         voxel_size: 0.05
         observation_sources: pointcloud
         pointcloud:
           topic: "/pointcloud_topic"
           max_obstacle_height: 2.0
           min_obstacle_height: 0.0
           obstacle_range: 2.5
           raytrace_range: 3.0
   ```

## Performance Issues

### High CPU Usage
**Symptoms**: Navigation stack consumes excessive CPU resources.

**Solutions**:
1. **Reduce Update Frequencies**:
   ```yaml
   local_costmap:
     ros__parameters:
       update_frequency: 10.0    # Reduce from default
       publish_frequency: 5.0    # Reduce from default
   ```

2. **Optimize Costmap Resolution**:
   ```yaml
   global_costmap:
     ros__parameters:
       resolution: 0.2    # Increase resolution (lower precision)
   ```

3. **Limit Planner Attempts**:
   ```yaml
   planner_server:
     ros__parameters:
       expected_planner_frequency: 5.0    # Reduce planning frequency
   ```

### Memory Issues
**Symptoms**: System runs out of memory during extended operation.

**Solutions**:
1. **Limit Map Sizes**:
   ```yaml
   global_costmap:
     ros__parameters:
       width: 20.0    # Reduce map width
       height: 20.0   # Reduce map height
   ```

2. **Implement Map Management**:
   - Use sliding window maps
   - Implement proper cleanup procedures
   - Monitor memory usage continuously

## Behavior Tree Issues

### Behavior Tree Fails to Execute
**Symptoms**: Navigation behaviors don't execute as expected.

**Solutions**:
1. **Verify Behavior Tree XML**:
   - Check XML syntax
   - Verify plugin names match installed plugins
   - Ensure all referenced plugins are loaded

2. **Check Plugin Libraries**:
   ```bash
   # Verify behavior tree plugins are available
   ros2 param list | grep bt
   ```

3. **Debug Behavior Execution**:
   ```bash
   # Enable debug output
   ros2 run nav2_behavior_tree bt_navigator --ros-args --log-level debug
   ```

## Social Navigation Issues

### Human Detection Integration Problems
**Symptoms**: Social navigation doesn't respond to humans properly.

**Solutions**:
1. **Verify Human Detection Topics**:
   ```bash
   ros2 topic list | grep human
   ros2 topic echo /human_detections
   ```

2. **Check Social Costmap Configuration**:
   ```yaml
   local_costmap:
     ros__parameters:
       plugins: ["voxel_layer", "static_layer", "inflation_layer", "social_layer"]
   ```

3. **Tune Social Parameters**:
   ```yaml
   social_navigation:
     ros__parameters:
       personal_space_radius: 0.8
       social_space_radius: 1.2
       approach_angle_preference: 45.0
   ```

## Common Error Messages and Solutions

### "Could not get robot pose"
**Cause**: TF tree issues or localization problems.
**Solution**: Check TF chain from map to base_link, verify localization is running.

### "Invalid Trajectory"
**Cause**: Controller cannot find valid command that satisfies constraints.
**Solution**: Relax controller constraints, check sensor data, verify robot state.

### "Global planner failed to create plan"
**Cause**: No valid path found or planner timeout.
**Solution**: Check map quality, adjust inflation parameters, verify start/goal validity.

### "Local planner failed to find valid velocity command"
**Cause**: Robot is boxed in or controller parameters are too restrictive.
**Solution**: Increase local costmap size, adjust controller parameters, check for obstacles.

### "TF Exception"
**Cause**: Transform lookup failures.
**Solution**: Check TF tree, verify all required transforms exist, check timing.

## Debugging Strategies

### Systematic Debugging Approach
1. **Isolate the Issue**: Identify which specific component is failing
2. **Check Dependencies**: Verify all required inputs are available
3. **Validate Configuration**: Confirm parameters are appropriate
4. **Monitor Resource Usage**: Check CPU, memory, and network usage
5. **Review Logs**: Examine ROS2 and system logs for errors

### Monitoring Tools
```bash
# Monitor navigation topics
ros2 topic hz /cmd_vel
ros2 topic hz /local_costmap/costmap_updates
ros2 topic hz /global_costmap/costmap_updates

# Check node health
ros2 lifecycle list controller_server
ros2 lifecycle list planner_server

# Monitor transforms
ros2 run tf2_ros tf2_echo map base_link
```

### Visualization with RViz
1. **Add Costmap Displays**: Monitor local and global costmaps
2. **Path Displays**: Visualize planned and executed paths
3. **Robot Model**: Verify TF tree with robot model display
4. **Sensor Data**: Monitor laser scans and other sensor data

## Performance Optimization

### Profiling Navigation Stack
```bash
# Use ROS2 tools to profile
ros2 run performance_test performance_test_fixture
# Use system tools to monitor resource usage
htop
nvidia-smi  # For GPU usage
```

### Tuning Guidelines
1. **Start Conservative**: Begin with safe parameters
2. **Incremental Improvements**: Make small adjustments
3. **Monitor Metrics**: Track success rates and performance
4. **Environment-Specific**: Tune for specific operating conditions

## Prevention and Maintenance

### Regular Maintenance
- Monitor system performance metrics
- Update Nav2 packages regularly
- Calibrate sensors periodically
- Validate navigation performance regularly

### Health Monitoring
- Implement system health checks
- Monitor navigation success rates
- Track error patterns and frequencies
- Set up alerts for critical failures

## Getting Help

### Official Resources
- [Nav2 Documentation](https://navigation.ros.org/)
- [ROS Answers](https://answers.ros.org/)
- [Nav2 GitHub Repository](https://github.com/ros-planning/navigation2)

### Community Resources
- ROS Discourse forum
- Robotics Stack Exchange
- Local ROS user groups

## Next Steps

If issues persist after consulting this guide, consider reaching out to the Nav2 community or consulting more specific documentation for your particular humanoid robot platform.