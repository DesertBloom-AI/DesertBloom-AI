// Robot types
export interface Robot {
  id: string;
  name: string;
  type: string;
  dimensions: {
    width: number;
    length: number;
    height: number;
  };
  capabilities: {
    maxSpeed: number;
    maxAcceleration: number;
    maxDeceleration: number;
    turningRadius: number;
  };
  status: {
    battery: number;
    state: 'idle' | 'moving' | 'charging' | 'error';
    currentPosition?: Position;
    currentPath?: PathPoint[];
  };
}

// Map types
export interface MapDimensions {
  width: number;
  height: number;
}

export interface Position {
  x: number;
  y: number;
}

export interface Area {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
}

export interface Obstacle {
  id?: string;
  type: 'rectangle' | 'circle';
  x?: number;
  y?: number;
  radius?: number;
  x1?: number;
  y1?: number;
  x2?: number;
  y2?: number;
  description?: string;
}

export interface Zone {
  id: string;
  name: string;
  type: string;
  area: {
    x1: number;
    y1: number;
    x2: number;
    y2: number;
  };
}

export interface ChargingStation {
  id: string;
  position: Position;
  type: string;
  status: string;
}

export interface PathPoint extends Position {
  timestamp?: number;
  velocity?: number;
  orientation?: number;
}

export interface Path {
  id: string;
  robot_id: string;
  points: PathPoint[];
  timestamp: string;
}

export interface MapData {
  dimensions: {
    width: number;
    height: number;
  };
  obstacles: Obstacle[];
  zones: Zone[];
  charging_stations?: Array<{ id: string; position: Position; status: string }>;
  paths?: Array<{ id: string; points: PathPoint[] }>;
}

// Path planning types
export interface PathPlanningRequest {
  start: Position;
  goal: Position;
  options?: {
    avoidObstacles?: boolean;
    optimizeForTime?: boolean;
    maxDeviation?: number;
  };
}

export interface PathPlanningResponse {
  path: PathPoint[];
}

export interface PathOptimizationRequest {
  path: PathPoint[];
  options?: {
    maxDeviation?: number;
    smoothness?: number;
  };
}

export interface PathOptimizationResponse {
  path: PathPoint[];
}

// Component state types
export interface PathPlanningState {
  robots: Robot[];
  selectedRobot: string | null;
  mapData: MapData | null;
  startPosition: Position | null;
  goalPosition: Position | null;
  currentPath: PathPoint[] | null;
  showObstacles: boolean;
  showZones: boolean;
  showChargingStations: boolean;
  showPaths: boolean;
  pathLength: number;
  estimatedTime: number;
  error: string | null;
  loading: boolean;
}

// Event types
export interface MapClickEvent {
  position: Position;
  type: 'start' | 'goal';
}

export interface PathMetrics {
  length: number;
  time: number;
  energy: number;
}

// API response types
export interface ApiResponse<T = any> {
  data: T;
}

export interface ErrorResponse {
  error: string;
}

// Utility types
export type MapLayer = 'obstacles' | 'zones' | 'charging_stations' | 'paths';

export interface MapLayerState {
  [key: string]: boolean;
}

export interface PathPlanningConfig {
  robotSpeed: number;
  optimizationLevel: number;
  safetyMargin: number;
  considerBattery: boolean;
}

// Example data types
export interface ExamplePath {
  name: string;
  start: Position;
  goal: Position;
  expected_path: PathPoint[];
}

export interface OptimizationExample {
  name: string;
  input_path: PathPoint[];
  optimized_path: PathPoint[];
}

export interface ExampleData {
  robots: Robot[];
  map: MapData;
  example_paths: ExamplePath[];
  optimization_examples: OptimizationExample[];
} 