---
title: Assessment Questions
sidebar_position: 14
---

# Assessment Questions

This document provides assessment questions for the AI-Robot Brain (NVIDIA Isaac™) module, organized by chapter and difficulty level. These questions test both theoretical understanding and practical application of the concepts covered.

## Chapter 1: Isaac Sim - Synthetic Data Generation

### Multiple Choice Questions

**Q1.1:** What is the primary advantage of using synthetic data for training perception models in robotics?
A) It's cheaper to generate than real data
B) It provides perfect ground truth labels
C) It can be generated in unlimited quantities
D) All of the above

**Answer:** D) All of the above

**Q1.2:** Domain randomization in Isaac Sim is primarily used for:
A) Increasing simulation speed
B) Improving the transfer of models from simulation to reality
C) Reducing computational requirements
D) Creating more realistic graphics

**Answer:** B) Improving the transfer of models from simulation to reality

**Q1.3:** Which file format does Isaac Sim use for 3D scene representation?
A) URDF
B) OBJ
C) USD (Universal Scene Description)
D) STL

**Answer:** C) USD (Universal Scene Description)

### Short Answer Questions

**Q1.4:** Explain the difference between semantic segmentation and instance segmentation in the context of synthetic data generation. Why are both important for humanoid robot perception?

**Sample Answer:** Semantic segmentation assigns a class label to each pixel (e.g., all pixels belonging to "human" are labeled as such), while instance segmentation additionally distinguishes between different instances of the same class (e.g., Person 1 vs Person 2). Both are important for humanoid robots because semantic segmentation helps the robot understand the environment composition, while instance segmentation enables tracking of individual humans and objects, which is crucial for navigation and interaction.

**Q1.5:** Describe three key parameters that should be randomized in domain randomization for humanoid robot training data, and explain why each is important.

**Sample Answer:**
1. **Lighting conditions** - Different lighting affects how sensors perceive the environment, so training with varied lighting improves robustness
2. **Material properties** - Randomizing textures and surface properties helps the model generalize to different real-world surfaces
3. **Object placement** - Varying object positions and configurations ensures the model can handle diverse real-world scenarios

### Practical Application Questions

**Q1.6:** You need to generate synthetic training data for a humanoid robot that will operate in office environments. Design a simulation scenario that would generate useful training data for detecting chairs, desks, and humans. Include at least 5 different environmental variations you would implement.

**Sample Answer:**
- **Lighting variations**: Natural light (windows), artificial light (fluorescent, LED), mixed lighting conditions
- **Furniture arrangements**: Different desk and chair configurations, cluttered vs. organized spaces
- **Human presence**: Various numbers of people, different poses and activities
- **Time of day**: Morning, afternoon, evening lighting conditions
- **Weather effects**: Clear, overcast lighting conditions affecting window light

**Q1.7:** Calculate the minimum number of unique training scenarios needed to adequately cover the following variations: 3 lighting conditions, 4 furniture arrangements, 5 human poses, and 2 office layouts. If each scenario takes 10 minutes to generate, how long would it take to generate all scenarios?

**Sample Answer:**
- Total combinations: 3 × 4 × 5 × 2 = 120 scenarios
- Total time: 120 × 10 minutes = 1,200 minutes = 20 hours

## Chapter 2: Isaac ROS - Perception & Navigation

### Multiple Choice Questions

**Q2.1:** Which of the following is NOT a primary advantage of Isaac ROS over traditional ROS perception packages?
A) GPU acceleration for faster processing
B) Hardware-specific optimizations
C) Built-in machine learning training capabilities
D) Integration with NVIDIA hardware

**Answer:** C) Built-in machine learning training capabilities

**Q2.2:** Visual-Inertial SLAM (VIO) combines:
A) Camera and LIDAR data
B) Camera and IMU data
C) Multiple camera viewpoints
D) Depth and RGB data

**Answer:** B) Camera and IMU data

