import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose, Twist
from sensor_msgs.msg import BatteryState, NavSatFix
from std_msgs.msg import String
import json
import time

class RobotControlNode(Node):
    def __init__(self, robot_id):
        super().__init__(f'robot_control_{robot_id}')
        
        # Load robot configuration
        with open('robotics/config/robot_config.json') as f:
            self.config = json.load(f)['robots'][robot_id]
        
        # Initialize publishers
        self.cmd_vel_pub = self.create_publisher(Twist, f'/{robot_id}/cmd_vel', 10)
        self.status_pub = self.create_publisher(String, f'/{robot_id}/status', 10)
        
        # Initialize subscribers
        self.pose_sub = self.create_subscription(
            Pose,
            f'/{robot_id}/pose',
            self.pose_callback,
            10
        )
        self.battery_sub = self.create_subscription(
            BatteryState,
            f'/{robot_id}/battery',
            self.battery_callback,
            10
        )
        self.gps_sub = self.create_subscription(
            NavSatFix,
            f'/{robot_id}/gps',
            self.gps_callback,
            10
        )
        
        # Initialize state
        self.current_pose = Pose()
        self.battery_level = 100.0
        self.gps_position = None
        self.current_task = None
        self.status = 'idle'
        
        # Create timer for status updates
        self.timer = self.create_timer(1.0, self.publish_status)

    def pose_callback(self, msg):
        """Handle pose updates"""
        self.current_pose = msg
        self.get_logger().info(f'Updated pose: {msg}')

    def battery_callback(self, msg):
        """Handle battery updates"""
        self.battery_level = msg.percentage * 100
        if self.battery_level < 20.0:
            self.get_logger().warning('Low battery!')

    def gps_callback(self, msg):
        """Handle GPS updates"""
        self.gps_position = {
            'latitude': msg.latitude,
            'longitude': msg.longitude,
            'altitude': msg.altitude
        }

    def publish_status(self):
        """Publish robot status"""
        status_msg = String()
        status_msg.data = json.dumps({
            'robot_id': self.get_name(),
            'status': self.status,
            'battery_level': self.battery_level,
            'current_task': self.current_task,
            'position': {
                'x': self.current_pose.position.x,
                'y': self.current_pose.position.y,
                'z': self.current_pose.position.z
            }
        })
        self.status_pub.publish(status_msg)

    def move_to_position(self, x, y, z):
        """Move robot to specified position"""
        # Calculate required movement
        dx = x - self.current_pose.position.x
        dy = y - self.current_pose.position.y
        dz = z - self.current_pose.position.z
        
        # Create twist message
        twist = Twist()
        twist.linear.x = min(dx, self.config['specifications']['max_speed'])
        twist.linear.y = min(dy, self.config['specifications']['max_speed'])
        twist.linear.z = min(dz, self.config['specifications']['max_speed'])
        
        # Publish movement command
        self.cmd_vel_pub.publish(twist)
        self.status = 'moving'

    def execute_task(self, task):
        """Execute a task"""
        self.current_task = task
        self.status = 'busy'
        
        if task['type'] == 'planting':
            self._execute_planting_task(task)
        elif task['type'] == 'watering':
            self._execute_watering_task(task)
        elif task['type'] == 'monitoring':
            self._execute_monitoring_task(task)

    def _execute_planting_task(self, task):
        """Execute planting task"""
        for i in range(task['quantity']):
            # Move to planting position
            self.move_to_position(
                task['positions'][i]['x'],
                task['positions'][i]['y'],
                task['positions'][i]['z']
            )
            
            # Simulate planting
            time.sleep(2)
            
            # Update status
            self.get_logger().info(f'Planted {i+1}/{task["quantity"]} plants')

    def _execute_watering_task(self, task):
        """Execute watering task"""
        for area in task['areas']:
            # Move to watering position
            self.move_to_position(
                area['x'],
                area['y'],
                area['z']
            )
            
            # Simulate watering
            time.sleep(task['duration'])
            
            # Update status
            self.get_logger().info(f'Watered area at ({area["x"]}, {area["y"]})')

    def _execute_monitoring_task(self, task):
        """Execute monitoring task"""
        for point in task['monitoring_points']:
            # Move to monitoring position
            self.move_to_position(
                point['x'],
                point['y'],
                point['z']
            )
            
            # Simulate data collection
            time.sleep(task['interval'])
            
            # Update status
            self.get_logger().info(f'Collected data at ({point["x"]}, {point["y"]})')

    def emergency_stop(self):
        """Emergency stop the robot"""
        twist = Twist()  # All zeros
        self.cmd_vel_pub.publish(twist)
        self.status = 'emergency_stop'
        self.get_logger().error('Emergency stop activated!')

def main(args=None):
    rclpy.init(args=args)
    
    # Create robot control nodes
    robots = ['planter_001', 'waterer_001', 'monitor_001']
    nodes = [RobotControlNode(robot_id) for robot_id in robots]
    
    try:
        rclpy.spin(nodes[0])  # Spin the first node
    except KeyboardInterrupt:
        pass
    finally:
        for node in nodes:
            node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main() 