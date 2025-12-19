---
title: Humanoid Robot Movement Execution with Nav2
sidebar_position: 2
---

# Humanoid Robot Movement Execution with Nav2

This tutorial covers the practical aspects of executing navigation commands with Nav2 on humanoid robots. You'll learn how to implement safe movement execution, handle humanoid-specific challenges, and integrate with balance control systems.

## Prerequisites

Before starting this tutorial, you should have:
- Completed the Nav2 configuration tutorial
- A humanoid robot with working Nav2 setup
- Balance control system integrated with ROS2
- Understanding of humanoid kinematics and constraints

## Step 1: Set Up Movement Execution Infrastructure

### Velocity Command Interface
Humanoid robots typically require specialized velocity command interfaces:

```python
#!/usr/bin/env python3
# humanoid_velocity_controller.py

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
import numpy as np

class HumanoidVelocityController(Node):
    def __init__(self):
        super().__init__('humanoid_velocity_controller')

        # Subscribers
        self.cmd_vel_sub = self.create_subscription(
            Twist, 'cmd_vel_in', self.cmd_vel_callback, 10)
        self.odom_sub = self.create_subscription(
            Odometry, 'odom', self.odom_callback, 10)
        self.imu_sub = self.create_subscription(
            Imu, 'imu/data', self.imu_callback, 10)

        # Publishers
        self.cmd_vel_pub = self.create_publisher(
            Twist, 'cmd_vel_out', 10)

        # Parameters
        self.max_linear_vel = self.declare_parameter(
            'max_linear_velocity', 0.4).value
        self.max_angular_vel = self.declare_parameter(
            'max_angular_velocity', 0.4).value
        self.min_linear_vel = self.declare_parameter(
            'min_linear_velocity', 0.1).value  # For balance
        self.balance_threshold = self.declare_parameter(
            'balance_threshold', 0.1).value

        # State variables
        self.current_twist = Twist()
        self.current_balance = 0.0
        self.is_balanced = True

        # Timer for safety checks
        self.safety_timer = self.create_timer(0.1, self.safety_check)

    def cmd_vel_callback(self, msg):
        """Process incoming velocity commands with humanoid constraints"""
        # Apply humanoid-specific constraints
        constrained_twist = Twist()

        # Linear velocity constraints
        linear_speed = np.sqrt(msg.linear.x**2 + msg.linear.y**2)
        if linear_speed > self.max_linear_vel:
            scale = self.max_linear_vel / linear_speed
            constrained_twist.linear.x = msg.linear.x * scale
            constrained_twist.linear.y = msg.linear.y * scale
        else:
            constrained_twist.linear.x = msg.linear.x
            constrained_twist.linear.y = msg.linear.y

        # Ensure minimum linear velocity for balance (if moving)
        if linear_speed > 0.01 and np.sqrt(constrained_twist.linear.x**2 + constrained_twist.linear.y**2) < self.min_linear_vel:
            scale = self.min_linear_vel / linear_speed
            constrained_twist.linear.x = msg.linear.x * scale
            constrained_twist.linear.y = msg.linear.y * scale

        # Angular velocity constraints
        constrained_twist.angular.z = max(-self.max_angular_vel,
                                         min(self.max_angular_vel, msg.angular.z))

        # Check balance before publishing
        if self.is_balanced:
            self.cmd_vel_pub.publish(constrained_twist)
            self.current_twist = constrained_twist
        else:
            # Emergency stop if not balanced
            emergency_stop = Twist()
            self.cmd_vel_pub.publish(emergency_stop)
            self.get_logger().warn("Emergency stop: Robot not balanced")

    def odom_callback(self, msg):
        """Process odometry data"""
        # Update position and velocity estimates
        pass

    def imu_callback(self, msg):
        """Process IMU data for balance monitoring"""
        # Calculate balance metric from IMU data
        # This is a simplified example
        self.current_balance = abs(msg.linear_acceleration.x) + abs(msg.linear_acceleration.y)
        self.is_balanced = self.current_balance < self.balance_threshold

    def safety_check(self):
        """Periodic safety checks"""
        if not self.is_balanced:
            # Publish emergency stop
            emergency_stop = Twist()
            self.cmd_vel_pub.publish(emergency_stop)
            self.get_logger().error("Balance lost - emergency stop activated")

def main(args=None):
    rclpy.init(args=args)
    controller = HumanoidVelocityController()
    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Step Execution Interface
For humanoid robots, you may need a step-by-step execution interface:

```python
#!/usr/bin/env python3
# humanoid_step_executor.py

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Pose, Point
from builtin_interfaces.msg import Duration
import time

