import axios from 'axios'
import {
  Robot,
  MapData,
  PathPoint,
  Position
} from '@/types/path_planning'

const API_BASE_URL = process.env.VUE_APP_API_BASE_URL || '/api/v1'

/**
 * Fetch available robots
 */
export async function getRobots(): Promise<{ data: Robot[] }> {
  const response = await axios.get(`${API_BASE_URL}/robots`)
  return response.data
}

/**
 * Fetch map data
 */
export async function getMapData(): Promise<{ data: MapData }> {
  const response = await axios.get(`${API_BASE_URL}/map`)
  return response.data
}

/**
 * Plan a path for a robot
 */
export async function planPath(
  robotId: string,
  params: {
    start: Position
    goal: Position
    options?: {
      avoidObstacles?: boolean
      optimizeForTime?: boolean
      maxDeviation?: number
    }
  }
): Promise<{ data: { path: PathPoint[] } }> {
  const response = await axios.post(
    `${API_BASE_URL}/robots/${robotId}/path`,
    params
  )
  return response.data
}

/**
 * Optimize an existing path
 */
export async function optimizePath(
  robotId: string,
  params: {
    path: PathPoint[]
    options?: {
      maxDeviation?: number
      smoothness?: number
    }
  }
): Promise<{ data: { path: PathPoint[] } }> {
  const response = await axios.post(
    `${API_BASE_URL}/robots/${robotId}/path/optimize`,
    params
  )
  return response.data
}

/**
 * Save a path for later use
 */
export async function savePath(
  robotId: string,
  path: PathPoint[],
  name?: string
): Promise<void> {
  await axios.post(`${API_BASE_URL}/robots/${robotId}/paths`, {
    path,
    name
  })
}

/**
 * Get saved paths for a robot
 */
export async function getSavedPaths(
  robotId: string
): Promise<{ data: Array<{ id: string; name: string; path: PathPoint[] }> }> {
  const response = await axios.get(`${API_BASE_URL}/robots/${robotId}/paths`)
  return response.data
}

/**
 * Delete a saved path
 */
export async function deletePath(robotId: string, pathId: string): Promise<void> {
  await axios.delete(`${API_BASE_URL}/robots/${robotId}/paths/${pathId}`)
}

/**
 * Execute a path on a robot
 */
export async function executePath(
  robotId: string,
  pathId: string
): Promise<void> {
  await axios.post(`${API_BASE_URL}/robots/${robotId}/paths/${pathId}/execute`)
}

/**
 * Stop a robot's current path execution
 */
export async function stopPathExecution(robotId: string): Promise<void> {
  await axios.post(`${API_BASE_URL}/robots/${robotId}/stop`)
}

/**
 * Get robot's current status
 */
export async function getRobotStatus(
  robotId: string
): Promise<{ data: Robot['status'] }> {
  const response = await axios.get(`${API_BASE_URL}/robots/${robotId}/status`)
  return response.data
}

/**
 * Subscribe to robot status updates
 */
export function subscribeToRobotStatus(
  robotId: string,
  callback: (status: Robot['status']) => void
): () => void {
  const eventSource = new EventSource(
    `${API_BASE_URL}/robots/${robotId}/status/stream`
  )

  eventSource.onmessage = (event) => {
    const status = JSON.parse(event.data)
    callback(status)
  }

  return () => {
    eventSource.close()
  }
} 