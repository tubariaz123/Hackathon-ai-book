---
title: ROS 2 Communication Model
sidebar_label: Communication Model
description: Understanding nodes, topics, services, and basic reply-based controller flow for humanoid robots
---

# ROS 2 Communication Model

## Learning Objectives

By the end of this chapter, you will be able to:
- Explain the core communication concepts in ROS 2: nodes, topics, services, and actions
- Implement basic publisher-subscriber communication patterns
- Create and use services for request-reply communication
- Design a basic reply-based controller flow for humanoid robots
- Understand when to use each communication pattern

## Nodes

In ROS 2, a node is an executable that uses ROS 2 to communicate with other nodes. Nodes are the fundamental building blocks of a ROS 2 system. Each node typically performs a specific task and communicates with other nodes through topics, services, or actions.

For humanoid robots, nodes might include:
- Joint controllers (one per joint or group of joints)
- Sensor processing nodes (camera, IMU, force sensors)
- High-level behavior nodes (walking, grasping, speech)
- Perception nodes (object detection, localization)

### Creating a Node

Nodes are typically implemented as classes that inherit from `rclcpp::Node` (in C++) or `rclpy.Node` (in Python). The node class provides methods for creating publishers, subscribers, services, and other ROS 2 entities.

## Topics and Message Passing

Topics are the primary method for asynchronous, one-way communication in ROS 2. Publishers send messages to topics, and subscribers receive messages from topics. This follows the publish-subscribe pattern where publishers don't know who is subscribed, and subscribers don't know who is publishing.

### Publishers and Subscribers

- **Publishers** create and send messages to a topic
- **Subscribers** receive messages from a topic
- Multiple publishers can publish to the same topic
- Multiple subscribers can subscribe to the same topic

For humanoid robots, topics are ideal for:
- Sensor data (camera images, IMU readings, joint positions)
- Control commands (joint positions, velocities, efforts)
- State information (robot state, battery level, system status)

### Quality of Service (QoS)

QoS settings allow you to configure how messages are delivered:
- **Reliability**: Reliable (all messages delivered) vs. Best Effort (some messages may be dropped)
- **Durability**: Volatile (only new messages) vs. Transient Local (includes old messages for late joiners)
- **History**: Keep all messages vs. Keep only last N messages

## Services

Services provide synchronous, request-response communication. A client sends a request to a service, and the service sends back a response. This is useful when you need to wait for a specific result.

For humanoid robots, services are ideal for:
- Calibration routines
- Mode changes
- Configuration updates
- Complex computations that return a result

## Actions

Actions are a more complex communication pattern that combines the features of topics and services. They're ideal for long-running tasks that need to provide feedback and can be canceled.

For humanoid robots, actions are ideal for:
- Navigation goals
- Complex manipulation tasks
- Walking patterns
- Any task that takes time and needs feedback

## Basic Reply-Based Controller Flow

In humanoid robotics, a common pattern is the reply-based controller flow, where the robot continuously senses its environment, processes the information, and responds with appropriate actions.

### Example Flow for Humanoid Walking Control:

1. **Sensing Phase**: Joint encoders and IMU publish current state to topics
2. **Processing Phase**: Walking controller subscribes to sensor data and computes desired movements
3. **Actuation Phase**: Walking controller publishes commands to joint controllers
4. **Feedback Phase**: Joint controllers may provide feedback through services or actions

### Implementation Example (Pseudocode):

```
class WalkingController:
    def __init__(self):
        # Create subscribers for sensor data
        self.imu_sub = create_subscription(IMU, '/imu/data', self.imu_callback)
        self.joint_state_sub = create_subscription(JointState, '/joint_states', self.joint_callback)

        # Create publishers for control commands
        self.joint_cmd_pub = create_publisher(JointCommand, '/joint_commands')

        # Create timer for control loop
        self.control_timer = create_timer(0.01, self.control_loop)

    def imu_callback(self, msg):
        # Process IMU data
        self.current_imu = msg

    def joint_callback(self, msg):
        # Process joint state data
        self.current_joints = msg

    def control_loop(self):
        # Implement walking algorithm
        commands = self.compute_walking_step(
            self.current_imu,
            self.current_joints
        )

        # Publish commands
        self.joint_cmd_pub.publish(commands)
```

## Code Examples

### C++ Publisher Example

```cpp
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class MinimalPublisher : public rclcpp::Node
{
public:
    MinimalPublisher()
    : Node("minimal_publisher"), count_(0)
    {
        publisher_ = this->create_publisher<std_msgs::msg::String>("/topic", 10);
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(500),
            std::bind(&MinimalPublisher::timer_callback, this)
        );
    }

private:
    void timer_callback()
    {
        auto message = std_msgs::msg::String();
        message.data = "Hello, ROS 2! " + std::to_string(count_++);
        RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
        publisher_->publish(message);
    }
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    size_t count_;
};
```

### Python Subscriber Example

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            '/topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
```

## Exercises

1. Design a communication architecture for a humanoid robot's grasping task. Identify which components would be nodes, what topics they would use, and any services needed.

2. Explain when you would use topics vs. services vs. actions for different humanoid robot behaviors.

3. Implement a simple publisher-subscriber pair in either C++ or Python that could be used for joint state communication in a humanoid robot.

## Summary

The ROS 2 communication model provides flexible and powerful ways to coordinate complex robotic systems like humanoid robots. Understanding nodes, topics, services, and actions allows you to design effective architectures for distributed robot control. The choice of communication pattern depends on the specific requirements of your application: use topics for streaming data, services for request-response interactions, and actions for long-running tasks with feedback.