class HumanoidStepExecutor(Node):
    def __init__(self):
        super().__init__('humanoid_step_executor')

        # Publishers for step execution
        self.step_command_pub = self.create_publisher(
            String, 'step_command', 10)

        # Service clients for balance and step planning
        self.balance_client = self.create_client(
            String, 'balance_check')
        self.step_planner_client = self.create_client(
            String, 'step_plan')

        # Movement state
        self.current_step = 0
        self.is_moving = False
        self.balance_ok = True

    def execute_path_step_by_step(self, path):
        """Execute a path by planning and executing individual steps"""
        self.is_moving = True

        for i in range(len(path.poses) - 1):
            if not self.is_moving:
                break

            # Plan next step
            step_command = self.plan_next_step(
                path.poses[i], path.poses[i+1])

            if step_command is None:
                self.get_logger().error("Cannot plan next step, stopping")
                break

            # Check balance before executing step
            if not self.check_balance():
                self.get_logger().warn("Balance check failed, pausing")
                time.sleep(1.0)
                continue

            # Execute the step
            self.execute_step(step_command)

            # Wait for step completion
            time.sleep(1.0)  # Adjust based on step duration

        self.is_moving = False

    def plan_next_step(self, current_pose, target_pose):
        """Plan the next step based on current and target poses"""
        # This would integrate with your step planner
        # For now, return a simple step command
        step_cmd = String()
        step_cmd.data = f"step_to {target_pose.position.x} {target_pose.position.y}"
        return step_cmd

    def execute_step(self, step_command):
        """Execute a single step"""
        self.step_command_pub.publish(step_command)
        self.current_step += 1

    def check_balance(self):
        """Check if robot is in balance state"""
        # Call balance check service
        if self.balance_client.wait_for_service(timeout_sec=1.0):
            request = String.Request()
            request.data = "check_balance"
            future = self.balance_client.call_async(request)
            rclpy.spin_until_future_complete(self, future)
            return future.result().data == "balanced"
        return False

def main(args=None):
    rclpy.init(args=args)
    executor = HumanoidStepExecutor()
    rclpy.spin(executor)
    executor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Step 2: Implement Navigation Monitoring

### Navigation State Monitor
Create a monitor to track navigation execution:

