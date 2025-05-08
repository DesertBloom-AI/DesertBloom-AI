# Path Planning Component Documentation

## Overview
The Path Planning component provides a user interface for planning and visualizing robot paths in the DesertBloom AI system. It allows users to:
- Select robots and define start/goal positions
- Plan and optimize paths
- Visualize the map with obstacles, zones, and charging stations
- View path information and metrics

## Component Structure

### Template
```vue
<template>
  <div class="path-planning">
    <!-- Map Display -->
    <div class="map-container">
      <canvas ref="mapCanvas" class="map-canvas"></canvas>
    </div>
    
    <!-- Controls -->
    <div class="controls">
      <!-- Robot Selection -->
      <div class="control-group">
        <label>Robot</label>
        <select v-model="selectedRobot">
          <option v-for="robot in robots" :key="robot.id" :value="robot.id">
            {{ robot.id }}
          </option>
        </select>
      </div>
      
      <!-- Position Inputs -->
      <div class="control-group">
        <label>Start Position</label>
        <div class="position-inputs">
          <input type="number" v-model="startPosition.x" placeholder="X">
          <input type="number" v-model="startPosition.y" placeholder="Y">
        </div>
      </div>
      
      <div class="control-group">
        <label>Goal Position</label>
        <div class="position-inputs">
          <input type="number" v-model="goalPosition.x" placeholder="X">
          <input type="number" v-model="goalPosition.y" placeholder="Y">
        </div>
      </div>
      
      <!-- Action Buttons -->
      <button @click="planPath" class="plan-btn">Plan Path</button>
      <button @click="optimizePath" class="optimize-btn">Optimize Path</button>
    </div>
    
    <!-- Path Information -->
    <div class="path-info" v-if="currentPath.length > 0">
      <h3>Path Information</h3>
      <p>Length: {{ pathLength.toFixed(2) }} meters</p>
      <p>Waypoints: {{ currentPath.length }}</p>
      <p>Estimated Time: {{ estimatedTime.toFixed(1) }} minutes</p>
    </div>
    
    <!-- Map Layers -->
    <div class="map-layers">
      <h3>Map Layers</h3>
      <div class="layer-controls">
        <label>
          <input type="checkbox" v-model="showObstacles"> Obstacles
        </label>
        <label>
          <input type="checkbox" v-model="showZones"> Zones
        </label>
        <label>
          <input type="checkbox" v-model="showChargingStations"> Charging Stations
        </label>
        <label>
          <input type="checkbox" v-model="showPaths"> Predefined Paths
        </label>
      </div>
    </div>
  </div>
</template>
```

### Script
```javascript
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'

export default {
  name: 'PathPlanning',
  setup() {
    // Component state
    const mapCanvas = ref(null)
    const ctx = ref(null)
    const selectedRobot = ref('')
    const robots = ref([])
    const startPosition = ref({ x: 0, y: 0 })
    const goalPosition = ref({ x: 0, y: 0 })
    const currentPath = ref([])
    const pathLength = ref(0)
    const estimatedTime = ref(0)
    const showObstacles = ref(true)
    const showZones = ref(true)
    const showChargingStations = ref(true)
    const showPaths = ref(true)
    
    // Map data
    const mapData = ref({
      obstacles: [],
      zones: [],
      chargingStations: [],
      paths: []
    })
    
    // Methods
    const setupCanvas = () => {
      const canvas = mapCanvas.value
      canvas.width = 800
      canvas.height = 800
      ctx.value = canvas.getContext('2d')
    }
    
    const drawMap = () => {
      // Implementation details...
    }
    
    const fetchMapData = async () => {
      // Implementation details...
    }
    
    const fetchRobots = async () => {
      // Implementation details...
    }
    
    const planPath = async () => {
      // Implementation details...
    }
    
    const optimizePath = async () => {
      // Implementation details...
    }
    
    const calculatePathMetrics = () => {
      // Implementation details...
    }
    
    // Lifecycle hooks
    onMounted(() => {
      setupCanvas()
      fetchMapData()
      fetchRobots()
    })
    
    // Watchers
    watch([showObstacles, showZones, showChargingStations, showPaths], () => {
      drawMap()
    })
    
    return {
      // Exposed properties and methods
      mapCanvas,
      selectedRobot,
      robots,
      startPosition,
      goalPosition,
      currentPath,
      pathLength,
      estimatedTime,
      showObstacles,
      showZones,
      showChargingStations,
      showPaths,
      planPath,
      optimizePath
    }
  }
}
```

### Styles
```css
.path-planning {
  padding: 20px;
}

.map-container {
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}

.map-canvas {
  width: 100%;
  height: 600px;
  background-color: #f5f5f5;
}

.controls {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.position-inputs {
  display: flex;
  gap: 10px;
}

.position-inputs input {
  width: 100px;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.plan-btn {
  background-color: #4CAF50;
  color: white;
}

.optimize-btn {
  background-color: #2196F3;
  color: white;
}

.path-info {
  background-color: #f5f5f5;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.map-layers {
  background-color: #f5f5f5;
  padding: 15px;
  border-radius: 8px;
}

.layer-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.layer-controls label {
  display: flex;
  align-items: center;
  gap: 5px;
}
```

## Features

### Map Visualization
- Displays a grid-based map with obstacles, zones, and charging stations
- Supports toggling different map layers
- Shows start and goal positions
- Visualizes planned paths with velocity information

### Path Planning
- Allows selection of robots from the system
- Supports manual input of start and goal positions
- Plans optimal paths using the backend API
- Optimizes paths for smoother movement
- Calculates path metrics (length, waypoints, estimated time)

### User Interface
- Responsive design that works on different screen sizes
- Intuitive controls for path planning
- Visual feedback for path planning operations
- Layer controls for customizing map display

## Usage

1. Select a robot from the dropdown menu
2. Enter start and goal positions (x, y coordinates)
3. Click "Plan Path" to generate a path
4. Optionally click "Optimize Path" to smooth the path
5. Use layer controls to show/hide different map elements
6. View path information in the metrics panel

## Dependencies

- Vue 3
- Axios for API communication
- Font Awesome for icons
- Canvas API for map rendering

## API Integration

The component integrates with the following backend endpoints:
- `GET /api/v1/robots` - Get list of robots
- `POST /api/v1/robots/{robot_id}/path` - Plan path
- `POST /api/v1/robots/{robot_id}/path/optimize` - Optimize path
- `GET /api/v1/map/zones` - Get map zones
- `GET /api/v1/map/obstacles` - Get map obstacles
- `GET /api/v1/map/charging_stations` - Get charging stations
- `GET /api/v1/map/paths` - Get predefined paths 