**Q2.3:** The primary benefit of using TensorRT in Isaac ROS is:
A) Better camera calibration
B) Accelerated AI inference
C) Improved sensor fusion
D) Enhanced SLAM accuracy

**Answer:** B) Accelerated AI inference

### Short Answer Questions

**Q2.4:** Explain the difference between Visual SLAM (VSLAM) and Visual-Inertial SLAM (VIO), and describe why VIO might be more suitable for humanoid robots.

**Sample Answer:** Visual SLAM uses only camera data for localization and mapping, while Visual-Inertial SLAM combines camera data with IMU data for more robust tracking. VIO is more suitable for humanoid robots because: 1) IMU data helps maintain tracking during rapid movements common in bipedal locomotion, 2) IMU provides motion estimates during periods where visual features are insufficient, and 3) the combination provides more accurate pose estimation for balance-critical applications.

**Q2.5:** What is the role of the Detection2D Compositor in Isaac ROS, and how does it contribute to 3D object detection?

**Sample Answer:** The Detection2D Compositor combines 2D object detections from a neural network with stereo depth information to create 3D bounding boxes around detected objects. It takes 2D detection results and stereo disparity data as inputs, then projects the 2D detections into 3D space, providing depth information for detected objects. This is crucial for humanoid robots to understand the 3D spatial relationships of objects in their environment.

### Practical Application Questions

**Q2.6:** You're configuring Isaac ROS for a humanoid robot with stereo cameras (baseline: 15cm, resolution: 640x480) and an IMU. Create a parameter configuration file for the visual SLAM node that optimizes for humanoid navigation in indoor environments.

**Sample Answer:**
```yaml
visual_slam_node:
  ros__parameters:
    # Input topics
    rectified_left_topic_name: "/camera/left/image_rect_color"
    rectified_right_topic_name: "/camera/right/image_rect_color"
    left_camera_info_topic_name: "/camera/left/camera_info"
    right_camera_info_topic_name: "/camera/right/camera_info"
    imu_topic_name: "/imu/data_raw"

    # Performance parameters
    tracking_rate: 20.0  # Lower for humanoid stability
    mapping_rate: 5.0
    enable_occupancy_map: true
    occupancy_map_width: 20.0
    occupancy_map_height: 20.0
    occupancy_map_resolution: 0.1

    # Humanoid-specific parameters
    enable_localization: true
    enable_mapping: true
    enable_freespace_map: true
    min_distance_between_keyframes: 0.2  # Humanoid step size
    min_rotation_between_keyframes: 0.2
```

**Q2.7:** Design a perception pipeline for a humanoid robot that needs to detect and track humans in a social environment. List the Isaac ROS components needed and explain how they work together.

**Sample Answer:**
Components needed:
1. **Stereo Image Rectification** - Rectifies stereo camera images
2. **Disparity Computation** - Computes depth from stereo images
3. **Isaac ROS Stereo DNN** - Detects humans in stereo images
4. **Detection2D Compositor** - Converts 2D detections to 3D
5. **Tracking Component** - Tracks detected humans over time

How they work together: Stereo cameras feed into rectification, then disparity computation provides depth. The stereo DNN detects humans in the rectified images, and the compositor combines this with depth to create 3D human positions. Tracking maintains identity over time for consistent social navigation.

## Chapter 3: Nav2 - Humanoid Path Planning

### Multiple Choice Questions

**Q3.1:** What is the primary difference between navigation for wheeled robots and humanoid robots?
A) Different sensor requirements
B) Humanoid robots have balance and step constraints
C) Different mapping algorithms
D) Higher computational requirements

**Answer:** B) Humanoid robots have balance and step constraints

**Q3.2:** In Nav2, the ZMP (Zero Moment Point) is important for humanoid navigation because:
A) It determines the robot's speed
B) It must remain within the support polygon for balance
C) It affects sensor accuracy
D) It determines the path planning algorithm

**Answer:** B) It must remain within the support polygon for balance

