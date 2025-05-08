import pytest
from api.v1.services.path_planning import PathPlanningService

@pytest.fixture
def path_planning_service():
    return PathPlanningService()

def test_plan_path(path_planning_service):
    # Test path planning with simple start and goal
    start = {'x': 0, 'y': 0}
    goal = {'x': 100, 'y': 100}
    robot_id = 'robot1'
    
    path = path_planning_service.plan_path(start, goal, robot_id)
    
    assert len(path) > 0
    assert path[0]['x'] == start['x']
    assert path[0]['y'] == start['y']
    assert path[-1]['x'] == goal['x']
    assert path[-1]['y'] == goal['y']

def test_optimize_path(path_planning_service):
    # Test path optimization
    path = [
        {'x': 0, 'y': 0},
        {'x': 50, 'y': 50},
        {'x': 100, 'y': 100}
    ]
    robot_id = 'robot1'
    
    optimized_path = path_planning_service.optimize_path(path, robot_id)
    
    assert len(optimized_path) > 0
    assert optimized_path[0]['x'] == path[0]['x']
    assert optimized_path[0]['y'] == path[0]['y']
    assert optimized_path[-1]['x'] == path[-1]['x']
    assert optimized_path[-1]['y'] == path[-1]['y']
    assert 'velocity' in optimized_path[0]

def test_check_collision(path_planning_service):
    # Test collision checking
    position = {'x': 50, 'y': 50}
    robot_id = 'robot1'
    
    has_collision = path_planning_service.check_collision(position, robot_id)
    
    assert isinstance(has_collision, bool)

def test_world_to_grid_conversion(path_planning_service):
    # Test world to grid coordinate conversion
    position = {'x': 100, 'y': 100}
    grid_pos = path_planning_service._world_to_grid(position)
    
    assert isinstance(grid_pos, tuple)
    assert len(grid_pos) == 2
    assert isinstance(grid_pos[0], int)
    assert isinstance(grid_pos[1], int)

def test_grid_to_world_conversion(path_planning_service):
    # Test grid to world coordinate conversion
    grid_pos = (100, 100)
    world_pos = path_planning_service._grid_to_world(grid_pos)
    
    assert isinstance(world_pos, dict)
    assert 'x' in world_pos
    assert 'y' in world_pos
    assert isinstance(world_pos['x'], float)
    assert isinstance(world_pos['y'], float)

def test_path_smoothing(path_planning_service):
    # Test path smoothing
    path = [
        {'x': 0, 'y': 0},
        {'x': 50, 'y': 50},
        {'x': 100, 'y': 100}
    ]
    
    smoothed_path = path_planning_service._smooth_path(path)
    
    assert len(smoothed_path) > len(path)
    assert smoothed_path[0]['x'] == path[0]['x']
    assert smoothed_path[0]['y'] == path[0]['y']
    assert smoothed_path[-1]['x'] == path[-1]['x']
    assert smoothed_path[-1]['y'] == path[-1]['y']

def test_velocity_profile(path_planning_service):
    # Test velocity profile generation
    path = [
        {'x': 0, 'y': 0},
        {'x': 50, 'y': 50},
        {'x': 100, 'y': 100}
    ]
    
    path_with_velocity = path_planning_service._add_velocity_profile(path)
    
    assert len(path_with_velocity) == len(path)
    assert 'velocity' in path_with_velocity[0]
    assert isinstance(path_with_velocity[0]['velocity'], float)
    assert path_with_velocity[0]['velocity'] >= 0
    assert path_with_velocity[0]['velocity'] <= path_planning_service.robot_specs['max_speed']

def test_rectangle_collision(path_planning_service):
    # Test rectangle collision detection
    position = (50, 50)
    width = 1.0
    length = 1.0
    obstacle = {
        'type': 'rectangle',
        'x1': 40,
        'y1': 40,
        'x2': 60,
        'y2': 60
    }
    
    has_collision = path_planning_service._check_rectangle_collision(
        position, width, length, obstacle
    )
    
    assert isinstance(has_collision, bool)

def test_circle_collision(path_planning_service):
    # Test circle collision detection
    position = (50, 50)
    radius = 1.0
    obstacle = {
        'type': 'point',
        'x': 55,
        'y': 55,
        'radius': 10
    }
    
    has_collision = path_planning_service._check_circle_collision(
        position, radius, obstacle
    )
    
    assert isinstance(has_collision, bool) 