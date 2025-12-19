---
title: Robot Structure with URDF
sidebar_label: Robot Structure with URDF
description: Understanding URDF for humanoid robots and simulation readiness
---

# Robot Structure with URDF

## Learning Objectives

By the end of this chapter, you will be able to:
- Explain what URDF (Unified Robot Description Format) is and its purpose
- Create a valid URDF file for a humanoid robot
- Define joints, links, and kinematic chains in URDF
- Understand simulation readiness requirements for humanoid robots
- Troubleshoot common URDF issues

## What is URDF?

URDF (Unified Robot Description Format) is an XML-based format used in ROS to describe robot models. It defines the physical and kinematic properties of a robot, including its links (rigid parts), joints (connections between links), and other properties like visual and collision geometry.

For humanoid robots, URDF is essential because it:
- Defines the robot's kinematic structure (how parts are connected)
- Provides geometric information for simulation and visualization
- Enables motion planning algorithms to understand the robot's capabilities
- Allows for physics simulation in environments like Gazebo

## Basic URDF Structure

A URDF file contains:
- **Links**: Rigid bodies with properties like mass, inertia, visual geometry, and collision geometry
- **Joints**: Connections between links that define how they can move relative to each other
- **Materials**: Visual properties like color and texture
- **Transmissions**: Information about how actuators connect to joints (for simulation)

## Links

Links represent rigid bodies in the robot. Each link can have:
- **Inertial properties**: Mass, center of mass, and inertia matrix
- **Visual properties**: How the link appears in visualization
- **Collision properties**: How the link interacts in collision detection

### Example Link Definition:

```xml
<link name="base_link">
  <inertial>
    <mass value="1.0" />
    <origin xyz="0 0 0" rpy="0 0 0" />
    <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01" />
  </inertial>
  <visual>
    <origin xyz="0 0 0" rpy="0 0 0" />
    <geometry>
      <cylinder length="0.1" radius="0.1" />
    </geometry>
    <material name="blue">
      <color rgba="0 0 1 1" />
    </material>
  </visual>
  <collision>
    <origin xyz="0 0 0" rpy="0 0 0" />
    <geometry>
      <cylinder length="0.1" radius="0.1" />
    </geometry>
  </collision>
</link>
```

## Joints

Joints define the connection between two links and specify how they can move relative to each other. The main joint types are:
- **Fixed**: No movement allowed (like welding)
- **Revolute**: Rotational movement around an axis (like a hinge)
- **Continuous**: Like revolute but unlimited rotation
- **Prismatic**: Linear sliding movement along an axis
- **Floating**: 6 degrees of freedom (for mobile bases)
- **Planar**: Movement in a plane

### Example Joint Definition:

```xml
<joint name="base_to_wheel" type="continuous">
  <parent link="base_link" />
  <child link="wheel_link" />
  <origin xyz="0.1 0 0" rpy="0 0 0" />
  <axis xyz="0 0 1" />
  <limit effort="100" velocity="1" />
</joint>
```

## Kinematic Chains for Humanoid Robots

Humanoid robots have complex kinematic structures that typically include:
- A torso or base body
- Two arms with shoulders, elbows, and wrists
- Two legs with hips, knees, and ankles
- A head or neck mechanism

The kinematic chain defines how these parts are connected and how movement propagates through the robot.

### Typical Humanoid URDF Structure:

```
base_link (torso)
├── head_link
├── left_upper_arm
│   ├── left_lower_arm
│   └── left_hand
├── right_upper_arm
│   ├── right_lower_arm
│   └── right_hand
├── left_upper_leg
│   ├── left_lower_leg
│   └── left_foot
└── right_upper_leg
    ├── right_lower_leg
    └── right_foot
```

## URDF for Humanoid Robots

When creating URDF for humanoid robots, special considerations include:

### Balance and Stability
- Accurate center of mass calculations
- Proper distribution of mass across links
- Consideration of dynamic effects during movement

### Degrees of Freedom
- Sufficient joints for desired movements
- Proper joint limits to prevent self-collision
- Consideration of workspace constraints

### Sensor Integration
- Mounting points for cameras, IMUs, and other sensors
- Proper placement for optimal sensing

## Simulation Readiness

For a URDF to be simulation-ready, it must include:

### Complete Physical Properties
- Accurate mass and inertia values for all links
- Proper collision geometry that matches visual geometry
- Appropriate friction and damping coefficients