**Q3.3:** Social navigation in humanoid robots typically requires maintaining a distance of at least:
A) 0.5 meters from humans
B) 1.0 meters from humans
C) 2.0 meters from humans
D) 3.0 meters from humans

**Answer:** A) 0.5 meters from humans

### Short Answer Questions

**Q3.4:** Explain the concept of "support polygon" in humanoid robotics and how it affects navigation planning.

**Sample Answer:** The support polygon is the area defined by the points of contact between the robot and the ground (e.g., the area covered by both feet during double support phase). For humanoid robots to maintain balance, the Center of Mass (CoM) and Zero Moment Point (ZMP) must remain within this support polygon. This constraint significantly affects navigation planning because the robot cannot make arbitrary movements; each step must be planned to maintain this balance constraint, limiting the possible paths and requiring step-by-step planning rather than continuous motion planning.

**Q3.5:** Describe three key parameters that must be customized for Nav2 to work effectively with humanoid robots, and explain why each is important.

**Sample Answer:**
1. **Step height/width limits** - Humanoid robots can only step over obstacles up to a certain height and have limited step width, which must be considered in path planning
2. **Minimum linear velocity** - Humanoid robots require a minimum speed to maintain dynamic balance, unlike wheeled robots that can stop instantly
3. **Balance preservation constraints** - Navigation commands must consider the robot's balance state to prevent falls during motion

### Practical Application Questions

**Q3.6:** You need to configure Nav2 for a humanoid robot with the following specifications: max step height 15cm, max step width 30cm, max walking speed 0.4 m/s, and personal space requirement of 0.8m for humans. Write the key configuration parameters for the global costmap, local planner, and behavior tree.

**Sample Answer:**
```yaml
# Global costmap for humanoid constraints
global_costmap:
  ros__parameters:
    robot_radius: 0.3  # Account for humanoid width
    plugins: ["static_layer", "step_layer", "inflation_layer"]
    inflation_layer:
      cost_scaling_factor: 4.0  # Higher for humanoid safety
      inflation_radius: 1.0     # Account for personal space
    step_layer:
      enabled: true
      max_step_height: 0.15     # Robot's capability
      max_traversable_height: 0.10

# Local planner configuration
controller_server:
  ros__parameters:
    HumanoidMPPI:
      max_linear_speed: 0.4     # Robot's max speed
      min_linear_speed: 0.1     # Minimum for balance
      acc_lim_x: 0.2           # Conservative acceleration
      decel_lim_x: -0.3

# Behavior tree modifications for humanoid
# Add step-aware recovery behaviors
```

**Q3.7:** Design a navigation scenario where a humanoid robot must navigate through a crowded hallway while respecting human personal space. Describe the challenges and how Nav2 should handle them.

**Sample Answer:**
Challenges:
1. **Dynamic obstacles** - Humans moving unpredictably
2. **Narrow spaces** - Hallway may be barely wider than robot
3. **Social constraints** - Must respect personal space while making progress
4. **Balance requirements** - Navigation must not compromise stability

Nav2 handling:
- Use social costmap layer to create buffers around humans
- Implement human-aware local planning with predictive models
- Use appropriate recovery behaviors for human interaction
- Adjust speed based on human proximity and hallway density
- Implement social navigation behaviors like yielding and polite passing

## Integrated System Assessment

### System Design Questions

**Q4.1:** Design a complete AI-Robot Brain system for a humanoid robot that needs to navigate in a hospital environment to deliver items to patients. The system should work both in simulation (for training) and on the real robot. Describe the complete architecture and data flow.

**Sample Answer:**
Architecture:
- **Isaac Sim**: Hospital environment simulation with patients, staff, and obstacles
- **Isaac ROS**: Perception stack for detecting humans, medical equipment, and navigation aids
- **Nav2**: Navigation system with hospital-specific constraints and social behaviors
- **Integration**: Real-time data flow between all components

