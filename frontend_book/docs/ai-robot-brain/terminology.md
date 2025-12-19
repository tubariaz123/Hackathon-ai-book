---
title: Terminology and Definitions
sidebar_position: 10
---

# Terminology and Definitions

This document standardizes terminology used throughout the AI-Robot Brain (NVIDIA Isaac™) module to ensure consistency and clarity across all chapters.

## General Robotics Terms

### Navigation
- **Path Planning**: The process of determining a route from start to goal
- **Path Following**: Executing a planned path while maintaining robot stability
- **Local Planning**: Short-term planning for obstacle avoidance
- **Global Planning**: Long-term planning for route finding
- **Waypoint**: A specific point along a planned path

### Perception
- **SLAM**: Simultaneous Localization and Mapping
- **VSLAM**: Visual SLAM using camera sensors
- **VO**: Visual Odometry
- **VIO**: Visual-Inertial Odometry
- **Sensor Fusion**: Combining data from multiple sensors
- **Synthetic Data**: Artificially generated data for training AI models

### Humanoid Robotics
- **Bipedal**: Walking on two legs
- **ZMP (Zero Moment Point)**: Point where ground reaction forces have no moment
- **CoM (Center of Mass)**: The average location of an object's mass
- **Support Polygon**: Area defined by contact points with ground
- **Step Planning**: Planning individual foot placements
- **Gait**: Pattern of leg movements during locomotion

## Isaac Sim Specific Terms

### Simulation Environment
- **USD (Universal Scene Description)**: File format for 3D scenes
- **Omniverse**: NVIDIA's simulation and collaboration platform
- **Asset**: 3D model, texture, or other simulation resource
- **Scene**: Composition of environment, objects, and robots
- **Stage**: The main container for USD content

### Synthetic Data Generation
- **Domain Randomization**: Randomizing visual properties to improve real-world transfer
- **Semantic Segmentation**: Pixel-level labeling of objects in images
- **Instance Segmentation**: Separating individual object instances
- **Annotation**: Labels and metadata for training data
- **Ground Truth**: Accurate reference data from simulation

## Isaac ROS Specific Terms

### Hardware Acceleration
- **CUDA**: NVIDIA's parallel computing platform
- **TensorRT**: NVIDIA's inference optimization library
- **GPU Acceleration**: Using graphics processing units for computation
- **Hardware Video Codecs**: GPU-accelerated video processing
- **Tensor Cores**: Specialized GPU cores for AI operations

### Perception Components
- **Stereo Vision**: Depth estimation using two cameras
- **Stereo Matching**: Finding corresponding points between stereo images
- **Disparity Map**: Depth information from stereo processing
- **Object Detection**: Identifying and localizing objects in images
- **Multi-Object Tracking**: Tracking multiple objects over time

## Nav2 Specific Terms

### Navigation Stack
- **Costmap**: 2D representation of environment with obstacle costs
- **Inflation**: Expanding obstacle areas for safety margins
- **Voxel Layer**: 3D costmap using volumetric elements
- **Behavior Tree**: Tree structure for navigation behaviors
- **Recovery Behavior**: Actions when navigation fails

### Humanoid Navigation
- **Step-Aware Planning**: Path planning considering step constraints
- **Balance Preservation**: Maintaining robot stability during navigation
- **Social Navigation**: Navigation considering human interactions
- **Personal Space**: Area humans prefer to keep clear of robots
- **Social Space**: Area where social interactions occur

## Humanoid-Specific Kinematic Terms

### Joint Definitions
- **DOF (Degrees of Freedom)**: Independent movements a robot can make
- **Hip Joint**: Joint connecting torso to leg (typically 3 DOF)
- **Knee Joint**: Joint in the middle of the leg (typically 1 DOF)
- **Ankle Joint**: Joint connecting leg to foot (typically 2 DOF)
- **Support Leg**: Leg currently bearing weight during walking

### Motion Patterns
- **Single Support**: Walking phase with one foot on ground
- **Double Support**: Walking phase with both feet on ground
- **Swing Phase**: Leg movement phase during walking
- **Stance Phase**: Support phase during walking
- **Gait Cycle**: Complete sequence of walking movements

## Performance and Optimization Terms

### Computational Performance
- **Real-time**: Processing at the rate of real-world events
- **Latency**: Delay between input and output
- **Throughput**: Amount of work completed per unit time
- **Jitter**: Variation in latency
- **Deterministic**: Predictable timing behavior

### Resource Management
- **CPU Utilization**: Percentage of CPU capacity in use
- **GPU Memory**: Memory allocated to graphics processing unit
- **VRAM**: Video random access memory
- **Bandwidth**: Data transfer rate
- **Thermal Management**: Controlling system temperature

## Safety and Reliability Terms

### Safety Systems
- **Emergency Stop**: Immediate halt of robot motion
- **Safety Margin**: Buffer zone for safe operation
- **Fail-Safe**: System behavior when failure occurs
- **Redundancy**: Backup systems for critical functions
- **Fault Tolerance**: Ability to continue operation with failures

### Validation and Testing
- **Simulation Testing**: Testing in virtual environments
- **Hardware-in-the-Loop**: Testing with real hardware components
- **Edge Case**: Unusual scenario that may cause system failure
- **Regression Testing**: Testing to ensure new changes don't break existing functionality
- **Validation**: Confirmation that system meets requirements

## Social Navigation Terms

### Human-Robot Interaction
- **Social Force**: Conceptual force in navigation models
- **Right of Way**: Priority rules for navigation
- **Approach Angle**: Direction humans prefer robots to approach
- **Gaze Behavior**: Robot head orientation during interaction
- **Interaction Readiness**: Robot's preparedness for human interaction

### Social Spaces
- **Intimate Distance**: 0-0.5m (personal interaction)
- **Personal Distance**: 0.5-1.2m (acquaintances)
- **Social Distance**: 1.2-3.6m (social interactions)
- **Public Distance**: 3.6m+ (public speaking)

This terminology guide should be referenced when creating or updating content in the AI-Robot Brain module to maintain consistency and clarity across all chapters.