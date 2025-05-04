import { Position, PathPoint, PathMetrics, MapData, Obstacle, Zone } from '@/types/path_planning'

/**
 * Calculate the Euclidean distance between two points
 */
export function calculateDistance(point1: Position, point2: Position): number {
  return Math.sqrt(
    Math.pow(point2.x - point1.x, 2) + Math.pow(point2.y - point1.y, 2)
  )
}

/**
 * Calculate the total length of a path
 */
export function calculatePathLength(path: PathPoint[]): number {
  if (path.length < 2) return 0

  let length = 0
  for (let i = 1; i < path.length; i++) {
    length += calculateDistance(path[i - 1], path[i])
  }
  return length
}

/**
 * Calculate estimated time to traverse a path
 */
export function calculatePathTime(path: PathPoint[], robotSpeed: number): number {
  const length = calculatePathLength(path)
  return length / robotSpeed
}

/**
 * Calculate energy consumption for a path
 */
export function calculatePathEnergy(
  path: PathPoint[],
  robotWeight: number,
  terrainFactor: number = 1
): number {
  const length = calculatePathLength(path)
  return length * robotWeight * terrainFactor
}

/**
 * Calculate path metrics (length, time, energy)
 */
export function calculatePathMetrics(
  path: PathPoint[],
  robotSpeed: number,
  robotWeight: number
): PathMetrics {
  return {
    length: calculatePathLength(path),
    time: calculatePathTime(path, robotSpeed),
    energy: calculatePathEnergy(path, robotWeight)
  }
}

/**
 * Check if a point is inside an obstacle
 */
export function isPointInObstacle(point: Position, obstacle: Obstacle): boolean {
  if (obstacle.type === 'rectangle') {
    return (
      point.x >= obstacle.x1! &&
      point.x <= obstacle.x2! &&
      point.y >= obstacle.y1! &&
      point.y <= obstacle.y2!
    )
  } else if (obstacle.type === 'circle') {
    const distance = calculateDistance(point, {
      x: obstacle.x!,
      y: obstacle.y!
    })
    return distance <= obstacle.radius!
  }
  return false
}

/**
 * Check if a point is inside a zone
 */
export function isPointInZone(point: Position, zone: Zone): boolean {
  return (
    point.x >= zone.area.x1 &&
    point.x <= zone.area.x2 &&
    point.y >= zone.area.y1 &&
    point.y <= zone.area.y2
  )
}

/**
 * Check if a path segment intersects with an obstacle
 */
export function doesSegmentIntersectObstacle(
  start: Position,
  end: Position,
  obstacle: Obstacle
): boolean {
  if (obstacle.type === 'rectangle') {
    return lineIntersectsRectangle(start, end, obstacle)
  } else if (obstacle.type === 'circle') {
    return lineIntersectsCircle(start, end, obstacle)
  }
  return false
}

/**
 * Check if a line segment intersects with a rectangle
 */
function lineIntersectsRectangle(
  start: Position,
  end: Position,
  rect: Obstacle
): boolean {
  // Check if either endpoint is inside the rectangle
  if (
    isPointInObstacle(start, rect) ||
    isPointInObstacle(end, rect)
  ) {
    return true
  }

  // Check if the line segment intersects any of the rectangle's edges
  const edges = [
    { start: { x: rect.x1!, y: rect.y1! }, end: { x: rect.x2!, y: rect.y1! } },
    { start: { x: rect.x2!, y: rect.y1! }, end: { x: rect.x2!, y: rect.y2! } },
    { start: { x: rect.x2!, y: rect.y2! }, end: { x: rect.x1!, y: rect.y2! } },
    { start: { x: rect.x1!, y: rect.y2! }, end: { x: rect.x1!, y: rect.y1! } }
  ]

  return edges.some(edge =>
    doLinesIntersect(start, end, edge.start, edge.end)
  )
}

/**
 * Check if a line segment intersects with a circle
 */
function lineIntersectsCircle(
  start: Position,
  end: Position,
  circle: Obstacle
): boolean {
  // Vector from start to end
  const dx = end.x - start.x
  const dy = end.y - start.y

  // Vector from start to circle center
  const fx = circle.x! - start.x
  const fy = circle.y! - start.y

  // Calculate projection of circle center onto line
  const dot = fx * dx + fy * dy
  const lenSq = dx * dx + dy * dy
  const proj = dot / lenSq

  // Find closest point on line to circle center
  let closestX: number
  let closestY: number

  if (proj < 0) {
    closestX = start.x
    closestY = start.y
  } else if (proj > 1) {
    closestX = end.x
    closestY = end.y
  } else {
    closestX = start.x + proj * dx
    closestY = start.y + proj * dy
  }

  // Check if closest point is within circle radius
  const distance = calculateDistance(
    { x: closestX, y: closestY },
    { x: circle.x!, y: circle.y! }
  )
  return distance <= circle.radius!
}