```python
#!/usr/bin/env python3
# navigation_monitor.py

import rclpy
from rclpy.node import Node
from action_msgs.msg import GoalStatus
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import Imu, JointState
import time

class NavigationMonitor(Node):
    def __init__(self):
        super().__init__('navigation_monitor')

        # Action client for navigation
        self.nav_client = rclpy.action.ActionClient(
            self, NavigateToPose, 'navigate_to_pose')

        # Subscribers for monitoring
        self.imu_sub = self.create_subscription(
            Imu, 'imu/data', self.imu_callback, 10)
        self.joint_state_sub = self.create_subscription(
            JointState, 'joint_states', self.joint_state_callback, 10)

        # Publishers for status
        self.status_pub = self.create_publisher(
            String, 'navigation_status', 10)

        # State variables
        self.balance_threshold = 0.15
        self.current_balance = 0.0
        self.navigation_active = False
        self.last_status_time = time.time()

    def send_navigation_goal(self, x, y, theta):
        """Send a navigation goal to Nav2"""
        while not self.nav_client.wait_for_server():
            self.get_logger().info('Waiting for navigation server...')

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.orientation.z = theta  # Simplified orientation

        self.navigation_active = True
        future = self.nav_client.send_goal_async(goal_msg)
        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """Handle navigation goal response"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            self.navigation_active = False
            return

        self.get_logger().info('Goal accepted')
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        """Handle navigation result"""
        result = future.result().result
        self.get_logger().info(f'Navigation result: {result}')
        self.navigation_active = False

    def imu_callback(self, msg):
        """Monitor balance from IMU data"""
        # Calculate balance metric
        self.current_balance = abs(msg.linear_acceleration.x) + abs(msg.linear_acceleration.y)

        # Check for balance issues during navigation
        if self.navigation_active and self.current_balance > self.balance_threshold:
            self.get_logger().warn(f"Balance issue detected: {self.current_balance}")

    def joint_state_callback(self, msg):
        """Monitor joint states for abnormal behavior"""
        # Check for joint limits or unusual positions
        pass

    def monitor_navigation(self):
        """Main monitoring loop"""
        current_time = time.time()
        if current_time - self.last_status_time > 1.0:  # Update every second
            status_msg = String()
            status_msg.data = f"Balance: {self.current_balance:.3f}, Active: {self.navigation_active}"
            self.status_pub.publish(status_msg)
            self.last_status_time = current_time

def main(args=None):
    rclpy.init(args=args)
    monitor = NavigationMonitor()

    # Example: Send a navigation goal
    monitor.send_navigation_goal(1.0, 1.0, 0.0)

    # Spin with monitoring
    while rclpy.ok():
        rclpy.spin_once(monitor)
        monitor.monitor_navigation()

    monitor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Step 3: Create Navigation Safety System

### Safety Monitor Node
Implement a safety system to monitor navigation execution:

```python
#!/usr/bin/env python3
# safety_monitor.py

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan, Imu
from std_msgs.msg import Bool
import numpy as np

class SafetyMonitor(Node):
    def __init__(self):
        super().__init__('safety_monitor')

        # Subscribers
        self.cmd_vel_sub = self.create_subscription(
            Twist, 'cmd_vel_out', self.cmd_vel_callback, 10)
        self.scan_sub = self.create_subscription(
            LaserScan, 'scan', self.scan_callback, 10)
        self.imu_sub = self.create_subscription(
            Imu, 'imu/data', self.imu_callback, 10)

        # Publishers
        self.safety_cmd_pub = self.create_publisher(
            Twist, 'safety_cmd_vel', 10)
        self.emergency_stop_pub = self.create_publisher(
            Bool, 'emergency_stop', 10)

        # Parameters
        self.safety_distance = self.declare_parameter(
            'safety_distance', 0.5).value
        self.balance_threshold = self.declare_parameter(
            'balance_threshold', 0.2).value
        self.velocity_threshold = self.declare_parameter(
            'velocity_threshold', 0.6).value

        # State variables
        self.current_twist = Twist()
        self.current_scan = None
        self.current_balance = 0.0
        self.emergency_active = False

        # Timer for safety checks
        self.safety_timer = self.create_timer(0.05, self.safety_check)

    def cmd_vel_callback(self, msg):
        """Monitor commanded velocities"""
        self.current_twist = msg

    def scan_callback(self, msg):
        """Process laser scan for obstacle detection"""
        self.current_scan = msg

    def imu_callback(self, msg):
        """Monitor balance from IMU"""
        self.current_balance = abs(msg.linear_acceleration.x) + abs(msg.linear_acceleration.y)

    def safety_check(self):
        """Perform safety checks"""
        if self.emergency_active:
            return

        # Check for obstacles
        if self.current_scan and self.check_obstacle_danger():
            self.activate_emergency_stop("Obstacle too close")
            return

        # Check for balance issues
        if self.current_balance > self.balance_threshold:
            self.activate_emergency_stop("Balance compromised")
            return

        # Check for excessive velocities
        linear_speed = np.sqrt(self.current_twist.linear.x**2 +
                              self.current_twist.linear.y**2)
        if linear_speed > self.velocity_threshold:
            self.activate_emergency_stop("Excessive velocity")
            return

    def check_obstacle_danger(self):
        """Check if obstacles are too close"""
        if not self.current_scan:
            return False

        # Check for obstacles within safety distance
        min_range = min(self.current_scan.ranges)
        return min_range < self.safety_distance

    def activate_emergency_stop(self, reason):
        """Activate emergency stop"""
        self.emergency_active = True
        self.get_logger().error(f"EMERGENCY STOP: {reason}")

        # Publish emergency stop command
        stop_cmd = Twist()
        self.safety_cmd_pub.publish(stop_cmd)

        # Publish emergency stop flag
        emergency_msg = Bool()
        emergency_msg.data = True
        self.emergency_stop_pub.publish(emergency_msg)

