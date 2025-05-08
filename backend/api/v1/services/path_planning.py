import json
import numpy as np
from typing import List, Dict
from ..schemas.robotics import RobotPosition

class PathPlanningService:
    def __init__(self):
        self.map_data = self._load_map_data()
        self.robot_specs = {
            'width': 0.5,  # meters
            'length': 0.8,  # meters
            'turning_radius': 1.0,  # meters
            'max_speed': 1.0  # meters/second
        }
    
    def _load_map_data(self) -> Dict:
        """Load map data from configuration file"""
        try:
            with open('robotics/config/map_data.json') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading map data: {e}")
            return {
                'map': {'width': 1000, 'height': 1000, 'resolution': 0.5},
                'obstacles': [],
                'zones': [],
                'charging_stations': [],
                'paths': []
            }
    
    def plan_path(self, start: Dict, goal: Dict, robot_id: str) -> List[Dict]:
        """Plan a path from start to goal position"""
        # Convert positions to grid coordinates
        start_grid = self._world_to_grid(start)
        goal_grid = self._world_to_grid(goal)
        
        # Create occupancy grid
        grid = self._create_occupancy_grid()
        
        # Use A* algorithm to find path
        path = self._astar(grid, start_grid, goal_grid)
        
        # Convert path back to world coordinates
        world_path = [self._grid_to_world(p) for p in path]
        
        # Smooth path
        smoothed_path = self._smooth_path(world_path)
        
        return smoothed_path
    
    def optimize_path(self, path: List[Dict], robot_id: str) -> List[Dict]:
        """Optimize an existing path for smoother movement"""
        if not path or len(path) < 3:
            return path
        
        # Apply path smoothing algorithm
        optimized_path = self._smooth_path(path)
        
        # Add velocity profile
        path_with_velocity = self._add_velocity_profile(optimized_path)
        
        return path_with_velocity
    
    def check_collision(self, position: Dict, robot_id: str) -> bool:
        """Check if a position would cause a collision"""
        # Convert position to grid coordinates
        grid_pos = self._world_to_grid(position)
        
        # Get robot dimensions
        robot_width = self.robot_specs['width']
        robot_length = self.robot_specs['length']
        
        # Check collision with obstacles
        for obstacle in self.map_data['obstacles']:
            if obstacle['type'] == 'rectangle':
                if self._check_rectangle_collision(
                    grid_pos,
                    robot_width,
                    robot_length,
                    obstacle
                ):
                    return True
            elif obstacle['type'] == 'point':
                if self._check_circle_collision(
                    grid_pos,
                    robot_width,
                    obstacle
                ):
                    return True
        
        return False
    
    def _create_occupancy_grid(self) -> np.ndarray:
        """Create an occupancy grid from map data"""
        width = self.map_data['map']['width']
        height = self.map_data['map']['height']
        resolution = self.map_data['map']['resolution']
        
        grid_width = int(width / resolution)
        grid_height = int(height / resolution)
        
        grid = np.zeros((grid_height, grid_width))
        
        # Mark obstacles
        for obstacle in self.map_data['obstacles']:
            if obstacle['type'] == 'rectangle':
                x1 = int(obstacle['x1'] / resolution)
                y1 = int(obstacle['y1'] / resolution)
                x2 = int(obstacle['x2'] / resolution)
                y2 = int(obstacle['y2'] / resolution)
                grid[y1:y2, x1:x2] = 1
            elif obstacle['type'] == 'point':
                x = int(obstacle['x'] / resolution)
                y = int(obstacle['y'] / resolution)
                radius = int(obstacle['radius'] / resolution)
                for i in range(-radius, radius + 1):
                    for j in range(-radius, radius + 1):
                        if i*i + j*j <= radius*radius:
                            if 0 <= y + i < grid_height and 0 <= x + j < grid_width:
                                grid[y + i, x + j] = 1
        
        return grid
    
    def _astar(self, grid: np.ndarray, start: tuple, goal: tuple) -> List[tuple]:
        """A* path planning algorithm"""
        # Implementation of A* algorithm
        # This is a simplified version - in practice, you'd want to use a more robust implementation
        from heapq import heappush, heappop
        
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
        neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        
        close_set = set()
        came_from = {}
        gscore = {start: 0}
        fscore = {start: heuristic(start, goal)}
        oheap = []
        heappush(oheap, (fscore[start], start))
        
        while oheap:
            current = heappop(oheap)[1]
            
            if current == goal:
                data = []
                while current in came_from:
                    data.append(current)
                    current = came_from[current]
                return data[::-1]
            
            close_set.add(current)
            for i, j in neighbors:
                neighbor = current[0] + i, current[1] + j
                tentative_g_score = gscore[current] + heuristic(current, neighbor)
                
                if 0 <= neighbor[0] < grid.shape[0]:
                    if 0 <= neighbor[1] < grid.shape[1]:
                        if grid[neighbor[0]][neighbor[1]] == 1:
                            continue
                    else:
                        continue
                else:
                    continue
                
                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue
                
                if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heappush(oheap, (fscore[neighbor], neighbor))
        
        return []
    
    def _smooth_path(self, path: List[Dict]) -> List[Dict]:
        """Smooth a path using spline interpolation"""
        if len(path) < 3:
            return path
        
        # Extract x and y coordinates
        x = [p['x'] for p in path]
        y = [p['y'] for p in path]
        
        # Create parameter t
        t = np.linspace(0, 1, len(path))
        
        # Create new parameter t for interpolation
        t_new = np.linspace(0, 1, len(path) * 2)
        
        # Interpolate x and y coordinates
        from scipy.interpolate import interp1d
        fx = interp1d(t, x, kind='cubic')
        fy = interp1d(t, y, kind='cubic')
        
        x_new = fx(t_new)
        y_new = fy(t_new)
        
        # Create new path
        smoothed_path = []
        for i in range(len(x_new)):
            smoothed_path.append({
                'x': float(x_new[i]),
                'y': float(y_new[i])
            })
        
        return smoothed_path
    
    def _add_velocity_profile(self, path: List[Dict]) -> List[Dict]:
        """Add velocity profile to path"""
        max_speed = self.robot_specs['max_speed']
        max_acceleration = 0.5  # m/s^2
        
        # Calculate distances between points
        distances = []
        for i in range(1, len(path)):
            dx = path[i]['x'] - path[i-1]['x']
            dy = path[i]['y'] - path[i-1]['y']
            distances.append(np.sqrt(dx*dx + dy*dy))
        
        # Calculate velocities
        velocities = [0.0]
        for i in range(1, len(distances)):
            # Simple velocity profile - accelerate to max speed, maintain, then decelerate
            if i < len(distances) / 3:
                # Acceleration phase
                velocities.append(min(velocities[-1] + max_acceleration, max_speed))
            elif i > 2 * len(distances) / 3:
                # Deceleration phase
                velocities.append(max(velocities[-1] - max_acceleration, 0.0))
            else:
                # Constant speed phase
                velocities.append(max_speed)
        
        # Add velocities to path
        for i in range(len(path)):
            path[i]['velocity'] = float(velocities[i])
        
        return path
    
    def _world_to_grid(self, position: Dict) -> tuple:
        """Convert world coordinates to grid coordinates"""
        resolution = self.map_data['map']['resolution']
        return (
            int(position['y'] / resolution),
            int(position['x'] / resolution)
        )
    
    def _grid_to_world(self, position: tuple) -> Dict:
        """Convert grid coordinates to world coordinates"""
        resolution = self.map_data['map']['resolution']
        return {
            'x': position[1] * resolution,
            'y': position[0] * resolution
        }
    
    def _check_rectangle_collision(self, position: tuple, width: float, length: float, obstacle: Dict) -> bool:
        """Check collision with rectangular obstacle"""
        # Convert robot dimensions to grid coordinates
        resolution = self.map_data['map']['resolution']
        robot_width_grid = int(width / resolution)
        robot_length_grid = int(length / resolution)
        
        # Check if robot rectangle overlaps with obstacle rectangle
        return not (
            position[1] + robot_width_grid < obstacle['x1'] or
            position[1] > obstacle['x2'] or
            position[0] + robot_length_grid < obstacle['y1'] or
            position[0] > obstacle['y2']
        )
    
    def _check_circle_collision(self, position: tuple, radius: float, obstacle: Dict) -> bool:
        """Check collision with circular obstacle"""
        # Convert robot radius to grid coordinates
        resolution = self.map_data['map']['resolution']
        robot_radius_grid = int(radius / resolution)
        obstacle_radius_grid = int(obstacle['radius'] / resolution)
        
        # Calculate distance between centers
        dx = position[1] - obstacle['x']
        dy = position[0] - obstacle['y']
        distance = np.sqrt(dx*dx + dy*dy)
        
        # Check if distance is less than sum of radii
        return distance < (robot_radius_grid + obstacle_radius_grid) 