### Proper Joint Definitions
- Correct joint types and limits
- Appropriate effort and velocity limits
- Transmission definitions for actuator simulation

### Gazebo Integration
- Gazebo-specific tags for physics simulation
- Plugin definitions for controllers and sensors
- Material definitions that work well in simulation

### Example Gazebo Integration:

```xml
<gazebo reference="link_name">
  <material>Gazebo/Blue</material>
  <mu1>0.2</mu1>
  <mu2>0.2</mu2>
  <kp>1000000.0</kp>
  <kd>100.0</kd>
</gazebo>
```

## Creating a Humanoid URDF Example

Here's a simplified example of a humanoid robot URDF:

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">
  <!-- Torso -->
  <link name="torso">
    <inertial>
      <mass value="10.0" />
      <origin xyz="0 0 0.3" />
      <inertia ixx="0.5" ixy="0" ixz="0" iyy="0.5" iyz="0" izz="0.2" />
    </inertial>
    <visual>
      <origin xyz="0 0 0.3" />
      <geometry>
        <box size="0.3 0.3 0.6" />
      </geometry>
    </visual>
    <collision>
      <origin xyz="0 0 0.3" />
      <geometry>
        <box size="0.3 0.3 0.6" />
      </geometry>
    </collision>
  </link>

  <!-- Head -->
  <link name="head">
    <inertial>
      <mass value="2.0" />
      <origin xyz="0 0 0" />
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01" />
    </inertial>
    <visual>
      <origin xyz="0 0 0" />
      <geometry>
        <sphere radius="0.15" />
      </geometry>
    </visual>
    <collision>
      <origin xyz="0 0 0" />
      <geometry>
        <sphere radius="0.15" />
      </geometry>
    </collision>
  </link>

  <joint name="torso_to_head" type="fixed">
    <parent link="torso" />
    <child link="head" />
    <origin xyz="0 0 0.6" />
  </joint>

  <!-- Left Arm -->
  <link name="left_upper_arm">
    <inertial>
      <mass value="1.5" />
      <origin xyz="0 0 -0.15" />
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.005" />
    </inertial>
    <visual>
      <origin xyz="0 0 -0.15" />
      <geometry>
        <cylinder length="0.3" radius="0.05" />
      </geometry>
    </visual>
    <collision>
      <origin xyz="0 0 -0.15" />
      <geometry>
        <cylinder length="0.3" radius="0.05" />
      </geometry>
    </collision>
  </link>

  <joint name="left_shoulder" type="revolute">
    <parent link="torso" />
    <child link="left_upper_arm" />
    <origin xyz="0.2 0 0.4" />
    <axis xyz="0 1 0" />
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1" />
  </joint>

  <!-- Additional links and joints would continue in a similar pattern -->
</robot>
```

## Troubleshooting Common URDF Issues

### 1. Self-Collisions
- Check joint limits to prevent parts from intersecting
- Adjust collision geometry to be more conservative
- Use collision filtering to ignore certain pairs

### 2. Kinematic Errors
- Verify that all joints have proper parent-child relationships
- Check that joint axes are correctly defined
- Ensure joint limits are appropriate for the intended motion

### 3. Simulation Instability
- Verify mass and inertia values are physically reasonable
- Check that the center of mass is properly positioned
- Adjust physics parameters like damping and friction

### 4. Visualization Problems
- Ensure visual and collision geometries are properly defined
- Check that origins and rotations are correct
- Verify that materials are properly specified

## Exercises

1. Create a simplified URDF for a bipedal robot with a torso, two legs, and a head. Include proper inertial properties and joint definitions.

2. Identify three potential issues in the following URDF snippet and explain how to fix them:
   ```xml
   <link name="leg">
     <inertial>
       <mass value="0" />
       <inertia ixx="0" ixy="0" ixz="0" iyy="0" iyz="0" izz="0" />
     </inertial>
   </link>
   ```

3. Explain why proper mass distribution is critical for humanoid robot simulation and control.

## Summary

URDF is fundamental to humanoid robotics as it defines the robot's physical structure, enabling simulation, visualization, and motion planning. Creating an accurate URDF requires careful attention to physical properties, proper joint definitions, and simulation readiness. For humanoid robots, the URDF must accurately represent the complex kinematic structure while supporting stable simulation and effective control algorithms.