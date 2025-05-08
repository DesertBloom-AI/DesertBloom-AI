# Path Planning Component Documentation

## Overview
The Path Planning component is a crucial part of the DesertBloom AI system that enables autonomous robot navigation in the agricultural environment. It provides an interactive interface for planning and optimizing robot paths while avoiding obstacles and respecting operational zones.

## Features

### Interactive Map
- SVG-based map visualization
- Real-time path rendering
- Obstacle and zone display
- Charging station markers
- Start and goal position selection

### Path Planning
- A* algorithm implementation
- Obstacle avoidance
- Zone awareness
- Optimal path generation
- Path smoothing and optimization

### User Interface
- Robot selection
- Position input
- Map layer toggling
- Path metrics display
- Clear and reset functionality

## Component Structure

### Files
- `PathPlanning.vue` - Main component file
- `PathPlanning.css` - Component styles
- `path_planning.spec.js` - Unit tests

### Dependencies
- Vue.js 3
- Axios
- SVG.js
- A* pathfinding library

## API Integration

### Endpoints
```javascript
// Get available robots
GET /api/v1/robots

// Get map data
GET /api/v1/map/obstacles
GET /api/v1/map/zones
GET /api/v1/map/charging_stations
GET /api/v1/map/paths

// Path planning
POST /api/v1/robots/{robot_id}/path
POST /api/v1/robots/{robot_id}/path/optimize
```

### Request/Response Formats
```typescript
// Path planning request
interface PathPlanningRequest {
  start: {
    x: number;
    y: number;
  };
  goal: {
    x: number;
    y: number;
  };
}

// Path planning response
interface PathPlanningResponse {
  path: Array<{
    x: number;
    y: number;
  }>;
}

// Path optimization request
interface PathOptimizationRequest {
  path: Array<{
    x: number;
    y: number;
  }>;
}

// Path optimization response
interface PathOptimizationResponse {
  path: Array<{
    x: number;
    y: number;
    velocity?: number;
  }>;
}
```

## Usage

### Basic Usage
1. Select a robot from the dropdown
2. Click on the map to set start position
3. Click again to set goal position
4. Click "Plan Path" to generate a path
5. Use "Optimize Path" to smooth the path
6. Toggle map layers as needed

### Advanced Features
- Drag and drop start/goal positions
- Adjust path optimization parameters
- Save and load path configurations
- Export path data for robot execution

## Styling

### CSS Classes
- `.path-planning` - Main container
- `.map-container` - Map wrapper
- `.map-canvas` - SVG canvas
- `.controls` - Control panel
- `.path-info` - Path metrics display
- `.obstacle` - Obstacle styling
- `.zone` - Zone styling
- `.path` - Path line styling

### Customization
The component can be styled using CSS variables:
```css
:root {
  --path-color: #9c27b0;
  --obstacle-color: #f44336;
  --zone-color: #4CAF50;
  --charging-station-color: #2196F3;
}
```

## Testing

### Unit Tests
Run tests with:
```bash
npm run test:unit path_planning.spec.js
```

### Test Coverage
- Component mounting
- API integration
- Path planning logic
- User interactions
- Error handling

## Best Practices

### Performance
- Use SVG for map rendering
- Implement path caching
- Optimize re-renders
- Debounce user interactions

### Error Handling
- Validate input positions
- Handle API errors gracefully
- Provide user feedback
- Implement fallback paths

### Accessibility
- Keyboard navigation
- Screen reader support
- Color contrast compliance
- Focus management

## Troubleshooting

### Common Issues
1. Path not generating
   - Check API connectivity
   - Verify input positions
   - Ensure robot is selected

2. Map not loading
   - Check SVG.js initialization
   - Verify map data format
   - Clear browser cache

3. Performance issues
   - Reduce path complexity
   - Optimize SVG rendering
   - Implement path simplification

## Contributing

### Development
1. Fork the repository
2. Create a feature branch
3. Implement changes
4. Run tests
5. Submit pull request

### Code Style
- Follow Vue.js style guide
- Use TypeScript for type safety
- Document complex logic
- Write unit tests

## License
This component is part of the DesertBloom AI project and is licensed under the MIT License. 