---
title: Quick Reference Guides
sidebar_position: 15
---

# Quick Reference Guides

This section provides quick reference materials for common Isaac Sim, Isaac ROS, and Nav2 operations and commands for humanoid robotics applications.

## Isaac Sim Quick Reference

### Common Isaac Sim Commands

#### Environment Setup
```bash
# Launch Isaac Sim
./isaac-sim.bat  # Windows
./isaac-sim.sh   # Linux

# Create new scene
File → New Scene

# Save scene
File → Save As → [filename].usd
```

#### Essential USD Paths
```
/World/Robot        # Robot root prim
/World/GroundPlane  # Ground plane
/World/Lights       # Light sources
/World/Cameras      # Camera sensors
```

### Synthetic Data Generation Parameters

#### Domain Randomization Settings
| Parameter | Range | Purpose |
|-----------|-------|---------|
| Material Roughness | 0.0 - 1.0 | Surface texture variation |
| Material Metallic | 0.0 - 1.0 | Metallic property variation |
| Lighting Intensity | 0.5 - 2.0 | Brightness variation |
| Object Position | ±0.5m | Position randomization |

#### Annotation Types
| Type | Purpose | Output |
|------|---------|---------|
| Semantic Segmentation | Class labeling | Per-pixel class IDs |
| Instance Segmentation | Individual object | Per-pixel instance IDs |
| Bounding Boxes | Object localization | 2D/3D bounding boxes |
| Depth Maps | Distance information | Z-buffer values |

### Isaac Sim Python API Quick Commands
```python
# Import Isaac Sim modules
import omni
from omni.isaac.core import World
from omni.isaac.core.utils.stage import add_reference_to_stage

# Load robot
add_reference_to_stage(
    usd_path="/path/to/robot.usd",
    prim_path="/World/Robot"
)

# Set camera position
camera.set_world_pose(position=np.array([0, 0, 1.5]), orientation=rot)

# Start simulation
world.play()
```

## Isaac ROS Quick Reference

### Common Isaac ROS Packages

#### Essential Packages
| Package | Purpose | Main Node |
|---------|---------|-----------|
| `isaac_ros_visual_slam` | Visual SLAM | `isaac_ros_visual_slam_node` |
| `isaac_ros_stereo_dnn` | Object detection | `isaac_ros_stereo_dnn` |
| `isaac_ros_stereo_image_proc` | Stereo processing | `disparity_node` |
| `isaac_ros_detection2d_compositor` | 3D detection | `detection2d_compositor` |

### Isaac ROS Launch Commands
```bash
# Launch Visual SLAM
ros2 launch isaac_ros_visual_slam visual_slam.launch.py

# Launch Stereo DNN
ros2 launch isaac_ros_stereo_dnn stereo_dnn.launch.py \
  engine_file_path:=/path/to/model.plan

# Launch Stereo Processing
ros2 launch isaac_ros_stereo_image_proc stereo_image_proc.launch.py
```

### Isaac ROS Parameter Tuning Guide

#### Visual SLAM Parameters
| Parameter | Default | Humanoid Use |
|-----------|---------|--------------|
| `tracking_rate` | 30.0 | 20.0 (slower for stability) |
| `min_distance_between_keyframes` | 0.2 | 0.15 (humanoid step size) |
| `min_rotation_between_keyframes` | 0.2 | 0.2 (balance consideration) |
| `max_num_landmarks` | 1000 | 2000 (for complex environments) |

#### Stereo DNN Parameters
| Parameter | Description | Typical Value |
|-----------|-------------|---------------|
| `confidence_threshold` | Detection confidence | 0.5-0.7 |
| `input_topic_width` | Image width | 640 |
| `input_topic_height` | Image height | 480 |
| `network_type` | Model type | `coco_tensorrt` |

### Isaac ROS Topic Reference
```bash
# Common Isaac ROS topics
/camera/left/image_rect_color     # Left rectified camera
/camera/right/image_rect_color    # Right rectified camera
/visual_slam/pose                 # SLAM pose estimate
/detections_2d                    # 2D object detections
/detections_3d                    # 3D object detections
/disparity/depth_image_rect       # Depth from stereo
```

## Nav2 Quick Reference

### Nav2 Launch Commands
```bash
# Launch Nav2 with default parameters
ros2 launch nav2_bringup navigation_launch.py

# Launch with custom parameters
ros2 launch nav2_bringup navigation_launch.py \
  params_file:=/path/to/humanoid_params.yaml

# Launch with simulation time
ros2 launch nav2_bringup navigation_launch.py \
  use_sim_time:=true
```

### Nav2 Action Commands
```bash
# Send navigation goal using action client
ros2 action send_goal /navigate_to_pose \
  nav2_msgs/action/NavigateToPose \
  "{pose: {position: {x: 1.0, y: 1.0, z: 0.0}, orientation: {w: 1.0}}}"
```

