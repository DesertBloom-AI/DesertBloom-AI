import { mount } from '@vue/test-utils'
import { createStore } from 'vuex'
import PathPlanning from '../PathPlanning.vue'
import pathPlanningModule from '@/store/modules/path_planning'
import { getRobots, getMapData, planPath, optimizePath } from '@/services/path_planning'

// Mock services
jest.mock('@/services/path_planning', () => ({
  getRobots: jest.fn(),
  getMapData: jest.fn(),
  planPath: jest.fn(),
  optimizePath: jest.fn()
}))

describe('PathPlanning', () => {
  let store: any
  let wrapper: any

  const mockRobots = [
    {
      id: 'robot1',
      name: 'Robot 1',
      type: 'mobile',
      dimensions: {
        width: 1,
        height: 1,
        length: 1
      },
      capabilities: {
        maxSpeed: 1,
        maxAcceleration: 1,
        maxDeceleration: 1,
        turningRadius: 1
      },
      status: {
        battery: 100,
        state: 'idle'
      }
    }
  ]

  const mockMapData = {
    dimensions: {
      width: 100,
      height: 100
    },
    obstacles: [
      {
        id: 'obs1',
        type: 'rectangle',
        x1: 10,
        y1: 10,
        x2: 20,
        y2: 20
      }
    ],
    zones: [
      {
        id: 'zone1',
        name: 'Zone 1',
        type: 'work',
        area: {
          x1: 30,
          y1: 30,
          x2: 40,
          y2: 40
        }
      }
    ],
    charging_stations: [
      {
        id: 'station1',
        position: { x: 50, y: 50 },
        status: 'available'
      }
    ],
    paths: []
  }

  beforeEach(() => {
    // Reset mocks
    jest.clearAllMocks()

    // Setup store
    store = createStore({
      modules: {
        pathPlanning: pathPlanningModule
      }
    })

    // Setup service mocks
    ;(getRobots as jest.Mock).mockResolvedValue({ data: mockRobots })
    ;(getMapData as jest.Mock).mockResolvedValue({ data: mockMapData })
    ;(planPath as jest.Mock).mockResolvedValue({
      data: {
        path: [
          { x: 0, y: 0 },
          { x: 10, y: 10 }
        ]
      }
    })
    ;(optimizePath as jest.Mock).mockResolvedValue({
      data: {
        path: [
          { x: 0, y: 0 },
          { x: 5, y: 5 },
          { x: 10, y: 10 }
        ]
      }
    })

    // Mount component
    wrapper = mount(PathPlanning, {
      global: {
        plugins: [store]
      }
    })
  })

  it('renders correctly', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('loads robots and map data on mount', async () => {
    await wrapper.vm.$nextTick()
    expect(getRobots).toHaveBeenCalled()
    expect(getMapData).toHaveBeenCalled()
  })

  it('updates start position on map click', async () => {
    const svg = wrapper.find('.map-canvas')
    await svg.trigger('click', { clientX: 10, clientY: 10 })
    expect(store.state.pathPlanning.startPosition).toEqual({ x: 10, y: 10 })
  })

  it('updates goal position on map click after start position', async () => {
    const svg = wrapper.find('.map-canvas')
    await svg.trigger('click', { clientX: 10, clientY: 10 })
    await svg.trigger('click', { clientX: 20, clientY: 20 })
    expect(store.state.pathPlanning.goalPosition).toEqual({ x: 20, y: 20 })
  })

  it('plans path when start and goal positions are set', async () => {
    store.commit('pathPlanning/SET_START_POSITION', { x: 0, y: 0 })
    store.commit('pathPlanning/SET_GOAL_POSITION', { x: 10, y: 10 })
    store.commit('pathPlanning/SET_SELECTED_ROBOT', 'robot1')

    const planButton = wrapper.find('.plan-btn')
    await planButton.trigger('click')

    expect(planPath).toHaveBeenCalledWith('robot1', {
      start: { x: 0, y: 0 },
      goal: { x: 10, y: 10 }
    })
  })

  it('optimizes path when a path exists', async () => {
    store.commit('pathPlanning/SET_CURRENT_PATH', [
      { x: 0, y: 0 },
      { x: 10, y: 10 }
    ])
    store.commit('pathPlanning/SET_SELECTED_ROBOT', 'robot1')

    const optimizeButton = wrapper.find('.optimize-btn')
    await optimizeButton.trigger('click')

    expect(optimizePath).toHaveBeenCalledWith('robot1', {
      path: [
        { x: 0, y: 0 },
        { x: 10, y: 10 }
      ]
    })
  })

  it('toggles map layers', async () => {
    const layerToggles = wrapper.findAll('.layer-toggle input')
    
    await layerToggles[0].setValue(false)
    expect(store.state.pathPlanning.showObstacles).toBe(false)

    await layerToggles[1].setValue(false)
    expect(store.state.pathPlanning.showZones).toBe(false)

    await layerToggles[2].setValue(false)
    expect(store.state.pathPlanning.showChargingStations).toBe(false)

    await layerToggles[3].setValue(false)
    expect(store.state.pathPlanning.showPaths).toBe(false)
  })

  it('clears path when clear button is clicked', async () => {
    store.commit('pathPlanning/SET_START_POSITION', { x: 0, y: 0 })
    store.commit('pathPlanning/SET_GOAL_POSITION', { x: 10, y: 10 })
    store.commit('pathPlanning/SET_CURRENT_PATH', [
      { x: 0, y: 0 },
      { x: 10, y: 10 }
    ])

    const clearButton = wrapper.find('.clear-btn')
    await clearButton.trigger('click')

    expect(store.state.pathPlanning.startPosition).toBeNull()
    expect(store.state.pathPlanning.goalPosition).toBeNull()
    expect(store.state.pathPlanning.currentPath).toBeNull()
  })

  it('displays error message when error occurs', async () => {
    const errorMessage = 'Test error'
    store.commit('pathPlanning/SET_ERROR', errorMessage)
    await wrapper.vm.$nextTick()

    const errorElement = wrapper.find('.error-message')
    expect(errorElement.text()).toBe(errorMessage)
  })

  it('disables plan button when required fields are missing', async () => {
    const planButton = wrapper.find('.plan-btn')
    expect(planButton.attributes('disabled')).toBeDefined()

    store.commit('pathPlanning/SET_START_POSITION', { x: 0, y: 0 })
    store.commit('pathPlanning/SET_GOAL_POSITION', { x: 10, y: 10 })
    store.commit('pathPlanning/SET_SELECTED_ROBOT', 'robot1')
    await wrapper.vm.$nextTick()

    expect(planButton.attributes('disabled')).toBeUndefined()
  })

  it('disables optimize button when no path exists', async () => {
    const optimizeButton = wrapper.find('.optimize-btn')
    expect(optimizeButton.attributes('disabled')).toBeDefined()

    store.commit('pathPlanning/SET_CURRENT_PATH', [
      { x: 0, y: 0 },
      { x: 10, y: 10 }
    ])
    store.commit('pathPlanning/SET_SELECTED_ROBOT', 'robot1')
    await wrapper.vm.$nextTick()

    expect(optimizeButton.attributes('disabled')).toBeUndefined()
  })
}) 