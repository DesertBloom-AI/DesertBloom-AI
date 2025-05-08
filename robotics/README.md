# DesertBloom AI Robotics System

This directory contains the robotics control system for DesertBloom AI, which manages autonomous robots for desert agriculture operations.

## System Architecture

The robotics system consists of the following components:

1. **Robot Control Service** (`backend\api\v1\services\robotics_service.py`)
   - Manages robot states and task execution
   - Handles communication with ROS2 nodes
   - Provides API endpoints for robot control

2. **ROS2 Nodes** (`robotics\nodes\`)
   - `robot_control.py`: Main control node for robot operations
   - Handles low-level robot control and sensor data

3. **Configuration** (`robotics\config\`)
   - `robot_config.json`: Robot specifications and capabilities
   - Defines robot types, sensors, and operational parameters

4. **API Endpoints** (`backend\api\v1\endpoints\robotics.py`)
   - REST API for robot control and monitoring
   - Task management and status updates

5. **Frontend Interface** (`frontend\src\components\RoboticsControl.vue`)
   - Web interface for robot control and monitoring
   - Real-time status updates and task management

## Setup Instructions

1. Install ROS2 dependencies:
   ```bash
   # For Windows
   # Visit https://docs.ros.org/en/foxy/Installation/Windows-Install-Binary.html for installation guide
   
   # For Linux
   sudo apt update
   sudo apt install ros-foxy-desktop
   ```

2. Install Python dependencies:
   ```bash
   pip install -r backend\requirements.txt
   ```

3. Configure robots:
   - Edit `robotics\config\robot_config.json` to match your robot specifications
   - Update sensor configurations and operational parameters

4. Start the system:
   ```bash
   # Start ROS2 nodes
   ros2 run desertbloom_robotics robot_control

   # Start backend API
   cd backend
   uvicorn main:app --reload

   # Start frontend
   cd frontend
   npm run serve
   ```

## Robot Types

1. **Planter Robot**
   - Capabilities: Planting, soil analysis
   - Sensors: GPS, LiDAR, camera, soil sensor
   - Tools: Planter arm, seed dispenser

2. **Waterer Robot**
   - Capabilities: Watering, moisture monitoring
   - Sensors: GPS, moisture sensor, flow meter
   - Tools: Watering arm, nozzle

3. **Monitor Robot**
   - Capabilities: Environment monitoring, data collection
   - Sensors: GPS, camera, temperature, humidity, wind speed
   - Tools: Sampling arm, data logger

## Task Types

1. **Planting Tasks**
   - Parameters: Quantity, species, spacing
   - Execution: Position-based planting with soil analysis

2. **Watering Tasks**
   - Parameters: Water amount, duration, frequency
   - Execution: Area-based watering with moisture monitoring

3. **Monitoring Tasks**
   - Parameters: Interval, duration, sensors
   - Execution: Position-based data collection

## Safety Features

1. **Emergency Stop**
   - Immediate robot halt
   - Status notification
   - Manual override capability

2. **Battery Management**
   - Low battery warnings
   - Automatic return to charging
   - Battery health monitoring

3. **Collision Avoidance**
   - LiDAR-based obstacle detection
   - Emergency stop on collision risk
   - Safe path planning

## API Documentation

See the API documentation at `/api/docs` for detailed endpoint information.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 