def main(args=None):
    rclpy.init(args=args)
    safety_monitor = SafetyMonitor()
    rclpy.spin(safety_monitor)
    safety_monitor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Step 4: Test Navigation Execution

### Basic Navigation Test Script
Create a test script to execute navigation:

```python
#!/usr/bin/env python3
# test_navigation.py

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
import time

class NavigationTest(Node):
    def __init__(self):
        super().__init__('navigation_test')
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

    def send_goal(self, x, y, theta):
        """Send a navigation goal"""
        # Wait for action server
        while not self.nav_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().info('Waiting for navigation server...')

        # Create goal
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y

        # Set orientation (simplified)
        import math
        goal_msg.pose.pose.orientation.z = math.sin(theta / 2.0)
        goal_msg.pose.pose.orientation.w = math.cos(theta / 2.0)

        # Send goal
        self.get_logger().info(f'Sending goal to ({x}, {y})')
        send_goal_future = self.nav_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)

        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """Handle goal response"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        """Handle result"""
        result = future.result().result
        self.get_logger().info(f'Result: {result}')
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        """Handle feedback"""
        feedback = feedback_msg.feedback
        # Process feedback as needed
        pass

def main(args=None):
    rclpy.init(args=args)
    test_node = NavigationTest()

    # Send a test goal
    test_node.send_goal(2.0, 2.0, 0.0)  # Navigate to (2,2) with 0 rotation

    # Spin until completion
    rclpy.spin(test_node)

if __name__ == '__main__':
    main()
```

## Step 5: Advanced Movement Execution Features

### Social Navigation Execution
Implement social navigation behaviors:

```python
#!/usr/bin/env python3
# social_navigation_executor.py

import rclpy
from rclpy.node import Node
from visualization_msgs.msg import MarkerArray
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
import numpy as np

class SocialNavigationExecutor(Node):
    def __init__(self):
        super().__init__('social_navigation_executor')

        # Subscribers
        self.human_detection_sub = self.create_subscription(
            MarkerArray, 'human_detections', self.human_detection_callback, 10)
        self.cmd_vel_sub = self.create_subscription(
            Twist, 'cmd_vel_in', self.cmd_vel_callback, 10)

        # Publishers
        self.social_cmd_pub = self.create_publisher(
            Twist, 'social_cmd_vel', 10)
        self.social_space_pub = self.create_publisher(
            Float32, 'social_space_distance', 10)

        # Parameters
        self.personal_space_radius = self.declare_parameter(
            'personal_space_radius', 0.8).value
        self.social_space_radius = self.declare_parameter(
            'social_space_radius', 1.2).value
        self.max_avoidance_force = self.declare_parameter(
            'max_avoidance_force', 1.0).value

        # State variables
        self.human_positions = []
        self.current_cmd = Twist()
        self.social_factor = 1.0

    def human_detection_callback(self, msg):
        """Process human detections"""
        self.human_positions = []
        for marker in msg.markers:
            pos = marker.pose.position
            self.human_positions.append(np.array([pos.x, pos.y]))

    def cmd_vel_callback(self, msg):
        """Process incoming velocity commands with social awareness"""
        self.current_cmd = msg

        # Calculate social adjustments
        adjusted_cmd = self.apply_social_adjustments(msg)
        self.social_cmd_pub.publish(adjusted_cmd)

    def apply_social_adjustments(self, original_cmd):
        """Apply social navigation adjustments to velocity command"""
        if not self.human_positions:
            return original_cmd

        # Calculate repulsive forces from humans
        repulsive_force = np.array([0.0, 0.0])

        for human_pos in self.human_positions:
            # Calculate distance to human
            robot_pos = np.array([0.0, 0.0])  # Relative to robot
            distance = np.linalg.norm(human_pos - robot_pos)

            if distance < self.social_space_radius:
                # Calculate repulsive direction
                direction = robot_pos - human_pos
                direction = direction / np.linalg.norm(direction) if np.linalg.norm(direction) > 0 else np.array([0,0])

                # Calculate force magnitude (inverse square law)
                force_magnitude = min(self.max_avoidance_force,
                                    (self.social_space_radius - distance) / self.social_space_radius)
                repulsive_force += direction * force_magnitude

        # Apply adjustments to command
        adjusted_cmd = Twist()
        adjusted_cmd.linear.x = max(0.0, original_cmd.linear.x - repulsive_force[0] * 0.1)
        adjusted_cmd.linear.y = original_cmd.linear.y - repulsive_force[1] * 0.1
        adjusted_cmd.angular.z = original_cmd.angular.z  # Keep original rotation

        # Ensure minimum forward speed for balance
        if adjusted_cmd.linear.x < 0.1 and original_cmd.linear.x > 0.05:
            adjusted_cmd.linear.x = 0.1

        return adjusted_cmd

def main(args=None):
    rclpy.init(args=args)
    executor = SocialNavigationExecutor()
    rclpy.spin(executor)
    executor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Step 6: Execute and Monitor Navigation

### Complete Navigation Execution Example
Now put everything together in a complete execution example:

```bash
# Launch sequence for complete navigation execution
# 1. Start the robot drivers
ros2 launch your_robot_bringup robot.launch.py