Data flow:
1. Cameras → Isaac ROS perception → Environment understanding
2. Perception → Nav2 costmaps → Safe path planning
3. Isaac Sim → Synthetic training data → Perception model improvement
4. SLAM → Localization → Accurate navigation

**Q4.2:** A humanoid robot's navigation system works well in simulation but fails when deployed on the real robot in similar environments. What are the potential causes and how would you address them?

**Sample Answer:**
Potential causes:
1. **Sim-to-real gap**: Differences in sensor data between simulation and reality
2. **Sensor calibration**: Real sensors may be miscalibrated
3. **Timing differences**: Simulation and real system may have different latencies
4. **Dynamics mismatch**: Simulation may not accurately model robot dynamics
5. **Environmental differences**: Real environment has more variability

Solutions:
- Improve domain randomization in simulation
- Carefully calibrate real robot sensors
- Match simulation timing to real system
- Validate simulation models against real robot
- Use domain adaptation techniques
- Gradual deployment with safety monitoring

### Troubleshooting Questions

**Q4.3:** The humanoid robot's navigation system suddenly stops working - it can't find paths in previously mapped areas. The perception system shows normal camera feeds and object detection. What systematic approach would you take to diagnose the issue?

**Sample Answer:**
Systematic diagnosis approach:
1. **Check TF tree** - Verify map→odom→base_link chain is intact
2. **Examine costmaps** - Check if local/global costmaps are updating properly
3. **Validate localization** - Confirm AMCL is providing good pose estimates
4. **Check planner** - Verify planner is receiving goals and attempting to plan
5. **Review parameters** - Check if any navigation parameters changed
6. **Sensor data** - Validate that sensor data is reaching costmap layers
7. **System resources** - Check CPU/memory usage for navigation nodes
8. **Logs** - Examine detailed logs for error messages

**Q4.4:** The robot's balance system frequently intervenes during navigation, causing stops and restarts. How would you analyze and fix this issue?

**Sample Answer:**
Analysis approach:
1. **Balance monitoring** - Log balance metrics during navigation
2. **Trajectory analysis** - Check if planned paths are too aggressive
3. **Control parameters** - Review velocity and acceleration limits
4. **Terrain analysis** - Check if environment is challenging for balance

Solutions:
- Reduce navigation speeds and accelerations
- Smooth planned trajectories for better balance
- Improve terrain assessment in path planning
- Coordinate with balance control system
- Implement balance-aware path planning
- Add buffer time for balance recovery in navigation

## Advanced Application Questions

**Q5.1:** How would you modify the AI-Robot Brain system to work in outdoor environments with varying terrain, weather conditions, and larger navigation distances?

**Sample Answer:**
Modifications needed:
- **Isaac Sim**: Outdoor environments with varying terrain, weather models
- **Perception**: Robust outdoor perception, weather-resistant sensor processing
- **SLAM**: Loop closure for large environments, GPS integration
- **Navigation**: Terrain-aware planning, outdoor-specific safety considerations
- **Hardware**: Weather protection, longer-range sensors, extended power management

**Q5.2:** Design an evaluation framework to measure the success of the AI-Robot Brain system in real-world deployment. What metrics would you track and how would you measure them?

**Sample Answer:**
Key metrics:
- **Navigation success rate**: Percentage of goals reached successfully
- **Time efficiency**: Time taken vs. optimal path time
- **Safety metrics**: Number of safety interventions, near-misses
- **Social acceptance**: Human comfort levels, interaction quality
- **System reliability**: Uptime, failure rates, recovery times
- **Energy efficiency**: Power consumption per navigation task

Measurement approach:
- Log all navigation attempts and outcomes
- Use safety system logs to track interventions
- Conduct human surveys for social metrics
- Monitor system resource usage
- Track maintenance and failure events

This assessment provides comprehensive coverage of the AI-Robot Brain module concepts, testing both theoretical understanding and practical application skills needed for implementing these systems.