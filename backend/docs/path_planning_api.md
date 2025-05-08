# Path Planning API Documentation

## Overview
The Path Planning API provides endpoints for planning and optimizing robot paths in the DesertBloom AI system. It handles path generation, optimization, and collision detection for autonomous robots.

## Endpoints

### Plan Path
```
POST /api/v1/robots/{robot_id}/path
```

Plan a path for a robot from start to goal position.

**Request Body:**
```json
{
  "start": {
    "x": 0.0,
    "y": 0.0
  },
  "goal": {
    "x": 100.0,
    "y": 100.0
  }
}
```

**Response:**
```json
[
  {
    "x": 0.0,
    "y": 0.0
  },
  {
    "x": 10.0,
    "y": 10.0
  },
  ...
]
```

### Optimize Path
```
POST /api/v1/robots/{robot_id}/path/optimize
```

Optimize an existing path for smoother movement.

**Request Body:**
```json
[
  {
    "x": 0.0,
    "y": 0.0
  },
  {
    "x": 50.0,
    "y": 50.0
  },
  {
    "x": 100.0,
    "y": 100.0
  }
]
```

**Response:**
```json
[
  {
    "x": 0.0,
    "y": 0.0,
    "velocity": 0.0
  },
  {
    "x": 10.0,
    "y": 10.0,
    "velocity": 0.5
  },
  ...
]
```

### Check Collision
```
POST /api/v1/robots/{robot_id}/collision
```

Check if a position would cause a collision.

**Request Body:**
```json
{
  "x": 50.0,
  "y": 50.0
}
```

**Response:**
```json
{
  "has_collision": true
}
```

### Get Map Zones
```
GET /api/v1/map/zones
```

Get all zones in the map.

**Response:**
```json
[
  {
    "id": "planting_zone_1",
    "type": "planting",
    "area": {
      "x1": 50,
      "y1": 50,
      "x2": 250,
      "y2": 250
    },
    "soil_type": "sandy",
    "water_availability": "high"
  },
  ...
]
```

### Get Map Obstacles
```
GET /api/v1/map/obstacles
```

Get all obstacles in the map.

**Response:**
```json
[
  {
    "type": "rectangle",
    "x1": 100,
    "y1": 100,
    "x2": 200,
    "y2": 200,
    "description": "Building 1"
  },
  {
    "type": "point",
    "x": 500,
    "y": 500,
    "radius": 50,
    "description": "Tree 1"
  },
  ...
]
```

### Get Charging Stations
```
GET /api/v1/map/charging_stations
```

Get all charging stations in the map.

**Response:**
```json
[
  {
    "id": "station_1",
    "position": {
      "x": 50,
      "y": 50
    },
    "capacity": 4,
    "available_slots": 4
  },
  ...
]
```

### Get Predefined Paths
```
GET /api/v1/map/paths
```

Get all predefined paths in the map.

**Response:**
```json
[
  {
    "id": "main_path_1",
    "points": [
      {"x": 0, "y": 0},
      {"x": 500, "y": 0},
      {"x": 500, "y": 500},
      {"x": 1000, "y": 500}
    ],
    "width": 2.0,
    "priority": "high"
  },
  ...
]
```

## Error Responses

All endpoints may return the following error responses:

- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

Example error response:
```json
{
  "detail": "Error message describing the issue"
}
```

## Notes

- All coordinates are in meters
- The map origin (0,0) is at the bottom-left corner
- Positive x is right, positive y is up
- Robot dimensions and specifications are defined in the robot configuration
- Path planning takes into account robot dimensions, turning radius, and maximum speed
- Collision detection includes both static and dynamic obstacles 