/**
 * Check if two line segments intersect
 */
function doLinesIntersect(
  p1: Position,
  p2: Position,
  p3: Position,
  p4: Position
): boolean {
  const denominator =
    (p4.y - p3.y) * (p2.x - p1.x) - (p4.x - p3.x) * (p2.y - p1.y)

  if (denominator === 0) return false

  const ua =
    ((p4.x - p3.x) * (p1.y - p3.y) - (p4.y - p3.y) * (p1.x - p3.x)) /
    denominator
  const ub =
    ((p2.x - p1.x) * (p1.y - p3.y) - (p2.y - p1.y) * (p1.x - p3.x)) /
    denominator

  return ua >= 0 && ua <= 1 && ub >= 0 && ub <= 1
}

/**
 * Smooth a path using Bezier curves
 */
export function smoothPath(path: PathPoint[], tension: number = 0.5): PathPoint[] {
  if (path.length < 3) return path

  const smoothed: PathPoint[] = []
  smoothed.push(path[0])

  for (let i = 1; i < path.length - 1; i++) {
    const prev = path[i - 1]
    const curr = path[i]
    const next = path[i + 1]

    const cp1 = {
      x: curr.x + (next.x - prev.x) * tension,
      y: curr.y + (next.y - prev.y) * tension
    }

    const cp2 = {
      x: curr.x - (next.x - prev.x) * tension,
      y: curr.y - (next.y - prev.y) * tension
    }

    // Add control points
    smoothed.push(cp1)
    smoothed.push(cp2)
    smoothed.push(curr)
  }

  smoothed.push(path[path.length - 1])
  return smoothed
}

/**
 * Optimize a path for robot movement
 */
export function optimizePath(
  path: PathPoint[],
  robotSpeed: number,
  // const maxAcceleration = ... // (commented out to fix lint error)
): PathPoint[] {
  if (path.length < 3) return path

  const optimized: PathPoint[] = []
  optimized.push({ ...path[0], velocity: 0 })

  for (let i = 1; i < path.length - 1; i++) {
    const prev = path[i - 1]
    const curr = path[i]
    const next = path[i + 1]

    // Calculate curvature
    const angle = calculateAngle(prev, curr, next)
    const curvature = Math.abs(angle) / Math.PI

    // Adjust velocity based on curvature
    const maxSpeed = robotSpeed * (1 - curvature)
    const velocity = Math.min(maxSpeed, robotSpeed)

    optimized.push({ ...curr, velocity })
  }

  optimized.push({ ...path[path.length - 1], velocity: 0 })
  return optimized
}

/**
 * Calculate the angle between three points
 */
function calculateAngle(
  p1: Position,
  p2: Position,
  p3: Position
): number {
  const v1 = { x: p1.x - p2.x, y: p1.y - p2.y }
  const v2 = { x: p3.x - p2.x, y: p3.y - p2.y }

  const dot = v1.x * v2.x + v1.y * v2.y
  const det = v1.x * v2.y - v1.y * v2.x

  return Math.atan2(det, dot)
}

/**
 * Validate a path against map data
 */
export function validatePath(
  path: PathPoint[],
  mapData: MapData
): { valid: boolean; errors: string[] } {
  const errors: string[] = []

  // Check if path is empty
  if (path.length === 0) {
    errors.push('Path is empty')
    return { valid: false, errors }
  }

  // Check if path stays within map boundaries
  for (const point of path) {
    if (
      point.x < 0 ||
      point.x > mapData.dimensions.width ||
      point.y < 0 ||
      point.y > mapData.dimensions.height
    ) {
      errors.push('Path goes outside map boundaries')
      break
    }
  }

  // Check for obstacle collisions
  for (let i = 1; i < path.length; i++) {
    const start = path[i - 1]
    const end = path[i]

    for (const obstacle of mapData.obstacles) {
      if (doesSegmentIntersectObstacle(start, end, obstacle)) {
        errors.push(`Path intersects with obstacle: ${obstacle.description}`)
        break
      }
    }
  }

  return {
    valid: errors.length === 0,
    errors
  }
}

/**
 * Convert path points to SVG path string
 */
export function pathToSVGString(points: PathPoint[]): string {
  if (points.length === 0) return ''

  const [first, ...rest] = points
  let path = `M ${first.x} ${first.y}`

  for (const point of rest) {
    path += ` L ${point.x} ${point.y}`
  }

  return path
}

/**
 * Convert SVG path string to points
 */
export function svgStringToPath(svgString: string): PathPoint[] {
  const points: PathPoint[] = []
  const commands = svgString.split(/(?=[A-Z])/)

  for (const cmd of commands) {
    const [type, ...coords] = cmd.trim().split(/\s+/)
    if (type === 'M' || type === 'L') {
      points.push({
        x: parseFloat(coords[0]),
        y: parseFloat(coords[1])
      })
    }
  }

  return points
} 