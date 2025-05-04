# Path Planning Component

The Path Planning component provides an interactive interface for planning and optimizing robot paths in a 2D environment.

## Features

- Interactive map display with SVG rendering
- Obstacle, zone, and charging station visualization
- Start and goal position selection via click or manual input
- Path planning and optimization
- Map layer toggling
- Path metrics display
- Error handling and loading states

## Usage

```vue
<template>
  <PathPlanning />
</template>

<script>
import PathPlanning from '@/components/PathPlanning.vue'

export default {
  components: {
    PathPlanning
  }
}
</script>
```

## Props

None

## Events

None

## Store Integration

The component integrates with the Vuex store using the `pathPlanning` module. The following state properties are used:

- `robots`: List of available robots
- `selectedRobot`: Currently selected robot ID
- `mapData`: Map data including obstacles, zones, and charging stations
- `startPosition`: Selected start position
- `goalPosition`: Selected goal position
- `currentPath`: Currently planned path
- `showObstacles`: Toggle for obstacle visibility
- `showZones`: Toggle for zone visibility
- `showChargingStations`: Toggle for charging station visibility
- `showPaths`: Toggle for path visibility
- `pathLength`: Length of current path in meters
- `estimatedTime`: Estimated time to complete path in seconds
- `error`: Current error message
- `loading`: Loading state indicator

## API Integration

The component uses the following API endpoints:

- `GET /api/v1/robots`: Fetch available robots
- `GET /api/v1/map`: Fetch map data
- `POST /api/v1/robots/{robotId}/path`: Plan a new path
- `POST /api/v1/robots/{robotId}/path/optimize`: Optimize an existing path
- `POST /api/v1/robots/{robotId}/paths`: Save a path
- `GET /api/v1/robots/{robotId}/paths`: Get saved paths
- `DELETE /api/v1/robots/{robotId}/paths/{pathId}`: Delete a saved path
- `POST /api/v1/robots/{robotId}/paths/{pathId}/execute`: Execute a saved path
- `POST /api/v1/robots/{robotId}/stop`: Stop current path execution
- `GET /api/v1/robots/{robotId}/status`: Get robot status
- `GET /api/v1/robots/{robotId}/status/stream`: Stream robot status updates

## Styling

The component uses CSS modules for styling. The following classes are available:

- `.path-planning`: Main container
- `.map-container`: Map display container
- `.map-canvas`: SVG canvas
- `.obstacle`: Obstacle elements
- `.zone`: Zone elements
- `.charging-station`: Charging station elements
- `.path`: Path line
- `.start-marker`: Start position marker
- `.goal-marker`: Goal position marker
- `.controls`: Control panel container
- `.control-group`: Group of related controls
- `.robot-select`: Robot selection dropdown
- `.position-input`: Position input fields
- `.button-group`: Button container
- `.plan-btn`: Plan path button
- `.optimize-btn`: Optimize path button
- `.clear-btn`: Clear path button
- `.map-layers`: Map layer controls
- `.layer-toggle`: Layer toggle checkbox
- `.path-info`: Path information display
- `.path-metrics`: Path metrics container
- `.metric`: Individual metric display
- `.metric-label`: Metric label
- `.metric-value`: Metric value
- `.error-message`: Error message display

## Responsive Design

The component is responsive and adapts to different screen sizes:

- On desktop: Map and controls are displayed side by side
- On mobile: Controls are displayed below the map and stick to the bottom

## Testing

The component includes comprehensive tests covering:

- Initial rendering
- Data loading
- User interactions
- Path planning
- Path optimization
- Map layer toggling
- Error handling
- Button state management

## Dependencies

- Vue 3
- Vuex 4
- Axios
- Jest
- Vue Test Utils

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest) 