### Nav2 Parameter Quick Guide

#### Costmap Parameters
| Parameter | Type | Humanoid Value | Purpose |
|-----------|------|----------------|---------|
| `robot_radius` | float | 0.25-0.35 | Collision buffer |
| `inflation_radius` | float | 0.5-1.0 | Safety margin |
| `resolution` | float | 0.05-0.1 | Map precision |
| `update_frequency` | float | 5-10 Hz | Update rate |

#### Controller Parameters
| Parameter | Humanoid Range | Purpose |
|-----------|----------------|---------|
| `max_linear_speed` | 0.3-0.5 m/s | Forward speed limit |
| `min_linear_speed` | 0.1-0.15 m/s | Minimum for balance |
| `max_angular_speed` | 0.3-0.5 rad/s | Rotation speed limit |
| `acc_lim_x` | 0.1-0.3 | Linear acceleration |

#### Planner Parameters
| Parameter | Humanoid Value | Purpose |
|-----------|----------------|---------|
| `tolerance` | 0.3-0.5 m | Goal acceptance |
| `step_height_limit` | 0.10-0.15 m | Step capability |
| `slope_limit` | 0.2-0.4 | Inclination limit |

### Nav2 TF Frame Requirements
```
Required TF tree:
map → odom → base_link → base_footprint
      ↓
  camera_link, imu_link, etc.
```

## Common Integration Commands

### Complete System Launch
```bash
# Launch complete AI-Robot Brain system
# Terminal 1: Robot drivers
ros2 launch your_robot_bringup robot.launch.py

# Terminal 2: Isaac ROS perception
ros2 launch your_perception_launch.py

# Terminal 3: Nav2 navigation
ros2 launch your_navigation_launch.py

# Terminal 4: RViz visualization
ros2 run rviz2 rviz2 -d /path/to/config.rviz
```

### Performance Monitoring
```bash
# Monitor key topics
ros2 topic hz /cmd_vel
ros2 topic hz /local_costmap/costmap_updates
ros2 topic hz /visual_slam/pose

# Check node status
ros2 lifecycle list controller_server
ros2 lifecycle list planner_server

# Monitor transforms
ros2 run tf2_tools view_frames
ros2 run tf2_ros tf2_echo map base_link
```

## Troubleshooting Quick Fixes

### Common Isaac Sim Issues
| Issue | Command | Solution |
|-------|---------|----------|
| GPU not detected | `nvidia-smi` | Update drivers |
| Scene not loading | Check USD path | Verify file exists |
| Camera not publishing | Check TF tree | Verify camera pose |

### Common Isaac ROS Issues
| Issue | Command | Solution |
|-------|---------|----------|
| No disparity output | `ros2 topic echo /disparity` | Check camera sync |
| SLAM drift | `ros2 topic echo /visual_slam/pose` | Check IMU calibration |
| Detection failures | `ros2 topic echo /detections` | Verify model path |

### Common Nav2 Issues
| Issue | Command | Solution |
|-------|---------|----------|
| No path found | `ros2 service call /is_path_valid ...` | Check costmap inflation |
| Robot stuck | `ros2 topic echo /cmd_vel` | Check local costmap |
| Localization lost | `ros2 topic echo /amcl_pose` | Reinitialize pose |

## Safety and Emergency Commands

### Emergency Stop
```bash
# Emergency stop command
ros2 topic pub /cmd_vel geometry_msgs/Twist '{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'
```

### System Reset
```bash
# Reset navigation system
ros2 lifecycle set controller_server configure
ros2 lifecycle set controller_server activate

# Clear costmaps
ros2 service call /global_costmap/clear_entirely_global_costmap std_srvs/srv/Empty
ros2 service call /local_costmap/clear_entirely_local_costmap std_srvs/srv/Empty
```

## Hardware-Specific Quick Reference

### GPU Memory Management
```bash
# Check GPU memory usage
nvidia-smi

# Set GPU memory fraction for Isaac ROS
export CUDA_VISIBLE_DEVICES=0
export NVIDIA_TENSORRT_PRECISION=fp16
```

### Real-time Priority (for critical nodes)
```bash
# Set real-time priority for navigation nodes
chrt -f 95 ros2 run nav2_controller controller_server
chrt -f 90 ros2 run nav2_planner planner_server
```

## Development Quick Commands

### Parameter Tuning
```bash
# Change parameter at runtime
ros2 param set controller_server HumanoidMPPI.max_linear_speed 0.4

# List all parameters
ros2 param list
```

### Debugging Tools
```bash
# Enable debug logging
ros2 run <package> <node> --ros-args --log-level debug

# Monitor specific topics
rqt_plot /controller_server/progress_checker/current_error
```

This quick reference guide provides essential commands and parameters for working with the AI-Robot Brain system, allowing for rapid development, debugging, and deployment of Isaac Sim, Isaac ROS, and Nav2 integrated systems for humanoid robotics.