# 2. Start Nav2 with humanoid configuration
ros2 launch nav2_bringup navigation_launch.py \
  params_file:=/path/to/nav2_params_humanoid.yaml

# 3. Start the safety monitor
ros2 run your_package safety_monitor.py

# 4. Start the velocity controller
ros2 run your_package humanoid_velocity_controller.py

# 5. Execute a navigation command
ros2 run your_package test_navigation.py
```

## Step 7: Troubleshooting Movement Execution

### Common Execution Issues and Solutions

**Issue: Robot stops unexpectedly during navigation**
- **Cause**: Balance system intervention or safety monitor activation
- **Solution**: Check balance controller parameters, increase safety margins

**Issue: Navigation is too slow**
- **Cause**: Conservative velocity parameters
- **Solution**: Gradually increase velocity limits while monitoring balance

**Issue: Robot cannot navigate around obstacles**
- **Cause**: Insufficient local planning or sensor coverage
- **Solution**: Check local costmap configuration and sensor placement

**Issue: Path following is inaccurate**
- **Cause**: Odometry drift or controller tuning
- **Solution**: Verify odometry accuracy and tune controller parameters

### Performance Monitoring
Monitor key metrics during execution:

```bash
# Monitor navigation performance
ros2 run nav2_util navigation_metrics

# Check TF tree for issues
ros2 run tf2_tools view_frames

# Monitor specific topics
ros2 topic hz /cmd_vel_out
ros2 topic hz /odom
ros2 topic echo /navigation_status
```

## Step 8: Validation and Testing

### Testing Protocol
1. **Static Tests**: Test balance in stationary positions
2. **Simple Motion**: Test basic forward/backward movement
3. **Turning Tests**: Test rotation capabilities
4. **Obstacle Avoidance**: Test local planning with obstacles
5. **Long-term Navigation**: Test extended navigation sessions

### Safety Validation
- Test emergency stop procedures
- Validate safety system responses
- Verify fallback behaviors
- Confirm human safety protocols

## Best Practices for Movement Execution

### Safety First
- Always have safety personnel during testing
- Implement multiple safety layers
- Test emergency procedures regularly
- Monitor robot state continuously

### Performance Optimization
- Start with conservative parameters
- Gradually increase performance parameters
- Monitor balance and stability metrics
- Validate in controlled environments first

### Integration Testing
- Test with complete perception pipeline
- Validate sensor fusion effectiveness
- Test in various environmental conditions
- Verify social navigation behaviors

## Next Steps

Continue learning about performance optimization and advanced navigation techniques to enhance your humanoid robot's navigation capabilities. Consider implementing learning-based approaches for improved navigation in complex environments.